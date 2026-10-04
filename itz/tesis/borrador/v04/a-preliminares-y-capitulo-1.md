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

@@ tesis_resumen
Esta tesis presenta Loom, un sistema de habilidades de inteligencia artificial que orquesta el ciclo de desarrollo de una funcionalidad a partir de una historia de usuario. El sistema lee la historia desde el backlog, la especifica con sus criterios de aceptación, genera casos de prueba, diseña la arquitectura, divide el trabajo en paquetes, genera el código de cada paquete con su Pull Request, lo revisa, lo corrige, lo despliega en la nube y valida la aplicación desplegada con pruebas ejecutadas en un navegador. La idea que lo organiza es entregar a cada etapa, como contexto explícito, la historia de usuario, sus casos de prueba y la arquitectura aprobada, y comprobar cada resultado con mecanismos que no dependen del modelo de lenguaje: compilación, pruebas unitarias, integración continua y ejecución contra un ambiente real. Una persona conserva las decisiones de criterio, como aprobar la arquitectura y confirmar los supuestos de una historia.

El trabajo sigue un enfoque de ciencia del diseño. El sistema se construyó como una plataforma web y sus decisiones se documentaron en más de noventa registros de decisión de arquitectura. Se validó con dos corridas piloto completas sobre proyectos de dominios y tecnologías distintos, un sistema de inventarios y la agenda de un taller mecánico, con tres historias de usuario cada uno. Para medir el efecto del contexto sobre la revisión de código se hizo un experimento de control: los 29 Pull Requests de las dos corridas se revisaron de nuevo con el mismo modelo, una vez con el contexto completo y otra solo con el cambio de código, y un segundo modelo calificó a ciegas las 177 observaciones resultantes.

Las dos corridas completaron el ciclo de punta a punta: 12 y 17 paquetes de código fusionados, la aplicación desplegada y 145 casos de prueba ejecutados, de los cuales 104 se aprobaron, 11 fallaron y 30 quedaron bloqueados por datos o condiciones que el ambiente no ofrecía. Todos los criterios de aceptación quedaron cubiertos por al menos un caso de prueba, aunque siete de cada diez criterios los infirió el propio sistema. El segundo proyecto obligó a corregir supuestos de la plataforma que solo valían para el primero. En el experimento de control, el contexto no aumentó la proporción de observaciones relevantes (33 % frente a 30 %, sin diferencia significativa), y en las dos condiciones cerca de dos de cada tres observaciones fueron ruido o incorrectas. El contexto sí cambió el tipo de hallazgo: solo con él la revisión señaló incumplimientos de criterios de aceptación, y las dos revisiones encontraron, en su mayoría, problemas distintos.

Se concluye que el flujo es viable de punta a punta y que las comprobaciones por ejecución son indispensables: defectos que la revisión automática y la compilación no señalaron aparecieron en la integración continua y en las pruebas sobre la aplicación desplegada. La hipótesis de que el contexto mejora la relevancia de la revisión no recibió apoyo, con la reserva de que la calificación fue automática y falta la de una persona. La comparación entre proveedores de inteligencia artificial no se ejecutó y queda como trabajo futuro, junto con la validación en proyectos con código previo.

Palabras clave: ingeniería de software asistida por inteligencia artificial, modelos de lenguaje de gran tamaño, historias de usuario, revisión de código, generación de casos de prueba, integración y despliegue continuos.

@@ tesis_abstract
This thesis presents Loom, a system of artificial intelligence skills that orchestrates the development cycle of a feature starting from a user story. The system reads the story from the backlog, specifies it with its acceptance criteria, generates test cases, designs the architecture, splits the work into packages, generates the code of each package with its pull request, reviews it, fixes it, deploys it to the cloud, and validates the deployed application with tests run in a browser. Its organizing idea is to give each stage, as explicit context, the user story, its test cases and the approved architecture, and to check every result with mechanisms that do not depend on the language model: compilation, unit tests, continuous integration and execution against a real environment. A person keeps the judgment calls, such as approving the architecture and confirming the assumptions of a story.

The work follows a design science approach. The system was built as a web platform and its decisions were documented in more than ninety architecture decision records. It was validated with two complete pilot runs on projects from different domains and technology stacks, an inventory system and a car repair shop scheduler, with three user stories each. To measure the effect of context on code review, a control experiment was carried out: the 29 pull requests of both runs were reviewed again with the same model, once with the full context and once with only the code change, and a second model blindly graded the 177 resulting review comments.

