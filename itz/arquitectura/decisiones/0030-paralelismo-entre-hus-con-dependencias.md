# ADR-0030: El orquestador puede procesar varias HUs en paralelo, salvo dependencia explícita entre ellas

## Estado

Aceptada. Cierra el pendiente de `skills/00-orquestador.md` sobre paralelismo entre HUs.

## Contexto

Quedaba sin decidir si el orquestador procesa una HU a la vez por Proyecto, o puede avanzar varias en
paralelo. Además, no toda HU es independiente: puede haber una HU que dependa de que otra ya esté
completa (p. ej. una HU que extiende una funcionalidad que otra HU todavía está construyendo).

## Decisión

El orquestador puede trabajar **varias HUs a la vez dentro del mismo Proyecto**, siempre que no haya
una dependencia declarada entre ellas. Se introduce `depende_de` también a **nivel HU** (en `spec.md`,
mismo campo que ya existe a nivel paquete de trabajo, ADR-0008) — si la HU-B declara que depende de la
HU-A, el orquestador no avanza la HU-B más allá de su especificación hasta que la HU-A esté completa.

Sin una dependencia declarada, dos HUs pueden avanzar en paralelo aunque compartan repositorio — la
coordinación a ese nivel (dos paquetes de trabajo de HUs distintas tocando el mismo repo al mismo
tiempo) se resuelve con el flujo normal de PRs y revisión de código, igual que si fueran de un mismo
equipo humano trabajando en paralelo.

## Consecuencias

- `spec.md` gana un campo opcional `depende_de` a nivel HU, con la misma semántica que el de
  `paquetes/PT-0N.md` (ADR-0008) pero un nivel arriba.
- El orquestador necesita mantener estado de varias HUs simultáneamente — ya lo hacía en el diseño
  (lee/escribe por HU independientemente), esto solo confirma que no hay una restricción artificial de
  "una HU a la vez".
- Pendiente: cómo se declara la dependencia entre HUs cuando vienen de una fuente que no la modela
  explícitamente (Jira sí tiene "issue links"; Markdown probablemente necesite declararla a mano).
- Pendiente: qué pasa si dos HUs sin dependencia declarada generan paquetes de trabajo que en la
  práctica sí chocan en el mismo repositorio (conflictos de merge) — se trata como conflicto normal de
  desarrollo, no como algo que el orquestador deba prevenir de antemano.
