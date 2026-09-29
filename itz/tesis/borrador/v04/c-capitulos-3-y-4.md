@@ tesis_3_1
Este apartado revisa los trabajos que automatizan con modelos de lenguaje una o varias etapas del desarrollo que Loom también cubre: resolver tareas sobre repositorios reales, coordinar varias etapas con agentes, revisar código y generar pruebas. Los trabajos que solo generan fragmentos de código aislados se tratan en el marco teórico (apartado 2.3).

### 3.1.1 Protocolo de búsqueda

La revisión es dirigida y no sistemática. Se hizo en dos momentos, en septiembre de 2026: una primera selección de trabajos conocidos del área (SWE-bench y los agentes evaluados con él, MetaGPT, ChatDev y la documentación de los asistentes comerciales), y una búsqueda el 28 de septiembre con un motor de búsqueda web general, sobre arXiv y las bibliotecas digitales de ACM e IEEE, con tres cadenas: «large language model automated code review industrial study», «LLaMA-Reviewer automating code review» y «large language models generate test cases from user stories acceptance criteria». A partir de los trabajos encontrados se siguieron las referencias hacia atrás y hacia adelante cuando apuntaban a otro trabajo del mismo tema.

Un trabajo se incluyó si cumplía cuatro condiciones: usa un modelo de lenguaje; automatiza al menos una de las etapas mencionadas; reporta una evaluación empírica sobre software real o sobre un *benchmark* reconocido (o, en el caso de las herramientas comerciales, tiene documentación oficial que describe sus capacidades); y es de 2020 o posterior. Se excluyeron los trabajos de autocompletado de código, los que no reportan evaluación y las versiones repetidas de un mismo trabajo. Cada descripción de esta sección se contrastó con el resumen o la página de la fuente. Los preprints se señalan como tales en la lista de referencias.

El protocolo tiene límites que conviene declarar. No se consultaron bases como Scopus o Web of Science, no se registró el número de resultados revisados en cada búsqueda y la selección favorece trabajos en inglés publicados en arXiv. Por eso esta revisión no permite afirmar que no exista un trabajo equivalente a Loom; permite ubicar a Loom frente a los trabajos más citados y más recientes de cada línea.

### 3.1.2 Resolución de tareas en repositorios reales

SWE-bench reúne 2,294 *issues* reales de 12 repositorios de Python y evalúa si un modelo, editando el código, logra resolverlos; en la evaluación original, el mejor modelo resolvió 1.96 % de los casos [N:swe-bench]. Su aporte es metodológico: evalúa por ejecución, con las pruebas que el propio proyecto escribió para el cambio. No aborda la especificación previa ni la revisión, y la entrada es un *issue* ya redactado.

Los agentes que atacan este problema difieren en cuánta autonomía le dan al modelo. SWE-agent propone una interfaz agente-computadora con la que el agente navega el repositorio, edita código y ejecuta pruebas; con ella alcanzó 12.5 % de resolución en SWE-bench, por encima de los enfoques no interactivos anteriores [N:swe-agent-aci]. AutoCodeRover combina el modelo con búsqueda de código sobre el árbol de sintaxis y con localización de fallos basada en espectro, y resolvió 19 % de SWE-bench-lite con un costo menor que otros enfoques comparables [N:autocoderover]. OpenHands es una plataforma abierta para construir agentes que escriben código, usan la terminal y navegan la web en un entorno aislado, y se evaluó en 15 tareas de ingeniería de software y de navegación [N:openhands].

Agentless tomó el camino contrario. Sin agente, con un proceso fijo de tres fases (localizar el problema, reparar y validar el parche), resolvió 32 % de SWE-bench Lite con un costo de 0.70 dólares por tarea, más que los agentes de código abierto con los que se comparó [N:agentless]. El resultado pesa en el diseño de Loom, que también prefiere un flujo fijo con etapas y compuertas definidas por el sistema a un agente único que decide su propio camino. En todos estos trabajos la tarea termina cuando pasan las pruebas del *issue*: no se revisa el cambio contra una especificación de negocio ni se valida la aplicación desplegada.

### 3.1.3 Sistemas de varios agentes y asistentes comerciales

MetaGPT codifica procedimientos operativos estándar en secuencias de *prompts* y reparte roles especializados entre agentes en forma de línea de ensamble, de modo que los resultados intermedios se verifican [N:hong-metagpt]. ChatDev hace que agentes con roles colaboren mediante diálogo estructurado en las fases de diseño, codificación y pruebas, y usa una técnica de comunicación para reducir las alucinaciones [N:qian-chatdev]. Son los más cercanos a Loom en la idea de recorrer varias etapas. Parten, sin embargo, de la descripción de un producto nuevo; ninguno toma historias de usuario de un backlog real ni trata un proyecto con avance previo.

Los asistentes comerciales integran la generación y la edición de código en el trabajo cotidiano. El agente de Copilot en la nube de GitHub recibe una tarea, investiga el repositorio, propone un plan, hace cambios en una rama y puede ejecutar pruebas y analizadores estáticos; la persona revisa los cambios antes de crear el Pull Request [N:github-copilot-agent]. Claude Code es una herramienta de programación con agentes que lee el código base, edita archivos, ejecuta comandos, crea *commits* y Pull Requests, y puede automatizar la revisión de código en integración continua [N:claude-code-docs]. Loom usa este último como uno de sus proveedores (apartado 4.2.2). La documentación consultada de ambos describe un tramo del ciclo; no describe la derivación de casos de prueba desde criterios de negocio ni la validación funcional en un ambiente desplegado.

En el desarrollo dirigido por especificaciones con agentes, GitHub publicó en 2025 un conjunto de herramientas de código abierto que organiza el trabajo en especificar, planear, dividir en tareas e implementar, con supervisión humana en cada etapa [N:delimarsky-sdd]. Comparte con Loom la especificación como fuente de verdad; no incluye la revisión con contexto, las pruebas de humo ni el despliegue.

### 3.1.4 Revisión de código automatizada

Los primeros trabajos entrenaron modelos específicos para la revisión. CodeReviewer se preentrenó con cambios y comentarios reales para estimar la calidad de un cambio, generar comentarios y refinar el código [N:li-codereviewer]. LLaMA-Reviewer ajustó un modelo de lenguaje general a las mismas tareas con técnicas de ajuste eficiente, entrenando menos del 1 % de sus parámetros [N:llama-reviewer]. Una evaluación manual de 2,291 predicciones de tres técnicas, con cerca de 105 horas de análisis, encontró que ChatGPT, usado sin ajuste, tiene dificultades para comentar el código como lo haría un revisor humano [N:tufano-sota].

