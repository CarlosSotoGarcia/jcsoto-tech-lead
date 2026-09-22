@@ tesis_6_1
### 6.1.1 Respuesta a las preguntas de investigación

PI1 (cobertura de los casos de prueba sobre los criterios de aceptación) tiene una respuesta parcial. Loom generó 44 casos de prueba a partir de los criterios de las tres HUs de la corrida del capítulo 5, y las pruebas de humo los ejecutaron contra la aplicación desplegada: 36 pasaron, 2 fallaron y 6 quedaron bloqueados por falta de datos de prueba. No se midió todavía qué proporción de los criterios de aceptación, uno por uno, quedó cubierta por al menos un caso, que es lo que la pregunta plantea en sentido estricto; el dato disponible es el resultado de ejecutar los casos generados, no la cobertura de los criterios de origen.

PI2, PI3 y PI4 no tienen respuesta: exigen comparar una revisión con contexto contra una revisión que solo recibe el *diff* (PI2), correr el mismo flujo en un segundo Proyecto de otro dominio (PI3) y repetir la corrida con Gemini en condiciones equivalentes (PI4). El capítulo 5 documenta una sola corrida, con un solo Proyecto y un solo proveedor, y por diseño no puede contestarlas.

PI5, exploratoria, tiene una respuesta parcial y es el hallazgo más claro del capítulo 5. Los dos fallos de las pruebas de humo (TC-014 de la HU-002 y TC-016 de la HU-003) son del mismo tipo: piden una bitácora de auditoría visible para el administrador que ni la revisión de código ni la compilación detectaron como ausente, porque ningún criterio de aceptación explícito la exige con ese nivel de detalle y las 66 observaciones de las 12 revisiones no señalaron el vacío. Es exactamente la clase de defecto que la pregunta anticipa: pasa la revisión automática y la compilación, y solo se manifiesta al ejecutar el sistema.

### 6.1.2 Estado de las hipótesis

Ninguna de las tres hipótesis se puede aceptar ni rechazar con la evidencia reunida hasta este corte.

H1 (el contexto entregado a la revisión mejora la relevancia de sus observaciones frente a solo el *diff*) sigue abierta. La corrida no incluyó una revisión de control con solo el *diff*, y las 66 observaciones registradas no se valoraron todavía como relevantes, mal sustentadas o ruido por una persona a ciegas, que es el instrumento que el capítulo 4 define para esta comparación.

H2 (el sistema es generalizable entre dominios cambiando solo la configuración) sigue abierta. Solo se corrió el Proyecto de inventarios; falta ejecutar el mismo flujo, sin tocar las *skills*, sobre el segundo Proyecto de dominio distinto que el diseño experimental prevé.

H3 (el proveedor de IA afecta la calidad y el costo del resultado, con la arquitectura permitiendo intercambiarlo) sigue abierta en su parte comparativa. La arquitectura sí demostró ser intercambiable en la práctica: la misma plataforma ejecutó corridas con Claude por API, con Claude por CLI y con Gemini sin cambiar ninguna *skill*, solo la configuración del Proyecto. Lo que falta es la comparación de calidad y costo en condiciones equivalentes: la corrida con Gemini de la primera etapa del piloto no cubrió las mismas HUs con el mismo procedimiento que la corrida de Claude reportada en el capítulo 5, y por eso no es comparable.

### 6.1.3 Cumplimiento de los objetivos específicos

De los 11 objetivos específicos del capítulo 1, la plataforma implementa las skills que cubren los objetivos 2 a 9: análisis de HU y generación de casos de prueba, diagnóstico de avance existente, diseño de arquitectura y descomposición, generación de código con Pull Requests, revisión con ciclo de observaciones y rondas de corrección, ejecución de casos de prueba con Playwright, y generación de fixes ante un caso fallido. El objetivo 1 (modelo de Proyecto y fuente de HUs *pluggable*) está cubierto para Jira y Markdown, y no para GitHub como fuente de HUs; el objetivo 9 (indexación multi-repositorio) quedó solo a nivel de diseño, sin implementación. El objetivo 10 (validar en dos o tres proyectos, con y sin avance previo, variando la fuente) no se cumplió: la corrida del capítulo 5 valida un solo Proyecto, greenfield, con Jira como fuente. El objetivo 11 (medir por HU) se cumplió de forma parcial: el capítulo 5 reporta tiempo, tokens y costo por *skill* y por paquete, pero no agregado por HU completa, ni el resultado de la integración continua desglosado por paquete más allá de lo narrado en el Anexo C.

