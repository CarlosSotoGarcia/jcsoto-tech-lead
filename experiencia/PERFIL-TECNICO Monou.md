# Perfil técnico — Monou Chat (torneos en tiempo real)

> Documento de trabajo para armar contenido de un landing page / CV. Es un volcado honesto de lo que hice en este proyecto, sacado de `git log` de ambos repos y de las sesiones de trabajo reales — no está redactado como bullets de CV todavía, así que elegí y recortá de acá lo que sirva. Al final dejo una sección con sugerencias de frases cortas.

## 1. Qué es el proyecto

Monou Chat es el **microservicio de chat en tiempo real** de la plataforma de torneos de esports Monou (monou.gg). Le da a cada torneo:

- Una sala de chat general del torneo, una por equipo y una por partida, con jerarquía entre ellas.
- Moderación en vivo (mute/ban), reportes de incidentes con evidencia, comandos de barra (`/players`, `/ot`, `/reportar`, `/gg`, `/score`…).
- Herramientas de organizador: llamar la atención de un jugador, difusión de mensajes programados, timers de partida, cierre y archivado automático de chats al terminar el torneo.
- Integración en vivo con el bracket del torneo (se abren y cierran salas de partida automáticamente según el estado del bracket en la API de Monou).

Es un proyecto de equipo (~5 personas) activo desde octubre 2025, todavía en desarrollo. Se usa en producción/staging real con torneos y jugadores reales.

## 2. Mi rol

Trabajé **full-stack** en los dos repos que componen el sistema:

| Repo | Stack | Mi participación |
|---|---|---|
| `repo-bot-back` | Java 21, Spring Boot 3 (WebFlux), Apache Pekko (actores + event sourcing + cluster sharding), PostgreSQL, AWS (S3, ECS) | 45 de 175 commits — arquitectura de tiempo real, integraciones externas, moderación, infraestructura/CI-CD |
| `repo-bot-front` | Angular 14 (librería npm publicable + app demo), TypeScript, RxJS | 87 de 184 commits — **mayor contribuyente individual** del frontend |

No fui el único desarrollador — es trabajo en equipo — pero soy quien más código aportó al frontend, y en el backend construí piezas centrales de la arquitectura (el manejo de sesiones WebSocket, la integración con la API de torneos, el sistema de moderación, timers/difusión, el archivado de chats) además de trabajo reciente de seguridad e infraestructura de despliegue.

## 3. Stack técnico que usé en el día a día

**Backend**: Java 21 · Spring Boot 3 / WebFlux (reactivo) · Apache Pekko (actor model, `EventSourcedBehavior`, Cluster Sharding, DistributedPubSub) · PostgreSQL (R2DBC para dominio, Slick/JDBC para el event journal de Pekko) · WebSocket · AWS S3 (archivado) · AWS ECS (despliegue, descubrimiento de nodos de cluster vía API de ECS) · Docker / docker-compose · Maven.

**Frontend**: Angular 14 · TypeScript (strict mode) · RxJS (estado reactivo sin NgRx) · arquitectura de librería npm publicable (AWS CodeArtifact) · WebSocket nativo · Karma/Jasmine.

**Infra / DevOps**: AWS CodeBuild (`buildspec.yml`), ECR, ECS, Secrets Manager (diseño de migración), LocalStack (S3 emulado en dev).

## 4. Contribuciones técnicas — Backend

