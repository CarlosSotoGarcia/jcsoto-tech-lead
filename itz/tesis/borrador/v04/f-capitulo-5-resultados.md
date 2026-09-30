@@ tesis_5_1
### 5.1.1 Alcance de las corridas

Este capítulo reporta dos corridas completas, una por cada proyecto del capítulo 4, hechas con «Claude (cuenta normal)» como proveedor de IA, que usa el CLI de Claude Code con una suscripción. La corrida E1c se hizo el 21 de septiembre de 2026 sobre el Proyecto de inventarios (P1) y la corrida E3c, el 26 y 27 de septiembre sobre el Proyecto de agenda de un taller mecánico (P2). Las dos partieron de un Proyecto sin datos previos (repositorio de GitHub reducido a su README inicial y colecciones de Mongo vacías), procesaron las tres primeras HUs del sprint de su backlog en Jira y recorrieron las cuatro fases.

Los dos proyectos se eligieron de dominios distintos y Loom generó para cada uno un stack distinto: Java con Spring Boot y Angular en P1, y Node con NestJS y Prisma y React con Vite en P2. Esa diferencia es la que permite observar la generalización del flujo (PI3), aunque con las reservas del apartado 5.1.4.

Del diseño experimental del capítulo 4 no se ejecutó ningún escenario con las APIs de los proveedores (Tabla 5.1): al momento de las corridas, la API de Anthropic no tenía saldo y la de Gemini tenía la facturación bloqueada. E1c y E3c son pilotos completos con el CLI; no comparan proveedores ni condiciones de contexto. Para H1 se hizo después un experimento de control sobre los Pull Requests de las dos corridas (apartado 5.2.14), evaluado de forma automática; H3 sigue sin evaluarse y H2 solo se evalúa en parte (apartado 5.2.16).

TABLA: Escenarios del diseño experimental y estado
| Escenario | Proyecto | Proveedor de IA | Estado |
| E1 | P1, inventarios | Claude por API | No ejecutado (sin saldo en la API) |
| E1c | P1, inventarios | Claude por CLI, claude-sonnet-5 | Ejecutado el 2026-09-21 |
| E2 | P1, inventarios | Gemini por API | Corrida parcial previa, no comparable |
| E3 | P2, agenda de taller | Claude por API | Configurado, no ejecutado (sin saldo en la API) |
| E3c | P2, agenda de taller | Claude por CLI, claude-opus-5-5 | Ejecutado el 2026-09-26 y 27 |
| E4 | P2, agenda de taller | Gemini por API | Configurado, no ejecutado (facturación bloqueada) |
| C (control de la revisión) | P1 y P2, 29 Pull Requests de E1c y E3c | Claude por CLI, claude-sonnet-5 fijado | Ejecutado el 2026-09-27 y 28; evaluación automática el 2026-09-29; calificación por una persona pendiente |

### 5.1.2 Procedimiento

La persona investigadora operó Loom desde su interfaz web con un guion de Playwright que pulsa los mismos botones que usaría una persona y guarda una captura de cada paso; el Anexo C reproduce el recorrido de E1c con las pantallas y el Anexo D resume el de E3c. En las dos corridas cada acción se ejecutó en este orden: leer las tres HUs, generar los casos de prueba, generar y aprobar la arquitectura, descomponer en paquetes, y por cada paquete generar el código, hacer una sola revisión y aceptar el Pull Request. Con el último paquete fusionado se generó y publicó el despliegue, se ejecutó el release en Google Cloud y se corrieron las pruebas de humo de las tres HUs.

Se fijaron las mismas reglas en las dos corridas. La primera es una sola revisión por paquete: el Pull Request se acepta aunque queden observaciones, para medir qué encuentra la revisión y no cuánto tarda en converger. La segunda es que Loom conserva sus propias reglas de fusión (integración continua en verde, dependencias resueltas), sin saltárselas; cuando el CI quedó en rojo se aplicó una corrección. Las decisiones sobre los supuestos de las HUs las redactó el equipo como política del piloto.

### 5.1.3 Instrumentos y fuentes de datos

