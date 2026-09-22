@@ tesis_5_1
### 5.1.1 Alcance de la corrida

Este capítulo reporta una corrida completa del escenario E1c: el Proyecto de inventarios del capítulo 4 con «Claude (cuenta normal)» como proveedor de IA, que usa el CLI de Claude Code con el modelo `claude-sonnet-5`. La corrida se hizo el 21 de septiembre de 2026, con la plataforma en el estado descrito en el capítulo 4, desde un Proyecto sin datos previos: el repositorio de GitHub estaba reducido a su README inicial y las colecciones de Mongo del Proyecto estaban vacías. Se procesaron tres HUs de Jira (ITZINV-12, ITZINV-13 e ITZINV-14) y se recorrieron las cuatro fases.

Del diseño experimental del capítulo 4 solo se ejecutó este escenario (Tabla 5.1). La corrida describe qué hace el sistema y con qué calidad, pero no compara proveedores ni proyectos ni condiciones de contexto, de modo que las hipótesis H1, H2 y H3 siguen sin evaluarse (apartado 5.2.9).

TABLA: Escenarios del diseño experimental y estado
| Escenario | Proyecto | Proveedor de IA | Estado |
| E1 | Inventarios | Claude por API | No ejecutado |
| E1c | Inventarios | Claude por CLI (cuenta personal) | Ejecutado (esta corrida) |
| E2 | Inventarios | Gemini | No ejecutado en esta etapa; existe una corrida parcial previa que no es comparable |
| E3 | IAT | Claude | No ejecutado |
| E4 | IAT | Gemini | No ejecutado |

### 5.1.2 Procedimiento

La persona investigadora operó Loom desde su interfaz web con un guion de Playwright que pulsa los mismos botones que usaría una persona y guarda una captura de cada paso; el Anexo C reproduce el recorrido con las pantallas. Cada acción se ejecutó en este orden: leer las tres HUs, generar los casos de prueba, generar y aprobar la arquitectura, descomponer en paquetes, y por cada paquete generar el código, hacer una sola revisión y aceptar el Pull Request. Con el último paquete fusionado se generó y publicó el despliegue, se ejecutó el release en Google Cloud y se corrieron las pruebas de humo de las tres HUs.

Se fijaron dos reglas para la corrida. La primera es una sola revisión por paquete: el Pull Request se acepta aunque queden observaciones, para medir qué encuentra la revisión y no cuánto tarda en converger. La segunda es que Loom conserva sus propias reglas de fusión (integración continua en verde, dependencias resueltas), sin saltárselas. Las decisiones sobre los supuestos de las tres HUs las redactó el equipo como política del piloto.

### 5.1.3 Instrumentos y fuentes de datos

Los datos provienen de tres fuentes. De MongoDB, las colecciones de procesos (duración y estado de cada ejecución), paquetes, revisiones (observaciones con fuente y severidad), métricas (llamadas al modelo con tokens, duración y costo; compuertas de ejecución y reintentos) y pruebas de humo. De la API de GitHub, el estado de los Pull Requests y de los *checks* de integración continua. De las capturas de pantalla, el registro visual de cada paso. El costo es el que informa el CLI de Claude; al usarse con una suscripción, es nocional y no comparable con la facturación de una API.

### 5.1.4 Amenazas a la validez de esta corrida

La corrida es una sola repetición, con un solo evaluador y un solo modelo, de modo que la variabilidad entre corridas no está medida. Los tiempos dependen de la máquina, de la red y de la carga del proveedor: una generación falló por el límite de sesión de la suscripción y hubo que repetirla. La persona que operó el sistema es también quien lo construyó, lo que favorece el conocimiento de sus puntos débiles. Las observaciones de la revisión no se valoraron todavía como relevantes o no, por lo que solo se reporta cuántas hay y de qué tipo. Por último, tres acciones de entorno se hicieron fuera de Loom (Tabla 5.5), y sus efectos no se cuentan como resultado del sistema.

@@ tesis_5_2
### 5.2.1 Ejecución de punta a punta

El flujo se completó con las tres HUs: 12 paquetes de trabajo fusionados, la aplicación desplegada en Cloud Run y 44 casos de prueba ejecutados contra ella. La Tabla 5.2 resume el tiempo de reloj de cada etapa. La plataforma trabajó unos 113 minutos, sin contar la espera de la integración continua ni el proceso de descomposición que falló.

TABLA: Etapas de la corrida y tiempo de reloj
| Etapa | Resultado | Tiempo (min) |
| Leer y especificar 3 HUs | 3 HUs, todas con supuestos por confirmar | 1.4 |
| Generar casos de prueba | 44 casos (14, 14 y 16) | 1.8 |
| Generar la arquitectura | 5 entidades, 7 decisiones, 7 preguntas abiertas | 2.0 |
| Descomponer en paquetes | 12 paquetes en 4 grupos; el primer intento (2.5 min) falló | 2.1 |
| Generar el código de los 12 paquetes | 12 Pull Requests abiertos | 70.7 |
| Revisar los 12 paquetes | 12 revisiones | 6.5 |
| Corregir un paquete | 1 corrección (HU-003/PT-02) | 6.2 |
| Ejecutar el release en Google Cloud | Backend y frontend desplegados (segundo intento) | 8.5 |
| Pruebas de humo de las 3 HUs | 36 aprobados, 2 fallidos, 6 bloqueados | 13.7 |

