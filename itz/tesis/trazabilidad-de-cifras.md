# Trazabilidad de cifras

Generado por `herramientas/verificar_cifras.py`, que recalcula cada cifra desde los archivos versionados en `evidencia/` y la
compara con el valor que reporta la tesis (v04). No se edita a mano: se corrige el guion o el borrador y se vuelve a generar.

Comprobaciones: 86. Coinciden: 86. No coinciden: 0.

Las rutas son relativas a `itz/tesis/evidencia/`. «T» es tabla; los números sin «T» son apartados.

| Dónde aparece | Cifra | Valor en la tesis | Valor recalculado | Fuente | Estado |
|---|---|---|---|---|---|
| 5.2.1, T 5.2, T 5.12 | E1c: casos de prueba por HU | [14, 14, 16] | [14, 14, 16] | `corrida-E1c-2026-09-21/datos/hus.json` | Coincide |
| 5.2.1, T 5.12, T 4.2 | E1c: paquetes de trabajo | 12 | 12 | `corrida-E1c-2026-09-21/datos/paquetes.json` | Coincide |
| 5.2.4, T 5.12, T 4.2 | E1c: observaciones de las 12 primeras revisiones | 66 | 66 | `corrida-E1c-2026-09-21/datos/revisiones.json` | Coincide |
| 5.2.4, T 5.12 | E1c: bloqueantes, mayores y menores | [2, 24, 40] | [2, 24, 40] | `corrida-E1c-2026-09-21/datos/revisiones.json` | Coincide |
| 5.2.4 | E1c: observaciones por fuente (buenas prácticas, criterios, pruebas, seguridad, arquitectura) | [23, 15, 14, 9, 5] | [23, 15, 14, 9, 5] | `corrida-E1c-2026-09-21/datos/revisiones.json` | Coincide |
| 5.2.4 | E1c: promedio de observaciones por paquete | 5.5 | 5.5 | `corrida-E1c-2026-09-21/datos/revisiones.json` | Coincide |
| 5.2.3, T 5.3 | E1c: compuerta de compilación (aprobada, fallida, omitida) | [10, 5, 2] | [10, 5, 2] | `corrida-E1c-2026-09-21/datos/metricas.json (tipo compuerta)` | Coincide |
| 5.2.6, T 5.4, T 5.12 | E1c: pruebas de humo (aprobados, fallidos, bloqueados) | [36, 2, 6] | [36, 2, 6] | `corrida-E1c-2026-09-21/datos/smoke.json` | Coincide |
| 5.2.6 | E1c: porcentaje de casos aprobados | 82 | 82 | `corrida-E1c-2026-09-21/datos/smoke.json` | Coincide |
| T 5.4 | E1c: duración de las pruebas de humo por HU (min) | [5.3, 5.1, 3.3] | [5.3, 5.1, 3.3] | `corrida-E1c-2026-09-21/datos/smoke.json` | Coincide |
| T 5.2 | E1c: pruebas de humo, tiempo total (min) | 13.7 | 13.7 | `corrida-E1c-2026-09-21/datos/smoke.json` | Coincide |
| 5.2.8, T 5.6, T 5.12 | E1c: llamadas al modelo | 128 | 128 | `corrida-E1c-2026-09-21/datos/metricas.json (tipo llamada)` | Coincide |
| 5.2.8, T 5.6 | E1c: tokens de entrada y de salida | [2146219, 516483] | [2146219, 516483] | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| 5.2.8 | E1c: tokens leídos de caché (millones) | 14.6 | 14.6 | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| 5.2.8, T 5.6, T 5.12 | E1c: costo nocional (USD) | 16.67 | 16.67 | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| T 5.6 | E1c: generar código (llamadas, tokens in, out, min, USD) | [15, 855897, 387314, 53.3, 9.27] | [15, 855897, 387314, 53.3, 9.27] | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| T 5.6 | E1c: revisar código (llamadas, tokens in, out, min, USD) | [12, 528048, 24550, 5.5, 2.44] | [12, 528048, 24550, 5.5, 2.44] | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| T 5.6 | E1c: pruebas de humo (llamadas, tokens in, out, min, USD) | [81, 311216, 34958, 10.6, 2.19] | [81, 311216, 34958, 10.6, 2.19] | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| T 5.6 | E1c: corregir código (llamadas, tokens in, out, min, USD) | [3, 155788, 16142, 2.6, 0.95] | [3, 155788, 16142, 2.6, 0.95] | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| T 5.6 | E1c: descomponer (llamadas, tokens in, out, min, USD) | [10, 146207, 23826, 4.5, 0.9] | [10, 146207, 23826, 4.5, 0.9] | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| T 5.6 | E1c: arquitectura (llamadas, tokens in, out, min, USD) | [1, 53454, 12504, 2.0, 0.34] | [1, 53454, 12504, 2.0, 0.34] | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| T 5.6 | E1c: generar casos de prueba (llamadas, tokens in, out, min, USD) | [3, 46488, 10407, 1.7, 0.31] | [3, 46488, 10407, 1.7, 0.31] | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| T 5.6 | E1c: leer y especificar HUs (llamadas, tokens in, out, min, USD) | [3, 49121, 6782, 1.4, 0.28] | [3, 49121, 6782, 1.4, 0.28] | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| T 5.6 | E1c: tiempo de modelo total (min) | 81.5 | 81.5 | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| 5.2.8 | E1c: generación como % del costo y del tiempo de modelo | [56, 65] | [56, 65] | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| 5.2.8 | E1c: costo por paquete de revisar y de generar (USD) | [0.2, 0.77] | [0.2, 0.77] | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| T 5.2 | E1c: generar el código de los 12 paquetes (min de proceso) | 70.7 | 70.7 | `corrida-E1c-2026-09-21/datos/procesos.json` | Coincide |
| T 5.2 | E1c: revisar los 12 paquetes (min de proceso) | 6.6 | 6.6 | `corrida-E1c-2026-09-21/datos/procesos.json` | Coincide |
| T 5.2 | E1c: corregir un paquete (min de proceso) | 6.2 | 6.2 | `corrida-E1c-2026-09-21/datos/procesos.json` | Coincide |
| 5.2.3 | E1c: generación por paquete, mínimo y máximo (min de modelo) | [0.9, 10.8] | [0.9, 10.8] | `corrida-E1c-2026-09-21/datos/metricas.json` | Coincide |
| 5.2.4 | E1c: duración de una revisión, mínimo y máximo (min) | [0.4, 0.8] | [0.4, 0.8] | `corrida-E1c-2026-09-21/datos/revisiones.json` | Coincide |
| 5.2.4 | E1c: revisiones que aprobaron y que dejaron observaciones | [2, 10] | [2, 10] | `corrida-E1c-2026-09-21/datos/revisiones.json` | Coincide |
| 5.2.2 | E1c: reintentos de la descomposición sin paquetes | 3 | 3 | `corrida-E1c-2026-09-21/datos/metricas.json (tipo reintento)` | Coincide |
| 5.2.10 | E3c: revisiones que aprobaron y que dejaron observaciones | [7, 10] | [7, 10] | `corrida-E3c-2026-09-26/datos/revisiones.json` | Coincide |
| T 5.8 | E3c: observaciones y mayores de la primera revisión de cada paquete, en el orden de la tabla | [[4, 0], [4, 0], [3, 1], [3, 1], [6, 0], [4, 1], [5, 1], [2, 1], [3, 0], [7, 1], [5, 1], [3, 0], [3, 1], [3, 1], [1, 1], [0, 0], [3, 0]] | [[4, 0], [4, 0], [3, 1], [3, 1], [6, 0], [4, 1], [5, 1], [2, 1], [3, 0], [7, 1], [5, 1], [3, 0], [3, 1], [3, 1], [1, 1], [0, 0], [3, 0]] | `corrida-E3c-2026-09-26/datos/revisiones.json` | Coincide |
| 5.2.9 | E3c: procesos de generación terminados y cortados | [16, 3] | [16, 3] | `corrida-E3c-2026-09-26/datos/procesos.json` | Coincide |
| 5.2.9, T 5.7, T 5.12 | E3c: casos de prueba por HU | [35, 39, 27] | [35, 39, 27] | `corrida-E3c-2026-09-26/datos/hus.json` | Coincide |
| 5.2.9, T 5.12, T 4.2 | E3c: paquetes de trabajo | 17 | 17 | `corrida-E3c-2026-09-26/datos/paquetes.json` | Coincide |
| 5.2.10, T 5.12, T 4.2 | E3c: observaciones de las 17 primeras revisiones | 59 | 59 | `corrida-E3c-2026-09-26/datos/revisiones.json` | Coincide |
| 5.2.10, T 5.12 | E3c: bloqueantes, mayores y menores | [0, 10, 49] | [0, 10, 49] | `corrida-E3c-2026-09-26/datos/revisiones.json` | Coincide |
| 5.2.10 | E3c: observaciones por fuente (buenas prácticas, arquitectura, pruebas, seguridad, criterios) | [22, 11, 10, 9, 7] | [22, 11, 10, 9, 7] | `corrida-E3c-2026-09-26/datos/revisiones.json` | Coincide |
| 5.2.10 | E3c: promedio de observaciones por paquete | 3.5 | 3.5 | `corrida-E3c-2026-09-26/datos/revisiones.json` | Coincide |
| 5.2.10 | E3c: revisiones de toda la corrida y sus observaciones | [19, 69] | [19, 69] | `corrida-E3c-2026-09-26/datos/revisiones.json` | Coincide |
| 5.2.10 | E3c: mayores y menores de las 19 revisiones | [12, 57] | [12, 57] | `corrida-E3c-2026-09-26/datos/revisiones.json` | Coincide |
| 5.2.10, T 5.12 | E3c: registros de la compuerta de compilación «omitida» | 21 | 21 | `corrida-E3c-2026-09-26/datos/metricas.json (tipo compuerta)` | Coincide |
| 5.2.10 | E3c: rechazos de la compuerta de archivos obligatorios | 4 | 4 | `corrida-E3c-2026-09-26/datos/metricas.json (tipo compuerta)` | Coincide |
| 5.2.11, T 5.9, T 5.12 | E3c: pruebas de humo, corrida final (aprobados, fallidos, bloqueados) | [68, 9, 24] | [68, 9, 24] | `corrida-E3c-2026-09-26/datos/smoke.json` | Coincide |
| T 5.9 | E3c: pruebas de humo por HU (aprobados, fallidos, bloqueados) | [[28, 4, 3], [19, 4, 16], [21, 1, 5]] | [[28, 4, 3], [19, 4, 16], [21, 1, 5]] | `corrida-E3c-2026-09-26/datos/smoke.json` | Coincide |
| T 5.9, T 5.7 | E3c: duración de la corrida final por HU y total (min) | [17.8, 34.7, 11.2, 63.7] | [17.8, 34.7, 11.2, 63.7] | `corrida-E3c-2026-09-26/datos/smoke.json` | Coincide |
| 5.2.11 | E3c: casos bloqueados en las dos primeras corridas de la HU-001 | [33, 33] | [33, 33] | `corrida-E3c-2026-09-26/datos/smoke.json` | Coincide |
| 5.2.13, T 5.12 | E3c: llamadas al modelo | 532 | 532 | `corrida-E3c-2026-09-26/datos/metricas.json` | Coincide |
| 5.2.13, T 5.12 | E3c: costo nocional (USD) | 120.99 | 120.99 | `corrida-E3c-2026-09-26/datos/metricas.json` | Coincide |
| T 5.7 | E3c: generar el código, 16 procesos terminados (min) | 185.2 | 185.2 | `corrida-E3c-2026-09-26/datos/procesos.json` | Coincide |
| T 5.7 | E3c: revisar los 17 paquetes (min de proceso) | 13.6 | 13.6 | `corrida-E3c-2026-09-26/datos/procesos.json` | Coincide |
| resumen, 5.2.15 | Casos de prueba ejecutados en las dos corridas: total, aprobados, fallidos, bloqueados | [145, 104, 11, 30] | [145, 104, 11, 30] | `corrida-E1c-2026-09-21/datos/smoke.json y corrida-E3c-2026-09-26/datos/smoke.json` | Coincide |
| 5.2.14, T 5.13 | Exp. C: observaciones con contexto y con solo el diff | [85, 92] | [85, 92] | `experimento-c-2026-09-27/datos/resumen-c1.json` | Coincide |
| T 5.13 | Exp. C: contexto, bloqueantes, mayores y menores | [7, 21, 57] | [7, 21, 57] | `experimento-c-2026-09-27/datos/resumen-c1.json` | Coincide |
| T 5.13 | Exp. C: solo diff, bloqueantes, mayores y menores | [2, 21, 69] | [2, 21, 69] | `experimento-c-2026-09-27/datos/resumen-c1.json` | Coincide |
| T 5.13 | Exp. C: contexto por fuente (criterios, arquitectura, buenas prácticas, pruebas, seguridad) | [13, 19, 39, 9, 5] | [13, 19, 39, 9, 5] | `experimento-c-2026-09-27/datos/resumen-c1.json` | Coincide |
| T 5.13 | Exp. C: solo diff por fuente (criterios, arquitectura, buenas prácticas, pruebas, seguridad) | [0, 15, 50, 7, 20] | [0, 15, 50, 7, 20] | `experimento-c-2026-09-27/datos/resumen-c1.json` | Coincide |
| T 5.13 | Exp. C: costo nocional por condición (USD) | [14.81, 11.39] | [14.81, 11.39] | `experimento-c-2026-09-27/datos/resumen-c1.json` | Coincide |
| 5.2.14 | Exp. C: minutos de modelo por condición | [92.4, 100.0] | [92.4, 100.0] | `experimento-c-2026-09-27/datos/resumen-c1.json` | Coincide |
| 5.2.14 | Exp. C: entrada media por condición (caracteres) | [121611, 76529] | [121611, 76529] | `experimento-c-2026-09-27/datos/experimento_c-c1.json` | Coincide |
| 5.2.14 | Exp. C: diffs recortados a 140,000 caracteres | 3 | 3 | `experimento-c-2026-09-27/datos/resumen-c1.json` | Coincide |
| 5.2.14 | Exp. C: costo de la ejecución descartada (USD) | 12.9 | 12.9 | `experimento-c-2026-09-27/datos/resumen-c1.json` | Coincide |
| T 4.2 | Exp. C: observaciones por proyecto (E1c contexto y solo diff; E3c contexto y solo diff) | [44, 49, 41, 43] | [44, 49, 41, 43] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| 5.2.14 | Evaluación automática: observaciones calificadas | 177 | 177 | `experimento-c-2026-09-27/segunda-opinion/opinion-c1.json` | Coincide |
| 5.2.14 | Evaluación automática: minutos de modelo | 11.7 | 11.7 | `experimento-c-2026-09-27/segunda-opinion/opinion-c1.json` | Coincide |
| T 5.14 | Con contexto: relevante y correcta, mal sustentada, ruido, falsa | [24, 4, 45, 12] | [24, 4, 45, 12] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| T 5.14 | Solo diff: relevante y correcta, mal sustentada, ruido, falsa | [21, 7, 53, 11] | [21, 7, 53, 11] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| T 5.14 | Con contexto: porcentajes de las cuatro calificaciones | [28.2, 4.7, 52.9, 14.1] | [28.2, 4.7, 52.9, 14.1] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| T 5.14 | Solo diff: porcentajes de las cuatro calificaciones | [22.8, 7.6, 57.6, 12.0] | [22.8, 7.6, 57.6, 12.0] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| T 5.14, 6.1 | Relevantes en sentido amplio por condición y su porcentaje | [28, 32.9, 28, 30.4] | [28, 32.9, 28, 30.4] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| 5.2.14, 6.1 | Prueba pareada amplia: a favor de contexto, a favor de solo diff, empates, p de Wilcoxon, r | [7, 7, 15, 1.0, 0.0] | [7, 7, 15, 1.0, 0.0] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| 5.2.14 | Prueba pareada estricta: a favor de contexto, a favor de solo diff, empates, p de Wilcoxon, r | [8, 6, 15, 0.47, 0.2] | [8, 6, 15, 0.47, 0.2] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| 5.2.14 | Relevantes y total por proyecto (E1c contexto, E1c solo diff, E3c contexto, E3c solo diff) | [[18, 44], [17, 49], [10, 41], [11, 43]] | [[18, 44], [17, 49], [10, 41], [11, 43]] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| T 5.15 | Relevantes y total por fuente, con contexto (criterios, arquitectura, buenas prácticas, pruebas, seguridad) | [[6, 13], [5, 19], [11, 39], [1, 9], [5, 5]] | [[6, 13], [5, 19], [11, 39], [1, 9], [5, 5]] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| T 5.15 | Relevantes y total por fuente, solo diff (arquitectura, buenas prácticas, pruebas, seguridad) | [[5, 15], [10, 50], [1, 7], [12, 20]] | [[5, 15], [10, 50], [1, 7], [12, 20]] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| 5.2.14 | Bloqueantes válidas y total; mayores válidas y total (contexto, solo diff) | [[4, 7], [1, 2], [12, 21], [13, 21]] | [[4, 7], [1, 2], [12, 21], [13, 21]] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| 5.2.14, 6.1 | Pares equivalentes entre condiciones, con ambas relevantes, y hallazgos relevantes distintos | [18, 9, 47] | [18, 9, 47] | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| 5.2.14 | PRs sin ninguna observación relevante en ninguna condición | 7 | 7 | `experimento-c-2026-09-27/datos/resultados-c1-opinion.json` | Coincide |
| 5.2.15, T 5.16, 6.1.1 | PI1: criterios, cubiertos, explícitos, inferidos, casos | [110, 110, 33, 77, 145] | [110, 110, 33, 77, 145] | `cobertura-pi1/cobertura-pi1.json` | Coincide |
| 5.2.15 | PI1: criterios inferidos en E1c y total de E1c | [32, 39] | [32, 39] | `cobertura-pi1/cobertura-pi1.json` | Coincide |
| 5.2.15 | PI1: casos por criterio en E3c y en E1c | [1.42, 1.13] | [1.42, 1.13] | `cobertura-pi1/cobertura-pi1.json` | Coincide |
| 5.2.15 | PI1: supuestos abiertos en las seis HUs | 50 | 50 | `cobertura-pi1/cobertura-pi1.json` | Coincide |
| 5.2.15 | PI1: porcentaje de criterios inferidos | 70 | 70 | `cobertura-pi1/cobertura-pi1.json` | Coincide |

## Cifras que este guion no recalcula

- Tiempos de reloj de las etapas cortas (leer HUs, generar casos, arquitectura, descomponer) y del release de las tablas 5.2 y 5.7: salen de `procesos.json`, pero dependen de qué intento se toma (el que terminó bien); se cotejaron a mano contra la bitácora de cada corrida.
- Conteos de intervenciones de la persona (tablas 5.5 y 5.11) y de lanzamientos de release: provienen de la bitácora (`logs/bitacora.log`) y de los registros de hallazgos, no de una colección.
- Cifras de trabajos ajenos (1.96 %, 12.5 %, 19 %, 55.8 %, reducción de hasta 28.9 %, entre otras): se cotejaron contra el resumen de cada fuente; su estado está en `referencias-candidatas.md`.
- Conteos de palabras y de cuartillas: los imprime `herramientas/llenar_tesis.py` al generar el documento.