Los datos provienen de tres fuentes. De MongoDB, las colecciones de procesos (duración y estado de cada ejecución), paquetes, revisiones (observaciones con fuente y severidad), métricas (llamadas al modelo con tokens, duración y costo; compuertas de ejecución y reintentos) y pruebas de humo. De la API de GitHub, el estado de los Pull Requests y de los *checks* de integración continua. De las capturas de pantalla, el registro visual de cada paso. Cada corrida tiene además una bitácora con la hora de cada hallazgo y de cada intervención. El costo es el que informa el CLI de Claude; al usarse con una suscripción, es nocional y no comparable con la facturación de una API.

### 5.1.4 Amenazas a la validez de estas corridas

Cada proyecto tiene una sola corrida, con un solo evaluador, de modo que la variabilidad entre corridas no está medida. Las dos corridas no usaron el mismo modelo: Loom no fija el modelo del CLI, que tomó el predeterminado de Claude Code, `claude-sonnet-5` en E1c y `claude-opus-5-5` (con `claude-haiku-4-5` para subtareas) en E3c. Por eso las diferencias de costo y de calidad entre E1c y E3c no se pueden atribuir al proyecto. La plataforma tampoco estuvo congelada: E3c encontró supuestos de Loom que no generalizaban y se corrigieron durante la corrida (apartado 5.2.12), así que E1c y E3c no corrieron sobre la misma versión.

Los tiempos dependen de la máquina, de la red y de la carga del proveedor; el límite de sesión de la suscripción cortó una generación en E1c y cuatro procesos en E3c, que se repitieron. La persona que operó el sistema es también quien lo construyó, lo que favorece el conocimiento de sus puntos débiles. Las observaciones de la revisión no se valoraron todavía como relevantes o no, por lo que solo se reporta cuántas hay y de qué tipo. Por último, varias acciones de entorno se hicieron fuera de la interfaz de Loom (Tablas 5.5 y 5.11), y sus efectos no se cuentan como resultado del sistema.

@@ tesis_5_2
### 5.2.1 Primer proyecto (E1c): ejecución de punta a punta

Los apartados 5.2.1 a 5.2.8 reportan la corrida E1c; los apartados 5.2.9 a 5.2.13, la corrida E3c y la comparación entre ambas. En E1c el flujo se completó con las tres HUs: 12 paquetes de trabajo fusionados, la aplicación desplegada en Cloud Run y 44 casos de prueba ejecutados contra ella. La Tabla 5.2 resume el tiempo de reloj de cada etapa. La plataforma trabajó unos 113 minutos, sin contar la espera de la integración continua ni el proceso de descomposición que falló.

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


### 5.2.9 Segundo proyecto (E3c): ejecución de punta a punta

En E3c el flujo también se completó con las tres HUs (IAT-2, autorregistro de cliente; IAT-3, inicio y cierre de sesión; IAT-4, recuperación de contraseña): 17 paquetes fusionados, la aplicación desplegada en Cloud Run y 101 casos de prueba ejecutados contra ella. La Tabla 5.7 resume cada etapa con la duración de sus procesos en Loom. La generación de código fue la etapa más larga y la única que el límite de sesión de la suscripción interrumpió: tres generaciones se cortaron y se repitieron.

TABLA: Etapas de la corrida E3c
| Etapa | Resultado | Tiempo (min) |
| Leer y especificar 3 HUs | 3 HUs, todas con supuestos por confirmar | 1.9 |
| Generar casos de prueba | 101 casos (35, 39 y 27) | 4.7 |
| Generar la arquitectura | 7 entidades, 8 decisiones, 10 preguntas abiertas | 1.5 |
| Descomponer en paquetes | 17 paquetes en 4 grupos, al primer intento | 3.0 |
| Generar el código de los 17 paquetes | 17 Pull Requests abiertos | 185.2 |
| Revisar los 17 paquetes | 17 revisiones | 13.6 |
| Ejecutar el release en Google Cloud | Correcto al tercer lanzamiento manual, tras cuatro automáticos fallidos | 9.5 |
| Pruebas de humo de las 3 HUs (corrida final de cada HU) | 68 aprobados, 9 fallidos, 24 bloqueados | 63.7 |

