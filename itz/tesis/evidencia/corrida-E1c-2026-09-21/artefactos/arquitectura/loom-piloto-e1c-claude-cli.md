---
proyecto: PILOTO E1c ITZ Inventarios (Claude cuenta normal CLI)
repositorio: https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli
tipo_repositorio: fullstack
modo: fundacional
fase: arquitectura_definida
fecha: 2026-09-21
hus_analizadas: 3
---

# Arquitectura — loom-piloto-e1c-claude-cli

Monolito modular Spring Boot + SPA Angular en un monorepo, desplegados como dos servicios en Cloud Run. Alcance: solo autenticación (HU-001, HU-002, HU-003). JWT de acceso de vida corta con revocación en servidor (jti) para el logout, y expiración por inactividad con renovación deslizante del token. Recuperación de contraseña con token de un solo uso enviado por correo. PostgreSQL (Cloud SQL) con Flyway.

## Backend

### Capas

- **web** — Controladores REST, DTOs anotados con OpenAPI, validación Bean Validation, @RestControllerAdvice. Sin lógica de negocio.
- **service** — Casos de uso, reglas y transacciones. Usa repositorios y mappers MapStruct.
- **repository** — Entidades JPA y repositorios Spring Data. Migraciones Flyway.
- **config** — Spring Security, filtro JWT, OpenAPI, JavaMailSender, propiedades tipadas. Dependencias: web -> service -> repository.

### Módulos

- **auth** — Login, emisión/validación de JWT, renovación deslizante por actividad, logout con revocación del jti, expiración por inactividad. _(HUs: HU-001, HU-003)_
- **user** — Usuario, rol y hash BCrypt. Endpoint /me con solo los datos de la cuenta propia. _(HUs: HU-001, HU-002)_
- **passwordreset** — Solicitud de recuperación, token de un solo uso con caducidad, envío de correo y nueva contraseña. _(HUs: HU-002)_

### API y Swagger/OpenAPI

- **Herramienta:** springdoc-openapi (springdoc-openapi-starter-webmvc-ui)
- **UI de Swagger:** `/swagger-ui.html`
- **Especificación OpenAPI:** `/v3/api-docs`
- **Convención:** @Tag por controlador, @Operation y @ApiResponse por endpoint, @Schema en DTOs (records), esquema bearerAuth (JWT) global; rutas públicas marcadas con @SecurityRequirements vacío. Swagger público en dev, restringido en prod.

| Método | Ruta | Descripción | HUs |
|---|---|---|---|
| POST | `/api/v1/auth/login` | Autentica con correo y contraseña y devuelve JWT. | HU-001 |
| GET | `/api/v1/users/me` | Datos de la cuenta autenticada (acceso solo a lo propio). | HU-001 |
| POST | `/api/v1/auth/refresh` | Renueva el JWT si hay actividad dentro de la ventana de inactividad. | HU-003 |
| POST | `/api/v1/auth/logout` | Revoca el jti del token en servidor. | HU-003 |
| POST | `/api/v1/auth/password/forgot` | Solicita recuperación; respuesta genérica, envía correo con enlace. | HU-002 |
| POST | `/api/v1/auth/password/reset` | Define nueva contraseña con token válido de un solo uso. | HU-002 |

### Estructura de carpetas

```
backend/
  README.md
  Dockerfile
  pom.xml
  src/main/java/com/itz/inventarios/
    InventariosApplication.java
    config/ (SecurityConfig, OpenApiConfig, JwtProperties, MailConfig)
    common/ (error, exception)
    auth/ (web, service, domain, repository, mapper)
    user/ (web, service, domain, repository, mapper)
    passwordreset/ (web, service, domain, repository)
  src/main/resources/ (application.yml, application-prod.yml, db/migration/V1__auth.sql)
  src/test/java/... (JUnit 5)
```

### Persistencia

PostgreSQL con Spring Data JPA/Hibernate. Esquema solo por Flyway (ddl-auto=validate). Tokens de reseteo guardados como hash SHA-256. Marcar el token de reseteo como usado en la misma transacción que el cambio de contraseña.