### 5.2.2 Requerimientos, casos de prueba y arquitectura

Las tres HUs se clasificaron como HU y se especificaron con supuestos abiertos. Los casos de prueba se generaron en una sola llamada por HU y sumaron 44. La arquitectura resultante propone un monolito modular de Spring Boot y Angular en un monorepo, con cinco entidades y siete decisiones, y deja siete preguntas abiertas que la persona no tuvo que resolver para aprobarla.

La descomposición falló en su primer intento: tras tres reintentos internos, el modelo no produjo ningún paquete para la HU-003. Un segundo intento produjo los 12 paquetes: cinco del esqueleto (entorno de desarrollo, base del backend, seguridad, base del frontend y despliegue), dos de la HU-001, tres de la HU-002 y dos de la HU-003.

### 5.2.3 Generación de código y compuertas

Los 12 paquetes produjeron un Pull Request. La generación tardó entre 0.9 y 10.8 minutos por paquete en tiempo de modelo (Figura 5.1), con una relación clara entre duración y costo, y los paquetes de las HUs cuestan más que los del esqueleto.

FIGURA: graficas/g5-1-duracion-y-costo-por-paquete.png | Duración y costo de la generación de código por paquete

La compuerta de ejecución en Docker se corrió en 10 de los 12 paquetes; en los dos paquetes de infraestructura se omite. En 8 de ellos pasó al primer intento, y en un noveno (HU-001/PT-02) pasó al segundo, después de que el error volviera al agente. El décimo paquete, HU-003/PT-02, falló en sus tres intentos, por lo que el Pull Request se abrió con la advertencia. La Tabla 5.3 resume las 17 ejecuciones de la compuerta.

TABLA: Ejecuciones de la compuerta de compilación, análisis estático y pruebas
| Resultado | Ejecuciones | Detalle |
| Aprobada | 10 | 8 paquetes al primer intento, HU-001/PT-02 al segundo y la corrección de HU-003/PT-02 al segundo |
| Fallida | 5 | HU-001/PT-02 (1), HU-003/PT-02 (3 en la generación y 1 en la corrección) |
| Omitida | 2 | BASE/PT-01 y BASE/PT-05 (paquetes de infraestructura) |

La compuerta señaló de antemano que HU-003/PT-02 tenía un problema, y el CI de GitHub marcó después un error de análisis estático en el frontend (no se verificó si es el mismo que vio la compuerta). Loom no dejó fusionar el paquete hasta corregirlo, y una ronda de corrección (6.2 minutos) dejó la compuerta y el CI en verde. Los otros 11 paquetes se fusionaron con el CI en verde sin corrección.

### 5.2.4 Revisión

Las 12 revisiones dejaron 66 observaciones: 2 bloqueantes, 24 mayores y 40 menores, con un promedio de 5.5 por paquete. Dos revisiones aprobaron el paquete (con dos observaciones menores cada una) y diez lo dejaron con observaciones. Cada revisión tardó entre 0.4 y 0.8 minutos y costó 0.20 USD en promedio. Por fuente (Figura 5.2), predominan las de buenas prácticas (23) y las de criterios de aceptación (15), seguidas por pruebas (14), seguridad (9) y arquitectura (5). De las 9 de seguridad, 7 son mayores, y de las 15 de criterios de aceptación, 10 son mayores.

FIGURA: graficas/g5-2-observaciones-por-fuente-y-severidad.png | Observaciones de las 12 revisiones por fuente y severidad

Las dos observaciones bloqueantes son de un solo paquete, HU-003/PT-02, el mismo que falló la compuerta. Con la política de una sola revisión, 11 paquetes se fusionaron con observaciones sin resolver (nueve con observaciones y dos aprobados con observaciones menores); el duodécimo, HU-003/PT-02, pasó por una corrección. Este capítulo no evalúa si esas observaciones eran relevantes o ruido: esa valoración es el dato que falta para H1.

### 5.2.5 Despliegue

El primer release construyó las imágenes pero el backend no arrancó en Cloud Run: la base de datos de Cloud SQL conservaba el historial de migraciones de la corrida anterior y Flyway detectó que las migraciones nuevas tenían otra suma de verificación. Con la base recreada, el release terminó bien en 8.5 minutos y dejó el backend y el frontend accesibles. El release automático, que Loom lanza al fusionarse el último paquete de una HU, falló la primera vez con un error 422 de GitHub, porque el flujo de trabajo de release aún no estaba en el repositorio; el lanzamiento manual desde Loom funcionó una vez fusionado el Pull Request de despliegue.

### 5.2.6 Validación funcional

