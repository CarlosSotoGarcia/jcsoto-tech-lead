# ADR-0090: Experimento C — segunda opinión automática, sellada hasta la calificación humana

## Estado

Aceptada. Complementa el experimento C ([ADR-0089](0089-experimento-c-revision-con-contexto-frente-a-solo-el-diff.md)) sin cambiar su instrumento principal.

## Contexto

H1 se decide con la calificación ciega, por una persona, de las 177 observaciones del experimento C. Esa calificación toma de 7 a 8 horas y depende de una sola persona, así que no se puede medir el acuerdo entre evaluadores. Un modelo puede aplicar la misma rúbrica en minutos, pero no debe ser el juez de la hipótesis: los modelos usados como jueces muestran sesgos de posición, de longitud y de preferencia por respuestas parecidas a las suyas, y el asistente que corrió el experimento conoce la clave.

La segunda opinión de la revisión ya existe como función de Loom para un paquete ([ADR-0069](0069-segunda-opinion-de-la-ia-sobre-las-observaciones-de-la-revision.md)); aquí se necesita sobre el paquete ciego completo y con las mismas categorías que usa la persona.

## Decisión

1. **Qué es.** Una calificación automática de las mismas 177 observaciones con la rúbrica de la persona (relevante y correcta, relevante pero mal sustentada, ruido, falsa), una llamada por Pull Request.
2. **A ciegas.** Cada llamada es nueva y sin memoria. Recibe lo mismo que la persona (paquete reconstruido, arquitectura aprobada, especificación y casos de prueba de la HU, diff del cambio revisado) y las observaciones con su identificador anónimo, en el orden de la hoja. No recibe la condición, la fuente ni la severidad.
3. **Otro modelo.** Se usa `claude-opus-5-5`, distinto del que hizo las revisiones (`claude-sonnet-5`), por el CLI. Es de la misma familia, y eso se declara como límite.
4. **Sellada.** Los resultados se guardan en la colección `experimento_c_opinion` y en `segunda-opinion/` de la evidencia, fuera de git y sin mostrarse a quien califica hasta que termine, para no anclar su juicio. Su SHA-256 se publica en el README. Tampoco se reportan cifras por condición antes de ese momento.
5. **Para qué sirve.** Al terminar la persona se calculan el acuerdo entre las dos calificaciones (porcentaje y kappa de Cohen) y, como análisis secundario, el resultado de H1 con la calificación automática. El resultado de H1 que reporta la tesis es el de la persona.
6. **Contexto del evaluador.** Se agrega al paquete ciego el documento de arquitectura de cada proyecto, que faltaba para juzgar las observaciones sobre arquitectura, y un plan de calificación por sesiones. La hoja y la clave no cambian.

## Consecuencias

- La tesis puede reportar un acuerdo entre la persona y un segundo calificador, aunque ese segundo sea un modelo; no sustituye a una segunda persona evaluadora, que sigue como trabajo futuro.
- Si el acuerdo es bajo, el hallazgo es que la rúbrica o el modelo no son confiables como juez, y se reporta así; no se ajusta la calificación humana para acercarla.
- El modelo calificador y el revisor son de la misma familia: un sesgo a favor de su propio estilo afectaría por igual a las dos condiciones, pero no se puede descartar.
- Costo nocional cercano a 1 USD por Pull Request con el CLI (suscripción).
