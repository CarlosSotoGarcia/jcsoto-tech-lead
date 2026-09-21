@@ tesis_3_1
[NOTA DE BORRADOR: los trabajos se eligieron por conveniencia y sus descripciones se contrastaron con la página de cada fuente en septiembre de 2026. Falta el protocolo de búsqueda sistemática (bases de datos, cadenas, criterios de inclusión y fecha), que debe documentarse antes de la entrega.]

La revisión se centra en trabajos que automatizan más de una etapa del desarrollo con modelos de lenguaje, y en los que evalúan esa automatización sobre software real. Se descartan los que atienden únicamente la generación de fragmentos de código aislados, que el marco teórico ya cubre.

SWE-bench reúne 2,294 *issues* reales de 12 repositorios de Python y evalúa si un modelo, editando el código, logra resolverlos; en la evaluación original el mejor modelo resolvió 1.96 % de los casos [N:swe-bench]. Aporta un método de evaluación por ejecución sobre software real. No aborda la especificación previa ni la revisión, y la entrada es un *issue* ya redactado.

SWE-agent propone una interfaz agente-computadora diseñada para que un agente basado en un modelo de lenguaje navegue repositorios, edite código y ejecute pruebas; con ella alcanzó 12.5 % de resolución en SWE-bench, por encima de los enfoques no interactivos anteriores [N:swe-agent-aci]. El trabajo se limita a resolver una tarea dada y no cubre pruebas derivadas de criterios de negocio ni el ciclo posterior a la corrección.

AutoCodeRover combina un modelo de lenguaje con búsqueda de código sobre el árbol de sintaxis y localización de fallos basada en espectro para resolver *issues* de forma autónoma; resolvió 19 % de SWE-bench-lite con un costo computacional menor que otros enfoques comparables [N:autocoderover]. Se ubica en la reparación, no en la construcción de una funcionalidad nueva desde su especificación.

MetaGPT codifica procedimientos operativos estándar en secuencias de *prompts* y reparte roles especializados entre agentes en forma de línea de ensamble, de modo que se verifican los resultados intermedios [N:hong-metagpt]. ChatDev hace que agentes con roles colaboren mediante diálogo estructurado en las fases de diseño, codificación y pruebas, y usa una técnica de comunicación para reducir las alucinaciones [N:qian-chatdev]. Son los más cercanos a Loom en la idea de recorrer varias etapas. Ninguno parte de historias de usuario de un backlog real ni trata un proyecto con avance previo.

Los asistentes comerciales integran la generación y la edición de código en el flujo cotidiano. El agente de Copilot en la nube de GitHub recibe una tarea, investiga el repositorio, propone un plan, hace cambios en una rama y puede ejecutar pruebas y analizadores estáticos; la persona revisa los cambios antes de crear el Pull Request [N:github-copilot-agent]. Claude Code es una herramienta de programación con agentes que lee el código base, edita archivos, ejecuta comandos, crea *commits* y Pull Requests, y puede automatizar la revisión de código en integración continua con GitHub Actions o GitLab CI/CD [N:claude-code-docs]. Ambas describen capacidades de una etapa o de un tramo del ciclo; la documentación consultada no describe la derivación de casos de prueba desde criterios de negocio ni la validación funcional en un ambiente desplegado, lo que debe confirmarse al cierre de la revisión.

En la revisión automática, CodeReviewer preentrena un modelo con objetivos específicos de la revisión y lo evalúa al valorar la calidad de un cambio, generar comentarios y sugerir refinamientos [N:li-codereviewer]. La pregunta sobre el efecto del contexto entregado (solo el *diff* frente a la HU, los casos de prueba y la arquitectura) es la que Loom somete a medición.

En el desarrollo dirigido por especificaciones con agentes, GitHub publicó en 2025 un conjunto de herramientas de código abierto que organiza el trabajo en especificar, planear, dividir en tareas e implementar con un agente de código, con supervisión humana en cada etapa [N:delimarsky-sdd]. Comparte con Loom la centralidad de la especificación; no incluye la revisión con contexto, las pruebas de humo ni el despliegue.