Los estudios más recientes miden herramientas desplegadas en empresas. En un estudio industrial, una herramienta de revisión basada en un LLM estuvo disponible para unas 238 personas en diez proyectos; en tres de ellos, de 4,335 Pull Requests, 1,568 pasaron por revisión automática, y 73.8 % de sus comentarios se marcaron como resueltos. Las personas reportaron una mejora menor en la calidad del código, y el tiempo para cerrar un Pull Request subió de 5 horas 52 minutos a 8 horas 20 minutos; entre los problemas mencionaron revisiones erróneas y comentarios irrelevantes [N:cihan-practice]. En Atlassian, RovoDev Code Reviewer se evaluó durante un año: 38.7 % de sus comentarios provocaron cambios de código en los *commits* siguientes, el tiempo de ciclo de los Pull Requests bajó 30.8 % y los comentarios escritos por personas se redujeron 35.6 % [N:rovodev]. En Ericsson, una herramienta ligera combinó el modelo con análisis estático del programa y obtuvo resultados preliminares alentadores con desarrolladores experimentados [N:ericsson-review].

El trabajo más cercano a la hipótesis H1 es SGCR, que ancla la revisión en especificaciones escritas por personas. Tiene dos rutas: una explícita, que verifica de forma determinista reglas derivadas de esas especificaciones, y una implícita, que busca y verifica problemas fuera de ellas. En un entorno industrial, 42 % de sus sugerencias fueron adoptadas por los desarrolladores, frente a 22 % de un LLM de base sin ese anclaje [N:sgcr]. El resultado apunta en la dirección de H1, aunque con otra especificación (reglas de revisión, no historias de usuario) y otra medida (adopción, no relevancia calificada a ciegas). Loom agrega a esa línea dos cosas: el contexto es el de la tarea (la HU, sus casos de prueba y la arquitectura aprobada) y la comparación se hace sobre los mismos Pull Requests, con y sin ese contexto (apartado 4.1.7).

### 3.1.5 Generación de pruebas

Con código como entrada, TestPilot generó pruebas unitarias para 25 paquetes de npm con 1,684 funciones de API y alcanzó una mediana de cobertura de sentencias de 70.2 % y de ramas de 52.8 %, por encima de la herramienta de referencia con la que se comparó [N:testpilot]. En Meta, TestGen-LLM mejora pruebas unitarias existentes y filtra sus propuestas antes de mostrarlas: 75 % de sus casos compilaron, 57 % pasaron de forma confiable y 25 % aumentaron la cobertura; mejoró 11.5 % de las clases a las que se aplicó, y los ingenieros aceptaron 73 % de sus recomendaciones para producción [N:testgen-llm]. Los dos generan pruebas a partir del código, así que verifican lo que el código hace y no lo que la historia de usuario pide.

La línea más cercana a Loom genera pruebas a partir de los requerimientos. Ferreira *et al.* reportan un caso industrial en dos pasos: de las historias de usuario a escenarios de aceptación en Gherkin, y de esos escenarios, junto con el HTML de las páginas, a guiones ejecutables en Cypress. Las personas que probaban consideraron útiles los escenarios 95 % de las veces; de los guiones generados, 92 % se consideraron útiles, 60 % se usaron tal cual y 8 % se descartaron [N:ferreira-acceptance]. Es la misma cadena que siguen las *skills* 2 y 8 de Loom, con otro *framework* de pruebas. Una revisión de 21 estudios primarios sobre generación de casos de prueba desde requerimientos en lenguaje natural concluyó que ningún enfoque satisface a la vez seis dimensiones de calidad (automatización, manejo de la ambigüedad, aplicabilidad al dominio, trazabilidad, evaluación y control de las alucinaciones) [N:folorunsho-survey].

### 3.1.6 Lo que queda abierto

Cada línea automatiza bien un tramo. Los agentes de repositorio resuelven *issues* redactados; los sistemas de varios agentes recorren etapas sobre productos nuevos; los revisores industriales comentan Pull Requests con el contexto del cambio y, en el mejor caso, con reglas escritas; los generadores de pruebas trabajan desde el código o, en un caso industrial, desde historias de usuario. Ningún trabajo revisado encadena la historia de usuario con sus casos de prueba, el código, una revisión que conoce esos casos y la arquitectura, y la validación de la aplicación desplegada. Esa es la brecha de diseño que Loom ocupa. Si cerrar la brecha produce mejores resultados es otra pregunta, y la tesis la acota a una parte medible: el efecto del contexto sobre la revisión (H1).

@@ tesis_3_2
El análisis compara los trabajos anteriores con Loom según los criterios de la tabla 3.1, fijados antes de llenar la tabla para evitar que se elijan a favor de una herramienta. Las celdas de otros trabajos se completan únicamente con lo que sus fuentes afirman; las que no se han comprobado quedan como «por verificar».

TABLA: Criterios de comparación
| Trabajo | Etapas que cubre | Entrada | Proyecto con avance previo | Revisión con la HU y la arquitectura | Validación funcional en un ambiente | Cierre hasta el despliegue |
| SWE-bench, SWE-agent, AutoCodeRover, Agentless | Resolución o reparación de un *issue* | *Issue* redactado | Sí (repositorios existentes) | No | No | No |
| MetaGPT y ChatDev | Varias, de la idea al código | Descripción del producto | No (producto nuevo) | No descrito en la fuente | No descrito en la fuente | No |
| Copilot, agente en la nube | Investigar, planear, cambiar código, ejecutar pruebas y analizadores | Tarea o *issue* asignado | Sí (investiga el repositorio) | No descrito en la fuente | No descrito en la fuente | No (la persona crea el Pull Request) |
| Claude Code | Editar, ejecutar comandos, *commits*, Pull Requests, revisión en CI | Instrucción o *issue* | Sí (lee el código base) | No descrito en la fuente | No descrito en la fuente | No descrito en la fuente |
| Revisores industriales (Cihan *et al.*, RovoDev, Ericsson) | Revisión de Pull Requests | Pull Request | Sí | No descrito en la fuente | No | No |
| SGCR | Revisión | Pull Request y especificaciones escritas por personas | Sí | Con reglas derivadas de especificaciones | No | No |
| TestPilot y TestGen-LLM | Pruebas unitarias | Código o pruebas existentes | Sí | No aplica | No | No |
| Ferreira *et al.* | Escenarios y guiones de aceptación | Historias de usuario y HTML de las páginas | Sí (caso industrial) | No aplica | Guiones ejecutables en Cypress | No |
| Loom | Especificación, casos de prueba, diseño, código, revisión, pruebas de humo y despliegue | HU de un backlog (Jira o Markdown) | Previsto, con el diagnóstico de avance (implementado, no ejercitado) | Sí | Sí, con Playwright contra el ambiente desplegado | Sí, hasta Cloud Run |

Loom se distingue por combinar en un solo flujo rasgos que los trabajos revisados presentan por separado: parte de una HU real con criterios, revisa con ese contexto y valida el resultado en un ambiente desplegado. Los rasgos más cercanos están en SGCR, que ancla la revisión en especificaciones, y en el caso industrial de Ferreira *et al.*, que genera pruebas de aceptación desde historias de usuario. La comparación es de diseño y depende de lo que cada fuente describe: una celda «No descrito en la fuente» no afirma que la herramienta carezca de esa capacidad. Que la combinación produzca mejores resultados es lo que el capítulo 5 debe medir.

