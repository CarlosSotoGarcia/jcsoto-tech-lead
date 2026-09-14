# ADR-0026: Vocabulario unificado — HU, Actividad, elemento del backlog, paquete de trabajo

## Estado

Aceptada. Es la referencia autoritativa de vocabulario hacia adelante. No reescribe el contenido de los
ADRs anteriores (ADR-0001) — donde digan "subtarea" o "tarea" en su sentido antiguo, siguen siendo
válidos como registro histórico de la decisión; los documentos vivos (`00-vision-general.md`,
`skills/`, `diagramas/`) sí adoptan este vocabulario de aquí en adelante.

## Contexto

La palabra "tarea"/"subtarea" llegó a chocar en tres sentidos distintos a la vez:

1. Nivel de la jerarquía del backlog de origen (épica → tarea → subtarea, ADR-0009/0019).
2. Un **tipo de elemento** del backlog sin criterios de aceptación — trabajo de arquitectura o
   preparación previo al código, que por naturaleza no tiene comportamiento verificable y por lo tanto
   no genera TCs ni pasa por smoke testing (distinción que surgió al discutir la parte C de
   `00-vision-general.md`).
3. Lo que la skill de descomposición (`skills/05-...md`) genera al partir una HU en unidades de
   implementación ("subtarea técnica").

## Decisión

Vocabulario, sin colisiones:

- **HU** (Historia de Usuario): un elemento del backlog **con criterios de aceptación** verificables.
  Recorre el pipeline completo — TCs, diagnóstico, arquitectura, paquetes de trabajo, código, revisión,
  smoke testing.
- **Actividad**: un elemento del backlog **sin criterios de aceptación** — trabajo de arquitectura o
  preparación (p. ej. definir un esquema de datos, investigar un enfoque) que antecede o sostiene una o
  varias HUs. Recorre un pipeline **reducido**: especificación → diseño/plan → código → revisión →
  merge — sin generación de TCs ni smoke testing, porque no hay comportamiento de usuario que verificar.
  La clasificación HU vs. Actividad la determina la skill de descubrimiento (`skills/01-...md`) según si
  el elemento tiene o no criterios de aceptación identificables — no es un tipo fijo declarado por la
  fuente, aunque la fuente puede darlo a entender (p. ej. un issue tipo "Task" en Jira/GitHub suele ser
  una Actividad).
- **Elemento del backlog**: término genérico para cualquier cosa que devuelve el contrato de lectura de
  un adaptador de fuente (ADR-0019) — una HU o una Actividad, antes de clasificarse. Reemplaza la
  necesidad de nombrar niveles de jerarquía como "tarea"/"subtarea"; la jerarquía se expresa con el
  campo `padre` (ADR-0019), no con una etiqueta de nivel.
- **Paquete de trabajo**: lo que `skills/05-...md` genera al descomponer una HU — la unidad que resulta
  en un PR propio y revisable. Reemplaza "subtarea técnica". La carpeta `subtareas/` (ADR-0008) pasa a
  llamarse **`paquetes/`**, y sus archivos `ST-0N.md` pasan a **`PT-0N.md`**.

**Ajuste al contrato de ADR-0019**: el campo `tipo` deja de tener valores `epica | tarea | subtarea` y
pasa a `epica | elemento` — la jerarquía interna más allá de "épica vs. lo demás" se resuelve con
`padre`, no con más niveles nombrados. Se agrega un campo nuevo, `clasificacion: hu | actividad`, que
la skill 01 llena al analizar el elemento.

## Consecuencias

- Los documentos vivos (`00-vision-general.md`, `skills/*.md`, `diagramas/*.md`) se actualizan para usar
  este vocabulario. Los ADRs 0001-0025 conservan su redacción original como registro histórico.
- El pipeline gana una bifurcación temprana real: al clasificar un elemento como Actividad, el
  orquestador lo despacha por el camino reducido (sin TCs/smoke testing) en vez del pipeline completo.
- `skills/05-...md`, `skills/06-...md`, `skills/07-...md`, `skills/08-...md`, `skills/09-...md` y
  `skills/00-...md` (orquestador) actualizan su terminología de "subtarea" a "paquete de trabajo" y su
  referencia de carpeta de `subtareas/ST-0N.md` a `paquetes/PT-0N.md`.
- Pendiente: si una Actividad puede en algún caso excepcional sí tener un criterio verificable (el
  usuario lo señaló como "por lo regular" no lo tienen, no nunca) — la clasificación se basa en la
  presencia real de criterios de aceptación, no en una etiqueta rígida, así que este caso ya queda
  cubierto de forma natural: si tiene criterios, se trata como HU aunque la fuente la haya tipeado como
  "Tarea".
