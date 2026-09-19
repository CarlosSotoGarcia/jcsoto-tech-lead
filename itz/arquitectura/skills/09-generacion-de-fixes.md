# Skill — Generación de fixes

**Alias en diagramas:** `S7` en [diagrama 02](../diagramas/02-skill-orquestador-y-skills-por-fase.md) y
el nodo `FIXSUB` del [diagrama 01](../diagramas/01-flujo-pipeline-hu-a-desarrollo.md).

## Propósito

Cuando smoke testing (`skills/08-...md`) reporta que uno o más TCs de la HU fallaron (tras fusionar
toda una ronda de paquetes de trabajo, ADR-0023 — no un paquete de trabajo aislado), generar uno o más
**paquetes de trabajo de fix** que corrijan el comportamiento — sin editar directamente el código ya fusionado en `develop`.
Cada fix forma una **nueva ronda** (ADR-0023): reentra al ciclo normal — genera código
(`skills/06-...md`), abre PR, pasa revisión (`skills/07-...md`) — y, a diferencia de la ronda original,
en cuanto esa ronda de fixes termina de fusionarse **se dispara smoke testing de inmediato** (ya no hay
más trabajo original pendiente esperando).

Esta skill no introduce un mecanismo nuevo de generación de código ni de revisión — **reutiliza
`skills/06-...md` y `skills/07-...md`** tal cual; lo único propio de esta skill es diagnosticar el
fallo y crear el o los paquetes de trabajo de fix correctamente vinculados a su origen.

## Cuándo se invoca

Cuando `skills/08-...md` (smoke testing) reporta al menos un TC fallido, tras correr sobre **todos los
TCs de la HU** al completarse una ronda (la original o una de fix anterior).

## Entradas

- `evidencia/smoke-0N.md`: qué TCs fallaron y qué se observó vs. qué se esperaba.
- `tasks.md` y los `paquetes/PT-0N.md` de la ronda recién fusionado (candidatos a haber causado el
  fallo — ver Notas sobre atribución).
- `spec.md` / `plan.md` de la HU: referencia de qué se pretendía construir.

## Salidas

Uno o más paquetes de trabajo nuevos, `paquetes/PT-0M.md`, con front-matter:

```yaml
id: PT-05
hu_id: HU-001
repo: backend-principal        # el repo donde se corrige el comportamiento
estado: pendiente
ronda: 2                        # nueva ronda de fix (ADR-0023) — incrementa sobre la ronda anterior
tcs_asociados: [TC-003]         # los TCs que fallaron en smoke testing
tipo: fix
paquete_origen: PT-02                   # paquete de trabajo candidato cuyo código causó el fallo, si se pudo atribuir
evidencia_origen: evidencia/smoke-01.md
pr: null
rondas_revision: 0
```

Y actualiza `tasks.md`: incrementa `total_paquetes`, agrega el o los nuevos paquetes de trabajo de fix
a la lista, todos con el mismo `ronda`.

## Qué hace (alto nivel)

1. Lee `evidencia/smoke-0N.md` para identificar los TCs fallidos y el detalle de cada fallo.
2. Diagnostica, contra `spec.md`/`plan.md` y los paquetes de trabajo de la ronda recién fusionado, si el fallo es
   porque el código no implementa correctamente el criterio, o porque el cambio introdujo una regresión
   en algo que antes funcionaba (ver Notas) — y, si es posible, a qué paquete de trabajo de esa ronda se puede
   atribuir.
3. Crea un paquete de trabajo `tipo: fix` por cada agrupación razonable de TCs fallidos (ver
   Pendientes), vinculado a la evidencia que lo disparó (`evidencia_origen`) y, si se pudo atribuir, al
   paquete de trabajo candidato (`paquete_origen`).
4. Actualiza `tasks.md` con la nueva ronda.
5. Despacha cada paquete de trabajo de fix a `skills/06-...md` como cualquier otro paquete de trabajo
   pendiente — mismo mecanismo de generación de código y PR, sin trato especial.

## Estado de implementación

Implementada — [ADR-0061](../decisiones/0061-generacion-de-fixes-desde-smoke-testing.md): diagnóstico con IA de los TCs fallidos, un fix por causa raíz (cada TC en exactamente un fix),
atribución de mejor esfuerzo, límite de 3 rondas y nueva corrida de smoke testing al fusionar la ronda.