@@ tesis_4_1
### 4.1.1 Enfoque de la investigación

El trabajo sigue un enfoque de ciencia del diseño, cuyo propósito es ampliar las capacidades humanas y organizacionales mediante la creación de artefactos novedosos [N:hevner-design-science]: se construye un artefacto, Loom, y se evalúa su utilidad sobre problemas reales de desarrollo. La evaluación combina mediciones cuantitativas (cobertura, rondas, tiempo, tokens, costo) con un análisis cualitativo de los defectos y de las intervenciones humanas que el sistema no evitó. No es un experimento controlado con asignación aleatoria: es un estudio con escenarios comparables, repeticiones y evaluación ciega de las salidas subjetivas.

La investigación avanza en dos etapas. En la primera, el sistema se ejecuta sobre un proyecto experimental para depurarlo: cada error se registra y corrige, y las intervenciones manuales se anotan. En la segunda, con la plataforma congelada en una versión identificada, el ejercicio se repite desde cero y produce los resultados que se reportan. Distinguir ambas etapas evita atribuir al sistema lo que en realidad corrigió una persona durante la depuración.

Cada corrida de un Proyecto es, además, un estudio de caso en el sentido de Runeson y Höst: observa el flujo en su contexto real, con un backlog, repositorios y un ambiente en la nube de verdad [N:runeson-host]. Las dos etapas describen el plan. En la práctica, la plataforma no llegó congelada a las corridas del capítulo 5: cada una encontró supuestos que no se sostenían y se corrigieron durante la corrida, y el modelo del CLI no estaba fijado. El apartado 5.1.4 detalla qué implica eso para la comparación entre corridas.

### 4.1.2 Proyectos, proveedores y escenarios

Se definen dos proyectos y dos proveedores de IA, que dan cuatro escenarios (tabla 4.1). El proyecto P1 es una aplicación web de control de inventarios con su backlog en Jira. El proyecto P2 (IAT) es una aplicación web para la agenda y la operación de un taller mecánico (clientes, vehículos, citas, órdenes de servicio y cobro), también con su backlog en Jira: 44 historias organizadas en nueve épicas. Para probar la generalización, a P2 se le configuró una pila distinta de la de P1: Node con NestJS y React, frente a Java con Spring Boot y Angular. Cada escenario es una corrida completa de las fases de requerimientos, diseño y desarrollo sobre el mismo backlog, y cambia únicamente el proveedor de IA. Se mantienen las mismas HUs, los mismos repositorios de partida, los mismos *prompts* y la misma cuenta de desarrollo.

TABLA: Escenarios de validación
| | Claude | Gemini |
| P1, control de inventarios | E1 | E2 |
| P2, agenda de taller mecánico | E3 | E4 |

Antes de la matriz se corrió un piloto completo por proyecto, E1c y E3c, con el CLI de Claude sobre una suscripción en lugar de la API. Sirvieron para que el flujo funcionara de punta a punta en los dos proyectos y para registrar cada error y cada intervención; sus resultados se reportan en el capítulo 5 como pilotos, no como escenarios de la matriz, porque el costo del CLI con suscripción es nocional y porque Loom no fijaba el modelo que el CLI usaba.

### 4.1.3 Unidades de análisis y muestra

La unidad de análisis cambia según la pregunta. Para la especificación y los casos de prueba (PI1) es la HU. Para la generación y la revisión de código (PI2 y H1) es el paquete de trabajo con su Pull Request y, dentro de él, cada observación de la revisión. Para la generalización (PI3 y H2) es la corrida completa de un Proyecto, y para los defectos que solo aparecen al ejecutar (PI5), cada caso de prueba ejecutado contra el ambiente y cada fallo de la integración continua.

La muestra es intencional. De cada backlog se tomaron las tres primeras HUs del sprint en el orden del tablero, que es el orden de la prioridad de negocio; así, las HUs son las que el equipo del Proyecto habría construido primero, y no las que mejor le convienen a Loom. La tabla 4.2 resume lo que produjeron.

TABLA: Tamaño de la muestra por proyecto
| Unidad | P1, inventarios (E1c) | P2, agenda de taller (E3c) |
| HUs procesadas | 3 | 3 |
| Casos de prueba generados | 44 | 101 |
| Paquetes de trabajo y Pull Requests | 12 | 17 |
| Observaciones de la primera revisión en la corrida | 66 | 59 |
| Observaciones del experimento C (con contexto y solo el diff) | 93 (44 y 49) | 84 (41 y 43) |
| Llamadas al modelo en la corrida | 128 | 532 |

Con tres HUs por proyecto, las cifras describen cada corrida y no permiten inferir sobre el conjunto de HUs posibles de un backlog. El experimento C es la excepción parcial: compara dos condiciones sobre los mismos 29 Pull Requests, de modo que cada Pull Request es su propio control y la comparación no depende de que las HUs sean representativas.

### 4.1.4 Reglas de comparación

Para que la comparación sea válida se establecen siete reglas: entradas idénticas (el backlog se congela y su texto se guarda antes de correr), un repositorio destino por escenario, repeticiones para acotar la variabilidad, evaluación ciega de las salidas por personas ajenas a la asignación del proveedor, registro de los fallos además de los éxitos (JSON mal formado, truncamientos, reintentos, terminaciones sin pruebas), uso de la API de cada proveedor en los experimentos, y congelación de la versión de Loom y de los modelos utilizados. La modalidad de Claude por línea de comandos con cuenta personal se emplea solo para desarrollo, porque no entrega tokens, tiempos ni costos comparables.

### 4.1.5 Instrumentos

Los instrumentos son de dos clases. Los automáticos son el registro de métricas por llamada al modelo (proveedor, modelo, tokens de entrada y salida, duración, reintentos, resultado y costo estimado), el registro de rondas de revisión y de corrección de cada Pull Request, el historial de procesos con su hora de inicio y de fin, los informes de las pruebas de humo y el estado de la integración continua. Los manuales son las rúbricas de evaluación humana: suficiencia de los casos de prueba por HU, relevancia de cada observación de la revisión (relevante y correcta, relevante pero mal sustentada, ruido o falsa), calidad de un paquete de código y calidad de la arquitectura y del plan.

### 4.1.6 Relación entre preguntas, hipótesis e instrumentos

La tabla 4.3 une cada pregunta de investigación y cada hipótesis con lo que se mide, el instrumento que lo registra y su estado al cierre de este documento. Sirve para comprobar que ninguna hipótesis se da por respondida con datos que no la miden.