Both runs completed the cycle end to end: 12 and 17 code packages merged, the application deployed, and 145 test cases executed, of which 104 passed, 11 failed and 30 were blocked by data or conditions the environment did not provide. Every acceptance criterion was covered by at least one test case, although seven out of ten criteria were inferred by the system itself. The second project forced corrections to platform assumptions that only held for the first one. In the control experiment, context did not increase the proportion of relevant review comments (33% versus 30%, with no significant difference), and in both conditions about two out of three comments were noise or incorrect. Context did change the kind of finding: only with it did the review point out unmet acceptance criteria, and the two reviews mostly found different problems.

The workflow is viable end to end, and checks by execution are indispensable: defects that the automatic review and the compilation did not flag appeared in continuous integration and in the tests on the deployed application. The data did not support the hypothesis that context improves the relevance of the review, with the caveat that the grading was automatic and a human grading is still missing. Comparing artificial intelligence providers was not carried out and remains as future work, together with validation on projects with existing code.

Keywords: AI-assisted software engineering, large language models, user stories, code review, test case generation, continuous integration and deployment.

@@ tesis_introduccion
El desarrollo de software con asistentes basados en modelos de lenguaje de gran tamaño (*large language models*, LLM) ya forma parte del trabajo cotidiano de muchos equipos. Un modelo escribe una función, propone pruebas o comenta un cambio ajeno, y una revisión sistemática reciente reunió cerca de cuatrocientos trabajos sobre esas aplicaciones [N:hou-slr]. Cada herramienta, sin embargo, atiende una etapa aislada del ciclo y deja a las personas la tarea de unirlas.

Esas herramientas, además, dan por hecho un proyecto nuevo y revisan el código que se les entrega sin conocer la intención de negocio que lo originó. La revisión de un cambio recibe el *diff*, pero no la historia de usuario (HU) que lo justifica, ni sus criterios de aceptación, ni la arquitectura acordada. En la revisión humana, la comprensión del código y del cambio es el aspecto central, y las herramientas actuales cubren mal esa necesidad [N:bacchelli-bird]. El ciclo tampoco se cierra con una validación funcional contra un ambiente real.

Este trabajo se ubica en la ingeniería de software asistida por inteligencia artificial, dentro de las ciencias de la computación. Propone y construye Loom, un sistema de *skills* de inteligencia artificial que, a partir de una HU, orquesta el ciclo de desarrollo de una funcionalidad. Recorre la generación de casos de prueba, el diagnóstico de lo que ya existe, el diseño de la arquitectura, la descomposición en paquetes de trabajo, la generación de código con su Pull Request, la revisión y corrección de ese código, la validación con pruebas de humo y el despliegue. La idea central es dar al modelo, como contexto explícito, la HU, los casos de prueba derivados de sus criterios y la arquitectura aprobada, y exigir evidencia verificable en cada paso. Una persona conserva los puntos de decisión: aprueba la arquitectura, confirma los supuestos de una HU y puede intervenir en cualquier fase.

Loom se implementa como una plataforma web con un servidor en Python, una base de datos documental y una interfaz en Angular. Trabaja con dos proveedores de IA (Claude y Gemini) sin cambiar las *skills*, y con fuentes de historias de usuario intercambiables (Jira y archivos Markdown). La validación se hizo con dos corridas piloto completas sobre proyectos de dominios y pilas distintos, y con un experimento de control sobre la revisión de código. El flujo completó el ciclo en los dos proyectos, de la historia de usuario a la aplicación desplegada y probada, y los casos de prueba cubrieron todos los criterios de aceptación. El experimento no confirmó la idea central en su forma más fuerte: con la evaluación automática disponible, el contexto no aumentó la proporción de observaciones relevantes de la revisión, aunque sí cambió qué problemas encuentra. La comparación entre proveedores de IA, prevista en el diseño, no llegó a ejecutarse.