El tiempo de generación suma los 16 procesos que terminaron; no incluye los intentos cortados ni la espera de la integración continua. El release corresponde al intento que terminó bien.

La especificación produjo más del doble de casos de prueba que en E1c (101 contra 44) para el mismo número de HUs, y la descomposición, cinco paquetes más (17 contra 12), en este caso sin fallar. Como el modelo también cambió (apartado 5.1.4), esas diferencias no se pueden atribuir solo al dominio.

### 5.2.10 Revisión, compuertas y corrección en E3c

Las 17 primeras revisiones aprobaron siete paquetes y dejaron diez con observaciones (Tabla 5.8). Sumaron 59 observaciones, ninguna bloqueante, 10 mayores y 49 menores, con un promedio de 3.5 por paquete, menor que en E1c. Por fuente, predominan las de buenas prácticas (22), seguidas por arquitectura (11), pruebas (10), seguridad (9) y criterios de aceptación (7).

TABLA: Primera revisión de cada paquete de E3c
| Paquete | Veredicto | Observaciones | Mayores | Menores | PR |
| BASE/PT-01 | Aprobado | 4 | 0 | 4 | #1 |
| BASE/PT-02 | Aprobado | 4 | 0 | 4 | #2 |
| BASE/PT-03 | Con observaciones | 3 | 1 | 2 | #3 |
| BASE/PT-04 | Con observaciones | 3 | 1 | 2 | #4 |
| BASE/PT-05 | Aprobado | 6 | 0 | 6 | #5 |
| HU-001/PT-01 | Con observaciones | 4 | 1 | 3 | #6 |
| HU-001/PT-02 | Con observaciones | 5 | 1 | 4 | #7 |
| HU-001/PT-03 | Con observaciones | 2 | 1 | 1 | #8 |
| HU-001/PT-04 | Aprobado | 3 | 0 | 3 | #9 |
| HU-002/PT-01 | Con observaciones | 7 | 1 | 6 | #10 |
| HU-002/PT-02 | Con observaciones | 5 | 1 | 4 | #11 |
| HU-002/PT-03 | Aprobado | 3 | 0 | 3 | #12 |
| HU-002/PT-04 | Con observaciones | 3 | 1 | 2 | #13 |
| HU-003/PT-01 | Con observaciones | 3 | 1 | 2 | #14 |
| HU-003/PT-02 | Con observaciones | 1 | 1 | 0 | #15 |
| HU-003/PT-03 | Aprobado | 0 | 0 | 0 | #16 |
| HU-003/PT-04 | Aprobado | 3 | 0 | 3 | #17 |

La diferencia más importante con E1c no está en la revisión sino en la compuerta de ejecución. En E3c la compuerta de compilación, análisis estático y pruebas no se ejecutó nunca: sus 21 registros son «omitida». La compuerta busca el `package.json` de cada capa en la carpeta de la capa y luego en la raíz; en este monorepo con *workspaces* encontró el `package.json` raíz, que no tiene `tsconfig.json`, y concluyó que no sabía compilar, sin revisar `apps/backend` ni `apps/frontend`. La compuerta de archivos obligatorios sí actuó: rechazó cuatro veces una entrega de los paquetes BASE/PT-02 y BASE/PT-04 por archivos faltantes, y el agente los completó.

Sin la compuerta, dos defectos llegaron hasta la integración continua de GitHub: una prueba de Vitest en rojo en HU-001/PT-04, un paquete que la revisión había aprobado, y una prueba de Jest en rojo en HU-002/PT-02. Loom no dejó fusionar ninguno de los dos. En los dos casos la corrección que resolvió el CI fue la que recibe el extracto del registro del CI (ADR-0078), disponible dentro de la acción «avanzar HU». La corrección del botón de la interfaz, que aplica solo las observaciones de la revisión, no resolvió la prueba de HU-002/PT-02, y para un paquete «Aprobado» la interfaz no ofrece corrección. En HU-002/PT-02, además, «avanzar HU» volvió a revisar el paquete antes de corregirlo, así que ese paquete tuvo tres revisiones en lugar de una. Con todo, las 19 revisiones de la corrida sumaron 69 observaciones (12 mayores y 57 menores).

