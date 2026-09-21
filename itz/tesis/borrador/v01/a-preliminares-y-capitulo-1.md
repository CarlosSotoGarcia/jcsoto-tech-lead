@@ tesis_simbolos
TABLA:
| Sigla | Significado |
| ADR | *Architecture Decision Record* (registro de decisión de arquitectura) |
| API | *Application Programming Interface* (interfaz de programación de aplicaciones) |
| CI/CD | Integración continua y entrega o despliegue continuos |
| CLI | *Command-Line Interface* (interfaz de línea de comandos) |
| E2E | *End-to-end* (de extremo a extremo) |
| GCP | *Google Cloud Platform* |
| HU | Historia de usuario |
| IA | Inteligencia artificial |
| LLM | *Large Language Model* (modelo de lenguaje de gran tamaño) |
| MCP | *Model Context Protocol* |
| PR | *Pull Request* (solicitud de integración de cambios) |
| SDD | *Spec-Driven Development* (desarrollo dirigido por especificaciones) |
| SSE | *Server-Sent Events* (eventos enviados por el servidor) |
| TC | *Test Case* (caso de prueba) |
| TDD | *Test-Driven Development* (desarrollo dirigido por pruebas) |
| WIF | *Workload Identity Federation* (federación de identidad de cargas de trabajo) |

@@ tesis_introduccion
El desarrollo de software con asistentes basados en modelos de lenguaje de gran tamaño (*large language models*, LLM) ya forma parte del trabajo cotidiano de muchos equipos. Un modelo escribe una función, propone pruebas o comenta un cambio ajeno, y una revisión sistemática reciente reunió cerca de cuatrocientos trabajos sobre esas aplicaciones [N:hou-slr]. Lo que sigue sin resolverse es el conjunto: cada herramienta atiende una etapa aislada del ciclo y deja a las personas la tarea de unirlas.

Esta tesis parte de una observación sobre esa práctica. Las herramientas actuales suelen automatizar una sola etapa, por ejemplo la generación de pruebas o la revisión de código. Además dan por hecho un proyecto nuevo y revisan el código que se les entrega sin conocer la intención de negocio que lo originó. La revisión de un cambio recibe el *diff*, pero no la historia de usuario (HU) que lo justifica, ni sus criterios de aceptación, ni la arquitectura acordada. Es una desventaja de fondo: en la revisión humana, la comprensión del código y del cambio es el aspecto central, y las herramientas actuales cubren mal esa necesidad [N:bacchelli-bird]. El ciclo tampoco se cierra con una validación funcional contra un ambiente real.

El trabajo propone y construye Loom, un sistema de *skills* de inteligencia artificial que, a partir de una HU, orquesta el ciclo de desarrollo de una funcionalidad. Recorre la generación de casos de prueba, el diagnóstico de lo que ya existe, el diseño de la arquitectura, la descomposición en paquetes de trabajo, la generación de código con su Pull Request, la revisión y corrección de ese código, la validación con pruebas de humo y el despliegue. La idea central es dar al modelo, como contexto explícito, la HU, los casos de prueba derivados de sus criterios y la arquitectura aprobada, y exigir evidencia verificable en cada paso. Una persona conserva los puntos de decisión: aprueba la arquitectura, confirma los supuestos de una HU y puede intervenir en cualquier fase.

Loom se implementa como una plataforma web con un servidor en Python, una base de datos documental y una interfaz en Angular. Trabaja con dos proveedores de IA (Claude y Gemini) sin cambiar las *skills*, y con fuentes de historias de usuario intercambiables (Jira y archivos Markdown). La validación se plantea sobre proyectos de dominios distintos y con más de un proveedor de IA, y mide, entre otras cosas, la cobertura que los casos de prueba dan a los criterios de aceptación, la relevancia de las observaciones de la revisión, el número de rondas hasta aprobar, el tiempo y el costo.

El documento se organiza en seis capítulos. El capítulo 1 delimita el problema, formula las preguntas de investigación, los objetivos, los alcances y las limitaciones, así como las hipótesis y las variables. El capítulo 2 reúne los fundamentos teóricos: modelos de lenguaje y agentes con herramientas, desarrollo dirigido por especificaciones, pruebas, revisión de código y entrega continua. El capítulo 3 revisa los trabajos relacionados y los compara con Loom. El capítulo 4 describe la metodología, tanto el diseño de la investigación como el sistema construido. El capítulo 5 presenta las pruebas y sus resultados. El capítulo 6 cierra con las conclusiones, las recomendaciones y el trabajo futuro.

