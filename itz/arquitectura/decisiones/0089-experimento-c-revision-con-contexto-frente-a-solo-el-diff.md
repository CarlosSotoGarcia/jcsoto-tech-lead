# ADR-0089: Experimento C — revisión con contexto frente a revisión solo con el diff

## Estado

Aceptada. Instrumenta la hipótesis H1 (experimento C del plan de la tesis) sin cambiar la skill 07 ([ADR-0049](0049-skill-07-revision-de-codigo-y-correcciones.md)).

## Contexto

H1 sostiene que la revisión de código que recibe la HU, sus casos de prueba, el paquete de trabajo y la arquitectura aprobada detecta observaciones relevantes en mayor proporción que una revisión que solo ve el diff. Las corridas piloto E1c (Inventarios, 12 paquetes) y E3c (Agenda Taller, 17 paquetes) solo produjeron revisiones con contexto: no hay línea base.

Correr de nuevo los escenarios con una skill 07 «solo diff» no sirve: el código generado cambiaría y la comparación dejaría de ser sobre los mismos PRs. Los PRs de las dos corridas siguen en GitHub, y el diff que vio cada primera revisión se puede reconstruir: es el cambio del primer commit del PR (la generación) respecto a su padre, antes de cualquier corrección. Se comprobó contra el diff guardado (primeros 60 000 caracteres) de las 29 primeras revisiones y coincidieron las 29; 17 de ellos estaban recortados en Mongo, por eso se usa el reconstruido.

## Decisión

1. **Mismos PRs, dos condiciones.** Cada una de las 29 primeras revisiones se repite dos veces:
   - **Contexto:** el prompt de sistema y el mensaje de la skill 07 tal cual (`REVISION_SYSTEM` + `_contexto_revision`: paquete, arquitectura del repositorio, spec y casos de prueba de la HU, título y descripción del PR, diff). El paquete se toma del repositorio de control en el commit anterior a «<paquete>: revisión 1», no de Mongo: el `md` guardado se regenera después de cada revisión con sus observaciones y el estado final (`fusionado`). La spec, los casos de prueba y la arquitectura no cambiaron después de las primeras revisiones (se comprobó en los 29 paquetes con `verificar_contexto.py`).
   - **Solo diff:** un prompt de sistema con la misma estructura, fuentes, severidades y reglas, que declara que solo se tiene el diff y restringe `criterio_aceptacion` y `arquitectura` a lo que el propio diff deje ver. El mensaje es únicamente el diff.
2. **Mismo modelo y misma herramienta.** Las dos condiciones usan el mismo modelo fijo (`claude-sonnet-5` por el CLI de Claude Code, `LOOM_CLAUDE_CLI_MODEL`), el mismo esquema de salida (`registrar_revision`) y el mismo tope de diff (140 000 caracteres).
3. **Solo lo que dice el modelo.** No se agregan las observaciones que Loom inyecta por su cuenta (compuerta de compilación, supuestos sin confirmar): no dependen del contexto y sesgarían la comparación.
4. **Orden aleatorio.** El orden de las condiciones dentro de cada PR se sortea con una semilla fija (20260927) y queda registrado.
5. **Fuera del flujo.** El experimento es un módulo aparte (`loom_backend.experimentos.revision_contexto`) que lee los datos de Loom y escribe en la colección `experimento_c`; no toca los paquetes, las revisiones ni los PRs. Las llamadas quedan en `metricas` con la skill `experimento-c-contexto` o `experimento-c-solo_diff`.
6. **Evaluación ciega por una persona.** Las observaciones de las dos condiciones se mezclan por PR, se barajan y reciben un identificador anónimo; se ocultan la fuente y la severidad, que delatan la condición. Quien califica ve el PR, el paquete y la HU, y aplica la rúbrica del plan: relevante y correcta / relevante pero mal sustentada / ruido / falsa. La clave que une cada identificador con su condición va en un archivo aparte que no se abre hasta terminar de calificar. No califica el asistente que generó las observaciones.

## Consecuencias

- H1 se contesta con 29 pares sobre los mismos PRs y el mismo modelo: proporción de observaciones relevantes por condición, observaciones relevantes por PR (prueba pareada) y, con la clave, cuántas bloqueantes o mayores resultaron válidas.
- La primera ejecución de la condición «contexto» (2026-09-27) usó el `md` de Mongo y recibió, como parte del paquete, las observaciones de la última revisión del piloto: se descartó (queda en `experimento_c` como corrida `c1-descartada` y en `metricas` como `experimento-c-contexto-descartada`) y se repitió con el paquete reconstruido. Por eso, en `c1` las revisiones «contexto» se hicieron después de las «solo_diff» y el orden aleatorio del punto 4 solo aplica a la parte descartada; como cada llamada es independiente (sin memoria entre llamadas), el orden no afecta el resultado.
- Es una sola ejecución por condición: la variabilidad del modelo no se mide. Si el resultado queda cerca del empate, conviene repetir una muestra (corrida `c2`) antes de concluir.
- Se corre con la suscripción (CLI), no con la API: el costo es nocional y los tokens no son comparables con los de E1/E3, pero la comparación es dentro del mismo modelo, que es lo que H1 necesita.
- El modelo del experimento (Sonnet 5) no es el de la corrida E3c (Opus 5.5): las observaciones del experimento no reemplazan las del piloto ni se suman a ellas.
- Los diffs de más de 140 000 caracteres se recortan igual en las dos condiciones; queda registrado el tamaño de cada uno.
- La calificación depende de una persona; su tiempo es el cuello de botella del experimento, no el costo del modelo.
