# ADR-0069: Segunda opinión de la IA sobre las observaciones de la revisión

## Estado

Aceptada. Amplía el registro de rondas ([ADR-0068](0068-registro-de-rondas-de-revision-y-correccion-como-evidencia.md)) y la rúbrica de relevancia del plan de tesis.

## Decisión

1. **Qué es.** Una llamada a la IA que recibe las observaciones de una revisión (numeradas) y el diff del PR **tal como lo veía la revisión**, y por cada una devuelve: dictamen (correcta, parcial, incorrecta o no verificable), si la severidad es adecuada, sobreestimada o subestimada, su confianza, una justificación que cita el archivo o fragmento del diff y una recomendación (corregir, ignorar o discutir). Se le pide ser escéptica: solo «correcta» si puede señalar en el diff lo que la sostiene.
2. **Bajo demanda y con IA a elegir.** Se ejecuta con «Evaluar las observaciones» en el historial del paquete (`POST /revisiones/{id}/evaluar?proveedor=`). Se puede elegir una IA distinta de la que revisó, que da una opinión **independiente**; la evaluación guarda quién la hizo y si fue independiente. Evaluar de nuevo reemplaza la anterior.
3. **Base de la evaluación.** Se guarda el diff de cada revisión desde ahora. Para rondas anteriores se reconstruye desde GitHub: el PR hasta el commit anterior a la corrección (o el PR completo si no se corrigió). Comparar contra el código ya corregido daría «incorrecta» a observaciones que la corrección sí resolvió, sesgo que se detectó en la primera prueba.
4. **No reemplaza a la persona.** La valoración humana (relevante y correcta, relevante mal sustentada, ruido, falsa) sigue siendo la que vale para la tesis; la opinión de la IA la orienta y se puede usar como punto de partida con un botón. Ambas van al CSV de revisiones, con el proveedor y la independencia.
5. **Pantalla.** El historial de revisión se rediseñó: resumen (revisiones, valoradas y evaluadas), filtro por severidad, una tarjeta plegable por ronda y, por observación, la descripción, lo que se respondió al corregir, la segunda opinión de la IA y la valoración humana, todo junto.

## Consecuencias

- Una IA que evalúa su propio trabajo tiende a coincidir consigo misma; por eso se guarda si la evaluación fue independiente y conviene reportar el acuerdo de la IA independiente con la valoración humana, no el de la misma IA.
- Una llamada más por ronda evaluada (observaciones y diff, con tope de 60 KB de diff).
- En la primera prueba (BASE/PT-03, revisión 1, 6 observaciones), una IA independiente (Gemini) dictaminó 5 correctas y 1 parcial y la misma IA que revisó (Claude por CLI) dictaminó 1 correcta y 5 parciales: la opinión depende de quién la da. No hay todavía valoración humana con la que compararlas.

## Pendiente

- Evaluar automáticamente cada revisión nueva, y calcular el acuerdo entre la IA y la valoración humana.
- Que la evaluación viva en un documento aparte cuando se evalúe con varias IAs (hoy la última reemplaza).
