@@ tesis_cap2
### 2.1 Modelos de lenguaje de gran tamaño

Un modelo de lenguaje de gran tamaño es una red neuronal, casi siempre con arquitectura *transformer* [N:vaswani], entrenada para predecir el siguiente fragmento de texto a partir del anterior. El preentrenamiento sobre corpus muy amplios, que incluyen código fuente, les permite realizar tareas nuevas a partir de instrucciones y ejemplos dados en el texto de entrada, sin actualizar sus parámetros, capacidad que se conoce como aprendizaje en contexto [N:brown-few-shot].

Tres propiedades condicionan su uso en ingeniería de software. La primera es el carácter probabilístico de la salida: la misma entrada puede producir salidas distintas, lo que obliga a repetir las mediciones y a reportar su variabilidad. La segunda es la ventana de contexto, el límite de texto que el modelo procesa en una llamada; todo lo que la tarea necesita saber debe caber en ella o recuperarse por otros medios. La tercera es la posibilidad de generar texto plausible y equivocado, incluidos fragmentos de código que no compilan o que no cumplen lo pedido. La literatura estudia ese fenómeno como alucinación [N:ji-hallucination], y en código se manifiesta como aciertos aparentes que se caen con pruebas más exigentes [N:evalplus]. Loom responde a las tres con salidas estructuradas y validadas, con contexto seleccionado por tarea y con comprobaciones que se ejecutan fuera del modelo.

### 2.2 Agentes y uso de herramientas

Un agente basado en un LLM alterna razonamiento y acciones: el modelo decide invocar una herramienta (leer un archivo, escribir uno, ejecutar un comando), recibe su resultado y continúa hasta completar la tarea [N:react]. El diseño de la interfaz que expone las herramientas al modelo condiciona su desempeño en tareas de ingeniería de software [N:swe-agent-aci]. Los proveedores ofrecen la invocación de funciones: el modelo decide cuándo llamar una función definida por la aplicación y devuelve una llamada estructurada, con su esquema de entrada, que la aplicación ejecuta [N:anthropic-tool-use]. Eso permite tratar su salida como datos y no como texto libre.

En Loom, las *skills* de análisis (leer una HU, generar casos de prueba, diseñar la arquitectura, revisar código) usan esa salida estructurada. Las *skills* que escriben código funcionan como agentes con acceso a los archivos del repositorio de trabajo, dentro de un directorio acotado.

### 2.3 Generación automática de código

La generación de código a partir de descripciones en lenguaje natural se evaluó primero con problemas de funciones aisladas, cuya corrección se comprueba con pruebas unitarias [N:chen-codex]. Trabajos posteriores llevaron la tarea a repositorios reales: SWE-bench reúne 2,294 *issues* reales de 12 repositorios de Python, y resolverlos exige editar código existente, con frecuencia en varios archivos, y no solo escribir funciones nuevas [N:swe-bench]. La distancia entre ambos tipos de problema es la que separa el código correcto de un ejercicio del código que se integra a un sistema en operación.

### 2.4 Historias de usuario, criterios de aceptación y especificaciones

Una historia de usuario describe una necesidad desde la perspectiva de quien la tiene y su valor de negocio, y se acompaña de criterios de aceptación que delimitan cuándo se considera cumplida [N:cohn-user-stories]. Los criterios suelen redactarse en la forma *Given/When/Then*, propuesta por North para el desarrollo dirigido por el comportamiento, que los vuelve verificables [N:north-bdd].

El desarrollo dirigido por especificaciones (*Spec-Driven Development*, SDD) da a la especificación el papel de artefacto principal. En la formulación difundida para agentes de código, la especificación es la fuente de verdad con la que las herramientas generan, prueban y validan el código, y el trabajo avanza por especificar, planear, dividir en tareas e implementar, con supervisión humana en cada punto de control [N:delimarsky-sdd]. Loom lo adopta: cada HU tiene su carpeta con la especificación, los casos de prueba, el plan, las tareas, los paquetes de trabajo y la evidencia, en Markdown versionado en git, de modo que cada decisión queda trazada hasta el criterio del que proviene.

