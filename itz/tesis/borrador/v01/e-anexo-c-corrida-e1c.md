@@ tesis_anexos+
CAPITULO: C
### Anexo C. Recorrido de la corrida piloto E1c en Loom, paso a paso

Este anexo documenta, con las pantallas de Loom, una corrida completa del escenario E1c (Proyecto de inventarios de un instituto tecnológico, con Claude por CLI con cuenta personal como proveedor de IA), realizada el 21 de septiembre de 2026 desde un Proyecto sin datos previos: el repositorio de GitHub estaba reducido a su README inicial y las colecciones de Mongo del Proyecto estaban vacías. La corrida cubre tres HUs del backlog de Jira (ITZINV-12, ITZINV-13 e ITZINV-14, que Loom nombra HU-001, HU-002 y HU-003) y recorre las cuatro fases, con una sola revisión por paquete y aceptación del Pull Request. Salvo donde se indica lo contrario, cada acción se ejecutó desde la interfaz de Loom mediante un guion de Playwright que pulsa los mismos botones que usaría una persona y guarda una captura por paso. Los guiones, los registros de la ejecución y las 275 capturas originales están en `itz/tesis/evidencia/corrida-E1c-2026-09-21/`.

### C.1 Fase 1: lectura y especificación de las HUs

El Proyecto parte de la ruta sin ninguna fase ejecutada. Desde la lista de HUs de Jira se eligieron las tres primeras historias del sprint y se procesaron sin usar el resto del sprint (33 historias).

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/01-proyecto-limpio-ruta-del-proyecto.png | Proyecto E1c sin ninguna fase ejecutada: la Fase 1 está lista para correr

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/02-fase1-seleccion-de-3-hus.png | Selección de las tres HUs de Jira que se van a procesar

Al procesar la selección, el panel de actividad muestra el avance en vivo. Loom analizó cada historia, la clasificó como HU y escribió su especificación en 1 min 24 s. Las tres quedaron marcadas «Con supuestos», es decir, con puntos que una persona debe confirmar.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/03-fase1-en-ejecucion-panel-actividad.png | La Fase 1 en ejecución: registro en vivo en el panel de actividad

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/04-fase1-terminada-ruta.png | Fase 1 completa: tres HUs especificadas, con supuestos por confirmar

La especificación de cada HU reúne la descripción, los criterios de aceptación explícitos, los inferidos por el modelo y los supuestos identificados.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/06b-HU-001-especificacion.png | Especificación generada para la HU-001

### C.2 Fase 2: casos de prueba y arquitectura

Con las tres HUs especificadas, Loom generó los casos de prueba en formato Given/When/Then en 1 min 45 s: 14 casos para la HU-001, 14 para la HU-002 y 16 para la HU-003.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/07-fase2-casos-de-prueba-terminado.png | Generación de casos de prueba terminada para las tres HUs

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/07b-HU-001-casos-de-prueba.png | Casos de prueba de la HU-001

A continuación se generó la arquitectura base del Proyecto (1 min 58 s). El resultado fue un monolito modular de Spring Boot y Angular en un monorepo, con 5 entidades, 7 decisiones y 7 preguntas abiertas. La arquitectura queda pendiente hasta que una persona la apruebe.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/09-arquitectura-generada-pendiente-de-aprobar.png | Arquitectura generada, pendiente de aprobación

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/10-documento-de-arquitectura.png | Documento de arquitectura generado, versionado en el repositorio de control

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/11-arquitectura-aprobada.png | Arquitectura aprobada: habilita la descomposición en paquetes

### C.3 Fase 3: descomposición, decisiones sobre los supuestos y ciclo de los paquetes

La descomposición produce el esqueleto del aplicativo (grupo BASE) y los paquetes de cada HU. El primer intento falló: tras tres reintentos internos, el análisis no produjo ningún paquete para la HU-003 y el proceso terminó con error a los 2 min 28 s. Se volvió a ejecutar la descomposición, que esta vez terminó en 2 min 3 s con 12 paquetes en 4 grupos: 5 de BASE, 2 de la HU-001, 3 de la HU-002 y 2 de la HU-003.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/13-fase3-descomposicion-intento1-terminado.png | Primer intento de descomposición: falla en la HU-003 tras tres reintentos

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/13-fase3-descomposicion-intento2-terminado.png | Segundo intento de descomposición: 12 paquetes en 4 grupos

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/14b-HU-001-paquetes-de-trabajo.png | Paquetes de trabajo de la HU-001 con sus dependencias

Mientras una HU tenga supuestos sin confirmar, la revisión de código deja una observación bloqueante en cada Pull Request. Antes de generar código se registró una decisión por HU en la pantalla de decisiones pendientes. Las decisiones las redactó el equipo de investigación como política del piloto (por ejemplo, sesión de 30 minutos y bloqueo tras cinco intentos fallidos), y Loom las pasa al agente como requisitos.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/15-decisiones-pendientes-supuestos.png | Decisiones pendientes: supuestos que bloquean la revisión

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/15b-decisiones-escritas-hu-001.png | Decisión escrita para los supuestos de una HU