### Seguridad

Spring Security stateless. Filtro JwtAuthenticationFilter valida firma HS256 (secreto en Secret Manager), expiración y que el jti no esté revocado. Access token corto (15 min) que se renueva con /refresh mientras haya actividad; pasado ese plazo sin actividad, la sesión expira. Roles en claim, autorización con @PreAuthorize. CORS limitado al origen del frontend. Contraseñas con BCrypt. Rate limit y mensajes genéricos en login y forgot para evitar enumeración. Auditoría: tabla auth_event (login ok/fallo, logout, reset).

### Convenciones

- Paquete por módulo, no por tipo técnico global.
- DTOs como records; entidades nunca expuestas en la API.
- MapStruct para mapeos y Lombok solo en entidades.
- Errores en formato ProblemDetail (RFC 7807).
- Migraciones Flyway inmutables, nombradas V<n>__desc.sql.
- Tests JUnit 5 por servicio y slice tests de controlador.

## Modelo de datos

### User

**Atributos:** id (UUID), email (único, normalizado en minúsculas), password_hash, full_name, enabled, created_at, last_login_at

**Relaciones:** N:M con Role, 1:N con PasswordResetToken, 1:N con AuthEvent

_HUs: HU-001, HU-002_

### Role

**Atributos:** id, name (único, p. ej. ADMIN, USER)

**Relaciones:** N:M con User (tabla user_role)

_HUs: HU-001_

### PasswordResetToken

**Atributos:** id, user_id, token_hash (único), expires_at, used_at

**Relaciones:** N:1 con User

_HUs: HU-002_

### RevokedToken

**Atributos:** jti (PK), user_id, expires_at (para limpieza periódica), revoked_at

**Relaciones:** N:1 con User

_HUs: HU-003_

### AuthEvent

**Atributos:** id, user_id (nullable), email_intentado, tipo (LOGIN_OK, LOGIN_FAIL, LOGOUT, RESET_REQUEST, RESET_DONE), ip, created_at

**Relaciones:** N:1 con User opcional

_HUs: HU-001, HU-002, HU-003_

## Frontend

### Estructura de carpetas

```
frontend/
  README.md
  Dockerfile
  nginx.conf.template
  package.json, angular.json, tailwind.config.js, jest.config.ts
  src/app/
    core/ (auth.service, token.storage, auth.interceptor, auth.guard, idle.service)
    shared/ (componentes UI, pipes)
    features/
      auth/ (login, forgot-password, reset-password)
      home/ (pantalla protegida inicial)
    app.routes.ts, app.config.ts
  src/environments/
```

### Módulos y pantallas

- **auth** — Login, Recuperar contraseña (solicitud), Restablecer contraseña (con token) _(HUs: HU-001, HU-002)_
- **core/session** — Diálogo de aviso de sesión por expirar, Botón Cerrar sesión (en layout) _(HUs: HU-003)_
- **home** — Inicio protegido (muestra datos de /users/me) _(HUs: HU-001)_

### Estado y acceso a datos

Servicios Angular con RxJS y HttpClient contra el contrato OpenAPI. Estado de sesión en un BehaviorSubject (AuthService) con token en memoria (sessionStorage para sobrevivir a recargas). Interceptor añade Bearer y ante 401 limpia sesión y redirige a login. IdleService detecta actividad del usuario, refresca el token y hace logout al vencer la inactividad. Guards protegen rutas.

### Convenciones

- Standalone components y lazy loading por feature.
- PrimeNG para formularios y diálogos; Tailwind para layout.
- Formularios reactivos con validación.
- Tests con Jest por servicio y componente.
- Sin lógica de negocio en componentes; va en servicios.

## Despliegue