@@ tesis_3_2
El análisis compara los trabajos anteriores con Loom según los criterios de la tabla 3.1, fijados antes de llenar la tabla para evitar que se elijan a favor de una herramienta. Las celdas de otros trabajos se completan únicamente con lo que sus fuentes afirman; las que no se han comprobado quedan como «por verificar».

TABLA: Criterios de comparación
| Trabajo | Etapas que cubre | Entrada | Proyecto con avance previo | Revisión con la HU y la arquitectura | Validación funcional en un ambiente | Cierre hasta el despliegue |
| SWE-bench y SWE-agent | Resolución de un *issue* | *Issue* redactado | Por verificar | No | No | No |
| AutoCodeRover | Reparación | *Issue* redactado | Por verificar | No | No | No |
| MetaGPT y ChatDev | Varias, de la idea al código | Descripción del producto | No (proyecto nuevo) | Por verificar | Por verificar | No |
| Copilot, agente en la nube [N:github-copilot-agent] | Investigar, planear, cambiar código, ejecutar pruebas y analizadores | Tarea o *issue* asignado | Por verificar | Por verificar | Por verificar | No (la persona crea el Pull Request) |
| Claude Code [N:claude-code-docs] | Editar, ejecutar comandos, *commits*, Pull Requests, revisión en CI | Instrucción o *issue* | Sí (lee el código base) | Por verificar | Por verificar | Por verificar |
| Loom | Especificación, casos de prueba, diseño, código, revisión, pruebas de humo y despliegue | HU de un backlog (Jira o Markdown) | Sí, mediante el modo de arranque y el diagnóstico | Sí | Sí, con Playwright | Sí, hasta Cloud Run |

Loom se distingue por combinar, en un solo flujo, tres rasgos que los trabajos revisados presentan por separado: parte de una HU real con criterios, revisa con ese contexto y valida el resultado en un ambiente desplegado. Esa afirmación es de diseño; que además produzca mejores resultados es lo que el capítulo 5 debe medir.

@@ tesis_4_1
### 4.1.1 Enfoque de la investigación

El trabajo sigue un enfoque de ciencia del diseño, cuyo propósito es ampliar las capacidades humanas y organizacionales mediante la creación de artefactos novedosos [N:hevner-design-science]: se construye un artefacto, Loom, y se evalúa su utilidad sobre problemas reales de desarrollo. La evaluación combina mediciones cuantitativas (cobertura, rondas, tiempo, tokens, costo) con un análisis cualitativo de los defectos y de las intervenciones humanas que el sistema no evitó. No es un experimento controlado con asignación aleatoria: es un estudio con escenarios comparables, repeticiones y evaluación ciega de las salidas subjetivas.

La investigación avanza en dos etapas. En la primera, el sistema se ejecuta sobre un proyecto experimental para depurarlo: cada error se registra y corrige, y las intervenciones manuales se anotan. En la segunda, con la plataforma congelada en una versión identificada, el ejercicio se repite desde cero y produce los resultados que se reportan. Distinguir ambas etapas evita atribuir al sistema lo que en realidad corrigió una persona durante la depuración.

### 4.1.2 Proyectos, proveedores y escenarios

Se definen dos proyectos y dos proveedores de IA, que dan cuatro escenarios (tabla 4.1). El proyecto P1 es una aplicación web de control de inventarios con su backlog en Jira; el proyecto P2 (IAT) es una segunda aplicación con backlog en Jira, cuyo dominio y pila tecnológica se documentan en su ficha de proyecto. Cada escenario es una corrida completa de las fases de requerimientos, diseño y desarrollo sobre el mismo backlog, y cambia únicamente el proveedor de IA. Se mantienen las mismas HUs, los mismos repositorios de partida, los mismos *prompts* y la misma cuenta de desarrollo.

TABLA: Escenarios de validación
| | Claude | Gemini |
| P1, control de inventarios | E1 | E2 |
| P2, segunda aplicación | E3 | E4 |

### 4.1.3 Reglas de comparación