### 5.2.11 Despliegue y validación funcional en E3c

El release automático, que Loom lanza al completarse el esqueleto y cada HU, falló las cuatro veces: suponía `backend/` y `frontend/` en la raíz del repositorio y no encontró los servicios. Con ese supuesto corregido (ADR-0086), el primer lanzamiento manual construyó las imágenes, pero el backend no arrancó: Prisma exige una cadena de conexión `DATABASE_URL` que el release solo entregaba en formato JDBC, para Java. El segundo, con esa cadena y con las variables de entorno del Proyecto ajustadas a las que exige el código generado, desplegó los dos servicios, pero el frontend quedó apuntando a su propio dominio porque fija la dirección de la API al compilar. El tercero, con esa dirección como argumento de construcción (ADR-0087), dejó la aplicación funcionando en 9.5 minutos. Loom registró como «terminados» los cuatro lanzamientos automáticos aunque habían fallado; el fallo solo quedó en el resultado del release del Proyecto.

Las pruebas de humo de la HU-001 se corrieron tres veces. Las dos primeras dejaron 33 de 35 casos bloqueados por «no hay cuenta de prueba para el rol»: los casos de E3c usan 32 roles distintos, escritos en texto libre («invitado (sin sesión); admin para verificar», «cliente_bloqueable», «personal_interno»…), y Loom buscaba la cuenta por el nombre exacto entre las tres configuradas. La segunda corrida repitió el resultado porque el backend de Loom no había recargado el cambio. Con la asignación por actor principal (ADR-0088) y una cuenta de prueba por cada rol que usan los casos, la tercera dio 28 aprobados, 4 fallidos y 3 bloqueados. La Tabla 5.9 resume la corrida final de cada HU.

TABLA: Resultado de las pruebas de humo de E3c por HU
| HU | Casos | Aprobados | Fallidos | Bloqueados | Duración (min) |
| HU-001, autorregistro | 35 | 28 | 4 | 3 | 17.8 |
| HU-002, inicio y cierre de sesión | 39 | 19 | 4 | 16 | 34.7 |
| HU-003, recuperación de contraseña | 27 | 21 | 1 | 5 | 11.2 |
| Total | 101 | 68 | 9 | 24 | 63.7 |

Los nueve fallos son omisiones de la aplicación generada. Recepción no tiene la sección de clientes que piden los criterios, el administrador no tiene módulo de auditoría, entrar a `/login` con sesión iniciada no redirige a la pantalla inicial, el personal interno puede abrir la pantalla de vehículos del cliente, y no hay documentación de la API publicada. La ausencia de una bitácora visible para el administrador es la misma omisión que produjo los dos fallos de E1c.

Los 24 bloqueos tienen tres causas. La primera es el orden de los casos: la cuenta preparada para probar el bloqueo por intentos fallidos quedó bloqueada por los primeros casos y arrastró a los siguientes (HU-002). La segunda son casos que el agente de navegador no puede montar, como esperar 25 o 30 minutos de inactividad o medir tiempos de 40 peticiones a la API. La tercera son precondiciones que dependen del correo, como abrir un enlace de verificación o de restablecimiento que el ambiente no permite leer.

### 5.2.12 Lo que cambió en Loom para el segundo proyecto

E3c es la primera evidencia de generalización del flujo: la misma plataforma, con las mismas *skills*, completó el ciclo en un segundo dominio y en un segundo stack. No lo hizo solo con cambios de configuración. Cuatro supuestos de Loom estaban atados a la forma del primer proyecto (Tabla 5.10): tres se corrigieron durante la corrida, cada uno con su registro de decisión, y el cuarto, la compuerta de compilación, sigue abierto.