TABLA: Preguntas, hipótesis, mediciones e instrumentos
| Pregunta o hipótesis | Qué se mide | Instrumento y fuente | Estado |
| PI1 | Proporción de criterios de aceptación con al menos un caso de prueba | Referencia al criterio de origen en cada caso; especificación de la HU | Datos disponibles, cálculo pendiente |
| PI2 y H1 | Proporción de observaciones relevantes con contexto y con solo el diff, sobre los mismos Pull Requests | Experimento C (apartado 4.1.7); rúbrica aplicada a ciegas | Ejecutado; calificación pendiente |
| PI3 y H2 | Ciclo completo en dos dominios y dos pilas; cambios que exigió Loom fuera de la configuración | Corridas E1c y E3c; registros de hallazgos; registros de decisión | Evidencia parcial |
| PI4 y H3 | Calidad, tiempo y costo por proveedor en condiciones equivalentes | Escenarios E1 a E4 con API; colección de métricas | No ejecutado |
| PI5 | Defectos que superan la revisión y la compilación y aparecen al ejecutar | Integración continua; pruebas de humo; registros de hallazgos | Evidencia en dos proyectos |

### 4.1.7 Experimento de control de la revisión

La hipótesis H1 compara dos revisiones del mismo cambio, y los pilotos solo produjeron una de ellas. La línea base se obtiene, por eso, de forma retrospectiva: las 29 primeras revisiones de E1c y E3c se repiten sobre los mismos Pull Requests en dos condiciones (ADR-0089). En la condición con contexto, el revisor recibe exactamente lo que recibe la *skill* de revisión: el paquete de trabajo, la arquitectura aprobada del repositorio, la especificación y los casos de prueba de la HU, el título y la descripción del Pull Request, y el *diff*. En la condición de control recibe solo el *diff*. Sus instrucciones conservan las fuentes, las severidades y las reglas de la *skill*, y declaran que no conoce la HU, sus criterios ni la arquitectura.

Tres controles sostienen la comparación. El *diff* es el mismo en las dos condiciones: se reconstruye desde GitHub como el cambio del primer commit del Pull Request, antes de cualquier corrección, y coincide con el que guardó la revisión original. El modelo está fijado (`claude-sonnet-5` por el CLI de Claude Code), con el mismo esquema de salida y el mismo tope de 140,000 caracteres para el *diff*. El contexto, por último, se reconstruye tal como estaba en el momento de la primera revisión, a partir del historial del repositorio de control y no del estado actual de la base de datos. A diferencia de la regla del apartado 4.1.4, el experimento usa el CLI con suscripción y no la API: las dos condiciones corren con el mismo modelo, y el costo, que en esa modalidad es nocional, no forma parte de la hipótesis.

La relevancia no la juzga el sistema. Una persona califica las observaciones de las dos condiciones con la rúbrica del apartado 4.1.5 (relevante y correcta, relevante pero mal sustentada, ruido o falsa). Las ve mezcladas dentro de cada Pull Request, en orden aleatorio, con un identificador anónimo y sin la fuente ni la severidad que les asignó el modelo, porque ambas delatan la condición. La clave que asocia cada identificador con su condición y los datos crudos quedan fuera del repositorio público hasta terminar la calificación; su huella SHA-256 se publica antes, para que después pueda comprobarse que no cambiaron. El análisis reporta la proporción de observaciones relevantes por condición y compara, Pull Request por Pull Request, el número de observaciones relevantes con la prueba de rangos con signo de Wilcoxon [N:wilcoxon] y con la prueba de signos, siguiendo las pautas de Arcuri y Briand para comparar resultados de ejecuciones aleatorias [N:arcuri-briand]. Las observaciones bloqueantes y mayores que resulten válidas se cuentan aparte.

### 4.1.8 Análisis de los datos

Las corridas piloto se analizan de forma descriptiva: conteos, proporciones y totales de tiempo, tokens y costo, por proyecto, por *skill* y por paquete. Con una sola corrida por proyecto no se hacen pruebas de hipótesis sobre ellas, y las diferencias entre E1c y E3c se reportan sin atribuirlas a una causa cuando el modelo o la versión de la plataforma cambiaron entre las dos (apartado 5.1.4).

Para H1, la calificación ciega produce dos medidas por condición. La proporción estricta cuenta solo las observaciones «relevante y correcta»; la amplia suma las «relevante pero mal sustentada». Además, para cada Pull Request se resta el número de observaciones relevantes sin contexto del número con contexto. Esas 29 diferencias pareadas se comparan con la prueba de rangos con signo de Wilcoxon [N:wilcoxon] y con la prueba de signos exacta, y el tamaño del efecto se reporta con la correlación rango-biserial pareada, que va de −1 a 1 [N:kerby-rank-biserial]. Se propone un nivel de significancia de 0.05 con prueba bilateral, a confirmar con el director antes de conocer los resultados. Se reportan aparte las observaciones bloqueantes y mayores que resultaron válidas y cuántas observaciones relevantes de una condición encontró también la otra. El cálculo está en un guion versionado con la evidencia del experimento, de modo que cualquiera puede repetirlo con la hoja calificada.

El análisis cualitativo se apoya en los registros de hallazgos de cada corrida. Cada hallazgo se anota con su hora y se clasifica en cuatro grupos: defectos del código generado, problemas del proceso o supuestos de Loom que no se sostuvieron, errores de la plataforma o del entorno, e intervenciones de la persona, separando las que se hicieron con la interfaz de Loom de las que se hicieron fuera de ella. Cuando un hallazgo llevó a cambiar Loom, el registro lo liga con su registro de decisión. De ahí salen las respuestas a PI5 y la evidencia sobre H2.

### 4.1.9 Validez y confiabilidad

La validez interna se protege con entradas idénticas entre escenarios y con el registro de la versión de Loom y de los modelos. La validez de constructo depende de que las rúbricas midan lo que declaran; por eso se escriben antes de evaluar y se aplican a ciegas. La validez externa está limitada: los proyectos son propios o de prueba, y un tercer proyecto de otro dominio ampliaría lo que puede generalizarse. La confiabilidad se aborda con repeticiones y con el reporte de la varianza, dado el carácter no determinista de los modelos. Un riesgo específico de este diseño es que las intervenciones manuales durante la corrida contaminen la medición de autonomía; se mitiga con un registro de intervenciones y con la repetición desde cero.

Otro riesgo es propio del enfoque de ciencia del diseño: el artefacto evoluciona con cada evaluación. Cada piloto encontró supuestos de Loom que no se sostenían y se corrigieron con un registro de decisión (ADR-0071 a 0084 tras el primer piloto, ADR-0085 a 0088 durante el segundo). Esa evolución es parte del resultado, pero implica que dos corridas solo son comparables si se hicieron con la misma versión de la plataforma, y por eso el commit de Loom y los modelos exactos se registran junto con cada corrida.

La validez de conclusión del experimento C tiene límites propios. Son 29 pares, cada condición se ejecutó una vez y una sola persona califica, así que no se mide la variabilidad del modelo ni el acuerdo entre evaluadores; las dos cosas quedan como trabajo futuro (apartado 6.3).

### 4.1.10 Datos y ética

El tema se generalizó deliberadamente respecto de cualquier sistema de un empleador, para no requerir autorización de datos de terceros. Los proyectos utilizados son propios o de prueba, los datos de acceso (llaves, contraseñas) no se almacenan en la documentación y las cuentas de prueba tienen credenciales generadas para ese fin.

@@ tesis_4_2
### 4.2.1 Visión general y nomenclatura

