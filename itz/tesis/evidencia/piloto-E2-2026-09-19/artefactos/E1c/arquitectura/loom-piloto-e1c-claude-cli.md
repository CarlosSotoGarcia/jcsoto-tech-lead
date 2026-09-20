---
proyecto: PILOTO E1c ITZ Inventarios (Claude cuenta normal CLI)
repositorio: https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli
tipo_repositorio: fullstack
modo: fundacional
fase: arquitectura_definida
fecha: 2026-09-19
hus_analizadas: 3
---

# Arquitectura — loom-piloto-e1c-claude-cli

Monolito modular Spring Boot (módulos auth, passwordreset, users, audit, common) más SPA Angular en un monorepo. Autenticación JWT stateless: access token corto y refresh token rotativo persistido (hash), lo que permite logout real por revocación y expiración por inactividad (HU-003). Recuperación de contraseña con token de un solo uso y caducidad enviado por correo (HU-002). Swagger con springdoc-openapi desde el primer paquete. Dos contenedores (backend y frontend/nginx) en Cloud Run con Cloud SQL PostgreSQL. Alcance limitado a las 3 HUs de identidad y sesión; el aislamiento de datos por usuario (HU-001) queda como mecanismo base reutilizable.

## Backend

### Capas

- **web** — Controllers REST, DTOs, Bean Validation, anotaciones OpenAPI y manejo global de errores (@RestControllerAdvice). Sin lógica de negocio.
- **application** — Servicios de casos de uso con @Transactional; orquestan repositorios, tokens y correo. MapStruct para entidad↔DTO.
- **domain** — Entidades JPA y repositorios Spring Data. No depende de web.
- **infrastructure** — Filtro JWT, SecurityFilterChain, emisión/validación de tokens, envío SMTP, propiedades de configuración.

### Módulos

- **auth** — Login, emisión de JWT, refresh con rotación, logout con revocación, expiración por inactividad, contexto de usuario actual para restringir el acceso a datos propios. _(HUs: HU-001, HU-003)_
- **passwordreset** — Solicitud de recuperación, token de un solo uso con caducidad, envío por correo, fijar nueva contraseña y revocar sesiones activas. _(HUs: HU-002)_
- **users** — Cuenta de usuario (correo, hash BCrypt, rol, estado), perfil propio, bloqueo temporal por intentos fallidos. _(HUs: HU-001)_
- **audit** — Registro de eventos de seguridad: login ok/fallido, logout, expiración, solicitud y completado de recuperación. _(HUs: HU-001, HU-002, HU-003)_
- **common** — Errores, config OpenAPI, utilidades. Sin dependencias hacia otros módulos. _(HUs: HU-001)_

### API y Swagger/OpenAPI

- **Herramienta:** springdoc-openapi-starter-webmvc-ui
- **UI de Swagger:** `/swagger-ui.html`
- **Especificación OpenAPI:** `/v3/api-docs`
- **Convención:** @Tag por controller, @Operation y @ApiResponse por método, @Schema en DTOs (records), esquema bearerAuth (JWT) declarado en OpenApiConfig; endpoints públicos marcados con @SecurityRequirements vacío.

| Método | Ruta | Descripción | HUs |
|---|---|---|---|
| POST | `/api/v1/auth/login` | Inicia sesión con correo y contraseña; devuelve access y refresh token. 401 genérico si son incorrectos. | HU-001 |
| GET | `/api/v1/users/me` | Perfil del usuario autenticado; solo su propia información. | HU-001 |
| POST | `/api/v1/auth/refresh` | Renueva access token con refresh token rotativo; falla si hay inactividad excedida o revocación. | HU-003 |
| POST | `/api/v1/auth/logout` | Revoca el refresh token y cierra la sesión. | HU-003 |
| POST | `/api/v1/auth/password/forgot` | Solicita recuperación; siempre responde 202 sin revelar si el correo existe. | HU-002 |
| POST | `/api/v1/auth/password/reset` | Completa el restablecimiento con token y nueva contraseña. | HU-002 |

### Estructura de carpetas

```
loom-piloto-e1c-claude-cli/
├── README.md
├── docker-compose.yml            (postgres + mailhog local)
├── .github/workflows/            (ci-backend.yml, ci-frontend.yml, deploy.yml)
├── backend/
│   ├── README.md
│   ├── pom.xml
│   ├── Dockerfile
│   └── src/
│       ├── main/java/com/itz/inventarios/
│       │   ├── InventariosApplication.java
│       │   ├── auth/{web,application,domain,infrastructure}
│       │   ├── passwordreset/{web,application,domain,infrastructure}
│       │   ├── users/{web,application,domain}
│       │   ├── audit/{application,domain}
│       │   └── common/{config,error,util}
│       ├── main/resources/{application.yml,application-dev.yml,application-prod.yml,db/migration/V1__usuarios.sql,...}
│       └── test/java/com/itz/inventarios/...
└── frontend/
    ├── README.md
    ├── package.json, angular.json, tailwind.config.js, jest.config.ts
    ├── Dockerfile, nginx.conf
    └── src/app/{core,shared,features}
```