Para que la comparación sea válida se establecen siete reglas: entradas idénticas (el backlog se congela y su texto se guarda antes de correr), un repositorio destino por escenario, repeticiones para acotar la variabilidad, evaluación ciega de las salidas por personas ajenas a la asignación del proveedor, registro de los fallos además de los éxitos (JSON mal formado, truncamientos, reintentos, terminaciones sin pruebas), uso de la API de cada proveedor en los experimentos, y congelación de la versión de Loom y de los modelos utilizados. La modalidad de Claude por línea de comandos con cuenta personal se emplea solo para desarrollo, porque no entrega tokens, tiempos ni costos comparables.

### 4.1.4 Instrumentos

Los instrumentos son de dos clases. Los automáticos son el registro de métricas por llamada al modelo (proveedor, modelo, tokens de entrada y salida, duración, reintentos, resultado y costo estimado), el registro de rondas de revisión y de corrección de cada Pull Request, el historial de procesos con su hora de inicio y de fin, los informes de las pruebas de humo y el estado de la integración continua. Los manuales son las rúbricas de evaluación humana: suficiencia de los casos de prueba por HU, relevancia de cada observación de la revisión (relevante y correcta, relevante pero mal sustentada, ruido o falsa), calidad de un paquete de código y calidad de la arquitectura y del plan.

### 4.1.5 Validez y confiabilidad

La validez interna se protege con entradas idénticas entre escenarios y con el registro de la versión de Loom y de los modelos. La validez de constructo depende de que las rúbricas midan lo que declaran; por eso se escriben antes de evaluar y se aplican a ciegas. La validez externa está limitada: los proyectos son propios o de prueba, y un tercer proyecto de otro dominio ampliaría lo que puede generalizarse. La confiabilidad se aborda con repeticiones y con el reporte de la varianza, dado el carácter no determinista de los modelos. Un riesgo específico de este diseño es que las intervenciones manuales durante la corrida contaminen la medición de autonomía; se mitiga con un registro de intervenciones y con la repetición desde cero.

### 4.1.6 Datos y ética

El tema se generalizó deliberadamente respecto de cualquier sistema de un empleador, para no requerir autorización de datos de terceros. Los proyectos utilizados son propios o de prueba, los datos de acceso (llaves, contraseñas) no se almacenan en la documentación y las cuentas de prueba tienen credenciales generadas para ese fin.

@@ tesis_4_2
### 4.2.1 Visión general y nomenclatura

Loom es un sistema de *skills* de IA con un orquestador que las despacha y una plataforma web que las ejecuta y muestra su avance. Los documentos de diseño llaman *Telar* al orquestador con sus *skills* y *Loom* a la plataforma; en esta tesis se usa Loom para el conjunto. *Proyecto*, con mayúscula, designa la aplicación objetivo que Loom construye o evalúa, y se distingue de Loom, que es la herramienta.

El flujo recorre cuatro fases. Requerimientos lee las HUs de la fuente configurada y las especifica. Diseño genera los casos de prueba y la arquitectura, y la persona aprueba la arquitectura. Desarrollo descompone las HUs en paquetes de trabajo, genera el código, lo revisa, lo corrige y lo fusiona. Implementación despliega la aplicación en la nube y valida las HUs con pruebas de humo. Cada fase puede ejecutarse por separado, por lo que un Proyecto puede entrar al flujo en el punto que corresponda a su estado.

La figura 4.1 resume el recorrido de una HU por las cuatro fases.

FIGURA: diagramas/02-flujo-por-fases.png | Flujo de una HU por las cuatro fases de Loom

### 4.2.2 Arquitectura de la plataforma

La plataforma se implementó como monorepo con un servidor en Python (con validación de datos mediante Pydantic), MongoDB como base de datos documental y una interfaz web en Angular con la biblioteca PrimeNG [ADR-0031]. Los procesos largos informan su progreso con eventos enviados por el servidor (SSE), que la interfaz muestra en un panel de actividad. El acceso de las personas requiere inicio de sesión. La figura 4.2 muestra los componentes y sus conexiones con los servicios externos.

FIGURA: diagramas/01-arquitectura-de-la-plataforma.png | Arquitectura de la plataforma y servicios externos

