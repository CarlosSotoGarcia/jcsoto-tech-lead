# ADR-0091: Experimento C — la evaluación que se reporta es la automática

## Estado

Aceptada. Para la corrida `c1`, sustituye el punto 6 de [ADR-0089](0089-experimento-c-revision-con-contexto-frente-a-solo-el-diff.md) (evaluación ciega por una persona) y los puntos 4 y 5 de [ADR-0090](0090-experimento-c-segunda-opinion-automatica-sellada.md) (segunda opinión sellada y secundaria) como fuente del resultado que reporta la tesis.

## Contexto

La calificación ciega de las 177 observaciones por una persona toma de 7 a 8 horas. El 2026-09-29 el autor decidió no hacerla en esta etapa y reportar la calificación automática que ya existía, sellada, por ADR-0090. Esa decisión cambia quién juzga la relevancia: el diseño pedía una persona precisamente porque un modelo usado como juez tiene sesgos conocidos, y la tesis lo argumenta en su marco teórico.

## Decisión

1. **Se reporta la evaluación automática, nombrada como tal.** El resultado de `c1` que aparece en la tesis es el de `claude-opus-5-5` calificando a ciegas con la rúbrica de cuatro categorías. En todo el texto se llama «evaluación automática» y nunca «evaluación ciega por una persona».
2. **El sello se abre con comprobación.** Antes de usar la calificación se verificó que las huellas SHA-256 publicadas de la opinión, de la clave y de los datos crudos coinciden con los archivos. El análisis es el mismo guion previsto para la calificación humana (`analizar.py c1 opinion`), y su salida se guarda aparte (`datos/resultados-c1-opinion.json`), con el calificador anotado.
3. **H1 no se declara aceptada ni rechazada.** El instrumento que decide la hipótesis sigue siendo la calificación por una persona. La tesis reporta que la evaluación automática no encontró evidencia a favor de H1 y deja la hipótesis abierta.
4. **Se versionan la clave, los datos crudos y la opinión.** El resultado publicado tiene que poder reproducirse. A cambio, una calificación humana posterior sobre `c1` dependerá de que quien califique no consulte esos archivos ni el resultado ya publicado; si se necesita un cegado limpio, se hará sobre una corrida nueva.
5. **El paquete ciego se conserva.** La hoja, el contexto, la guía y el plan de sesiones quedan listos para la calificación humana, que pasa a trabajo futuro; con ella se medirá el acuerdo (`comparar_opiniones.py`).

## Consecuencias

- El resultado de `c1`: 28 observaciones relevantes en cada condición (32.9 % de 85 con contexto, 30.4 % de 92 con solo el diff); en la comparación pareada, 7 Pull Requests a favor de cada condición y 15 empates (Wilcoxon, p = 1.0). Con el criterio estricto, 28.2 % frente a 22.8 % (p = 0.47). Solo 9 de las 28 observaciones relevantes de cada condición son el mismo hallazgo.
- El límite principal es el juez: un modelo de la misma familia que el revisor, sin una calificación humana que permita medir su acuerdo. La tesis lo declara en el método, en los resultados y en las conclusiones, junto con la contradicción con su propio marco teórico.
- El nivel de significancia (0.05, bilateral) y el tamaño del efecto se fijaron y se versionaron antes de abrir el sello.
- Queda abierta la posibilidad de que una calificación humana cambie el resultado; si ocurre, se reportan las dos y el acuerdo entre ellas.