Loom es un sistema de *skills* de IA con un orquestador que las despacha y una plataforma web que las ejecuta y muestra su avance. Los documentos de diseño llaman *Telar* al orquestador con sus *skills* y *Loom* a la plataforma; en esta tesis se usa Loom para el conjunto. *Proyecto*, con mayúscula, designa la aplicación objetivo que Loom construye o evalúa, y se distingue de Loom, que es la herramienta.

El flujo recorre cuatro fases. Requerimientos lee las HUs de la fuente configurada y las especifica. Diseño genera los casos de prueba y la arquitectura, y la persona aprueba la arquitectura. Desarrollo descompone las HUs en paquetes de trabajo, genera el código, lo revisa, lo corrige y lo fusiona. Implementación despliega la aplicación en la nube y valida las HUs con pruebas de humo. Cada fase puede ejecutarse por separado, por lo que un Proyecto puede entrar al flujo en el punto que corresponda a su estado.

La figura 4.1 resume el recorrido de una HU por las cuatro fases.

FIGURA: diagramas/02-flujo-por-fases.png | Flujo de una HU por las cuatro fases de Loom

### 4.2.2 Arquitectura de la plataforma

La plataforma se implementó como monorepo con un servidor en Python (con validación de datos mediante Pydantic), MongoDB como base de datos documental y una interfaz web en Angular con la biblioteca PrimeNG (ADR-0031). Los procesos largos informan su progreso con eventos enviados por el servidor (SSE), que la interfaz muestra en un panel de actividad. El acceso de las personas requiere inicio de sesión. La figura 4.2 muestra los componentes y sus conexiones con los servicios externos.

FIGURA: diagramas/01-arquitectura-de-la-plataforma.png | Arquitectura de la plataforma y servicios externos

Tres proveedores de IA quedan disponibles por Proyecto: la API de Claude, la API de Gemini y el CLI de Claude Code con cuenta personal, este último solo para desarrollo. Las *skills* no dependen del proveedor; una capa común resuelve la llamada, valida la salida contra un esquema y reintenta ante respuestas truncadas o mal formadas.

Loom trabaja con tres tipos de almacenamiento. En MongoDB guarda el estado operativo (Proyectos, HUs, paquetes, revisiones, métricas y procesos). En un repositorio de control por Proyecto guarda, como Markdown versionado con git, la documentación de cada HU. Sobre los repositorios de la aplicación opera con una cuenta de desarrollo dedicada, de modo que todo cambio generado queda identificado como del sistema.

La cuenta de desarrollo se configura por Proyecto con un usuario de GitHub y un token de acceso de grano fino, limitado a los repositorios del Proyecto y a los permisos de contenido y de Pull Requests (ADR-0032). Loom clona cada repositorio una sola vez y, para cada rama de trabajo, crea un *worktree* propio desde la rama base del remoto, lo que permite trabajar en varias ramas a la vez sin tocar la rama base del clon (ADR-0043). El token llega a git por variables de entorno, sin aparecer en la URL ni en la línea de comandos. El token de la cuenta de desarrollo y el de Jira se guardan en la base de datos y la API nunca los vuelve a exponer, ni en el detalle ni en las listas; guardarlos en un gestor de secretos es una deuda documentada del diseño (ADR-0033 y ADR-0043).

### 4.2.3 Modelo de datos y artefactos por HU

La unidad central es el Proyecto, que reúne la fuente de HUs, los repositorios, el ambiente de desarrollo, el modo de arranque, el proveedor de IA, las cuentas de prueba por rol y la configuración de despliegue. Cada HU produce artefactos en su carpeta del repositorio de control: la especificación con sus criterios explícitos e inferidos y sus supuestos, los casos de prueba con el criterio del que derivan, el plan, las tareas, un archivo por paquete de trabajo y la evidencia de las pruebas de humo. Cada versión de la especificación y de los casos de prueba se guarda y se compara con la anterior.

El repositorio de control es un repositorio git local, uno por Proyecto y sin remoto (ADR-0035). Cada vez que una *skill* crea o cambia un artefacto, Loom hace un commit con un mensaje que dice qué pasó (por ejemplo, `HU-003/PT-01: en revisión, PR abierto` o `HU-003/PT-01: revisión 1 — aprobado`). La bitácora que muestra la plataforma es ese mismo historial, leído en cada consulta (ADR-0037), y gracias a él se puede recuperar cualquier artefacto tal como estaba en un momento dado. El experimento C lo aprovechó para reconstruir cada paquete como lo vio su primera revisión (apartado 5.2.14).

Un elemento del backlog se clasifica como HU, con criterios de aceptación y pipeline completo, o como Actividad, sin criterios, con un pipeline reducido. Los paquetes de trabajo son las unidades de código: cada uno pertenece a un solo repositorio, declara sus entregables, los casos de prueba que cubre y sus dependencias, y produce una rama y un Pull Request propios.

### 4.2.4 Las *skills* del pipeline

La tabla 4.4 resume las *skills*. Las que analizan devuelven salida estructurada; las que escriben código operan como agentes sobre una copia de trabajo del repositorio.

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

La *skill* 1 lee la fuente y hace el trabajo de un analista de requerimientos. Con Jira consulta el sprint por su API REST en el orden del tablero, que se guarda como la prioridad de negocio de cada HU (ADR-0048), y aplana la descripción, que Jira entrega en un formato de documento anidado, a texto plano. El modelo recibe cada elemento con un esquema de salida fijo y lo devuelve interpretado: la narrativa de la HU, los criterios explícitos que ya traía, los criterios que infiere y que un analista daría por incluidos (validaciones, permisos, manejo de errores), los supuestos que no puede resolver y la clasificación como HU o como Actividad (ADR-0033). Los criterios inferidos quedan separados de los explícitos, para que una persona vea qué agregó el modelo. La fuente Markdown funciona igual con archivos que se suben a la plataforma (ADR-0058). Cada HU guarda además una huella SHA-256 de su título y su descripción; una revisión que no usa el modelo compara esa huella con la fuente para saber qué HUs son nuevas o cambiaron, y solo esas se regeneran (ADR-0040).

En un Proyecto nuevo, al terminar de leer las HUs, la misma *skill* hace un análisis más, ahora con el papel de arquitecto. Decide si el sistema amerita microservicios (por omisión, un monolito), elige lenguaje, *framework* y herramientas de un catálogo cerrado, la autenticación y la estructura de repositorios, y justifica cada elección con las HUs que la motivan y las alternativas que descartó (ADR-0039). La propuesta precarga la configuración de la fase de Diseño, y la persona la confirma o la cambia.

La *skill* 2 deriva los casos de prueba. Cada criterio, explícito o inferido, produce al menos un caso en la forma *Given/When/Then*, con el resultado esperado, el rol de la cuenta con la que debe ejecutarse y la referencia al criterio del que deriva. Los casos se piensan como interacciones con la interfaz, porque se van a ejecutar con Playwright contra la aplicación desplegada. Un criterio que depende de un supuesto sin confirmar también genera su caso, con la interpretación de la *skill* 1; el supuesto se resuelve después, en la revisión (ADR-0011).