El documento se organiza en seis capítulos. El primero delimita el problema y formula las preguntas de investigación, los objetivos, los alcances y las limitaciones, las hipótesis y las variables; el segundo reúne los fundamentos teóricos: modelos de lenguaje y agentes con herramientas, desarrollo dirigido por especificaciones, pruebas, revisión de código y entrega continua. Los trabajos relacionados y su comparación con Loom ocupan el capítulo 3, y la metodología, tanto el diseño de la investigación como el sistema construido, el capítulo 4. El capítulo 5 presenta las pruebas y sus resultados, y el 6 cierra con las conclusiones, las recomendaciones y el trabajo futuro.

@@ tesis_1_1
Las herramientas de asistencia por IA para el desarrollo de software cubren, en su mayoría, un tramo estrecho del ciclo. Unas generan código a partir de una instrucción, otras sugieren pruebas y otras comentan un cambio ya escrito [N:hou-slr]. Quien desarrolla una funcionalidad completa debe encadenar esas piezas a mano: pasar la intención de negocio de un asistente al siguiente, comprobar que las pruebas correspondan a los criterios acordados y verificar que lo generado funcione en un ambiente real.

Ese encadenamiento manual deja tres carencias. La primera es la falta de continuidad entre etapas: nada garantiza que los casos de prueba, el diseño, el código y la revisión partan de la misma historia de usuario y de sus criterios de aceptación. La segunda es el supuesto de un proyecto nuevo. En la práctica, la mayoría del trabajo ocurre sobre aplicaciones con código, convenciones y arquitectura existentes, y una herramienta que ignora ese avance previo reescribe o contradice lo que ya hay. Los bancos de tareas construidos con repositorios reales lo muestran: resolver un *issue* obliga a editar varios archivos de un código existente, y los primeros modelos evaluados resolvieron una fracción mínima de las tareas [N:swe-bench]. La tercera es la revisión sin contexto: el modelo que revisa ve el *diff*, pero no sabe qué problema de negocio resuelve ni qué arquitectura se aprobó, por lo que no puede comprobar si el cambio cumple lo pedido.

A esto se suma un problema de verificación. Un modelo de lenguaje produce código plausible sin garantía de que compile, pase sus pruebas o arranque en un ambiente real. Al endurecer las pruebas con que se evalúa, la tasa de aciertos de los modelos evaluados se reduce hasta en 28.9 % [N:evalplus]. Una revisión, humana o automática, que solo lee el código no sustituye esa comprobación. El flujo completo necesita compuertas de ejecución y una validación funcional que cierre el ciclo.

La figura 1.1 resume esa situación: la persona lleva la intención de negocio de una herramienta a la siguiente, y cada carencia aparece en un punto distinto del encadenamiento.

FIGURA: diagramas/05-problema-encadenamiento-manual.png | Encadenamiento manual de herramientas de IA aisladas y sus carencias

La pregunta que guía este trabajo es la siguiente: ¿cómo orquestar con IA el ciclo de desarrollo de una funcionalidad a partir de una historia de usuario, entregando como contexto la intención de negocio, de modo que el resultado sea verificable, revisable y generalizable a distintos proyectos y proveedores de IA?

La figura 1.2 muestra, frente a la anterior, el flujo que propone este trabajo. Todas las etapas parten de la misma HU; el código, la revisión y las pruebas de humo reciben su especificación, sus casos de prueba y la arquitectura aprobada; el código pasa por compuertas de ejecución antes de revisarse y solo se fusiona con la integración continua en verde; y las pruebas de humo contra el ambiente desplegado cierran el ciclo. El capítulo 4 describe cada etapa.

FIGURA: diagramas/06-propuesta-flujo-con-contexto.png | Flujo propuesto: contexto común, compuertas de ejecución y validación funcional

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
Loom se dirige a equipos pequeños, y a personas que desarrollan solas, que mantienen aplicaciones web con un backlog en una herramienta de seguimiento. En ese contexto, una misma persona puede tener que aclarar requerimientos, escribir pruebas, programar, revisar y desplegar. Entre los desperdicios que un estudio empírico identificó en el desarrollo de software están la espera entre tareas, la pérdida de conocimiento que después hay que recuperar y la comunicación ineficaz [N:sedano-waste], costos que aparecen en cada traspaso entre etapas. Un experimento controlado con una tarea acotada reportó que quienes usaron un asistente la completaron 55.8 % más rápido que el grupo de control [N:peng-copilot]; el resultado corresponde a una sola tarea y no a un ciclo completo.