@@ tesis_1_1
Las herramientas de asistencia por IA para el desarrollo de software cubren, en su mayoría, un tramo estrecho del ciclo. Unas generan código a partir de una instrucción, otras sugieren pruebas y otras comentan un cambio ya escrito [N:hou-slr]. Quien desarrolla una funcionalidad completa debe encadenar esas piezas a mano: pasar la intención de negocio de un asistente al siguiente, comprobar que las pruebas correspondan a los criterios acordados y verificar que lo generado funcione en un ambiente real.

Ese encadenamiento manual deja tres carencias. La primera es la falta de continuidad entre etapas: nada garantiza que los casos de prueba, el diseño, el código y la revisión partan de la misma historia de usuario y de sus criterios de aceptación. La segunda es el supuesto de un proyecto nuevo. En la práctica, la mayoría del trabajo ocurre sobre aplicaciones con código, convenciones y arquitectura existentes, y una herramienta que ignora ese avance previo reescribe o contradice lo que ya hay. Los bancos de tareas construidos con repositorios reales lo muestran: resolver un *issue* obliga a editar varios archivos de un código existente, y los primeros modelos evaluados resolvieron una fracción mínima de las tareas [N:swe-bench]. La tercera es la revisión sin contexto: el modelo que revisa ve el *diff*, pero no sabe qué problema de negocio resuelve ni qué arquitectura se aprobó, por lo que sus observaciones tienden a la forma del código y no a su adecuación a lo pedido.

A esto se suma un problema de verificación. Un modelo de lenguaje produce código plausible sin garantía de que compile, pase sus pruebas o arranque en un ambiente real. Al endurecer las pruebas con que se evalúa, la tasa de aciertos de modelos muy usados cae hasta 28.9 % [N:evalplus]. Una revisión, humana o automática, que solo lee el código no sustituye esa comprobación. El flujo completo necesita compuertas de ejecución y una validación funcional que cierre el ciclo.

La pregunta que guía este trabajo es la siguiente: ¿cómo orquestar con IA el ciclo de desarrollo de una funcionalidad a partir de una historia de usuario, entregando como contexto la intención de negocio, de modo que el resultado sea verificable, revisable y generalizable a distintos proyectos y proveedores de IA?

@@ tesis_1_2
Las preguntas de investigación se derivan del problema y de las hipótesis del apartado 1.6. Las cuatro primeras son confirmatorias y la última es exploratoria.

PI1. ¿En qué medida los casos de prueba generados a partir de los criterios de aceptación de una HU cubren esos criterios?

PI2. ¿Una revisión de código que recibe la HU, sus casos de prueba y la arquitectura aprobada produce observaciones más relevantes que una revisión que solo recibe el *diff*?

PI3. ¿Puede el mismo flujo completar el ciclo de desarrollo en proyectos de dominios distintos modificando su configuración y no sus *skills*?

PI4. ¿Qué diferencias de calidad, tiempo y costo se observan al intercambiar el proveedor de IA (Claude y Gemini) sin cambiar el resto del sistema?

PI5 (exploratoria). ¿Qué defectos del código generado superan la revisión automática y la compilación, y solo se manifiestan al ejecutar el sistema?

@@ tesis_1_3_1
Diseñar e implementar un sistema de *skills* de IA que, a partir de una historia de usuario, orqueste todo el ciclo de desarrollo de una funcionalidad (generación de casos de prueba, diagnóstico de avance existente, diseño de arquitectura, descomposición en paquetes de trabajo, generación de código, revisión de código, integración y validación funcional mediante pruebas de humo) de forma generalizable a distintos repositorios y sistemas, ya sea que el proyecto arranque desde cero o ya tenga avance previo.

@@ tesis_1_3_2
1. Diseñar el modelo de configuración de Proyecto (tipo de proyecto, repositorios y ambiente de desarrollo) y el mecanismo de lectura de elementos del backlog desde una fuente intercambiable (Jira, Markdown o GitHub), clasificando cada uno como HU o Actividad.

2. Diseñar el mecanismo de análisis de una HU y sus criterios de aceptación para generar casos de prueba derivados de ellos, documentado como especificación y casos de prueba (SDD).