TABLA: Supuestos de Loom que no generalizaron en E3c
| Supuesto | Efecto en E3c | Corrección |
| El release busca `backend/` y `frontend/` en la raíz y construye cada uno desde su carpeta | El release automático falló al completarse cada HU | ADR-0086: busca también en `apps/`, `packages/` y `services/`, y construye desde la raíz con `-f` cuando el Dockerfile lo pide |
| La base de datos se entrega en variables sueltas y en JDBC; la URL de la API llega al frontend en tiempo de ejecución | El backend no arrancó y el frontend apuntaba a su propio dominio | ADR-0087: `DATABASE_URL` como secreto para stacks que no son Java y URL de la API como *build-arg* |
| El rol de cada caso de prueba coincide con el nombre de una cuenta configurada | 33 de 35 casos bloqueados en HU-001 | ADR-0088: se asigna la cuenta por el actor principal del rol; se configuraron cuentas por rol |
| La compuerta de compilación encuentra el proyecto de cada capa en su carpeta o en la raíz | La compuerta no se ejecutó nunca | Abierto |

A la configuración del Proyecto también hubo que ajustarle las variables de entorno del backend (`JWT_ACCESS_SECRET` y `FRONTEND_URL`), que se habían escrito por analogía con E1c antes de que existiera el código, y sembrar las cuentas de prueba con el propio *seed* de la aplicación, que el contenedor no ejecuta al arrancar. La Tabla 5.11 reúne las intervenciones hechas fuera de la interfaz de Loom. Ninguna editó el código generado.

TABLA: Intervenciones fuera de la interfaz de Loom en E3c
| Intervención | Causa |
| «Avanzar HU» llamado por la API en dos paquetes, y cancelado a mano en uno de ellos | La interfaz no ofrece corregir con el registro del CI en esos estados |
| Fusión del Pull Request de despliegue por su *endpoint* | La interfaz no tiene el botón |
| *Seed* de la aplicación contra Cloud SQL y dos cambios de estado de cuenta por SQL | Cuentas de prueba por rol |
| Corrección de Loom (ADR-0086, 0087 y 0088) y reinicios de su backend | Supuestos que no generalizaron |
| Repetir los procesos cortados por el límite de sesión | Entorno (suscripción del CLI) |

### 5.2.13 Comparación de las dos corridas

La Tabla 5.12 pone lado a lado las cifras principales. Sirve para ver la forma de cada corrida, no para comparar calidad, porque el modelo y la versión de la plataforma cambiaron entre ellas.

TABLA: Cifras principales de E1c y E3c
| Cifra | E1c (P1, inventarios) | E3c (P2, agenda de taller) |
| Stack generado | Java con Spring Boot y Angular | Node con NestJS y Prisma, React con Vite |
| Modelo | claude-sonnet-5 | claude-opus-5-5 y claude-haiku-4-5 |
| Casos de prueba | 44 | 101 |
| Paquetes fusionados | 12 | 17 |
| Observaciones de la primera revisión | 66 (2 bloqueantes, 24 mayores, 40 menores) | 59 (10 mayores, 49 menores) |
| Paquetes con el CI en rojo | 1 | 2 |
| Compuerta de compilación | Ejecutada en 10 de 12 paquetes | No se ejecutó |
| Lanzamientos de release hasta desplegar | 2 manuales (y 1 automático fallido) | 3 manuales (y 4 automáticos fallidos) |
| Pruebas de humo (aprobados, fallidos, bloqueados) | 36, 2, 6 de 44 | 68, 9, 24 de 101 |
| Llamadas al modelo | 128 | 532 |
| Costo nocional informado por el CLI (USD) | 16.67 | 120.99 |

FIGURA: graficas/g5-4-smoke-e1c-e3c.png | Resultado de las pruebas de humo de E1c y E3c, en porcentaje de casos

Tres rasgos se repiten en las dos corridas. Primero, lo que la revisión no ve aparece al ejecutar: en E1c, la compuerta y el CI detuvieron un paquete y las pruebas de humo encontraron una bitácora ausente; en E3c, el CI detuvo dos paquetes y las pruebas de humo encontraron nueve omisiones. Segundo, el despliegue es la etapa más frágil: ninguna de las dos corridas desplegó al primer intento, y en ambas el motivo estuvo fuera del código de las HUs (una base de datos con migraciones previas en E1c, supuestos del release en E3c). Tercero, la mayoría de los bloqueos de las pruebas de humo se deben a datos y precondiciones que el ambiente no ofrece, no a la aplicación.