Tres proveedores de IA quedan disponibles por Proyecto: la API de Claude, la API de Gemini y el CLI de Claude Code con cuenta personal, este último solo para desarrollo. Las *skills* no dependen del proveedor; una capa común resuelve la llamada, valida la salida contra un esquema y reintenta ante respuestas truncadas o mal formadas.

Loom trabaja con tres tipos de almacenamiento. En MongoDB guarda el estado operativo (Proyectos, HUs, paquetes, revisiones, métricas y procesos). En un repositorio de control por Proyecto guarda, como Markdown versionado con git, la documentación de cada HU. Sobre los repositorios de la aplicación opera con una cuenta de desarrollo dedicada, de modo que todo cambio generado queda identificado como del sistema.

### 4.2.3 Modelo de datos y artefactos por HU

La unidad central es el Proyecto, que reúne la fuente de HUs, los repositorios, el ambiente de desarrollo, el modo de arranque, el proveedor de IA, las cuentas de prueba por rol y la configuración de despliegue. Cada HU produce artefactos en su carpeta del repositorio de control: la especificación con sus criterios explícitos e inferidos y sus supuestos, los casos de prueba con el criterio del que derivan, el plan, las tareas, un archivo por paquete de trabajo y la evidencia de las pruebas de humo. Cada versión de la especificación y de los casos de prueba se guarda y se compara con la anterior.

Un elemento del backlog se clasifica como HU, con criterios de aceptación y pipeline completo, o como Actividad, sin criterios, con un pipeline reducido. Los paquetes de trabajo son las unidades de código: cada uno pertenece a un solo repositorio, declara sus entregables, los casos de prueba que cubre y sus dependencias, y produce una rama y un Pull Request propios.

### 4.2.4 Las *skills* del pipeline

La tabla 4.2 resume las *skills*. Las que analizan devuelven salida estructurada; las que escriben código operan como agentes sobre una copia de trabajo del repositorio.

TABLA: *Skills* de Loom
| N.º | *Skill* | Entrada | Salida |
| 1 | Descubrimiento y especificación | Fuente de HUs (Jira o Markdown) | Especificación de la HU y su clasificación |
| 2 | Generación de casos de prueba | Especificación | Casos de prueba con criterio de origen |
| 3 | Diagnóstico de avance existente | Casos de prueba y ambiente desplegado | Casos cubiertos y pendientes |
| 4 | Diseño de arquitectura | Casos pendientes y código existente | Plan de arquitectura a aprobar |
| 5 | Descomposición en paquetes | Plan aprobado | Tareas y un archivo por paquete |
| 6 | Generación de código | Paquete, especificación, arquitectura y árbol del repositorio | Rama y Pull Request |
| 7 | Revisión de código | Pull Request, especificación, casos y arquitectura | Observaciones con severidad y fuente |
| 8 | Pruebas de humo | Casos de prueba y ambiente | Informe con evidencia por caso |
| 9 | Generación de correcciones | Casos fallidos de una corrida | Paquetes de corrección |
| 10 | Generación de release | Configuración de despliegue | Script de despliegue y su disparador |

### 4.2.5 Generación de código y compuertas de ejecución

La generación de código sigue TDD: el agente escribe pruebas y código de cada paquete, y el sistema rechaza el resultado si no incluye pruebas o si faltan los archivos obligatorios de un servicio (por ejemplo, un README o un archivo de composición de contenedores). Antes de subir el código, una compuerta lo ejecuta dentro de un contenedor de Docker aislado de la rama de trabajo: instala dependencias, compila, corre el análisis estático (*lint*) y las pruebas unitarias del proyecto, con los mismos comandos que definen sus *scripts* y su integración continua. Las pruebas que requieren Docker desde dentro del contenedor, como las que usan Testcontainers, quedan excluidas y las cubre la integración continua. Si la compuerta falla, el error vuelve al agente hasta dos veces; si no se corrige, el Pull Request se abre con la advertencia y la revisión lo marca con una observación bloqueante.

La compuerta responde a un hallazgo de las primeras corridas: el agente no ejecuta nada por sí solo, y la revisión de código lee el *diff* sin compilarlo. Sin la compuerta, un error de compilación o de estilo solo aparecía al esperar la integración continua de GitHub.

