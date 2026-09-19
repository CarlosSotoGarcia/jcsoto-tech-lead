# Skill — Generación de código

**Alias en diagramas:** `S4` en [diagrama 02](../diagramas/02-skill-orquestador-y-skills-por-fase.md).

## Propósito

Por cada paquete de trabajo (`paquetes/PT-0N.md`), generar el código correspondiente en su repositorio objetivo
y abrir un Pull Request — el "vibecoding" del que habla ADR-0008, siempre contra una especificación
concreta (`plan.md` + `spec.md` + `test-cases.md`), nunca a partir de un prompt suelto.

## Cuándo se invoca

Cuando un paquete de trabajo está en estado `pendiente` (salida de `skills/05-...md`), respetando su
`depende_de` si tiene dependencias sin resolver. También la reutiliza la skill de generación de fixes
(`S7`, pendiente de documentar) cuando un TC falla en smoke testing.

## Entradas

- `paquetes/PT-0N.md`: repositorio objetivo, TCs asociados, dependencias.
- `plan.md`: enfoque de diseño de la HU.
- `spec.md` / `test-cases.md`: criterios de aceptación y TCs relacionados, incluyendo cualquier
  supuesto marcado (`tiene_supuestos`, ADR-0011) que este paquete de trabajo deba respetar.
- Configuración del Proyecto: referencia al repositorio objetivo correspondiente (ADR-0005) y la
  credencial de la **cuenta de desarrollo dedicada** (ADR-0013) para operar sobre él.

## Salidas

Esta skill escribe en **dos lugares distintos** — vale la pena tenerlo presente (ADR-0012):

**En el repositorio objetivo** (código real, ADR-0005):
- Una rama nueva, nombrada `hu/{id_fuente}/{paquete_id}` — `id_fuente` es el identificador del ticket
  tal como está dado de alta en la fuente (el issue de GitHub, el ticket de Jira); si la fuente es
  Markdown, se usa el identificador propio del documento si lo trae, o uno generado por el adaptador si
  no (ADR-0019, ADR-0021).
- Uno o más commits con el código generado, con autoría de la cuenta de desarrollo (ADR-0013).
- Un Pull Request contra la rama base configurada, cuya descripción incluye: qué paquete de trabajo resuelve, qué
  TCs cubre, y — si aplica — los supuestos heredados de `spec.md` que el revisor debe confirmar
  (ADR-0011). Esto es obligatorio cuando el paquete de trabajo desciende de una HU con `tiene_supuestos: true`.

**En el repositorio de control** (documentación, ADR-0012):
- Actualiza `paquetes/PT-0N.md`: `pr` (URL del PR recién abierto), `estado: en_revision`.

## Qué hace (alto nivel)

1. Verifica que las dependencias del paquete de trabajo (`depende_de`) ya estén resueltas; si no, espera.
2. Lee el paquete de trabajo, `plan.md` y el `spec.md`/`test-cases.md` relacionados.
3. Genera el código en el repositorio objetivo identificado, siguiendo el enfoque de `plan.md` y
   respetando las convenciones ya presentes (ADR-0007).
4. Crea la rama y hace commit(s) con la cuenta de desarrollo dedicada (ADR-0013).
5. Abre el PR, propagando a su descripción los supuestos sin resolver de `spec.md` si los hay
   (ADR-0011) — esto es lo que le permite a la skill de revisión de código (`S5`, pendiente) saber que
   no puede aprobar en automático.
6. Actualiza `paquetes/PT-0N.md` en el repositorio de control con la URL del PR y el nuevo estado.

## Estado de implementación

Implementada — [ADR-0046](../decisiones/0046-skill-06-generacion-de-codigo-agente-con-tdd.md): agente con
herramientas acotadas sobre un worktree, desarrollo con TDD (compuerta que exige pruebas unitarias en
paquetes de backend/frontend), PR con la cuenta de desarrollo y sincronización del estado de los PRs.
Sin ejecución local del código en esta versión.

## Orden de las HUs

El orden de las HUs ([ADR-0048](../decisiones/0048-orden-de-implementacion-de-hus-y-avance-por-hu.md)): el siguiente paquete se elige por ese orden, y se puede avanzar con una HU concreta (`grupo` sin `pt`) respetando dependencias.

## ADRs relacionados

- [ADR-0046](../decisiones/0046-skill-06-generacion-de-codigo-agente-con-tdd.md) — implementación y TDD.

- [ADR-0004](../decisiones/0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md) —
  generación de código y apertura de PR como fase del flujo.
- [ADR-0005](../decisiones/0005-solucion-configurable-repositorios-y-ambiente-dev.md) — repositorio
  objetivo por paquete de trabajo.
- [ADR-0007](../decisiones/0007-soporte-proyectos-con-avance-previo.md) — respetar el código existente.
- [ADR-0008](../decisiones/0008-adopcion-de-sdd-y-nombres-de-artefactos.md) — SDD como fuente del
  código generado (spec/plan/tasks), no un prompt suelto.
- [ADR-0011](../decisiones/0011-supuestos-no-bloquean-se-resuelven-en-revision-de-codigo.md) — cómo se
  propagan los supuestos a la descripción del PR (queda resuelto aquí: van explícitos en la
  descripción).
- [ADR-0012](../decisiones/0012-plataforma-de-visualizacion-y-reportes.md) — esta skill toca repo de
  control y repo objetivo a la vez.
- [ADR-0013](../decisiones/0013-cuenta-de-desarrollo-dedicada-para-acceso-a-repositorios.md) — la
  identidad con la que se hacen commits, push y PRs.
- [ADR-0021](../decisiones/0021-convencion-de-nombre-de-rama-basada-en-id-fuente.md) — convención de
  nombre de rama basada en `id_fuente`.
- [ADR-0026](../decisiones/0026-vocabulario-unificado-hu-actividad-paquete-de-trabajo.md) — vocabulario
  "paquete de trabajo".
- [ADR-0028](../decisiones/0028-ciclo-automatizado-de-calidad-como-mecanismo-suficiente.md) — el ciclo
  código→revisión→corrección es el mecanismo de calidad, con o sin revisión manual.
- [ADR-0029](../decisiones/0029-orden-secuencial-de-paquetes-de-trabajo-dependientes.md) — orden
  secuencial para paquetes dependientes entre repos.

## Criterios de éxito

Existe un PR abierto en el repositorio objetivo correcto, con autoría de la cuenta de desarrollo,
descripción completa (paquete de trabajo, TCs cubiertos, supuestos si aplica), y `paquetes/PT-0N.md` refleja el
estado y la URL del PR.

## Pendientes propios de esta skill

- ~~Qué hace el sistema si el código generado no compila~~ — v1: se abre igual y la CI/la revisión lo
  detectan (ADR-0046); validar localmente antes del PR queda como mejora.
- ~~Cómo se coordinan paquetes de trabajo relacionados que tocan repos distintos~~ — resuelto en
  [ADR-0029](../decisiones/0029-orden-secuencial-de-paquetes-de-trabajo-dependientes.md): en secuencia
  estricta, nunca en paralelo — el dependiente no arranca hasta que la dependencia está fusionada.
- Formato/convención exacta para que un PR "generado por el sistema" sea identificable de forma
  confiable en los reportes (ADR-0012) — ¿basta la autoría de la cuenta de desarrollo (ADR-0013), o
  hace falta además un label o un prefijo de rama?
- Qué pasa si la generación de código para un paquete de trabajo falla repetidamente (¿cuántos
  reintentos antes de marcarlo como bloqueado y escalar a un humano?).