La diferencia de costo (16.67 contra 120.99 USD nocionales) se explica en buena parte por el modelo: E3c corrió con Opus 5.5, y además sus pruebas de humo de la HU-001 se repitieron tres veces. El capítulo 4 prevé medir el costo con la API y con el modelo fijado; con estas corridas solo se puede decir que el mismo flujo, en proyectos de tamaño parecido, puede costar un orden de magnitud más según el modelo que lo ejecute.

### 5.2.14 Revisión con contexto frente a solo el *diff* (experimento C)

El experimento de control del apartado 4.1.7 se corrió entre el 27 y el 28 de septiembre de 2026: 58 revisiones, dos por cada uno de los 29 Pull Requests, con `claude-sonnet-5`. El modelo ocupó 92.4 minutos en la condición con contexto y 100.0 en la de solo el *diff*, con una entrada media de 121,611 y 76,529 caracteres. Tres *diffs* de E3c superaron el tope de 140,000 caracteres y se recortaron igual en las dos condiciones. La corrida se interrumpió tres veces, dos por el límite de sesión de la suscripción y una por un fallo de red con la API de GitHub, y se reanudó sin repetir las revisiones ya guardadas.

TABLA: Observaciones por condición antes de calificarlas
| Cifra | Con contexto | Solo el diff |
| Observaciones | 85 | 92 |
| Bloqueantes, mayores y menores | 7, 21 y 57 | 2, 21 y 69 |
| Fuente: criterio de aceptación | 13 | 0 |
| Fuente: arquitectura | 19 | 15 |
| Fuente: buenas prácticas | 39 | 50 |
| Fuente: pruebas | 9 | 7 |
| Fuente: seguridad | 5 | 20 |
| Pull Requests sin observaciones | 0 | 0 |
| Costo nocional informado por el CLI (USD) | 14.81 | 11.39 |

La Tabla 5.13 describe qué produjo cada condición, no cuál revisó mejor. Con contexto hubo menos observaciones (85 contra 92) y más bloqueantes (7 contra 2). Las 13 observaciones sobre criterios de aceptación no tienen contraparte en la condición de control, que no conoce esos criterios. Sin contexto, el modelo dedicó más observaciones a seguridad (20 contra 5) y a buenas prácticas (50 contra 39). Nada de esto dice qué condición encuentra más problemas reales: una observación de seguridad puede ser un hallazgo o ruido, y una bloqueante puede ser falsa. Lo decide la calificación de las 177 observaciones, que se reporta más abajo.

La primera ejecución de la condición con contexto se descartó. Tomó el paquete de trabajo de la base de datos, donde Loom lo regenera después de cada revisión con las observaciones de la última ronda y el estado final del paquete, así que el revisor recibió en su entrada observaciones que el piloto ya había hecho. El problema se detectó al armar la hoja de calificación, antes de calificar, y la condición se repitió con el paquete reconstruido desde el historial del repositorio de control. La ejecución descartada había producido 123 observaciones, 38 más que la válida; no se analizó cuántas de ellas repetían las del piloto. Queda registrada, con su costo de 12.90 USD nocionales, y fuera del análisis. La lección es de método: un experimento retrospectivo sobre un sistema que actualiza sus artefactos tiene que reconstruir las entradas desde el historial de versiones.

La calificación la hizo un modelo distinto del revisor, `claude-opus-5-5`, a ciegas y con la rúbrica de cuatro categorías (apartado 4.1.7). Calificó las 177 observaciones en 29 llamadas, una por Pull Request, en 11.7 minutos. La Tabla 5.14 y la Figura 5.4 muestran el resultado.