### 4.2.6 Revisión, corrección y fusión

La revisión recibe el Pull Request y el contexto completo (especificación, casos de prueba, arquitectura aprobada y el resumen de la implementación). Cada observación lleva una fuente (criterio de aceptación, arquitectura, buenas prácticas, pruebas o seguridad), una severidad (bloqueante, mayor o menor) y, cuando aplica, archivo y línea, y se publica como comentario en el Pull Request. La figura 4.3 resume el ciclo completo de un paquete, desde la generación hasta la fusión.

FIGURA: diagramas/03-ciclo-de-un-paquete.png | Ciclo de un paquete de trabajo: generación, compuertas, revisión, corrección y fusión

Si una HU tiene supuestos sin confirmar, el sistema agrega una observación bloqueante hasta que una persona registre su decisión.

La corrección aplica las observaciones sobre la misma rama, responde cada comentario y marca las conversaciones resueltas. Cada ronda de revisión y de corrección se guarda con su resultado, y las observaciones pueden valorarse por una persona (relevante, mal sustentada, ruido, falsa) o pasar por una segunda opinión de otro proveedor de IA, para disponer de evidencia de su relevancia.

La fusión de un Pull Request exige que los *checks* de la integración continua estén en verde. Loom consulta el estado de esos *checks* en GitHub. Si alguno falla durante el avance de una HU, lee el registro del *job* fallido, extrae las líneas que preceden a la marca de error y lo devuelve al agente como una observación bloqueante, con hasta dos correcciones por paquete. Si sigue en rojo, el avance se detiene y el Pull Request queda abierto.

### 4.2.7 Avance de una HU de punta a punta

La acción «avanzar con una HU» encadena el ciclo para todos los paquetes de una HU en el orden de sus dependencias. Por cada paquete genera el código, lo revisa, aplica hasta un número de rondas de corrección elegido por la persona (de cero a tres), espera la integración continua y fusiona. Se detiene ante una observación bloqueante que no se pudo resolver y deja el Pull Request abierto para que la persona lo decida. Al fusionarse el último paquete, la HU queda completa y se lanza el despliegue.

### 4.2.8 Despliegue

Un generador determinista produce, a partir de la configuración del Proyecto, un *script* de despliegue (`release.py`) y su disparador, sin credenciales. El *script* es idempotente: habilita las APIs necesarias de Google Cloud, crea la instancia de base de datos PostgreSQL y su usuario cuando la aplicación lo requiere, guarda las contraseñas y los secretos aleatorios en el gestor de secretos, crea una cuenta de servicio de ejecución con acceso solo a esos secretos, construye las imágenes con el servicio de construcción de la nube y despliega el backend y el frontend en Cloud Run. Las direcciones de los servicios se calculan antes de desplegar, de modo que la configuración de origen cruzado (CORS) del backend se establece en una sola pasada.

El despliegue automático usa GitHub Actions con federación de identidad: el propio *script* crea el pool y el proveedor de identidad, que solo aceptan a ese repositorio, la cuenta de servicio desplegadora y las variables del repositorio que el flujo de trabajo necesita. El flujo de trabajo se dispara por solicitud y Loom lo lanza cuando una HU queda completa, en lugar de reaccionar a cada cambio de la rama principal, para que una HU a medias no llegue al ambiente. Los Pull Requests que publican estos archivos de despliegue se fusionan desde Loom, con la misma regla de integración continua en verde.

### 4.2.9 Validación funcional

Las pruebas de humo recorren todos los casos de prueba de una HU cuando toda su ronda de paquetes está fusionada. Un modelo lee el código de la aplicación y los casos y escribe un guion de Playwright con las acciones y las verificaciones de cada caso; el guion se ejecuta contra el ambiente desplegado con la cuenta de prueba del rol que el caso requiere. Cuando un caso falla, un agente de navegador lo reproduce para distinguir un guion mal escrito de un fallo real de la aplicación. El resultado de cada caso es aprobado, fallido o bloqueado, y el informe con capturas queda como evidencia. Los casos fallidos pueden convertirse en paquetes de corrección que reingresan al ciclo de código y revisión. La figura 4.4 muestra la secuencia del despliegue y de la validación.

