# ADR-0040: Detección de cambios en la fuente y regeneración selectiva de specs

## Estado

Aceptada. Resuelve el pendiente de `skills/01-descubrimiento-y-especificacion-hu.md`: "cómo se
detectan HUs ya procesadas antes vs. nuevas/modificadas, para no reprocesar todo el backlog en cada
corrida".

## Contexto

La Fase 1 (ADR-0033) analizaba con el LLM todo el sprint activo en cada corrida y emparejaba por
`fuente_ref` solo para no duplicar. No distinguía "sin cambios" de "modificada", así que una HU
editada en Jira no se detectaba, y la única forma de reflejar el cambio era volver a correr todo
(una llamada al LLM por HU, aunque casi nada hubiera cambiado).

## Decisión

1. **Huella de la fuente**: cada HU guarda `fuente_hash`, un SHA-256 del título + descripción tal
   como vienen de Jira (lo que realmente alimenta el análisis), y `fuente_actualizada_en`
   (`updated` de Jira, informativo). No se usa `updated` como criterio: cambia también con
   comentarios o cambios de estado que no alteran la especificación.
2. **Revisión sin LLM**: `GET /proyectos/{id}/hus/revision-fuente` compara el sprint activo contra
   las HUs guardadas y clasifica cada elemento como `nueva`, `modificada` o `sin_cambios`, y
   reporta las HUs que ya no están en el sprint (`retiradas`; sus specs se conservan). Es
   barata: solo una consulta a Jira.
3. **Regeneración selectiva**: `POST .../descubrir` acepta `solo_cambios=true` (procesa únicamente
   nuevas y modificadas) y `claves=ITZINV-12` (repetible, regenera HUs puntuales). Sin parámetros
   conserva el comportamiento de siempre (todo el sprint). La propuesta de stack del arquitecto
   (ADR-0039) solo se recalcula en corridas completas.
4. **Historial**: cada regeneración que cambia el `spec.md` queda como commit "Actualiza HU-xxx"
   en el repositorio de control (ADR-0035), así que la bitácora (ADR-0037) muestra cuándo y qué
   versión se leyó.
5. **Lo generado después queda obsoleto**: si la fuente cambió desde la última especificación, la
   HU vuelve a la fase `especificada`, para que la Fase 2 regenere sus TCs en la siguiente corrida.
   Las HUs sin cambios conservan su fase.
6. **HUs anteriores a la huella** (sin línea base): la primera revisión las compara por fecha
   (`updated` de Jira contra la fecha de descubrimiento) y, si no cambiaron, les guarda la huella
   como línea base sin tocar su spec.
7. En la plataforma, la pestaña Requerimientos tiene "Revisar cambios en Jira": muestra cuántas
   son nuevas/modificadas, "Regenerar spec" por HU y "Actualizar las N con cambios", con el
   mismo visualizador de progreso.

## Consecuencias

- Reprocesar solo lo que cambió reduce el costo de mantener las specs al día.
- La revisión es manual (botón); no hay polling ni webhooks.

## Pendiente

- Cambios hechos en Jira el mismo día del descubrimiento no se detectan en HUs sin huella
  (la comparación de respaldo es por fecha, no por hora); las HUs nuevas ya traen huella.
- Detección automática (polling o webhook de Jira) en vez de solo bajo demanda.
- No hay comparación del `spec.md` anterior contra el nuevo; para ver el detalle de qué cambió
  se usa `git diff` sobre el repositorio de control.