TABLA: Calificación automática de las observaciones por condición
| Calificación | Con contexto | Solo el diff |
| Relevante y correcta | 24 (28.2 %) | 21 (22.8 %) |
| Relevante pero mal sustentada | 4 (4.7 %) | 7 (7.6 %) |
| Ruido | 45 (52.9 %) | 53 (57.6 %) |
| Falsa | 12 (14.1 %) | 11 (12.0 %) |
| Total | 85 | 92 |
| Relevantes en sentido amplio | 28 (32.9 %) | 28 (30.4 %) |

FIGURA: graficas/g5-5-experimento-c-calificacion-automatica.png | Calificación automática de las observaciones del experimento C por condición

La evaluación automática no encuentra evidencia a favor de H1. Las dos condiciones produjeron el mismo número de observaciones relevantes, 28, y la proporción es algo mayor con contexto (32.9 % frente a 30.4 %) porque esa condición hizo menos observaciones. En la comparación pareada, el contexto dio más observaciones relevantes en 7 Pull Requests, menos en otros 7 y las mismas en 15; la prueba de Wilcoxon da p = 1.0 y un tamaño del efecto de 0. Con el criterio estricto la diferencia favorece al contexto (28.2 % frente a 22.8 %; 8 Pull Requests contra 6, con 15 empates), y tampoco es significativa (p = 0.47; correlación rango-biserial de 0.2). Por proyecto el patrón es el mismo: en E1c, 18 de 44 observaciones relevantes con contexto y 17 de 49 sin él; en E3c, 10 de 41 y 11 de 43.

Hay un resultado que pesa más que la comparación. En las dos condiciones, cerca de dos de cada tres observaciones no ameritan un cambio: más de la mitad se calificaron como ruido y alrededor de una de cada ocho como falsa. En 7 de los 29 Pull Requests ninguna de las dos revisiones produjo una observación relevante.

El contexto no aumentó la proporción de observaciones relevantes, pero sí cambió cuáles son (Tabla 5.15). Seis de las 28 observaciones relevantes con contexto señalan incumplimientos de criterios de aceptación, una fuente que la revisión sin contexto no puede usar. Sin contexto, la revisión encontró más problemas de seguridad relevantes (12 frente a 5), aunque con más ruido alrededor: necesitó 20 observaciones de seguridad para 12 relevantes, mientras que las 5 de la otra condición lo fueron todas. De las observaciones bloqueantes resultaron válidas 4 de las 7 con contexto y 1 de las 2 sin él; de las mayores, 12 de 21 y 13 de 21.

TABLA: Observaciones relevantes por la fuente que les asignó el revisor
| Fuente | Con contexto (relevantes de total) | Solo el diff (relevantes de total) |
| Criterio de aceptación | 6 de 13 | 0 de 0 |
| Arquitectura | 5 de 19 | 5 de 15 |
| Buenas prácticas | 11 de 39 | 10 de 50 |
| Pruebas | 1 de 9 | 1 de 7 |
| Seguridad | 5 de 5 | 12 de 20 |

Las dos revisiones encuentran, además, problemas distintos. El calificador marcó 18 pares de observaciones como equivalentes entre condiciones, y solo en 9 de ellos las dos son relevantes. De las 28 observaciones relevantes de cada condición, 19 no tienen equivalente en la otra: entre las dos revisiones suman 47 hallazgos relevantes distintos, y cada una ve 28. Revisar con contexto no sustituyó a revisar sin él; las dos revisiones se complementaron.

El experimento tiene límites propios. El mayor es el calificador: la relevancia la juzgó un modelo de la misma familia que el revisor, y no una persona. El apartado 2.9 describe los sesgos de ese tipo de juez, y todavía no hay una calificación humana para medir cuánto coincide con él, de modo que el resultado debe leerse como una evaluación automática preliminar. Además, cada condición se ejecutó una sola vez y la variabilidad del modelo no está medida. Las revisiones se hicieron sobre código que generaron otros modelos (Sonnet 5 en E1c, Opus 5.5 en E3c), y por eso sus observaciones no sustituyen a las de los pilotos. Por último, una búsqueda de términos encontró que 50 de las 177 observaciones mencionan la HU, sus criterios, los casos de prueba o la arquitectura (35 de la condición con contexto y 15 de la de control), lo que puede sugerir su origen a quien las califica, sea un modelo o una persona.