- **Arquitectura de actores con event sourcing**: diseño e implementación de `ChatRoomActor` sobre Apache Pekko (`EventSourcedBehavior`) — cada sala de chat es un actor independiente cuyo estado se reconstruye reproduciendo eventos persistidos (`event_journal`), con snapshots cada 100 eventos. Soporta dos modos: nodo único local (para dev) y **Cluster Sharding** distribuido entre múltiples nodos ECS en staging.
- **Capa de WebSocket en tiempo real**: `ChatWebSocketHandler` (Spring WebFlux reactivo) y `WebSocketSessionManager` para manejar sesiones multi-sala por usuario, reconexión, y entrega de mensajes tanto en modo local (mapa en memoria) como en modo cluster (`DistributedPubSub`).
- **Integración con la API externa de Monou**: `MonouApiService` y `TournamentProxyController` para traer datos de torneo/equipos/partidas y reportar resultados de partida (eliminación simple, round robin, royale), con fallback a mocks si la API externa no responde.
- **Sincronización de bracket en vivo**: `BracketEventService` — abre y cierra salas de partida automáticamente según el estado real del bracket (webhook `bracket-updated`), cierra los chats del torneo completo cuando termina o se cancela.
- **Sistema de moderación**: mute/ban/unban con expiración, tanto por WebSocket como por REST (`/api/chat/moderation/*`).
- **Difusión y timers programados**: `DifusionService` (mensajes de sistema programados a futuro, por sala o por tipo de sala) y `TimerSchedulerService` (cuentas regresivas de partida), ambos como jobs `@Scheduled` que pollean tablas de PostgreSQL.
- **Llamada al organizador (OT)**: comando `/llamar` con señales especiales (`OT_BROADCAST`, `OT_ATTENTION`) enrutadas solo a moderadores/organizadores.
- **Ciclo de vida y archivado de chats**: diseño del período de gracia post-torneo (48h en staging) — al vencer, se exporta todo el chat como ZIP a S3 y se purga la base de datos; el organizador puede posponer el cierre o cerrarlo manualmente de forma reversible (con respaldo en S3 igual). Documentado en detalle en `ResumenFeatures.md`.
- **Multi-entorno / infraestructura de despliegue (2026-08-22)**: agregué el perfil `prod` (hasta entonces solo existía `uat`), parametricé `ECS_CLUSTER_NAME`/`ECS_SERVICE_NAME` (antes hardcodeados) para que producción pueda tener su propio cluster sin pisar el de staging, y documenté el runbook completo para separar los pipelines de UAT y Producción (migraciones con Flyway, gate de tests en CI, Secrets Manager, verificación post-deploy con rollback).
- **Seguridad — remoción de credenciales hardcodeadas**: saqué usuario/contraseña de la RDS de staging de `application-uat.yml` (estaban en texto plano en el repo).
- **Seguridad — fix de escalación de privilegios en moderación (2026-09-06)**: detecté y corregí que un organizador podía ser muteado/baneado por otro admin porque `MuteUser`/`BanUser` no validaban el rol del objetivo — agregué el guard en el actor (`ChatRoomActor`) para bloquear esa acción contra roles `ORGANIZER`/`MODERATOR`.

## 5. Contribuciones técnicas — Frontend

- **`ChatComponent`**, el componente más grande y central de la librería: layout multi-pestaña (Salas / Matches / Panel de Control), navegación entre salas de torneo/equipo/partida, sidebar de administración con moderación, difusión, timers y comandos — construido y evolucionado a lo largo de decenas de commits.
- **`CanalTorneoService`**: el servicio que maneja toda la conexión WebSocket — reconexión automática (hasta 5 intentos), streams de mensajes por sala con buffer de replay, máquina de estados de conexión (`DESCONECTADO → CONECTANDO → CONECTADO → RECONECTANDO`).
- **Panel de moderación** (`ModerationPanelComponent`): lista de usuarios conectados con mute/ban, lista de baneados, reportes con detalle de evidencia — incluye el fix reciente (2026-09-06) para ocultar organizadores/moderadores de la lista de objetivos muteables.
- **Visualización de bracket**: `BracketModalComponent` con dos modos (árbol para eliminación, ranking para round robin/royale), estados de partida en vivo.
- **UI basada en rol**: mostrar controles administrativos solo al organizador real (no a cualquier admin), indicadores de presencia en vivo (usuarios conectados), reconocimiento inmediato de un usuario en el panel al conectarse.
- **Componentes de flujo de partida**: `ScoreModalComponent`, `ResultsModalComponent`, `ReportModalComponent` (con subida de evidencia), `MatchRoundsAccordionComponent`.
- **Arquitectura de librería publicable**: separación entre la librería (`projects/repo-bot-lib`, publicada a AWS CodeArtifact como `@monou/repo-bot-lib`) y la app demo que la consume — incluyendo mover configuración que estaba hardcodeada (URLs de imágenes, timeouts de reconexión) a inputs/tokens de inyección para que otros consumidores del paquete la puedan ajustar sin fork.

## 6. Casos destacados de resolución de problemas

Estos tres sirven como ejemplos concretos de "cómo pienso", más allá de la lista de features — útiles para un portfolio o para hablar de ellos en una entrevista.

### a) Escalación de privilegios en moderación (fix cross-stack, 2026-09-06)