El ciclo de cada paquete se operó con la acción «Siguiente paquete» (genera el código con TDD, ejecuta las compuertas de compilación, análisis estático y pruebas unitarias en Docker, y abre el Pull Request), después «Revisar PRs» (una sola revisión) y, por último, «Aceptar el PR y fusionarlo». Las figuras siguientes muestran el ciclo completo del primer paquete, BASE/PT-01 (entorno de desarrollo dockerizado).

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/17-BASE-PT-01-generar-codigo-en-ejecucion.png | Generación de código de BASE/PT-01 en ejecución

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/17b-BASE-PT-01-paquete-en-revision.png | BASE/PT-01 con su Pull Request abierto, en revisión

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/18b-BASE-PT-01-resultado-de-la-revision.png | Resultado de la revisión: con observaciones (6)

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/19-BASE-PT-01-observaciones-de-la-revision.png | Observaciones de la revisión, con su severidad y su fuente

Con la política de una sola revisión, el Pull Request se acepta aunque queden observaciones. Loom pide confirmación y advierte cuántas observaciones quedan sin resolver.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/20-BASE-PT-01-confirmar-aceptar-pr.png | Confirmación de la fusión del Pull Request con observaciones pendientes

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/22-BASE-PT-01-fusionado.png | BASE/PT-01 fusionado

La tabla siguiente resume el ciclo de los doce paquetes. La generación de código tardó entre 1.0 y 14.7 minutos por paquete; cada revisión, entre 0.4 y 0.8 minutos.

TABLA: Resultado de la revisión de cada paquete de trabajo
| Paquete | Rondas de revisión | Observaciones | Mayores | Menores | PR |
| BASE/PT-01 | 1 | 6 | 3 | 3 | #32 |
| BASE/PT-02 | 1 | 2 | 0 | 2 | #33 |
| BASE/PT-03 | 1 | 4 | 1 | 3 | #34 |
| BASE/PT-04 | 1 | 6 | 3 | 3 | #35 |
| BASE/PT-05 | 1 | 9 | 4 | 5 | #36 |
| HU-001/PT-01 | 1 | 8 | 3 | 5 | #37 |
| HU-001/PT-02 | 1 | 5 | 1 | 4 | #38 |
| HU-002/PT-01 | 1 | 6 | 3 | 3 | #39 |
| HU-002/PT-02 | 1 | 6 | 1 | 5 | #40 |
| HU-002/PT-03 | 1 | 5 | 2 | 3 | #41 |
| HU-003/PT-01 | 1 | 2 | 0 | 2 | #42 |
| HU-003/PT-02 | 1 | 0 (tras la corrección) | 0 | 0 | #43 |

Tres situaciones se apartaron del ciclo previsto y quedan registradas como hallazgos de la corrida.

Primero, al aceptar BASE/PT-05, que incorpora el flujo de integración continua, Loom rechazó la fusión porque los *checks* de GitHub seguían corriendo (regla ADR-0076); se esperó a que terminaran en verde y se repitió la acción. En los paquetes siguientes el guion espera a los *checks* antes de pulsar el botón.