La *skill* 3 existe para los Proyectos que ya tienen código. Antes de diseñar, un agente de navegador ejecuta los casos de prueba de cada HU contra el ambiente desplegado y marca cada caso como cubierto, pendiente o sin evaluar (cuando no hay cuenta para su rol). Lo que no está cubierto, incluido lo que no se pudo evaluar, pasa a la descomposición; una HU con todos sus casos cubiertos no genera paquetes (ADR-0060).

La *skill* 4 diseña la arquitectura. En su variante fundacional, la única implementada, escribe un documento Markdown por repositorio con secciones fijas: resumen, backend (capas, módulos, estructura de carpetas, persistencia, seguridad), modelo de datos, frontend, despliegue, decisiones con sus alternativas descartadas, y supuestos y preguntas abiertas (ADR-0044). El stack configurado es una restricción; si no hay stack, la *skill* se detiene. Cada módulo, entidad y pantalla cita las HUs que lo motivan, y la sección de despliegue declara por cada servicio su Dockerfile de producción, su puerto y sus variables de entorno (ADR-0063). La arquitectura queda pendiente hasta que una persona la aprueba; si se regenera, la aprobación se pierde.

La *skill* 5 convierte la arquitectura aprobada en paquetes de trabajo, en dos pasos. El primero, de planeación, define el esqueleto (grupo `BASE`, entre tres y seis paquetes) y el orden de las HUs. El primer paquete del esqueleto deja el entorno de desarrollo en contenedores, con su `docker-compose.yml` y un README que explica cómo levantarlo y probarlo (ADR-0050); el último deja la aplicación desplegable, y ninguna HU arranca hasta que esté fusionado (ADR-0063). El orden de las HUs respeta la prioridad de la fuente salvo que una dependencia real obligue a adelantar otra, y si el modelo propone dependencias circulares se rompen solo las que forman el ciclo (ADR-0045 y ADR-0048). El segundo paso parte cada HU en uno a cuatro paquetes de una sola capa, con sus entregables, los casos de prueba que cubre y sus dependencias; el backend va antes que el frontend que lo consume, y cada paquete toca un solo repositorio. Todo caso de prueba de la HU tiene que quedar en algún paquete. Una respuesta sin paquetes para una HU con casos pendientes no se acepta: se repite hasta tres veces y, si sigue vacía, la descomposición se detiene con un error que nombra la HU (ADR-0062).

La *skill* 9 genera correcciones a partir de las pruebas de humo. Toma las HUs con casos fallidos y todos sus paquetes fusionados; los casos bloqueados no cuentan, porque no son un defecto del código. Con la especificación, la arquitectura, los casos fallidos y los archivos que tocó cada paquete, el modelo agrupa los fallos por causa probable y devuelve un paquete de corrección por causa, cada uno con una prueba que falle sin la corrección. Cada caso fallido queda en exactamente una corrección. El paquete de origen se atribuye solo si el modelo devuelve uno que existe, y nunca se inventa. Los casos que pasaban en la corrida anterior se marcan como regresión. Tras tres rondas de corrección sin éxito, la *skill* se niega a seguir y pide que una persona revise (ADR-0061).

Las *skills* 6, 7, 8 y 10 se describen en los apartados siguientes, junto con las compuertas y las reglas que las rodean.

### 4.2.5 Generación de código y compuertas de ejecución

Un paquete es elegible cuando está pendiente, la arquitectura está aprobada y todas sus dependencias están fusionadas, tanto las de paquete como las de las HUs de las que depende (ADR-0046). La generación trabaja sobre un *worktree* de la rama del paquete, creado desde la rama base actualizada. Con la API, el agente tiene cuatro herramientas: listar un directorio, leer un archivo, escribir un archivo y terminar. No ejecuta comandos ni tiene red, las rutas quedan confinadas al *worktree* y hay límites de 40 turnos, 60 archivos, 200 KB por archivo y 1.5 MB por paquete. Con el CLI de Claude Code, el agente usa el ciclo de herramientas del propio CLI con permisos acotados por ruta: puede leer y editar dentro del repositorio, sin terminal, sin red y sin subagentes (ADR-0053). En los dos casos recibe el paquete, la arquitectura del repositorio, la especificación y los casos de prueba de la HU, los paquetes de los que depende y el árbol de archivos existente. Al terminar, Loom hace un commit con la identidad de la cuenta de desarrollo, sube la rama y abre el Pull Request con los entregables, los casos cubiertos, los supuestos heredados de la HU y un resumen del agente.

La generación de código sigue TDD: el agente escribe pruebas y código de cada paquete, y el sistema rechaza el resultado si no incluye pruebas o si faltan los archivos obligatorios de un servicio (por ejemplo, un README o un archivo de composición de contenedores). Antes de subir el código, una compuerta lo ejecuta dentro de un contenedor de Docker aislado de la rama de trabajo: instala dependencias, compila, corre el análisis estático (*lint*) y las pruebas unitarias del proyecto, con los mismos comandos que definen sus *scripts* y su integración continua. Las pruebas que requieren Docker desde dentro del contenedor, como las que usan Testcontainers, quedan excluidas y las cubre la integración continua. Si la compuerta falla, el error vuelve al agente hasta dos veces; si no se corrige, el Pull Request se abre con la advertencia y la revisión lo marca con una observación bloqueante.

La compuerta responde a un hallazgo de las primeras corridas: el agente no ejecuta nada por sí solo, y la revisión de código lee el *diff* sin compilarlo. Sin la compuerta, un error de compilación o de estilo solo aparecía al esperar la integración continua de GitHub.

### 4.2.6 Revisión, corrección y fusión

La revisión recibe el Pull Request y el contexto completo (especificación, casos de prueba, arquitectura aprobada y el resumen de la implementación). Cada observación lleva una fuente (criterio de aceptación, arquitectura, buenas prácticas, pruebas o seguridad), una severidad (bloqueante, mayor o menor) y, cuando aplica, archivo y línea, y se publica como comentario en el Pull Request. La figura 4.3 resume el ciclo completo de un paquete, desde la generación hasta la fusión.

FIGURA: diagramas/03-ciclo-de-un-paquete.png | Ciclo de un paquete de trabajo: generación, compuertas, revisión, corrección y fusión

Si una HU tiene supuestos sin confirmar, el sistema agrega una observación bloqueante hasta que una persona registre su decisión.

La corrección aplica las observaciones sobre la misma rama, responde cada comentario y marca las conversaciones resueltas (ADR-0064). Cada ronda de revisión y de corrección se guarda con su resultado y con el *diff* que se revisó (ADR-0068).

Las observaciones pueden valorarse de dos maneras. Una persona las califica con la rúbrica de la tesis (relevante y correcta, relevante pero mal sustentada, ruido o falsa). Además, bajo demanda, un modelo puede dar una segunda opinión: recibe las observaciones numeradas y el *diff* tal como lo vio la revisión, y dictamina por cada una si es correcta, parcial, incorrecta o no verificable, si su severidad está bien puesta y qué recomienda hacer, citando el fragmento del *diff* que lo sostiene (ADR-0069). Esa opinión puede venir de un proveedor distinto del que revisó. Sirve para orientar, pero la calificación que vale para la tesis es la de la persona; el apartado 2.9 explica por qué un modelo no debe ser el juez de otro.