### Persistencia

PostgreSQL (Cloud Sql en prod, contenedor en local). Spring Data JPA/Hibernate con ddl-auto=validate; esquema solo con migraciones Flyway versionadas. Contraseñas con BCrypt. Tokens de refresh y de recuperación se guardan como hash SHA-256, nunca en claro. Operaciones de rotación/consumo de token en una sola transacción con bloqueo optimista (@Version) para evitar reutilización.

### Seguridad

Spring Security stateless: filtro JWT valida firma HS256/RS256 y expiración; access token 15 min; refresh con rotación y expiración deslizante por inactividad (valor configurable, ver supuestos). Logout revoca la familia de refresh tokens. Reutilización de un refresh revocado invalida la familia. Roles ADMIN/USER en claim; acceso a datos propios por identidad del token (nunca por id enviado por el cliente) y @PreAuthorize. Mensaje de error genérico en login y forgot para no enumerar cuentas. Bloqueo temporal tras N intentos fallidos. CORS restringido al origen del frontend. Secretos (clave JWT, SMTP) en Secret Manager. Auditoría en tabla eventos_auditoria.

### Convenciones

- Paquete raíz com.itz.inventarios; paquetes por módulo y dentro por capa; un módulo solo accede a otro por su servicio público, nunca a sus repositorios.
- DTOs como records; entidades nunca se exponen en la API.
- Lombok en entidades (@Getter, @Builder); MapStruct con componentModel spring.
- Rutas /api/v1/...; errores en formato ProblemDetail (RFC 7807).
- Migraciones Flyway V{n}__descripcion.sql, inmutables una vez fusionadas.
- Tests JUnit 5: unitarios de servicios y @SpringBootTest con Testcontainers PostgreSQL para seguridad.

## Modelo de datos

### Usuario

**Atributos:** id (UUID), correo (único, minúsculas), password_hash, rol, activo, intentos_fallidos, bloqueado_hasta, creado_en, version

**Relaciones:** 1..N RefreshToken, 1..N TokenRecuperacion, 1..N EventoAuditoria

_HUs: HU-001_

### RefreshToken

**Atributos:** id, usuario_id, familia_id, token_hash (único), emitido_en, ultimo_uso_en, expira_en, revocado_en, version

**Relaciones:** N..1 Usuario

_HUs: HU-001, HU-003_

### TokenRecuperacion

**Atributos:** id, usuario_id, token_hash (único), creado_en, expira_en, usado_en

**Relaciones:** N..1 Usuario

_HUs: HU-002_

### EventoAuditoria

**Atributos:** id, usuario_id (nullable), tipo (LOGIN_OK, LOGIN_FALLIDO, LOGOUT, SESION_EXPIRADA, RECUPERACION_SOLICITADA, RECUPERACION_COMPLETADA), correo_intentado, ip, ocurrido_en

**Relaciones:** N..1 Usuario (opcional)

_HUs: HU-001, HU-002, HU-003_

## Frontend

### Estructura de carpetas

```
frontend/src/app/
├── core/{auth (auth.service, token.storage, auth.guard, jwt.interceptor, refresh.interceptor, idle.service), layout}
├── shared/{components,pipes}
├── features/
│   ├── login/
│   ├── password-recovery/{forgot,reset}
│   └── home/
├── app.routes.ts, app.config.ts
src/environments/, src/assets/, src/styles.css (Tailwind)
```

### Módulos y pantallas

- **login** — Pantalla de inicio de sesión (correo, contraseña, mensaje de error genérico) _(HUs: HU-001)_
- **home** — Página inicial protegida con datos del perfil propio y botón Cerrar sesión _(HUs: HU-001, HU-003)_
- **password-recovery** — Solicitar recuperación (correo), Restablecer contraseña (token de la URL y nueva contraseña) _(HUs: HU-002)_
- **core/auth** — Guard de rutas, interceptores JWT y refresh, servicio de inactividad con aviso previo de expiración _(HUs: HU-001, HU-003)_

### Estado y acceso a datos

Sin store global: servicios con RxJS (BehaviorSubject para el usuario actual) y HttpClient. Cliente HTTP tipado generado a partir del JSON de OpenAPI (/v3/api-docs). Access token en memoria; refresh token en sessionStorage (ver supuestos). IdleService detecta actividad del usuario (eventos DOM) y llama a logout local al agotar el tiempo.