### 2.5 Pruebas de software

El desarrollo dirigido por pruebas (*Test-Driven Development*, TDD) escribe la prueba antes que el código que la satisface, en ciclos cortos de prueba en rojo, código mínimo y refactorización [N:beck-tdd]. Loom exige que cada paquete de código entregue sus pruebas y rechaza los que no las incluyen.

Las pruebas de extremo a extremo comprueban el sistema completo desde la interfaz, como lo usaría una persona. Playwright, por ejemplo, es un *framework* de pruebas de extremo a extremo para aplicaciones web modernas que automatiza Chromium, WebKit y Firefox [N:playwright-docs]. Son más costosas y frágiles que las pruebas unitarias, y por eso la pirámide de pruebas recomienda muchas más pruebas unitarias que pruebas de alto nivel a través de la interfaz gráfica [N:fowler-pyramid]. En Loom, los casos de prueba derivados de los criterios de aceptación se ejecutan de este modo contra un ambiente desplegado.

### 2.6 Revisión de código

La revisión de código por pares es una práctica extendida. Un estudio en Microsoft encontró que detectar defectos sigue siendo la motivación principal, pero que la revisión trata menos de defectos de lo esperado y aporta transferencia de conocimiento, conciencia del equipo y soluciones alternativas; la comprensión del código y del cambio resultó ser el aspecto central [N:bacchelli-bird]. Las observaciones de una revisión se distinguen por su severidad y por la fuente de la que provienen: el cumplimiento de la HU, la conformidad con la arquitectura, las buenas prácticas del lenguaje, la calidad de las pruebas o la seguridad. La revisión automática con modelos se ha estudiado con modelos entrenados para evaluar la calidad de un cambio, generar comentarios de revisión y sugerir refinamientos del código [N:li-codereviewer]. Si su calidad depende del contexto que recibe, como sostiene la hipótesis H1 de esta tesis, es una pregunta empírica que el capítulo 5 debe contestar.

### 2.7 Integración continua, entrega continua y contenedores

La integración continua ejecuta de forma automática la construcción y las pruebas de cada cambio; la entrega continua extiende esa cadena hasta dejar el sistema listo para desplegarse mediante una *pipeline* automatizada de despliegue que va del *check-in* al *release* [N:humble-farley]. Los contenedores empaquetan una aplicación con sus dependencias y permiten construir y ejecutar la misma imagen en el desarrollo, en la integración continua y en la nube [N:merkel-docker].

Para autenticar un flujo de despliegue sin guardar llaves, la federación de identidad de cargas de trabajo permite que un proveedor de identidad externo, como el que emite GitHub Actions, obtenga credenciales temporales de la nube a partir de un token firmado. Google Cloud la propone para que cargas externas, como los sistemas de integración continua, accedan a sus recursos sin llaves de cuenta de servicio, cuyo manejo incorrecto representa un riesgo [N:google-wif]; GitHub Actions emite esos tokens mediante OpenID Connect [N:github-oidc]. Loom usa esa alternativa para el despliegue automático.

### 2.8 Registros de decisión de arquitectura

Un registro de decisión de arquitectura (*Architecture Decision Record*, ADR) documenta una decisión significativa con su contexto, la decisión tomada y sus consecuencias, y no se modifica: si la decisión cambia, un registro nuevo sustituye al anterior [N:nygard-adr]. El diseño de Loom se documentó en más de ochenta registros de este tipo, lo que permite reconstruir por qué el sistema tiene su forma actual y qué se descartó.

### 2.9 Evaluación experimental en ingeniería de software

Comparar sistemas que incorporan LLM plantea problemas de validez propios. La aleatoriedad de las salidas exige repetir las corridas y reportar la varianza. La evolución de los modelos hace que un resultado no se reproduzca meses después si no se registran la versión y la fecha. La evaluación de la calidad de una salida por parte de personas debe ser ciega y apoyarse en una rúbrica escrita, para reducir el sesgo del evaluador. Los tipos de amenazas a la validez (interna, externa, de constructo y de conclusión) ofrecen una lista de comprobación para el diseño del estudio [N:wohlin-experimentation].