Segundo, la generación de HU-003/PT-02 falló en su primer intento porque el CLI de Claude alcanzó el límite de sesión de la suscripción («You've hit your session limit»); se reintentó al reiniciarse el límite.

Tercero, el Pull Request de HU-003/PT-02 tuvo un *check* de integración continua en rojo por una regla de análisis estático del frontend (prefijo del selector de un componente de Angular) que la compuerta local no detectó. Loom no dejó fusionarlo. Se aplicó una ronda de corrección desde la interfaz (6 min 13 s), el CI quedó en verde y se fusionó.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/34-HU-003-PT-02-con-observaciones-y-ci-rojo.png | HU-003/PT-02 con observaciones y la integración continua en rojo

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/35c-HU-003-PT-02-fusionado.png | HU-003/PT-02 fusionado tras la corrección

Con el último paquete fusionado, la Fase 3 quedó completa.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/36-fase3-completa-ruta-del-proyecto.png | Fase 3 completa: 12 de 12 paquetes fusionados

### C.4 Fase 4: liberación en la nube

La Fase 4 exige la configuración de despliegue del Proyecto. Se completaron los datos de identidad que Loom pide para armar el `release.py`: la cuenta de servicio desplegadora y el proveedor de Workload Identity Federation (recursos que ya existían en el proyecto de Google Cloud de la corrida anterior). Después se generó el `release.py` y el flujo de trabajo de GitHub Actions, y se publicaron en un Pull Request.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/37-fase4-configuracion-de-despliegue-service-account-y-wif.png | Configuración de despliegue: cuenta de servicio y proveedor de identidad

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/38c-fase4-pr-publicado.png | Pull Request con los archivos de despliegue publicado desde Loom

El release automático, que Loom lanza al fusionarse el último paquete de una HU, falló en esa primera ocasión con un error 422 de GitHub, porque el flujo de trabajo de release todavía no estaba en el repositorio. La interfaz de Loom no tiene un botón para fusionar el Pull Request de despliegue, por lo que se fusionó con el *endpoint* correspondiente de Loom, que aplica la misma regla de integración continua en verde. Con el archivo ya en la rama principal, el release se lanzó con el botón «Ejecutar release».

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/39-fase4-ejecutar-release-confirmacion.png | Confirmación de la ejecución del release en Google Cloud

El primer release construyó las imágenes, pero el backend no arrancó en Cloud Run: la base de datos de Cloud SQL conservaba el historial de migraciones de la corrida anterior y Flyway detectó que las migraciones de esta corrida tenían una suma de verificación distinta. Con autorización de la persona responsable se recreó la base de datos `inventarios` y se relanzó el release, que esta vez terminó bien en 8 min 33 s.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/39c-fase4-release-terminado.png | Release terminado y registrado en el Proyecto

Para las pruebas de humo hicieron falta dos ajustes fuera de Loom: se registró la dirección del frontend desplegado como URL del ambiente de desarrollo (desde el formulario de Loom) y se sembraron en la base de datos las tres cuentas de prueba (administrador, usuario final y usuario inactivo), porque el código generado en esta corrida no incluye una pantalla para crear usuarios.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/40-fase4-url-del-ambiente-de-desarrollo.png | URL del ambiente de desarrollo registrada en el Proyecto

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/41-ruta-tras-el-release.png | Ruta del Proyecto con la Fase 4 en curso

### C.5 Pruebas de humo

Las pruebas de humo se ejecutaron por HU. Para cada una, un modelo lee el código y los casos de prueba, escribe un guion de Playwright que se ejecuta contra el ambiente desplegado, y un agente de navegador verifica los fallos. Las tres HUs sumaron 44 casos: 36 aprobados, 2 fallidos y 6 bloqueados.

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/42b-HU-001-smoke-en-ejecucion.png | Pruebas de humo de la HU-001 en ejecución

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/42f-HU-001-resultado-del-smoke-testing-completo.png | Resultado de las pruebas de humo de la HU-001: 11 aprobados y 3 bloqueados

TABLA: Resultado de las pruebas de humo por HU
| HU | Casos | Aprobados | Fallidos | Bloqueados | Duración |
| HU-001 | 14 | 11 | 0 | 3 | 5.3 min |
| HU-002 | 14 | 10 | 1 | 3 | 5.1 min |
| HU-003 | 16 | 15 | 1 | 0 | 3.3 min |

Los seis casos bloqueados dependen de datos que la corrida no pudo proporcionar: una cuenta registrada con la contraseña incorrecta, un buzón de correo para verificar el envío, o un escenario que exige forzar un fallo del servicio de correo. Uno de ellos (TC-013 de la HU-002) se bloqueó porque el guion que generó el modelo no era válido (sintaxis inválida en la primera línea). Los dos fallos son consistentes: los casos TC-014 de la HU-002 y TC-016 de la HU-003 esperan una bitácora o auditoría de eventos visible para el administrador, y la aplicación desplegada no la ofrece (al abrir `/auditoria` o `/bitacora` redirige al inicio).

FIGURA: evidencia/corrida-E1c-2026-09-21/capturas/43f-HU-002-resultado-del-smoke-testing-completo.png | Resultado de las pruebas de humo de la HU-002: un fallo y tres bloqueos

### C.6 Resumen de la corrida

TABLA: Resumen de la corrida E1c
| Etapa | Resultado | Duración |
| Fase 1: leer y especificar 3 HUs | 3 HUs especificadas | 1.4 min |
| Fase 2: casos de prueba | 44 casos (14, 14 y 16) | 1.8 min |
| Fase 2: arquitectura | 5 entidades, 7 decisiones, 7 preguntas | 2.0 min |
| Fase 3: descomposición | 12 paquetes (2 intentos) | 2.1 min (más 2.5 min del intento fallido) |
| Fase 3: ciclo de 12 paquetes | 12 fusionados; 1 corrección por CI en rojo | 0.5 a 14.7 min por paquete |
| Fase 4: release en Google Cloud | Backend y frontend desplegados (2.º intento) | 8.5 min |
| Fase 4: pruebas de humo | 36 aprobados, 2 fallidos, 6 bloqueados | 13.7 min en total |

El costo nocional informado por el CLI de Claude fue de 16.67 USD para 228 llamadas al modelo (no comparable con la facturación de una API, porque el CLI se usó con una suscripción). Cada valor de este anexo proviene de las bases de datos de Loom, de la API de GitHub o de las pantallas capturadas; los tiempos son de reloj y dependen de la máquina, de la red y de la carga del proveedor.
