# Skills de Telar — fichas de detalle

Una ficha por skill de **Telar** (el sistema orquestador, no el Proyecto que construye o evalúa) (ver [`../diagramas/02-skill-orquestador-y-skills-por-fase.md`](../diagramas/02-skill-orquestador-y-skills-por-fase.md)
para el panorama completo), con: propósito, cuándo se invoca, entradas/salidas, qué hace a alto nivel,
ADRs relacionados, criterios de éxito y pendientes propios de esa skill. Se van agregando de una en una,
en el orden del pipeline — no de golpe.

Cada skill que lee o escribe uno de los archivos SDD de ADR-0008 (`spec.md`, `test-cases.md`, `plan.md`,
`tasks.md`, `paquetes/*.md`, `evidencia/*.md`) documenta ahí mismo los campos de front-matter que le
corresponden. El esquema completo de cada archivo se arma incrementalmente, skill por skill, no de una
sola vez — evitar inventar campos que ninguna skill vaya a usar todavía.

## Progreso

0. [00-orquestador.md](00-orquestador.md) — no es una skill de fase: es el despachador que decide, para
   cada HU/paquete de trabajo, cuál de las 9 skills invocar (tabla de transición, gates de merge/revisión manual).
1. [01-descubrimiento-y-especificacion-hu.md](01-descubrimiento-y-especificacion-hu.md) — lee la fuente
   configurada del Proyecto (Jira, Markdown o GitHub), produce `spec.md` con criterio de analista de
   requerimientos, y clasifica el elemento como HU o Actividad (ADR-0026).
2. [02-generacion-de-tcs.md](02-generacion-de-tcs.md) — a partir de `spec.md`, genera `test-cases.md`
   (Given/When/Then), pensados para ejecutarse con Playwright.
3. [03-diagnostico-de-avance-existente.md](03-diagnostico-de-avance-existente.md) — corre los TCs
   contra el ambiente de desarrollo actual antes de diseñar; mismo motor que usará `smoke testing` más
   adelante. No necesita acceso a los repos, solo al ambiente desplegado.
4. [04-diseno-de-arquitectura.md](04-diseno-de-arquitectura.md) — a partir de los TCs pendientes,
   produce `plan.md`, extendiendo la arquitectura y convenciones ya presentes en el código. Tiene un
   modo fundacional para Proyectos nuevos sin arquitectura previa (ADR-0014).
5. [05-descomposicion-en-paquetes-de-trabajo.md](05-descomposicion-en-paquetes-de-trabajo.md) — a partir
   de `plan.md`, produce `tasks.md` y un `paquetes/PT-0N.md` por paquete de trabajo, cada uno anclado a
   un solo repositorio.
6. [06-generacion-de-codigo.md](06-generacion-de-codigo.md) — por paquete de trabajo, genera código en el
   repo objetivo y abre PR (con la cuenta de desarrollo de ADR-0013), y actualiza el repo de control.
7. [07-revision-de-codigo.md](07-revision-de-codigo.md) — revisa el PR contra `spec.md`, `plan.md` y
   las mejores prácticas del lenguaje/framework; no aprueba con supuestos sin resolver (ADR-0011).
8. [08-smoke-testing.md](08-smoke-testing.md) — mismo motor que la skill 03, aplicado a todos los TCs de
   la HU una vez que toda una ronda de paquetes de trabajo queda fusionada (ADR-0023); dispara fixes si
   algo falla.
9. [09-generacion-de-fixes.md](09-generacion-de-fixes.md) — ante un TC fallido en smoke testing, crea
   un paquete de trabajo de fix vinculado a su origen y lo reenvía al ciclo normal de código y revisión.

Con el orquestador (`00`), quedan documentadas las 9 skills de fase y el despachador que las coordina —
el diseño de Telar está completo a este nivel de detalle. Lo que sigue son los pendientes ya anotados en
cada ficha y en `00-vision-general.md` (framework de agentes, mecanismo de indexación de código, etc.),
no piezas nuevas del pipeline.
