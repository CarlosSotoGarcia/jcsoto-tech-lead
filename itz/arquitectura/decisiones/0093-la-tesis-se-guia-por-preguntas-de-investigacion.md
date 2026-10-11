# ADR-0093: La tesis se guía por preguntas de investigación y no por hipótesis

## Estado

Aceptada (2026-10-08). Sustituye el punto 3 de [ADR-0091](0091-experimento-c-se-reporta-la-evaluacion-automatica.md) («H1 no se declara aceptada ni rechazada»): el resultado del experimento C se reporta como respuesta a la pregunta PI2.

## Contexto

Hasta la v04, la tesis formulaba cinco preguntas de investigación (PI1 a PI5) y tres hipótesis (H1 a H3) con sus variables. Las hipótesis repetían el contenido de tres de las preguntas (H1 con PI2, H2 con PI3 y H3 con PI4), y ninguna podía comprobarse con la evidencia reunida: H1 dependía de una calificación humana que pasó a trabajo futuro (ADR-0091), H2 tenía evidencia parcial y H3 dependía de la matriz con API que no se ejecutó (ADR-0092).

En la revisión 1 de la v04, la directora de tesis propuso dejar solo las preguntas de investigación, «para no tener que comprobar hipótesis», salvo que hubiera una manera alcanzable de comprobarlas. El autor decidió quitarlas.

## Decisión

1. **Se quitan las hipótesis y las variables** (apartados 1.6 y 1.7 de la guía institucional, que los marca «si es pertinente»). La tesis se guía por PI1 a PI5.
2. **Cada resultado se reporta contra su pregunta.** El experimento C responde PI2; la corrida E3c, PI3; la matriz no ejecutada deja sin respuesta PI4. El método (4.1.6 y 4.1.8), los resultados (5.2.16) y las conclusiones (6.1.1) se organizan por pregunta.
3. **El análisis estadístico del experimento C no cambia.** La prueba de Wilcoxon, la prueba de signos, la correlación rango-biserial y el nivel de 0.05 se mantienen como forma de responder PI2; ya no se presentan como contraste de una hipótesis de la tesis.

## Consecuencias

- Los registros anteriores que mencionan H1 (ADR-0089 a ADR-0091) no se editan; H1 corresponde a PI2.
- El resumen, el *abstract*, la introducción y los capítulos 1, 3, 4, 5 y 6 de la tesis v05 dejan de mencionar hipótesis.
- La respuesta a PI2 sigue siendo preliminar mientras falte la calificación por una persona.