La utilidad práctica está en la trazabilidad y en el control. Cada HU deja una cadena de evidencia verificable: la especificación con sus criterios, los casos de prueba y el criterio del que cada uno deriva, los paquetes de trabajo, el Pull Request con sus rondas de revisión y el informe de las pruebas de humo. Esa cadena permite auditar qué decidió el sistema y por qué, y localizar en qué etapa se introdujo un defecto. Las compuertas de ejecución (compilación, pruebas y verificación de la integración continua) impiden que el flujo avance sobre código que no pasa lo que un ejecutor real comprueba.

Dejar el ciclo sin automatizar de punta a punta tiene un costo. Una revisión sin contexto no puede comprobar la adecuación del cambio a lo pedido, y el código que se revisó con detalle puede fallar igualmente al ejecutarse; la revisión trata menos de defectos de lo que suele suponerse y se apoya sobre todo en comprender el cambio [N:bacchelli-bird]. Además, quien adopta un asistente por etapa debe integrar sus salidas sin una fuente común de contexto.

Desde el punto de vista académico, el trabajo aporta un marco reproducible, con su herramienta funcional, que somete a medición una idea concreta: que entregar al modelo la HU, sus casos de prueba y la arquitectura aprobada mejora la relevancia de la revisión frente a un modelo que solo ve el *diff*. También muestra que el proveedor de IA puede intercambiarse sin modificar las *skills*, y deja un registro de los defectos que el código generado presenta al ejecutarse.

@@ tesis_1_5
El sistema abarca las fases de requerimientos, diseño, desarrollo e implementación para aplicaciones de tipo web. Acepta como fuente de HUs Jira y archivos Markdown, y contempla el modo de arranque de un Proyecto (nuevo, con arquitectura o avanzado), la ejecución de una sola fase bajo demanda, la cuenta de desarrollo dedicada, la aprobación humana opcional antes de fusionar y una cuenta de prueba por rol para ejecutar los casos de prueba. Genera código por paquete de trabajo, abre y revisa Pull Requests, corrige a partir de las observaciones, ejecuta pruebas de humo con Playwright y despliega en Google Cloud. La documentación de cada HU se guarda en un repositorio de control por Proyecto, y una plataforma web muestra el avance, los procesos en ejecución y su historial.

Quedan fuera de alcance la sustitución completa de la revisión humana, la optimización para un lenguaje o *framework* particular, los tipos de proyecto distintos de web (el campo es extensible pero no se implementó ni se validó), las fuentes de HUs distintas de las anteriores y la administración del ambiente de desarrollo sobre el que corren las pruebas de humo, que se supone ya existente. El mecanismo de indexación multi-repositorio se documenta como diseño y no se despliega.

La primera limitación es el proveedor de código. Los Pull Requests, la lectura del estado de la integración continua, la fusión y el despliegue automático están implementados sobre GitHub; con otra plataforma, como GitLab, hace falta un adaptador que hoy no existe. La segunda es la fuente de HUs: GitHub como fuente está diseñada pero no implementada. La tercera se refiere a la validación, que se hace sobre dos proyectos propios y de prueba, de dominios distintos (control de inventarios y agenda de un taller mecánico) y con pilas distintas (Java con Spring Boot y Angular; Node con NestJS y React), los dos nuevos y con Jira como fuente; eso restringe la validez externa de los resultados y deja sin probar el modo con avance previo. La cuarta es la dependencia de servicios externos: los modelos de IA cambian o se retiran, y las corridas dependen de la disponibilidad de GitHub, de Google Cloud y de las cuentas de acceso.

La quinta es el alcance de la evaluación. La comparación entre proveedores de IA no se ejecutó, y la relevancia de las observaciones de la revisión la calificó un modelo y no una persona, de modo que el resultado sobre la hipótesis H1 es preliminar.

Otras limitaciones son de operación. La plataforma se ejecuta en una sola máquina y con un usuario administrador; el ambiente desplegado para las pruebas usó una base de datos con dirección pública, sin respaldos automáticos y con permisos amplios en la cuenta de despliegue, adecuados para pruebas y no para producción. La protección de la rama principal en GitHub depende de un plan que el piloto no tuvo, por lo que solo Loom impide fusionar con la integración continua en rojo. Por último, la habilidad de diagnóstico de avance existente está implementada, pero no se ejercitó en el piloto, y el ciclo de corrección de fallos no se ejercitó con fallos reales de la aplicación.

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