La fusión de un Pull Request exige que los *checks* de la integración continua estén en verde. Loom consulta el estado de esos *checks* en GitHub. Si alguno falla durante el avance de una HU, lee el registro del *job* fallido, extrae las líneas que preceden a la marca de error y lo devuelve al agente como una observación bloqueante, con hasta dos correcciones por paquete. Si sigue en rojo, el avance se detiene y el Pull Request queda abierto.

### 4.2.7 Avance de una HU de punta a punta

La acción «avanzar con una HU» encadena el ciclo para todos los paquetes de una HU en el orden de sus dependencias. Por cada paquete genera el código, lo revisa, aplica hasta un número de rondas de corrección elegido por la persona (de cero a tres), espera la integración continua y fusiona. Se detiene ante una observación bloqueante que no se pudo resolver y deja el Pull Request abierto para que la persona lo decida. Al fusionarse el último paquete, la HU queda completa y se lanza el despliegue.

### 4.2.8 Despliegue

Un generador determinista produce, a partir de la configuración del Proyecto, un *script* de despliegue (`release.py`) y su disparador, sin credenciales. El *script* es idempotente: habilita las APIs necesarias de Google Cloud, crea la instancia de base de datos PostgreSQL y su usuario cuando la aplicación lo requiere, guarda las contraseñas y los secretos aleatorios en el gestor de secretos, crea una cuenta de servicio de ejecución con acceso solo a esos secretos, construye las imágenes con el servicio de construcción de la nube y despliega el backend y el frontend en Cloud Run. Las direcciones de los servicios se calculan antes de desplegar, de modo que la configuración de origen cruzado (CORS) del backend se establece en una sola pasada.

El *script* ubica cada servicio aunque el monorepo lo ponga en `apps/`, `packages/` o `services/`, y lo construye desde la raíz del repositorio cuando su Dockerfile copia archivos de otros *workspaces* (ADR-0086). A un backend que no es Java le entrega, además de las variables sueltas de la base de datos, la cadena de conexión `DATABASE_URL` como secreto; y a un frontend que fija la dirección de la API al compilar le pasa la URL del backend como argumento de construcción (ADR-0087). Estas tres reglas salieron del segundo piloto, cuyo stack Node y React no cabía en los supuestos del primero.

El despliegue automático usa GitHub Actions con federación de identidad: el propio *script* crea el pool y el proveedor de identidad, compartidos por todos los Proyectos del mismo proyecto de la nube y restringidos a sus repositorios (ADR-0085), la cuenta de servicio desplegadora y las variables del repositorio que el flujo de trabajo necesita. El flujo de trabajo se dispara por solicitud y Loom lo lanza cuando una HU queda completa, en lugar de reaccionar a cada cambio de la rama principal, para que una HU a medias no llegue al ambiente. Los Pull Requests que publican estos archivos de despliegue se fusionan desde Loom, con la misma regla de integración continua en verde.

### 4.2.9 Validación funcional

Las pruebas de humo recorren todos los casos de prueba de una HU cuando toda su ronda de paquetes está fusionada. Un modelo lee el código de la aplicación y los casos y escribe un guion de Playwright con las acciones y las verificaciones de cada caso; el guion se ejecuta contra el ambiente desplegado con la cuenta de prueba del rol que el caso requiere. Como la *skill* de casos de prueba escribe el rol en texto libre, a veces con varios actores («invitado (sin sesión); admin para verificar»), la cuenta se elige por el actor principal y un caso de invitado no la necesita (ADR-0088). Cuando un caso falla, un agente de navegador lo reproduce para distinguir un guion mal escrito de un fallo real de la aplicación. El resultado de cada caso es aprobado, fallido o bloqueado, y el informe con capturas queda como evidencia. Los casos fallidos pueden convertirse en paquetes de corrección que reingresan al ciclo de código y revisión. La figura 4.4 muestra la secuencia del despliegue y de la validación.

FIGURA: diagramas/04-liberacion-y-validacion.png | Secuencia de liberación en la nube y validación funcional

### 4.2.10 Cambios en los requisitos

Cuando la especificación o los casos de prueba de una HU cambian después de haberse usado, Loom guarda una versión nueva sin borrar las anteriores, marca como desactualizado lo que dependía de ellas (casos, arquitectura, código, guion de pruebas) y, para las HUs cuyo código ya existe, genera paquetes de cambio que llevan el código a los casos nuevos.

Las versiones se identifican por el elemento de la fuente (la clave del *issue* en Jira) y no por el identificador interno de la HU, de modo que la numeración continúa aunque el Proyecto se reinicie; guardar sin cambios no crea una versión (ADR-0065). Cada paquete guarda la versión de los casos de prueba con la que se planeó, y cada corrida de pruebas de humo, la versión con la que se hizo. Con eso, la plataforma calcula sin guardar estado propio qué está desactualizado: casos de una especificación que cambió, código planeado con casos anteriores, pruebas de humo hechas con casos anteriores. Como los identificadores de los casos se reasignan al regenerarlos, la diferencia entre versiones se calcula por criterio de aceptación de origen (casos agregados, eliminados o distintos), y una prueba de humo de regresión con un guion viejo se niega en lugar de omitir los casos nuevos (ADR-0066).

El paquete de cambio es un paquete normal, con su propia etiqueta. Un modelo recibe la especificación vigente, la arquitectura, los paquetes existentes con los archivos que tocó cada uno, los casos nuevos o modificados (con su versión anterior) y los criterios eliminados, y devuelve los paquetes que ajustan el código, siempre con pruebas nuevas o adaptadas. Un criterio eliminado también produce trabajo: el paquete indica qué código y qué pruebas quitar (ADR-0067). La arquitectura guarda la versión de cada especificación con la que se generó y avisa cuando una de ellas cambia.

### 4.2.11 Control de la ejecución

Cada proceso que Loom ejecuta queda registrado con su tipo, las HUs sobre las que trabaja, su estado y su registro de eventos, y se guarda en una colección de la base de datos para conservar el historial con la hora de inicio y de fin. Varios procesos pueden correr a la vez si trabajan sobre HUs distintas. Sobre la misma HU, o sobre todo el Proyecto, el segundo se rechaza. El despliegue es exclusivo: espera en cola a que terminen los demás y, mientras corre, los demás esperan. Un proceso puede cancelarse; la cancelación detiene su trabajo y los procesos externos que lanzó (el agente, el contenedor de compilación, la suite de pruebas), y conserva lo ya hecho. Cerrar o recargar la pantalla que lo lanzó no lo detiene.

### 4.2.12 Puntos de decisión humana