### 5.2.15 Cobertura de los criterios de aceptación por los casos de prueba

PI1 pregunta en qué medida los casos de prueba generados cubren los criterios de aceptación de una HU. Cada caso guarda el texto del criterio del que deriva, y con esa referencia se contó, para las seis HUs de las dos corridas, cuántos criterios tienen al menos un caso (Tabla 5.16).

TABLA: Cobertura de los criterios de aceptación por HU
| Proyecto y HU | Criterios explícitos (cubiertos) | Criterios inferidos (cubiertos) | Casos de prueba | Criterios con más de un caso |
| E1c, HU-001 | 2 (2) | 11 (11) | 14 | 1 |
| E1c, HU-002 | 2 (2) | 12 (12) | 14 | 0 |
| E1c, HU-003 | 3 (3) | 9 (9) | 16 | 4 |
| E3c, HU-001 | 10 (10) | 16 (16) | 35 | 8 |
| E3c, HU-002 | 9 (9) | 14 (14) | 39 | 14 |
| E3c, HU-003 | 7 (7) | 15 (15) | 27 | 4 |
| Total | 33 (33) | 77 (77) | 145 | 31 |

Los 110 criterios quedaron cubiertos, y ninguno de los 145 casos apunta a un criterio que no exista en su HU. En todos, la referencia reproduce el texto del criterio de forma exacta. Loom no obliga a ese resultado. La *skill* entrega al modelo la lista de criterios y le pide al menos un caso por cada uno, pero después no comprueba que todos estén cubiertos. La cobertura completa es un comportamiento del modelo en estas seis HUs y no una garantía del sistema. En E3c, que corrió con otro modelo, los casos por criterio fueron más (1.42 en promedio, frente a 1.13 en E1c) y 26 de sus 71 criterios tienen más de un caso.

El dato tiene tres límites. Mide que cada criterio tiene un caso, no que el caso lo verifique bien; esa suficiencia es la que mide la rúbrica humana del apartado 4.1.5, que todavía no se aplica. Además, 77 de los 110 criterios (70 %) los infirió la *skill* 1 y no venían en la fuente, y en E1c fueron 32 de 39. La cobertura se mide, en buena parte, contra criterios que escribió el propio sistema, y nadie ha valorado aún si esos criterios inferidos son los que el negocio habría pedido. Por último, los 50 supuestos que las seis HUs dejaron abiertos no son criterios y quedan fuera de la cuenta.

Cubrir un criterio tampoco equivale a verificarlo en la aplicación. De los 145 casos, las pruebas de humo aprobaron 104, reprobaron 11 y dejaron 30 bloqueados (apartados 5.2.6 y 5.2.11); un criterio cuyo único caso quedó bloqueado está cubierto y sin comprobar.

### 5.2.16 Lo que las corridas no permiten concluir

Las dos corridas muestran que el flujo completa el ciclo de punta a punta en dos proyectos de dominios y stacks distintos, que la regla de integración continua impidió fusionar código roto y que las pruebas de humo encuentran omisiones reales de la aplicación. No permiten todavía responder las preguntas de investigación centrales. PI1 tiene respuesta en su sentido nominal: todos los criterios tienen al menos un caso de prueba (apartado 5.2.15), y falta valorar si esos casos son suficientes. Para la hipótesis H1, la revisión de control y su evaluación automática no muestran una ventaja del contexto en la proporción de observaciones relevantes (apartado 5.2.14); falta que una persona las califique a ciegas para confirmarlo o corregirlo. Para H2 hay evidencia parcial: el ciclo se completó en el segundo proyecto, pero no solo con cambios de configuración, y la compuerta de compilación sigue sin generalizar. Para H3 faltan las corridas equivalentes con las APIs de Claude y de Gemini, con el modelo fijado y la plataforma congelada. Estos conjuntos de datos son el trabajo pendiente del capítulo.