Un cliente reportó en una presentación que el organizador del torneo aparecía en la lista de "usuarios muteables" del panel de moderación. Rastreé la causa en las dos capas: en el frontend, el filtro de la lista solo excluía al propio admin logueado, no por rol; en el backend, `ChatRoomActor.onMuteUser`/`onBanUser` tampoco validaban el rol del objetivo — cualquier admin podía mutear/banear a otro organizador o moderador sin que nada lo bloqueara, incluso llamando el endpoint REST directo. Corregí ambas capas: filtro por rol en el panel (frontend) y un guard explícito en el actor (backend) que rechaza la acción si el objetivo es `ORGANIZER`/`MODERATOR`, con logging para trazabilidad.

### b) Diagnóstico de un "split-brain" de persistencia distribuida (debugging de sistemas)

Un feature de difusión de mensajes fallaba de forma intermitente: el primer intento no llegaba a nadie, pero un reintento sí. Reproduje el error real en consola (`duplicate key value violates unique constraint "event_journal_pkey"`) y seguí el rastro hasta la causa raíz: estaba corriendo una instancia local de la app (perfil `default`, sin Cluster Sharding) apuntando a la misma base de datos de staging que el servicio real desplegado en ECS (perfil `uat`, con Cluster Sharding real). Dos procesos no coordinados entre sí terminaban creando, cada uno por su cuenta, un actor para la misma sala de chat y compitiendo por escribir el mismo número de secuencia en el event journal — un caso de split-brain típico de sistemas con actores con estado. Expliqué por qué el propio mecanismo de reintento de `DifusionService` "curaba" el síntoma en el segundo intento, y documenté el riesgo real (mensajes de chat normales, sin ese reintento automático, se pueden perder en silencio bajo la misma condición).

### c) De credenciales en texto plano a un pipeline de despliegue con dos ambientes

El repo tenía la contraseña real de la base de datos de staging hardcodeada en `application-uat.yml` (y, por un descuido posterior, vuelta a aparecer en un archivo de notas del repo). Sané el archivo de config, y de ahí escalé el problema a nivel de infraestructura: hoy solo existe un ambiente de despliegue (todo el CI/CD apunta siempre a staging, sin importar la rama). Diseñé y documenté — con partes ya implementadas en código (perfil `prod`, variables de entorno parametrizadas para el cluster de ECS) — el plan completo para separar staging y producción de verdad: RDS, bucket S3, cluster ECS y secretos independientes, migraciones con Flyway en vez de `CREATE TABLE IF NOT EXISTS` en cada arranque, gate de tests en el pipeline, y verificación de salud post-deploy con rollback.

## 7. Datos objetivos (por si sirven de referencia numérica)

- Antigüedad del proyecto: octubre 2025 → activo a la fecha (septiembre 2026), ~11 meses.
- Equipo: 5 contribuyentes en total entre los dos repos.
- Commits propios: 45/175 en `repo-bot-back`, 87/184 en `repo-bot-front` (el mayor número de commits individual del frontend).
- Alcance: full-stack (Java/Spring/Pekko en el backend, Angular/TypeScript en el frontend) + trabajo puntual de infraestructura AWS (ECS, S3, CI/CD) y seguridad.

## 8. Para el landing page — frases cortas sugeridas

Elegí de acá según el tono que quieras (más técnico vs. más de impacto):

- "Desarrollador full-stack en un microservicio de chat en tiempo real para torneos de esports (Java/Spring Boot/Apache Pekko + Angular), con arquitectura de actores, event sourcing y cluster distribuido."
- "Diseñé e implementé la capa de WebSocket y moderación en tiempo real de una plataforma de torneos, incluyendo reconexión automática, mute/ban con expiración y difusión de mensajes programados."
- "Diagnostiqué y resolví un bug de consistencia distribuida (split-brain en persistencia de eventos) causado por instancias no coordinadas compitiendo por el mismo estado — sistemas basados en actores con Apache Pekko."
- "Encontré y corregí una vulnerabilidad de escalación de privilegios en el sistema de moderación, con fix coordinado en frontend y backend."
- "Lideré la remoción de credenciales hardcodeadas del repositorio y diseñé el plan de separación de ambientes staging/producción (AWS ECS, Secrets Manager, migraciones de esquema)."
- "Mayor contribuyente individual del frontend Angular de la librería `@monou/repo-bot-lib`, publicada vía AWS CodeArtifact y consumida por la plataforma de torneos Monou."