El sistema deja a las personas los puntos donde se requiere criterio: aprobar la arquitectura, confirmar los supuestos de una HU con una decisión que el agente recibe como requisito, valorar la relevancia de las observaciones, decidir si se fusiona un Pull Request con observaciones abiertas, y cancelar o relanzar procesos. Una aprobación manual adicional antes de fusionar es configurable por Proyecto.

### 4.2.13 Medición

Cada llamada a un modelo escribe un registro con el proveedor, el modelo, los tokens de entrada y salida, la duración, los reintentos, el resultado y el costo estimado según una tabla de precios configurable. Los rechazos de las compuertas y los eventos de cada proceso se registran también. Esos datos alimentan la tarjeta de uso de IA de la plataforma y una exportación a CSV, que son la fuente de las tablas de tiempo, tokens y costo del capítulo 5.

### 4.2.14 Interfaz de la plataforma

La interfaz está pensada como una consola de desarrollo para un monitor de escritorio y sesiones largas, en las que el contenido principal son registros y progreso en vivo. Usa un solo tema oscuro, tipografía monoespaciada para identificadores, rutas y cifras, y tablas densas; cada estado (fase, resultado de una prueba, situación de un paquete) se muestra con icono, texto y color, de modo que no depende solo del color (ADR-0075).

La pantalla de un Proyecto tiene una pestaña por fase. Cada pestaña reúne el resumen de la fase, la hora de su última ejecución, el botón para ejecutarla y su configuración, porque cada fase puede correr por separado (ADR-0037). La plataforma muestra además el siguiente paso recomendado para el Proyecto: diagnosticar el avance existente, generar paquetes de cambio cuando una HU quedó desactualizada, corregir los fallos de las pruebas de humo o volver a probar una HU corregida, según el estado del Proyecto (ADR-0060, ADR-0061, ADR-0066 y ADR-0067).

El panel de actividad muestra en vivo el registro del proceso que está corriendo. Consulta al servidor cada cuatro segundos, así que también muestra un proceso lanzado desde otra sesión o desde un guion, y mientras algo corre deshabilita los botones de ejecución (ADR-0080). El detalle de una HU agrupa su especificación, sus casos de prueba, sus paquetes, el historial de versiones, todas sus corridas de pruebas de humo con el resultado y el motivo de cada caso, y sus incidencias, que son los paquetes de corrección de la propia HU (ADR-0065 y ADR-0073). El Anexo C recorre estas pantallas en el orden en que se usaron en la corrida E1c.

### 4.2.15 Estado de implementación

La tabla 4.5 separa lo que está implementado y se ejercitó en las corridas del capítulo 5, lo que está implementado y no se ejercitó, y lo que solo existe como diseño. Un resultado del capítulo 5 solo se atribuye a una función implementada y ejercitada.

TABLA: Estado de implementación de las funciones de Loom
| Función | Estado | Observación |
| *Skill* 1, lectura desde Jira | Implementada y ejercitada | E1c y E3c |
| *Skill* 1, fuente Markdown | Implementada, no ejercitada | No se usó en las corridas del capítulo 5 |
| *Skill* 1, fuente GitHub | Solo diseño | ADR-0010 |
| *Skill* 2, casos de prueba | Implementada y ejercitada | 44 casos en E1c y 101 en E3c |
| *Skill* 3, diagnóstico de avance | Implementada, no ejercitada | Los dos Proyectos eran nuevos |
| *Skill* 4, arquitectura fundacional | Implementada y ejercitada | Un documento por Proyecto (monorepo) |
| *Skill* 4, modo extensión | Pendiente | Depende de la *skill* 3 |
| *Skill* 5, descomposición | Implementada y ejercitada | 12 paquetes en E1c y 17 en E3c |
| *Skill* 6, generación de código | Implementada y ejercitada | Con el CLI de Claude Code |
| *Skill* 7, revisión | Implementada y ejercitada | También en el experimento C |
| *Skill* 8, pruebas de humo | Implementada y ejercitada | Contra el ambiente desplegado |
| *Skill* 9, correcciones desde las pruebas de humo | Implementada, no ejercitada | Las corridas no generaron correcciones a partir de sus pruebas de humo |
| *Skill* 10, release | Implementada y ejercitada | Google Cloud con GitHub Actions |
| Versiones de las HUs y paquetes de cambio | Implementada, no ejercitada | Las HUs no cambiaron durante las corridas |
| Indexación de varios repositorios | Solo diseño | Objetivo específico 9 |

@@ tesis_6_3
El trabajo deja abiertas líneas que se derivan de sus propias decisiones y de lo que no alcanzó a ejercitarse.

La primera es la generalización a otros proveedores de código. La revisión, la fusión, la lectura de la integración continua y el despliegue automático están implementados sobre GitHub. Un adaptador para GitLab y una separación explícita entre el proveedor de código y la estrategia de despliegue permitirían usar Loom en otros entornos, incluida la conexión de un servicio de construcción por *tokens*, que sí puede automatizarse.

La segunda es una compuerta de arranque. La compilación, el análisis estático y las pruebas unitarias antes de subir el código no detectan los defectos que solo aparecen al ejecutar la aplicación con una base de datos real (migraciones, configuración, arranque). Levantar la imagen de producción junto a una base desechable y comprobar su estado de salud antes del despliegue, y ejecutar en ese entorno las pruebas de integración con contenedores, cerrarían esa brecha.

La tercera es el diagnóstico de avance existente sobre proyectos con código previo y la ejecución del ciclo de corrección con fallos reales de la aplicación, que están implementados pero no se ejercitaron. También queda pendiente la conexión de las incidencias con la herramienta de seguimiento (crear en Jira la incidencia de cada fallo) y la creación de subtareas en la fuente de HUs.

La cuarta es operativa: persistir y reanudar los procesos interrumpidos, en lugar de solo marcarlos, y ligar cada proceso del historial con sus métricas de costo. La quinta es la infraestructura como código: Terraform daría estado declarativo y vista previa de los cambios de despliegue, a cambio de una dependencia adicional, y se justifica cuando el sistema atienda varios ambientes.

La sexta nace del segundo piloto: que la compuerta de compilación reconozca los monorepos con *workspaces* (no se ejecutó en ningún paquete del segundo proyecto); que la *skill* de casos de prueba escriba el rol con los nombres de las cuentas configuradas en lugar de texto libre; que la plataforma contraste las variables de entorno configuradas con las que exige el código generado (su `.env.example` o su esquema de configuración); que la corrección con el registro del CI esté disponible desde la interfaz para cualquier paquete con el CI en rojo, incluso uno aprobado; y que el modelo del CLI quede fijado y registrado por corrida.

La séptima es completar el experimento de control de la revisión: repetir cada condición sobre una muestra de Pull Requests para medir la variabilidad del modelo, y sumar una segunda persona evaluadora para estimar el acuerdo entre calificaciones.

Por último, la validez externa mejoraría con un tercer proyecto con avance previo, con otra fuente de HUs y con evaluadores independientes, y la protección de la rama principal en la propia plataforma de código, que exige un plan de pago, evitaría que un cambio se fusione con la integración continua en rojo por una vía distinta de Loom.
