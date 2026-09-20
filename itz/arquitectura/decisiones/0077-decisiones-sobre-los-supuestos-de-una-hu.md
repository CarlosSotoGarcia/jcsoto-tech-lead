# ADR-0077: Decisiones sobre los supuestos de una HU

## Estado

Aceptada. Concreta cómo se resuelven los supuestos que fija el [ADR-0011](0011-supuestos-no-bloquean-se-resuelven-en-revision-de-codigo.md). Da contenido a la pantalla 3.11 «Decisiones pendientes» (ADR-0022, [repos fuera de alcance](0022-repos-fuera-de-configuracion-o-de-alcance.md)).

## Contexto

La revisión de código marca como bloqueante cualquier PR de una HU con supuestos sin confirmar (por ejemplo, «el tiempo de inactividad no está definido»). Ninguna ronda de corrección lo resuelve, porque es una decisión de negocio, y Loom no tenía dónde registrarla: la pantalla «Decisiones pendientes» era un marcador de posición. En el piloto, HU-003/PT-01 se quedó tres rondas con esa observación.

## Decisión

1. **La HU guarda las decisiones de una persona** (`decisiones` y `supuestos_confirmados_en`). Se registran con `POST /hus/{id}/confirmar-supuestos`, solo administradores. No cambian la especificación ni los casos de prueba, así que no generan versión nueva.
2. **Con la decisión confirmada, la revisión ya no bloquea** por «supuestos sin confirmar», y el PR deja de listarlos como pendientes.
3. **El agente recibe la decisión como requisito**, en el contexto de la generación de código, de la revisión y de las correcciones («Decisiones confirmadas por la persona sobre los supuestos de la HU»).
4. **Dónde se gestiona:** la pantalla «Decisiones pendientes» lista, de todos los Proyectos, las HUs con supuestos por confirmar, con su texto y un cuadro para escribir la decisión. El detalle de la HU muestra las decisiones confirmadas o un enlace a esa pantalla.

## Consecuencias

- Una sola decisión cubre todos los supuestos de la HU; conviene responder cada uno. Si después aparecen supuestos nuevos, hay que confirmar de nuevo.
- Confirmar no es aprobar el código: solo quita el bloqueo automático por supuestos.
- En el piloto quedaron HU-001 y HU-002 con supuestos sin confirmar cuyos PR ya se habían fusionado con esa observación abierta.

## Pendiente

- Registrar quién y cuándo tomó la decisión (hoy solo la fecha).
- Editar o retirar una decisión ya confirmada.
- Proponer una respuesta por supuesto con la IA para que la persona la apruebe.
