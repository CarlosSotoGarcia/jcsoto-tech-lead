# Skill — Revisión de código

**Alias en diagramas:** `S5` en [diagrama 02](../diagramas/02-skill-orquestador-y-skills-por-fase.md).

## Propósito

Revisar el PR abierto por la skill de generación de código (`skills/06-...md`) contra **tres fuentes de
verdad a la vez**, no solo "¿se ve bien el código?":

1. **`spec.md`** — ¿el código realmente cumple los criterios de aceptación (explícitos e inferidos) de
   la HU, y quedó resuelto cualquier supuesto heredado (`tiene_supuestos`, ADR-0011)?
2. **`plan.md`** — ¿el código sigue el enfoque de arquitectura definido para esta HU (ADR-0007: extiende
   lo existente, no lo contradice sin justificación)?
3. **Mejores prácticas del lenguaje/framework** que ya usa el repositorio objetivo — convenciones
   idiomáticas específicas (p. ej. PEP 8 y type hints en Python, la guía de estilo de Angular en
   TypeScript), no reglas genéricas de "buen código" independientes del stack.

Es esta skill la que finalmente implementa la regla de ADR-0011: **no se puede aprobar un PR en
automático si arrastra un supuesto sin resolver.**

## Cuándo se invoca

- Cuando un paquete de trabajo entra en estado `en_revision` (salida de `skills/06-...md`).
- Cada vez que se sube una nueva versión del PR tras aplicar observaciones — es el ciclo `revisión ↔
  aplicar cambios` del [diagrama 01](../diagramas/01-flujo-pipeline-hu-a-desarrollo.md), que se repite
  hasta que no quedan observaciones pendientes.

## Entradas

- El diff del PR en el repositorio objetivo (ADR-0005).
- `spec.md` de la HU: criterios de aceptación y supuestos (ADR-0011).
- `plan.md` de la HU: enfoque de arquitectura acordado.
- Convenciones/mejores prácticas del lenguaje y framework detectados en el repositorio — vía el mismo
  mecanismo de indexación de código del que depende `skills/04-...md` (ADR-0002).

## Salidas

- Comentarios de revisión publicados en el PR (en la plataforma donde vive el repo objetivo — GitHub,
  GitLab, etc., ADR-0005), agrupados por fuente: incumplimiento de criterio de aceptación, desviación
  del plan, o convención de lenguaje/framework.
- Si hay un supuesto sin resolver: una observación explícitamente marcada como **bloqueante**,
  pidiendo confirmación o corrección — no se mezcla con sugerencias menores.
- Actualiza `paquetes/PT-0N.md` (repo de control, ADR-0012): incrementa `rondas_revision`, y cambia
  `estado` a `aprobado` (sin observaciones pendientes) o lo deja en `en_revision` (con observaciones).

## Qué hace (alto nivel)

1. Lee el diff del PR junto con `spec.md` y `plan.md` de la HU/paquete de trabajo correspondiente.
2. Verifica cumplimiento de cada criterio de aceptación relevante a este paquete de trabajo — no en abstracto,
   contra lo que el código efectivamente hace.
3. Verifica que el código sigue el enfoque de `plan.md`; si se desvía, evalúa si la desviación está
   justificada o es una observación a corregir.
4. Aplica revisión de mejores prácticas específicas del lenguaje/framework detectado, apoyándose en las
   herramientas de lint/formato que ya tenga configuradas el repositorio si existen.
5. Si la HU tiene `tiene_supuestos: true` y el supuesto en cuestión no fue resuelto en esta versión del
   código, genera la observación bloqueante correspondiente.
6. Publica las observaciones en el PR.
7. Si no quedan observaciones pendientes (incluidos los supuestos), aprueba el PR; si quedan, deja el
   PR esperando una nueva versión (vuelve a `skills/06-...md`) y actualiza `paquetes/PT-0N.md`.
8. La aprobación de esta skill **no siempre implica merge inmediato**: si el Proyecto tiene
   `requiere_revision_manual: true` (ADR-0015), el PR queda esperando la aprobación de alguno de los
   `usuarios_autorizados_a_aprobar` antes de fusionarse — este paso ya no lo hace esta skill, es un
   gate del orquestador (ver [diagrama 01](../diagramas/01-flujo-pipeline-hu-a-desarrollo.md)).

## ADRs relacionados

- [ADR-0004](../decisiones/0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md) — el
  ciclo de revisión como fase del flujo.
- [ADR-0005](../decisiones/0005-solucion-configurable-repositorios-y-ambiente-dev.md) — el PR vive en
  el repositorio objetivo configurado.
- [ADR-0007](../decisiones/0007-soporte-proyectos-con-avance-previo.md) — el código no debe contradecir
  sin justificación lo que ya existe.
- [ADR-0008](../decisiones/0008-adopcion-de-sdd-y-nombres-de-artefactos.md) — formato de
  `paquetes/PT-0N.md`.
- [ADR-0011](../decisiones/0011-supuestos-no-bloquean-se-resuelven-en-revision-de-codigo.md) — esta
  skill es donde se aplica la regla de no aprobar con supuestos sin resolver.
- [ADR-0012](../decisiones/0012-plataforma-de-visualizacion-y-reportes.md) — actualiza el repo de
  control, no el objetivo.
- [ADR-0015](../decisiones/0015-revision-manual-opcional-antes-de-merge.md) — la aprobación de esta
  skill puede no ser suficiente para el merge si el Proyecto exige revisión manual.
- [ADR-0026](../decisiones/0026-vocabulario-unificado-hu-actividad-paquete-de-trabajo.md) — vocabulario
  "paquete de trabajo".
- [ADR-0028](../decisiones/0028-ciclo-automatizado-de-calidad-como-mecanismo-suficiente.md) — esta
  skill, dentro del ciclo código→revisión→corrección, es el mecanismo de calidad documentado incluso
  sin revisión manual.

## Criterios de éxito

Un PR solo se aprueba cuando: cumple los criterios de aceptación de `spec.md` relevantes al paquete de
trabajo, sigue (o justifica su desviación de) el enfoque de `plan.md`, no tiene observaciones de
convención de lenguaje/framework sin resolver, y no arrastra ningún supuesto sin confirmar.

## Pendientes propios de esta skill

- Fuente del catálogo de "mejores prácticas por lenguaje": ¿reglas propias del sistema, integración con
  los linters/formatters ya configurados en el repo (ESLint, Ruff, Flake8, Prettier...), o el criterio
  del propio LLM sin catálogo explícito?
- Qué cuenta como "resolver" un supuesto en revisión: ¿un comentario del revisor aceptándolo basta, o
  se exige un cambio de código o una confirmación humana explícita?
- Si esta skill debe operar con una identidad distinta a la cuenta de desarrollo que generó el código
  (ADR-0013) — separar "quien escribe" de "quien revisa" — o si es aceptable que sea el mismo sistema
  actuando en dos roles.
- Umbral de severidad: ¿toda observación bloquea el avance, o hay clasificación (bloqueante vs.
  sugerencia) como en una revisión humana normal?
- Qué pasa si, tras varias rondas, el PR sigue sin poder aprobarse — ¿existe un límite antes de escalar
  a revisión humana?
