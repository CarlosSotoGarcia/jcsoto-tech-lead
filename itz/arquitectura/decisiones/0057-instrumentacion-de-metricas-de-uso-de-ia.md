# ADR-0057: Instrumentación de métricas de uso de IA

## Estado

Aceptada. Da la evidencia que necesita el capítulo de resultados de la tesis (`itz/tesis/00-plan-de-llenado-de-tesis.md` § 3.2): comparar Claude y Gemini y
medir tiempo, tokens y costo por HU y por paquete.

## Decisión

1. **Colección `metricas`** (Mongo) con un registro por evento, siempre asociado a un Proyecto, a la skill que corría, a su ejecución y a la referencia (HU,
   paquete o repositorio) en curso:
   - `llamada`: cada llamada a la IA (análisis y cada turno del agente de código) con proveedor, modelo, resultado (`ok`, `truncado`, `sin_resultado`, `error`),
     duración, tokens de entrada, salida, caché y razonamiento, y costo.
   - `skill`: cada ejecución de una skill (duración y resultado).
   - `reintento`: cada reintento por respuesta truncada, sin resultado, mal formada o reparada.
   - `compuerta`: cada rechazo de las compuertas del agente (falta de pruebas, README o archivos obligatorios).
2. **Los tres proveedores se miden** (Claude API, Gemini, Claude con cuenta normal). El CLI informa un costo propio (nocional en suscripción), que se marca como
   reportado y no como estimado.
3. **Costo estimado con una tabla de precios configurable** (`LOOM_PRECIOS_MODELOS`, USD por millón de tokens), no fija en el código porque los precios
   cambian. Los tokens de razonamiento de Gemini se cobran como salida. Sin precio para un modelo el costo queda vacío y la interfaz muestra «—».
4. **Las métricas nunca rompen el flujo:** si guardarlas falla, se ignora; y fuera de una ejecución de skill no se mide.
5. **Consulta y exportación.** `GET /proyectos/{id}/metricas` devuelve el resumen (por skill, proveedor y modelo; ejecuciones; reintentos; rechazos) y
   `GET /proyectos/{id}/metricas/exportar` los registros crudos en CSV. La pantalla del Proyecto muestra la tarjeta «Uso de IA» con la tabla y el botón
   «Exportar CSV».

## Consecuencias

- Para que el costo aparezca hay que cargar los precios vigentes en `LOOM_PRECIOS_MODELOS` antes de correr los escenarios.
- La duración de una llamada incluye la espera de red; la de una skill incluye todo su recorrido (Git, GitHub, esperas). Son distintas a propósito.
- Los datos quedan por Proyecto: para comparar proveedores sobre el mismo backlog hay que correr cada escenario en un Proyecto (o repositorio) propio.
- Las corridas anteriores a este ADR no tienen métricas.

## Pendiente

- Registrar el resultado de la revisión (observaciones por severidad) y la calificación humana (evaluación ciega) junto a estas métricas.
- Vista comparativa entre Proyectos y gráficas.