La plataforma incorpora, además, capacidades que los 11 objetivos originales no previeron: el despliegue a Google Cloud con base de datos y secretos, el release automático por GitHub Actions con identidad federada, las compuertas de ejecución previas al Pull Request, la corrección automática con el registro de la integración continua, la pantalla de decisiones de negocio sobre los supuestos de una HU, y los procesos concurrentes con reglas de exclusión, historial y cancelación. Estas capacidades resultaron necesarias durante la construcción del sistema, principalmente porque un flujo que termina en código sin ejecutar sirve de poco: sin desplegar la aplicación no hay ambiente contra el cual correr las pruebas de humo del objetivo 7. Se reportan aquí como alcance ampliado y no como desviación, precisamente porque no estaban en el objetivo original.

@@ tesis_6_2
La corrida del capítulo 5 y el registro de hallazgos de las dos etapas del piloto dejan un conjunto de recomendaciones para quien adopte un enfoque semejante, derivadas de lo que ocurrió y no de principios generales.

Ejecutar en un contenedor aislado, antes de abrir el Pull Request, la compilación, el análisis estático y las pruebas unitarias del código generado. En la primera etapa del piloto, sin esa compuerta, el código llegaba a integración continua o al despliegue con errores que un paso local barato habría detectado antes; con la compuerta en su lugar, la corrida del capítulo 5 solo tuvo un paquete que la agotó en sus tres intentos, y ese fue el único que necesitó una ronda de corrección.

No fusionar con la integración continua en un estado distinto de verde, incluida la espera activa cuando los *checks* todavía están corriendo. La corrida del capítulo 5 topó con este caso (BASE/PT-05) y la plataforma detuvo la fusión hasta que el resultado quedó disponible.

Dar a la revisión el contexto de la historia de usuario, sus criterios de aceptación y la arquitectura aprobada, y no solo el cambio de código. La corrida no midió si ese contexto mejora la relevancia de las observaciones frente a solo el *diff* (H1 sigue abierta), pero si se agrega esa medición, debe hacerse con una persona evaluando a ciegas y con una rúbrica escrita, para que el resultado no dependa del juicio de quien construyó el sistema.

Correr pruebas de humo contra un ambiente desplegado, no solo revisar el código. Los dos fallos detectados en la corrida del capítulo 5 (bitácora de auditoría ausente) no aparecieron en ninguna de las 66 observaciones de las 12 revisiones ni impidieron que el código compilara: solo se manifestaron al ejecutar el sistema.

Sembrar las cuentas y los datos de prueba antes de correr las pruebas de humo, y no después de que fallen por falta de datos. Cinco de los seis casos bloqueados en la corrida dependían de una cuenta, un buzón de correo o un estado de cuenta que el ambiente no tenía preparado.

Congelar la versión del modelo y de la plataforma antes de medir, y registrar ambas junto con la fecha de cada corrida. La salida de un modelo de lenguaje es probabilística y su versión cambia con el tiempo; sin ese registro, una corrida posterior no es comparable con esta.

Prever el límite de uso del proveedor de IA como parte del plan de una corrida larga, no como una excepción. La generación de un paquete de la corrida del capítulo 5 falló por el límite de sesión de una suscripción, y una corrida de varias horas debe esperar ese tipo de interrupción y saber reanudar donde quedó.

Declarar, para cada intervención de la persona durante una corrida, si ocurrió con una acción de la propia plataforma o fuera de ella. Tres de las nueve intervenciones de la corrida del capítulo 5 se hicieron fuera de Loom (fusionar el Pull Request de despliegue, recrear una base de datos con datos de una corrida anterior y sembrar las cuentas de prueba); sin esa distinción, un informe de autonomía puede dar a entender que el sistema hizo más de lo que hizo.