Dos servicios en Cloud Run desde el monorepo, cada uno con su Dockerfile de producción.
- backend: backend/Dockerfile. Build multi-stage: maven:3.9-eclipse-temurin-21 (mvn -DskipTests package) y runtime eclipse-temurin:21-jre. Puerto 8080 (server.port=${PORT}). Healthcheck: GET /actuator/health. Variables: SPRING_PROFILES_ACTIVE=prod, DB_URL, DB_USER, DB_PASSWORD, JWT_SECRET, JWT_ACCESS_TTL_MINUTES, IDLE_TIMEOUT_MINUTES, MAIL_HOST, MAIL_PORT, MAIL_USER, MAIL_PASSWORD, MAIL_FROM, FRONTEND_BASE_URL, CORS_ALLOWED_ORIGINS. Secretos desde Secret Manager. Conexión a Cloud SQL (PostgreSQL) por conector de Cloud Run.
- frontend: frontend/Dockerfile. Multi-stage: node:20-alpine (npm ci && npm run build) y runtime nginx:alpine sirviendo dist con fallback a index.html. Puerto 8080. Healthcheck: GET /healthz (nginx). Variable: API_BASE_URL (inyectada en runtime en nginx.conf.template/config.json).
- CI (GitHub Actions): en cada PR, mvn verify en backend y npm ci, lint y jest en frontend. En push a main, docker build de ambas imágenes, push a Artifact Registry y gcloud run deploy de cada servicio, con autenticación por Workload Identity Federation. Cada servicio solo se reconstruye si cambian sus rutas.

## Decisiones

### Revocación de JWT

**Decisión:** Access token corto + tabla de jti revocados consultada por el filtro.

**Por qué:** HU-003 exige invalidar el token en servidor al cerrar sesión.

**Alternativas descartadas:** Sesiones HTTP con estado (contradice JWT); JWT sin revocación.

### Inactividad

**Decisión:** TTL corto renovado con /refresh mientras hay actividad; el frontend dispara el refresh y el logout.

**Por qué:** Sin refresh token de larga vida, si no hay actividad el token caduca solo, también en servidor.

**Alternativas descartadas:** Solo temporizador en cliente (no es seguro); refresh token de larga duración.

### Recuperación de contraseña

**Decisión:** Enlace por correo con token aleatorio, guardado como hash, de un solo uso y con caducidad (30 min).

**Por qué:** Cumple HU-002 sin intervención del administrador y limita el riesgo si se filtra la BD.

**Alternativas descartadas:** Código numérico corto; contraseña temporal por correo.

### Arquitectura

**Decisión:** Monolito modular con paquetes por módulo.

**Por qué:** Alcance pequeño, 0 microservicios por restricción.

**Alternativas descartadas:** Microservicios.

### Base de datos

**Decisión:** PostgreSQL en Cloud SQL con Flyway.

**Por qué:** Encaja con JPA y con GCP; migraciones versionadas.

**Alternativas descartadas:** H2 en producción; MySQL.

### Almacenamiento del token en el cliente

**Decisión:** sessionStorage, con cabecera Authorization.

**Por qué:** Sencillo y se cierra con la pestaña, útil en equipos compartidos.

**Alternativas descartadas:** localStorage (persiste); cookie HttpOnly (requiere gestionar CSRF).

### Frontend servido por separado

**Decisión:** Un servicio Cloud Run propio con nginx.

**Por qué:** Despliegue independiente del backend dentro del monorepo.

**Alternativas descartadas:** Servir la SPA desde Spring Boot.

## Supuestos y preguntas abiertas

- ¿Cómo se crean los usuarios? Las HUs no incluyen alta ni administración de usuarios: se asume un seed/migración inicial de usuarios y roles.
- ¿Cuál es el periodo de inactividad exacto? Se asume 15 min configurable (IDLE_TIMEOUT_MINUTES).
- ¿Qué significa 'información que le corresponde'? Aún no hay entidades de negocio (inventarios); se asume control por rol y por cuenta propia (/users/me). Los roles concretos y sus permisos están por definir.
- ¿Qué proveedor SMTP usar para el correo de recuperación (SendGrid, Gmail, otro) y cuál es la URL pública del frontend?
- ¿Hay política de contraseñas (longitud, complejidad) y de bloqueo tras intentos fallidos?
- ¿El aviso previo a la expiración por inactividad es obligatorio? Se asume un diálogo de aviso opcional.
- ¿Se requiere multiidioma? Se asume solo español.