3. Diseñar el mecanismo de diagnóstico de avance existente: ejecutar los casos de prueba generados contra el estado actual del ambiente antes de diseñar, para distinguir lo que ya está cubierto de lo que falta.

4. Diseñar el mecanismo de diseño de arquitectura y de descomposición en paquetes de trabajo a partir de los casos de prueba que el diagnóstico marcó como pendientes, respetando y extendiendo lo que ya existe.

5. Implementar la *skill* de generación de código por paquete de trabajo y de apertura de Pull Requests.

6. Implementar la *skill* de revisión de código y el ciclo de aplicación de observaciones hasta que un Pull Request queda sin pendientes.

7. Implementar la *skill* de ejecución de casos de prueba (Playwright, Python) contra un ambiente de desarrollo configurado, reutilizada para el diagnóstico inicial y para las pruebas de humo finales, con evidencia como salida.

8. Diseñar el mecanismo de fallo a paquete de trabajo de corrección, que reintroduce el ciclo de generación y revisión de código hasta que los casos de prueba correspondientes pasan.

9. Diseñar, sin desplegarlo ni operarlo como servicio persistente, el mecanismo de indexación multi-repositorio que da contexto de código a las *skills* anteriores.

10. Validar el sistema completo sobre al menos dos o tres proyectos web de dominios distintos, con al menos un caso sin código previo y uno con avance previo, variando la fuente de HUs, cada uno con su propia configuración.

11. Medir, por HU procesada, la tasa de casos de prueba que cubren los criterios de aceptación, la proporción de criterios ya cubiertos detectada correctamente en el diagnóstico inicial, el número de rondas de revisión hasta la aprobación, la tasa de éxito de las pruebas de humo por iteración y el grado de generalización entre proyectos y fuentes de HUs distintas.

@@ tesis_1_4
Loom se dirige a equipos pequeños, y a personas que desarrollan solas, que mantienen aplicaciones web con un backlog en una herramienta de seguimiento. En ese contexto una misma persona suele encargarse de aclarar requerimientos, escribir pruebas, programar, revisar y desplegar, y cada traspaso entre etapas consume tiempo y se presta a omisiones [CITA PENDIENTE: carga de trabajo y traspasos en equipos pequeños]. Un experimento controlado con una tarea acotada reportó que quienes usaron un asistente la completaron 55.8 % más rápido que el grupo de control [N:peng-copilot]; el resultado corresponde a una sola tarea y no a un ciclo completo.

La utilidad práctica está en la trazabilidad y en el control. Cada HU deja una cadena de evidencia verificable: la especificación con sus criterios, los casos de prueba y el criterio del que cada uno deriva, los paquetes de trabajo, el Pull Request con sus rondas de revisión y el informe de las pruebas de humo. Esa cadena permite auditar qué decidió el sistema y por qué, y localizar en qué etapa se introdujo un defecto. Las compuertas de ejecución (compilación, pruebas y verificación de la integración continua) impiden que el flujo avance sobre código que no pasa lo que un ejecutor real comprueba.

Dejar el ciclo sin automatizar de punta a punta tiene un costo. La revisión sin contexto genera observaciones sobre la forma y no sobre la adecuación a lo pedido, y el código que se revisó con detalle puede fallar igualmente al ejecutarse; la revisión trata menos de defectos de lo que suele suponerse y se apoya sobre todo en comprender el cambio [N:bacchelli-bird]. Además, quien adopta un asistente por etapa debe integrar sus salidas sin una fuente común de contexto.

Desde el punto de vista académico, el trabajo aporta un marco reproducible, con su herramienta funcional, que somete a medición una idea concreta: que entregar al modelo la HU, sus casos de prueba y la arquitectura aprobada mejora la relevancia de la revisión y la cobertura de los criterios frente a un modelo que solo ve el *diff*. También aporta datos sobre el intercambio de proveedor de IA sin modificar las *skills*, y un registro de los defectos que el código generado presenta al ejecutarse.

