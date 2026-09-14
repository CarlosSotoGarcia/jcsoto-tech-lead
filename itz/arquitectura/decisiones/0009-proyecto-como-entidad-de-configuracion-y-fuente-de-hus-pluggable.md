# ADR-0009: "Proyecto" como entidad de configuración, con fuente de historias de usuario pluggable

## Estado

Aceptada

## Contexto

ADR-0005 estableció que la solución es configurable por repositorios y ambiente de desarrollo, pero
asumía implícitamente que las HUs llegan de una sola forma. En la práctica, las HUs de un equipo pueden
vivir en distintos lugares — un proyecto de Jira, un conjunto de archivos Markdown, u otras fuentes — y
esa fuente no es la misma para todos los equipos ni se puede fijar en el diseño: se decide al momento
de configurar cada proyecto. Además, la plataforma necesita un punto de entrada explícito donde se dé
de alta cada solución objetivo antes de poder operar sobre ella.

## Decisión

Se introduce **"Proyecto"** como la entidad de configuración de más alto nivel de la plataforma. Dar de
alta un Proyecto implica capturar:

- **Tipo de proyecto**: por ahora, únicamente **web**. La plataforma se diseña para que este campo sea
  extensible (API, mobile, otros), pero solo se implementa y valida el tipo web en esta tesis.
- **Repositorios y ambiente de desarrollo** (ya definidos en ADR-0005): N repos backend/frontend + URL
  del ambiente dev.
- **Fuente de historias de usuario**, pluggable: un proyecto de **Jira**, o una ubicación de archivos
  **Markdown**. La plataforma implementa un adaptador por tipo de fuente; agregar un tipo de fuente
  nuevo no debería requerir cambiar el resto del sistema.

Con la fuente configurada, el sistema **recorre la jerarquía del backlog** (épicas → tareas →
subtareas, tal como estén organizadas en esa fuente) para descubrir las HUs a procesar. A partir de ahí
entra el flujo de ADR-0004/ADR-0007, que genera su **propio** `spec.md`/`plan.md`/`tasks.md`/subtareas
de trabajo (ADR-0008) — el `spec.md` del sistema se deriva de la HU leída desde la fuente, no la
reemplaza.

## Consecuencias

- El "Proyecto" es el objeto de configuración raíz: tipo, repos+ambiente (ADR-0005), y fuente de HUs
  quedan agrupados bajo él — cualquier ADR futuro sobre configuración debería anclarse aquí.
- Requiere un adaptador de lectura por tipo de fuente (Jira, Markdown) que normalice épicas/tareas/
  subtareas del backlog a lo que el flujo interno espera como "HU con criterios de aceptación". El
  diseño concreto de esa normalización queda pendiente.
- **Ambigüedad de nombres a resolver**: "subtarea" ya se usa en ADR-0004 para las subtareas que el
  propio sistema genera al descomponer una HU. La fuente externa (Jira, por ejemplo) también organiza
  su jerarquía en épicas/tareas/subtareas. Hace falta un vocabulario que distinga ambas cosas antes de
  implementar (p. ej. "elemento del backlog" para lo que viene de la fuente, "subtarea técnica" para lo
  que el sistema genera).
- Limita el alcance de esta tesis a proyectos de tipo **web** — validar tipos API/mobile queda como
  trabajo futuro, no como objetivo de esta tesis (actualiza el alcance en `00-vision-general.md`).
- Refuerza que ADR-0006 (Playwright) es una decisión válida específicamente para el tipo de proyecto
  web; un tipo de proyecto futuro (API, mobile) necesitaría su propio mecanismo de ejecución de TCs.