### Convenciones

- Componentes standalone con rutas lazy por feature.
- PrimeNG para formularios y mensajes; Tailwind para layout.
- Reactive Forms con validación de correo y política de contraseña.
- Tests Jest por servicio/componente; sin lógica de negocio en templates.
- Nunca registrar tokens ni contraseñas en consola.

## Despliegue

Monorepo con dos imágenes: backend (Maven build multietapa, JRE 21) y frontend (build Angular servido por nginx). Cada una en su servicio de Cloud Run (backend y frontend), construidas con Cloud Build o GitHub Actions y publicadas en Artifact Registry. Backend se conecta a Cloud SQL PostgreSQL por conector; secretos (clave JWT, credenciales SMTP, BD) en Secret Manager. Flyway migra al arrancar. Variables por entorno (dev/prod). Swagger habilitado en dev y protegido o deshabilitado en prod. CI por carpeta (paths) para backend y frontend. Local: docker-compose con PostgreSQL y MailHog.

## Decisiones

### Estilo de arquitectura

**Decisión:** Monolito modular con paquetes por módulo y capas internas.

**Por qué:** Restricción de 0 microservicios; alcance pequeño de 3 HUs.

**Alternativas descartadas:** Microservicios; arquitectura solo por capas técnicas.

### Sesión y expiración por inactividad

**Decisión:** Access JWT de 15 min + refresh token rotativo persistido con expiración deslizante por inactividad.

**Por qué:** JWT es stateless, así que el logout real y la inactividad requieren estado del refresh en servidor (HU-003).

**Alternativas descartadas:** Solo JWT largo sin revocación; sesiones HTTP en servidor.

### Recuperación de contraseña

**Decisión:** Token aleatorio de un solo uso, guardado como hash, con caducidad corta, enviado por correo con enlace al frontend.

**Por qué:** Cumple autonomía sin administrador (HU-002) y evita enumeración de cuentas.

**Alternativas descartadas:** Contraseña temporal por correo; JWT firmado como token de reset.

### Base de datos

**Decisión:** PostgreSQL con Flyway.

**Por qué:** Encaja con Cloud SQL y con la integridad transaccional exigida en rotación de tokens.

**Alternativas descartadas:** MySQL; H2 en producción.

### Documentación de API

**Decisión:** springdoc-openapi con cliente TS generado.

**Por qué:** Contrato único consumido por el frontend desde el primer paquete.

**Alternativas descartadas:** Contrato manual en documento.

### Almacenamiento de tokens en el cliente

**Decisión:** Access en memoria, refresh en sessionStorage.

**Por qué:** Reduce la exposición en equipos compartidos y se pierde al cerrar la pestaña (HU-003).

**Alternativas descartadas:** localStorage; cookie HttpOnly (requiere manejo CSRF y mismo sitio entre Cloud Run services).

### Aislamiento de datos por usuario

**Decisión:** Identidad tomada siempre del token y filtros en servicio/consulta, con @PreAuthorize por rol.

**Por qué:** HU-001 exige ver solo lo que corresponde a la cuenta.

**Alternativas descartadas:** Recibir el id de usuario desde el cliente; Row Level Security en BD.

### Despliegue

**Decisión:** Dos servicios de Cloud Run desde el mismo monorepo con CI por rutas.

**Por qué:** Coherente con el stack y permite escalar y desplegar cada parte de forma independiente.

**Alternativas descartadas:** Un único contenedor con el frontend embebido en Spring.

## Supuestos y preguntas abiertas

- ¿Cuál es el periodo de inactividad exacto (HU-003 no lo fija)? Se asume 15 min con refresh deslizante; configurable.
- ¿Cómo se crean las cuentas? Las HUs no incluyen registro ni administración de usuarios; se asume alta por script/migración semilla o por un administrador fuera de alcance.
- ¿Qué información 'le corresponde' a cada usuario (HU-001)? No hay entidades de negocio en las HUs; se asume solo perfil propio y un mecanismo reutilizable (rol + identidad del token). ¿Existen roles o pertenencia a unidades/almacenes?
- ¿Proveedor de correo (SMTP corporativo, SendGrid, Gmail API)? Se asume SMTP configurable; MailHog en local.
- ¿Enlace o código para el restablecimiento (HU-002)? Se asume enlace con token; ¿caducidad deseada (se asume 30 min)?
- ¿Política de contraseñas y de bloqueo por intentos fallidos? Se asume mínimo 8 caracteres y bloqueo temporal tras 5 intentos.
- ¿Debe cerrar el restablecimiento todas las sesiones activas? Se asume que sí.
- ¿Swagger accesible en producción? Se asume solo en dev/staging.