Las pruebas de humo ejecutaron los 44 casos contra el ambiente desplegado (Tabla 5.4): 36 aprobados (82 %), 2 fallidos y 6 bloqueados. Los dos fallos tienen la misma causa: los casos TC-014 de la HU-002 y TC-016 de la HU-003 esperan una bitácora de eventos visible para el administrador, y la aplicación no la ofrece. Los seis bloqueos dependen de datos que el ambiente no tenía (una cuenta registrada con contraseña incorrecta, un buzón de correo o un fallo forzado del servicio de correo), salvo uno, TC-013 de la HU-002, cuyo guion generado por el modelo tenía sintaxis inválida.

TABLA: Resultado de las pruebas de humo por HU
| HU | Casos | Aprobados | Fallidos | Bloqueados | Duración (min) |
| HU-001 | 14 | 11 | 0 | 3 | 5.3 |
| HU-002 | 14 | 10 | 1 | 3 | 5.1 |
| HU-003 | 16 | 15 | 1 | 0 | 3.3 |

### 5.2.7 Autonomía: intervenciones manuales

Se contaron nueve intervenciones de la persona (Tabla 5.5). Seis se hicieron con acciones de Loom y tres, fuera de él. Ninguna consistió en editar el código generado.

TABLA: Intervenciones de la persona durante la corrida
| Intervención | Dónde se hizo | Causa |
| Reintentar la descomposición | Loom | El modelo no produjo paquetes para una HU |
| Registrar una decisión por HU | Loom | Regla de supuestos sin confirmar |
| Esperar la integración continua antes de fusionar (BASE/PT-05) | Loom | Loom rechazó la fusión con el CI corriendo |
| Repetir la generación de HU-003/PT-02 | Loom | Límite de sesión del CLI de Claude |
| Aplicar una ronda de corrección (HU-003/PT-02) | Loom | Compuerta y CI en rojo |
| Completar cuenta de servicio y proveedor de identidad | Loom | Datos del entorno de Google Cloud |
| Fusionar el Pull Request de despliegue | Fuera (endpoint de Loom) | La interfaz no tiene el botón |
| Recrear la base de datos de Cloud SQL | Fuera | Historial de migraciones de la corrida anterior |
| Sembrar las cuentas de prueba | Fuera (SQL) | El código generado no incluye gestión de usuarios |

Como referencia, en la segunda etapa del piloto (19 y 20 de septiembre) hubo seis Pull Requests manuales para corregir defectos del código generado que impedían arrancar la aplicación o pasar el CI (registro de hallazgos, apartado A). En esta corrida no hizo falta ninguno. La plataforma cambió entre ambas etapas, entre otras cosas con las compuertas de ejecución previas al Pull Request, pero una sola comparación no permite atribuir la mejora a un cambio concreto.

### 5.2.8 Costo y uso del modelo

La corrida hizo 128 llamadas al modelo, con 2.15 millones de tokens de entrada y 0.52 millones de salida (además de 14.6 millones de tokens leídos de caché), y un costo nocional de 16.67 USD (Tabla 5.6). La generación de código concentra el 56 % del costo y el 65 % del tiempo de modelo. La revisión es barata (0.20 USD por paquete) frente a la generación (0.77 USD por paquete).

TABLA: Uso del modelo por skill
| Skill | Llamadas | Tokens de entrada | Tokens de salida | Tiempo de modelo (min) | Costo (USD) |
| Generar código | 15 | 855,897 | 387,314 | 53.3 | 9.27 |
| Revisar código | 12 | 528,048 | 24,550 | 5.5 | 2.44 |
| Pruebas de humo | 81 | 311,216 | 34,958 | 10.6 | 2.19 |
| Corregir código | 3 | 155,788 | 16,142 | 2.6 | 0.95 |
| Descomponer | 10 | 146,207 | 23,826 | 4.5 | 0.90 |
| Arquitectura | 1 | 53,454 | 12,504 | 2.0 | 0.34 |
| Generar casos de prueba | 3 | 46,488 | 10,407 | 1.7 | 0.31 |
| Leer y especificar HUs | 3 | 49,121 | 6,782 | 1.4 | 0.28 |
| Total | 128 | 2,146,219 | 516,483 | 81.6 | 16.67 |

### 5.2.9 Lo que la corrida no permite concluir

La corrida muestra que el flujo se puede completar de punta a punta con una intervención mínima, que las compuertas y la regla de integración continua impidieron fusionar código roto y que las pruebas de humo encuentran omisiones reales de la aplicación. No permite todavía responder las preguntas de investigación centrales. Para la hipótesis H1 faltan la corrida con una revisión que solo recibe el *diff* y la valoración, por una persona y a ciegas, de la relevancia de las observaciones. Para H2 falta el segundo Proyecto (IAT), con el que se probaría que solo cambia la configuración. Para H3 falta la corrida equivalente con Gemini y la misma medición. Estos tres conjuntos de datos son el trabajo pendiente del capítulo.