@@ tesis_1_5
El sistema abarca las fases de requerimientos, diseño, desarrollo e implementación para aplicaciones de tipo web. Acepta como fuente de HUs Jira y archivos Markdown, y contempla el modo de arranque de un Proyecto (nuevo, con arquitectura o avanzado), la ejecución de una sola fase bajo demanda, la cuenta de desarrollo dedicada, la aprobación humana opcional antes de fusionar y una cuenta de prueba por rol para ejecutar los casos de prueba. Genera código por paquete de trabajo, abre y revisa Pull Requests, corrige a partir de las observaciones, ejecuta pruebas de humo con Playwright y despliega en Google Cloud. La documentación de cada HU se guarda en un repositorio de control por Proyecto, y una plataforma web muestra el avance, los procesos en ejecución y su historial.

Quedan fuera de alcance la sustitución completa de la revisión humana, la optimización para un lenguaje o *framework* particular, los tipos de proyecto distintos de web (el campo es extensible pero no se implementó ni se validó), las fuentes de HUs distintas de las anteriores y la administración del ambiente de desarrollo sobre el que corren las pruebas de humo, que se supone ya existente. El mecanismo de indexación multi-repositorio se documenta como diseño y no se despliega.

Las limitaciones son las siguientes.

La primera es el proveedor de código. Los Pull Requests, la lectura del estado de la integración continua, la fusión y el despliegue automático están implementados sobre GitHub; con otra plataforma, como GitLab, hace falta un adaptador que hoy no existe. La segunda es la fuente de HUs: GitHub como fuente está diseñada pero no implementada. La tercera se refiere a la validación, que se hace sobre proyectos propios y de prueba, lo que restringe la validez externa de los resultados. La cuarta es la dependencia de servicios externos: los modelos de IA cambian o se retiran, y las corridas dependen de la disponibilidad de GitHub, de Google Cloud y de las cuentas de acceso.

Otras limitaciones son de operación. La plataforma se ejecuta en una sola máquina y con un usuario administrador; el ambiente desplegado para las pruebas usa una base de datos con dirección pública y permisos amplios en la cuenta de despliegue, adecuados para pruebas y no para producción. La protección de la rama principal en GitHub depende de un plan que el piloto no tuvo, por lo que solo Loom impide fusionar con la integración continua en rojo. Por último, la habilidad de diagnóstico de avance existente está implementada, pero no se ejercitó en el piloto, y el ciclo de corrección de fallos no se ejercitó con fallos reales de la aplicación.

@@ tesis_1_6
Las hipótesis se formulan sobre las preguntas de investigación y están sujetas a validación con el director de la tesis.

H1. Un flujo que alimenta al LLM con la HU, los casos de prueba derivados de sus criterios y la arquitectura aprobada produce paquetes de código cuya revisión automática detecta observaciones relevantes, y no ruido, en una proporción mayor que una revisión que solo recibe el *diff*.

H2. El sistema es generalizable: con la misma configuración base completa el ciclo en proyectos de dominios distintos, con cambios de configuración y no de *skills*.

H3. El proveedor de IA (Claude o Gemini) afecta la calidad y el costo del resultado, y la arquitectura del sistema permite intercambiarlo sin modificar las *skills*.

@@ tesis_1_7
La tabla 1.1 resume las variables. La independiente principal es el contexto entregado al modelo; las dependientes miden la calidad del resultado y su costo.

TABLA: Variables del estudio
| Variable | Tipo | Definición | Instrumento |
| Contexto entregado al LLM | Independiente | Solo el *diff* o HU, casos de prueba y arquitectura aprobada | Configuración de la revisión |
| Proveedor de IA | Independiente | Claude o Gemini | Configuración del Proyecto |
| Proyecto | Independiente | Dominio y pila tecnológica de la aplicación | Fichas de proyecto |
| Cobertura de criterios | Dependiente | Proporción de criterios de aceptación con al menos un caso de prueba | Campo de trazabilidad de cada caso |
| Relevancia de las observaciones | Dependiente | Proporción de observaciones relevantes y correctas frente a ruido o falsas | Rúbrica con evaluación ciega |
| Rondas de revisión | Dependiente | Rondas hasta la aprobación de un paquete | Registro de rondas |
| Tiempo, tokens y costo | Dependiente | Duración, tokens de entrada y salida y costo estimado por HU | Colección de métricas |
| Reintentos por salida mal formada | Dependiente | Truncamientos y respuestas no estructuradas por proveedor | Colección de métricas |
| Defectos al ejecutar | Dependiente | Defectos que superan la revisión y compilación y aparecen al ejecutar | Registro de hallazgos |
