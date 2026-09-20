# ADR-0068: Registro de cada ronda de revisión y de corrección como evidencia de la tesis

## Estado

Aceptada. Amplía la skill 07 ([ADR-0049](0049-skill-07-revision-de-codigo-y-correcciones.md)) y las respuestas a las observaciones ([ADR-0064](0064-responder-y-resolver-las-observaciones-al-corregir-un-pr.md)).

## Contexto

La tesis necesita evidencia de qué hacen la revisión y la corrección de código: qué observaciones encuentra la revisión, qué se hizo con cada una y qué tan relevantes son. Loom no la conservaba: al corregir un paquete se borraban sus observaciones del registro, lo respondido a cada una solo quedaba en comentarios de GitHub y el reinicio de un proyecto no dejaba rastro.

## Decisión

1. **Cada ronda se guarda** en la colección `revisiones`, sin borrarse nunca ni tocarse en el reinicio de un proyecto:
   - **Revisión:** paquete, PR, número de ronda, veredicto (aprobado o con observaciones), resumen de la revisión, proveedor de IA, duración y cada observación con su severidad, fuente, archivo, línea, descripción, sugerencia e id del comentario de GitHub.
   - **Corrección:** ronda que atiende, commit, archivos que tocó, tamaño del cambio (archivos, líneas agregadas y eliminadas), resumen del agente y la respuesta a cada observación (`corregida`, `parcial` o `no_corregida`, con el texto que se publicó).
2. **Valoración humana.** Cada observación admite una valoración de la rúbrica de relevancia de la tesis: relevante y correcta, relevante mal sustentada, ruido o falsa. Se asigna desde el historial del paquete (`PUT /revisiones/{id}/observaciones/{n}/valoracion`).
3. **Consulta y exportación.** `GET /revisiones` (por proyecto, opcionalmente por paquete), la interfaz muestra el historial de cada paquete con rondas de revisión y `GET /revisiones/exportar` da un CSV con una fila por observación: ronda, severidad, fuente, ubicación, estado en la corrección, respuesta, commit y valoración.
4. **Lo anterior al registro se reconstruye desde GitHub** cuando sus comentarios lo permiten (marcado como «reconstruida desde los comentarios del PR»): por ahora, la primera ronda del PR #8 del proyecto E1c. Los datos que no viven en el PR (duración, archivos de la corrección) quedan vacíos.

## Consecuencias

- Las tablas del capítulo 5 (observaciones por severidad y fuente, rondas hasta aprobar, proporción corregida, relevancia) salen del CSV en lugar de reconstruirse a mano.
- La respuesta de la corrección la escribe la IA a partir del diff; la valoración humana es la que da validez a la relevancia.
- Las rondas de los escenarios anteriores (E2 y el resto de E1c) no se guardaron: solo existen en los PR de GitHub y en los archivos de evidencia del piloto.
- Probado con la ronda real del PR #8 y con las rutas de valoración y exportación; el registro automático de una ronda nueva se verá en la próxima revisión y corrección.

## Pendiente

- Reconstruir desde GitHub las rondas del escenario E2.
- Registrar si la conversación se resolvió y quién la resolvió.
