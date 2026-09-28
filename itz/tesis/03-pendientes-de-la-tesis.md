# Pendientes de la tesis

Registro vivo de lo que falta actualizar o modificar en la tesis. Se agrega una fila cada vez que un cambio deja algo por hacer y se
marca como hecha (con la versión en que se resolvió) cuando se atiende. Complementa el § 14 del plan
([00-plan-de-llenado-de-tesis.md](00-plan-de-llenado-de-tesis.md)), que describe el estado general; aquí van las tareas concretas.

Última versión generada: **v03** (2026-09-28), desde `borrador/v03/`.

## Abiertos

| # | Sección | Qué hay que hacer | Origen | Depende de |
|---|---|---|---|---|
| 1 | 5.2.14, 5.1.4, 5.2.15, 6.1.1 (PI2), 6.1.2 (H1), 6.2, resumen | Agregar el resultado de H1: proporción de observaciones relevantes por condición, prueba pareada, bloqueantes y mayores válidas, observaciones compartidas; una gráfica por condición y calificación; aceptar o rechazar H1. Quitar «pendiente» de 5.1.4 («no se valoraron todavía») y de 5.2.15. | Experimento C (v03) | Calificación ciega de la hoja (`evidencia/experimento-c-2026-09-27/evaluacion-ciega/`) y `analizar.py c1` |
| 2 | Evidencia del experimento C | Tras calificar: versionar `clave/clave-c1.json` y `datos/experimento_c-c1.json`, comprobar sus SHA-256 contra el README y quitarlos del `.gitignore`. | Experimento C (v03) | Punto 1 |
| 3 | 4.1.7 | Sustituir `[CITA PENDIENTE: pruebas pareadas no paramétricas]` por una referencia verificada (prueba de rangos con signo de Wilcoxon y prueba de signos) y agregarla a `referencias-candidatas.md`. | v03 | — |
| 4 | 1.4 | Sustituir `[CITA PENDIENTE: carga de trabajo y traspasos en equipos pequeños]` por una referencia verificada o reformular la frase sin ella. | v01 | — |
| 5 | Anexos | La lista de anexos de `d-anexos-y-referencias.md` (C = *prompts*, D = ejemplo de una HU) choca con los anexos que sí existen (C = recorrido E1c, D = recorrido E3c): en el documento hay dos «Anexo C» y dos «Anexo D». Decidir la numeración final y reordenar. Propuesta: A ADR, B *skills*, C recorrido E1c, D recorrido E3c, E rúbricas, F *prompts*, G ejemplo completo de una HU, H datos crudos, I manual de instalación. | Revisión de v03 | Decisión del autor |
| 6 | Anexo E | Integrar las otras tres rúbricas (suficiencia de casos de prueba, calidad de un paquete, calidad de la arquitectura y del plan) cuando se apliquen; hoy solo está la de relevancia de observaciones. | v03 | Que se apliquen |
| 7 | Anexo de *prompts* | Incluir los *prompts* de la revisión en sus dos condiciones (`REVISION_SYSTEM` y `REVISION_SYSTEM_SOLO_DIFF`), extraídos del código, junto con los del resto de las *skills*. | Experimento C (v03) | Punto 5 |
| 8 | 5.2.14 | Opcional: medir cuántas de las 123 observaciones de la ejecución descartada repetían las del piloto (hoy el texto dice que no se analizó). | v03 | — |
| 9 | 4.1.3, 4.1.2, 1.5 | Si la validación se queda en los pilotos y el experimento C (sin la matriz E1–E4 con API), registrar la reducción de alcance en un ADR y ajustar la regla «uso de la API» y el diseño del capítulo 4. | Plan § 14.3 | Decisión del director (§ 10, decisiones 3, 4, 6, 7) |
| 10 | 5, 6 | Resultados de la matriz E1–E4 con API y de H3 (Claude frente a Gemini). | Plan § 14.2 punto 4 | Saldo en la API de Anthropic y facturación de Gemini; punto 9 |
| 11 | 6.3, 4.1.7 | Si hay tiempo: repetir el experimento C sobre una muestra (corrida `c2`) para medir la variabilidad y sumar una segunda persona evaluadora (acuerdo entre calificaciones). | v03 (trabajo futuro) | Punto 1 |
| 12 | Portada, oficio, agradecimientos | Título definitivo, nombre, director, fecha. | Plan § 14.2 punto 1 | Autor y director |
| 13 | Resumen y *abstract* | Escribirlos al final. | Plan § 14.2 punto 2 | Puntos 1 y 10 |
| 14 | 2, 3.1, 4.1, 4.2 | Ampliar volumen: capítulo 2 (+14 cuartillas), 3.1 (+6), 4.1 (+5), 4.2 (+10). v03 tiene ≈ 18,150 palabras (≈ 65 cuartillas con anexos); la guía pide 80 como mínimo. | Plan § 14.2 punto 3 | — |
| 15 | Todas | Crear `trazabilidad-de-cifras.md`: cada cifra del texto con su fuente (archivo de evidencia, consulta o commit). Incluir las nuevas del experimento C (Tabla 5.13). | Plan § 14.2 punto 6 | — |
| 16 | Anexos D–H del plan | Ejemplo completo de una HU, capturas finales, datos crudos, manual de instalación. | Plan § 14.2 punto 7 | Punto 5 |
| 17 | Todas | Pasadas de estilo (`redaccion-academica`, `humanizer`) y fijar la voz (decisión 14). | Plan § 14.2 punto 8 | — |
| 18 | Todas | Quitar los párrafos de instrucciones de la plantilla institucional antes de entregar, previa confirmación del director. | Plan § 14.5 | Director |
| 19 | 4.1 o nota metodológica | Declaración del uso de IA en la redacción (decisión 13). | Plan § 10 | Director |

## Hechos

| # | Qué | Versión |
|---|---|---|
| H1 | Experimento C en 4.1.7 (método), 5.2.14 (datos descriptivos, descarte y límites), Tabla 5.1 (fila del experimento), 5.2.15, 6.1.1, 6.1.2, 6.2 (dos recomendaciones), 6.3 (séptima línea) y Anexo E (rúbrica de relevancia). | v03 |
| H2 | `llenar_tesis.py`: los subtítulos aplican `*cursiva*` (antes salían los asteriscos, p. ej. «4.2.4 Las *skills* del pipeline» en v02). | v03 |
