@@ tesis_referencias
[POR COMPLETAR: la lista de referencias sigue el formato IEEE, numerada por orden de primera aparición en el texto. Las claves [N:...] del cuerpo son marcas de trabajo y se sustituyen por su número cuando la fuente se verifique. La lista de claves y el estado de cada una están en referencias-candidatas.md. No se incluye ninguna referencia cuyos datos (autores, año, título, publicación) no se hayan comprobado contra la fuente.]

@@ tesis_anexos
CAPITULO: A
Anexo A. Registros de decisión de arquitectura (ADR). Lista generada de la carpeta de decisiones del repositorio; cada registro conserva su contexto, su decisión y sus consecuencias.

TABLA-ADR:

Anexo B. Fichas de las *skills*. Cada ficha describe el propósito de la *skill*, cuándo se invoca, sus entradas y salidas, los registros de decisión relacionados, los criterios de éxito y los pendientes propios. Las fichas se conservan en la carpeta de *skills* del repositorio y se integrarán completas: 00 Orquestador; 01 Descubrimiento y especificación de HU; 02 Generación de casos de prueba; 03 Diagnóstico de avance existente; 04 Diseño de arquitectura; 05 Descomposición en paquetes de trabajo; 06 Generación de código; 07 Revisión de código; 08 Pruebas de humo; 09 Generación de correcciones; 10 Generación de release.

Anexo C. Prompts de cada skill. Pendiente de integrar: se extraerán del código de la plataforma para evitar transcripciones manuales.

Anexo D. Ejemplo completo de una HU. Pendiente de integrar: se usará la HU de inicio de sesión del proyecto experimental, con su especificación, sus casos de prueba, sus paquetes, los Pull Requests con sus rondas de revisión y el informe de las pruebas de humo.

CAPITULO: E
Anexo E. Rúbricas de evaluación humana. La rúbrica de relevancia de una observación de revisión es la del experimento de control del apartado 4.1.7. La aplicó el modelo de la evaluación automática y es la misma que usará la persona, que recibe además una guía con el procedimiento, las reglas del cegado y un plan de calificación por sesiones. Las rúbricas de suficiencia de los casos de prueba, de calidad de un paquete de código y de calidad de la arquitectura y del plan se integrarán cuando se apliquen.

TABLA: Rúbrica de relevancia de una observación de revisión
| Calificación | Cuándo se usa |
| Relevante y correcta | Señala un problema real del cambio, y lo que dice es correcto y accionable. |
| Relevante pero mal sustentada | El problema es real, pero la explicación, la ubicación o la sugerencia son imprecisas o incompletas. |
| Ruido | Es cierto pero no aporta: una preferencia de estilo sin impacto, una obviedad o algo que no vale la pena corregir. |
| Falsa | Es incorrecta: el problema no existe o contradice el código, la HU o la arquitectura. |

Si dos observaciones del mismo Pull Request dicen en esencia lo mismo, quien califica las marca como equivalentes; así se cuenta cuántas observaciones relevantes de una condición encontró también la otra.

Anexo F. Capturas de la plataforma. Pendiente de integrar: se tomarán al final, con la interfaz ya estabilizada.

Anexo G. Datos crudos de los escenarios. Pendiente de integrar.

Anexo H. Manual de instalación. Pendiente de integrar.
