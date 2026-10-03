@@ tesis_anexos+
CAPITULO: E
### Anexo E. Rúbricas de evaluación humana

El diseño de la evaluación define cuatro rúbricas (apartado 4.1.5). La de relevancia de una observación de revisión es la del experimento de control (apartado 4.1.7): la aplicó el modelo de la evaluación automática y es la misma que usará la persona, que recibe además una guía con el procedimiento, las reglas del cegado y un plan de calificación por sesiones. Las otras tres están definidas y no se aplicaron en esta etapa; se incluyen para que su aplicación posterior use los mismos criterios.

TABLA: Rúbrica de relevancia de una observación de revisión
| Calificación | Cuándo se usa |
| Relevante y correcta | Señala un problema real del cambio, y lo que dice es correcto y accionable. |
| Relevante pero mal sustentada | El problema es real, pero la explicación, la ubicación o la sugerencia son imprecisas o incompletas. |
| Ruido | Es cierto pero no aporta: una preferencia de estilo sin impacto, una obviedad o algo que no vale la pena corregir. |
| Falsa | Es incorrecta: el problema no existe o contradice el código, la HU o la arquitectura. |

Si dos observaciones del mismo Pull Request dicen en esencia lo mismo, quien califica las marca como equivalentes; así se cuenta cuántas observaciones relevantes de una condición encontró también la otra.

TABLA: Rúbrica de suficiencia de los casos de prueba de una HU
| Puntaje por criterio | Cuándo se asigna |
| 0, no cubierto | Ningún caso de prueba verifica el criterio. |
| 1, parcial | Algún caso toca el criterio, pero no verifica su resultado esperado o deja fuera alguna de sus condiciones. |
| 2, cubierto | Al menos un caso verifica el criterio completo, con un resultado esperado que se puede observar. |

Los casos redundantes, que repiten lo que ya verifica otro, y los inventados, que no derivan de ningún criterio, se cuentan aparte.

TABLA: Rúbrica de calidad de un paquete de código
| Dimensión | 0 | 1 | 2 |
| Cumple sus entregables | Falta la mayoría | Faltan algunos | Están todos |
| Sigue la arquitectura aprobada | La contradice | Se desvía en partes sin justificarlo | La sigue o justifica cada desviación |
| Pruebas con sentido | No prueba su lógica | Tiene pruebas que no verifican el comportamiento importante | Sus pruebas verifican el comportamiento que el paquete agrega |
| Compila y corre | No compila | Compila, pero falla al correr o en sus pruebas | Compila, corre y pasa sus pruebas |

Cada paquete recibe de 0 a 8 puntos.

TABLA: Rúbrica de calidad de la arquitectura y del plan (skills 4 y 5)
| Aspecto | Qué se valora |
| Coherencia con las HUs | Cada módulo, entidad y pantalla responde a una HU, y ninguna HU queda sin lugar donde implementarse. |
| Dependencias correctas | El orden de los paquetes y de las HUs respeta lo que cada uno necesita de los otros, sin ciclos. |
| Tamaño razonable de los paquetes | Cada paquete se puede generar, revisar y corregir por separado, sin mezclar capas ni repositorios. |

Cada aspecto se califica con la misma escala de 0 a 2 que las demás rúbricas.