## ADRs relacionados

- [ADR-0061](../decisiones/0061-generacion-de-fixes-desde-smoke-testing.md) — implementación.

- [ADR-0004](../decisiones/0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md) — el
  ciclo de fix como fase del flujo.
- [ADR-0006](../decisiones/0006-smoke-tests-con-playwright-y-bitacora-de-hus.md) /
  [ADR-0007](../decisiones/0007-soporte-proyectos-con-avance-previo.md) — origen del TC fallido que
  dispara esta skill.
- [ADR-0008](../decisiones/0008-adopcion-de-sdd-y-nombres-de-artefactos.md) — formato de
  `paquetes/PT-0N.md`.
- [ADR-0011](../decisiones/0011-supuestos-no-bloquean-se-resuelven-en-revision-de-codigo.md) — si el
  fix hereda algún supuesto, se propaga igual que en `skills/06-...md`.
- [ADR-0020](../decisiones/0020-smoke-testing-corre-todos-los-tcs-como-regresion.md) — cuando el fix se
  fusione, `skills/08-...md` vuelve a correr todos los TCs de la HU, no solo el que disparó este fix.
- [ADR-0023](../decisiones/0023-smoke-testing-espera-a-toda-la-hu-no-por-subtarea.md) — cada fix forma
  una nueva ronda; a diferencia de la ronda original, al fusionarse dispara smoke testing de inmediato.
- [ADR-0026](../decisiones/0026-vocabulario-unificado-hu-actividad-paquete-de-trabajo.md) — vocabulario
  "paquete de trabajo".

## Criterios de éxito

Cada TC fallido en smoke testing queda cubierto por exactamente un paquete de trabajo de fix, vinculado a su
origen, y ese paquete de trabajo sigue el ciclo normal (código → revisión → smoke) hasta que el TC pasa.

## Notas

Un TC que **falló en smoke testing pero había pasado en una corrida anterior** (`skills/03-...md` o un
`smoke-0N.md` previo) es una **regresión** introducida por el propio cambio — distinto de un TC que
nunca pasó (trabajo nunca terminado). Esta skill puede necesitar tratar ambos casos distinto (ver
Pendientes); por ahora, el front-matter no distingue uno de otro más allá de lo que ya cuenta
`evidencia_origen`.

**Atribución más difícil desde ADR-0023**: como smoke testing ahora corre una sola vez para toda una
ronda de paquetes de trabajo (no una por una), un TC fallido ya no apunta obviamente a "el paquete de trabajo que se acaba
de fusionar" — pudo haber sido cualquiera de los paquetes de trabajo de esa ronda, o una interacción entre
varias. `paquete_origen` queda como *mejor esfuerzo*, no garantizado; cuando no se puede atribuir con
confianza, el paquete de trabajo de fix puede quedar sin `paquete_origen` y describir el fallo directamente contra
`spec.md`/`plan.md`.

## Pendientes propios de esta skill

- Cómo se agrupan TCs fallidos relacionados en un solo paquete de trabajo de fix vs. varios — ¿un fix
  por TC, o uno que cubre varios TCs que probablemente comparten causa raíz?
- Cómo se diagnostica a qué paquete de trabajo de la ronda recién fusionado atribuir un TC fallido cuando no es
  evidente (ver Notas) — puede requerir analizar el diff de cada paquete de trabajo de la ronda, no solo el
  resultado del TC.
- Si una regresión (TC que antes pasaba) debería generar un paquete de trabajo de fix con mayor prioridad o
  señal distinta que un TC que simplemente nunca se implementó — sigue sin decidirse (ver Notas).
- Qué pasa si un fix, a su vez, vuelve a fallar en smoke testing — ¿se generan fixes indefinidamente, o
  hay un límite de rondas antes de escalar a revisión humana? (mismo tipo de pendiente que quedó abierto
  en `skills/06-...md` sobre reintentos de generación de código).
- Cómo se refleja un paquete de trabajo de fix en los reportes agregados (ADR-0012): ¿cuenta como trabajo nuevo,
  o como "retrabajo" del paquete de trabajo original para las métricas del objetivo 11 de
  `00-vision-general.md`?