FIGURA: diagramas/04-liberacion-y-validacion.png | Secuencia de liberación en la nube y validación funcional

### 4.2.10 Cambios en los requisitos

Cuando la especificación o los casos de prueba de una HU cambian después de haberse usado, Loom guarda una versión nueva sin borrar las anteriores, marca como desactualizado lo que dependía de ellas (casos, arquitectura, código, guion de pruebas) y, para las HUs cuyo código ya existe, genera paquetes de cambio que llevan el código a los casos nuevos.

### 4.2.11 Control de la ejecución

Cada proceso que Loom ejecuta queda registrado con su tipo, las HUs sobre las que trabaja, su estado y su registro de eventos, y se guarda en una colección de la base de datos para conservar el historial con la hora de inicio y de fin. Varios procesos pueden correr a la vez si trabajan sobre HUs distintas. Sobre la misma HU, o sobre todo el Proyecto, el segundo se rechaza. El despliegue es exclusivo: espera en cola a que terminen los demás y, mientras corre, los demás esperan. Un proceso puede cancelarse; la cancelación detiene su trabajo y los procesos externos que lanzó (el agente, el contenedor de compilación, la suite de pruebas), y conserva lo ya hecho. Cerrar o recargar la pantalla que lo lanzó no lo detiene.

### 4.2.12 Puntos de decisión humana

El sistema deja a las personas los puntos donde se requiere criterio: aprobar la arquitectura, confirmar los supuestos de una HU con una decisión que el agente recibe como requisito, valorar la relevancia de las observaciones, decidir si se fusiona un Pull Request con observaciones abiertas, y cancelar o relanzar procesos. Una aprobación manual adicional antes de fusionar es configurable por Proyecto.

### 4.2.13 Medición

Cada llamada a un modelo escribe un registro con el proveedor, el modelo, los tokens de entrada y salida, la duración, los reintentos, el resultado y el costo estimado según una tabla de precios configurable. Los rechazos de las compuertas y los eventos de cada proceso se registran también. Esos datos alimentan la tarjeta de uso de IA de la plataforma y una exportación a CSV, que son la fuente de las tablas de tiempo, tokens y costo del capítulo 5.

@@ tesis_6_3
El trabajo deja abiertas líneas que se derivan de sus propias decisiones y de lo que no alcanzó a ejercitarse.

La primera es la generalización a otros proveedores de código. La revisión, la fusión, la lectura de la integración continua y el despliegue automático están implementados sobre GitHub. Un adaptador para GitLab y una separación explícita entre el proveedor de código y la estrategia de despliegue permitirían usar Loom en otros entornos, incluida la conexión de un servicio de construcción por *tokens*, que sí puede automatizarse.

La segunda es una compuerta de arranque. La compilación, el análisis estático y las pruebas unitarias antes de subir el código no detectan los defectos que solo aparecen al ejecutar la aplicación con una base de datos real (migraciones, configuración, arranque). Levantar la imagen de producción junto a una base desechable y comprobar su estado de salud antes del despliegue, y ejecutar en ese entorno las pruebas de integración con contenedores, cerrarían esa brecha.

La tercera es el diagnóstico de avance existente sobre proyectos con código previo y la ejecución del ciclo de corrección con fallos reales de la aplicación, que están implementados pero no se ejercitaron. También queda pendiente la conexión de las incidencias con la herramienta de seguimiento (crear en Jira la incidencia de cada fallo) y la creación de subtareas en la fuente de HUs.

La cuarta es operativa: persistir y reanudar los procesos interrumpidos, en lugar de solo marcarlos, y ligar cada proceso del historial con sus métricas de costo. La quinta es la infraestructura como código: Terraform daría estado declarativo y vista previa de los cambios de despliegue, a cambio de una dependencia adicional, y se justifica cuando el sistema atienda varios ambientes.

Por último, la validez externa mejoraría con un proyecto de otro dominio y con evaluadores independientes, y la protección de la rama principal en la propia plataforma de código, que exige un plan de pago, evitaría que un cambio se fusione con la integración continua en rojo por una vía distinta de Loom.
