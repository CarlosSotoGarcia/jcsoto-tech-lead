---
proyecto: PILOTO E3c ITZ Agenda Taller (Claude cuenta normal CLI)
repositorio: https://github.com/CarlosSotoGarcia/loom-piloto-e3c-claude-cli
tipo_repositorio: fullstack
modo: fundacional
fase: arquitectura_definida
fecha: 2026-09-26
hus_analizadas: 3
---

# Arquitectura — loom-piloto-e3c-claude-cli

Monolito modular en un monorepo: `apps/backend` (NestJS + Prisma + PostgreSQL) y `apps/frontend` (React + MUI). Las tres HUs cubren la identidad del portal: autorregistro con verificación de correo y vinculación al expediente de cliente (HU-001), login y logout por rol con JWT (HU-002) y recuperación de contraseña (HU-003). El backend usa un access token JWT corto y un refresh token rotativo guardado con hash, lo que permite un cierre de sesión real. Los tokens de un solo uso (verificación y restablecimiento) comparten un mismo mecanismo y todo evento sensible se audita. Se despliegan dos servicios en Cloud Run con Cloud SQL, y el envío de correo queda detrás de un puerto intercambiable.

## Backend

### Capas

- **api (controllers + DTOs)** — HTTP, validación con class-validator, documentación Swagger, mapeo de errores a códigos de negocio. No contiene lógica.
- **application (services / casos de uso)** — Orquesta reglas de negocio y transacciones (prisma.$transaction). Depende solo de domain y de puertos.
- **domain** — Reglas puras: política de contraseña, normalización de correo y celular, estados de cuenta, roles. Sin dependencias de framework.
- **infrastructure** — Repositorios Prisma, adaptador de correo (SMTP/proveedor), hashing argon2, firma JWT. Implementa los puertos.

### Módulos

- **auth** — Login, refresh, logout, /me, guards JWT y de roles, redirección por rol (devuelve rutaInicial). _(HUs: HU-002)_
- **registro** — Autorregistro de cliente, aceptación de documentos legales, verificación de correo y reenvío, vinculación al expediente de cliente existente sin duplicados. _(HUs: HU-001)_
- **password-recovery** — Solicitud de enlace (respuesta neutra aunque el correo no exista), validación del token y restablecimiento. Al restablecer revoca las sesiones activas. _(HUs: HU-003)_
- **usuarios** — Entidad Usuario, estados (PENDIENTE_VERIFICACION, ACTIVA, BLOQUEADA, INACTIVA) y roles. Repositorio compartido por auth, registro y recovery. _(HUs: HU-001, HU-002, HU-003)_
- **clientes** — Expediente de cliente (lo crea recepción o el autorregistro). Búsqueda de coincidencias para vincular. _(HUs: HU-001)_
- **tokens** — Emisión y consumo de tokens de un solo uso (se guarda un hash SHA-256, con expiración y uso único). _(HUs: HU-001, HU-003)_
- **notificaciones** — Puerto MailerPort con plantillas de verificación y restablecimiento. Adaptador SMTP en producción y adaptador de consola o log en desarrollo. _(HUs: HU-001, HU-003)_
- **legal** — Versiones vigentes del aviso de privacidad y de los términos, y registro de su aceptación. _(HUs: HU-001)_
- **auditoria** — Registro append-only de eventos: registro, verificación, login OK/fallido, logout, solicitud y cambio de contraseña, vinculación. _(HUs: HU-001, HU-002, HU-003)_
- **health** — GET /api/health con liveness y ping a la base de datos, para Cloud Run. _(HUs: —)_

### API y Swagger/OpenAPI

- **Herramienta:** @nestjs/swagger (OpenAPI 3) con el plugin CLI de Nest activado en nest-cli.json
- **UI de Swagger:** `/api/docs`
- **Especificación OpenAPI:** `/api/docs-json`
- **Convención:** Prefijo global /api/v1. Cada controller lleva @ApiTags(<modulo>) y los endpoints protegidos @ApiBearerAuth(). Cada endpoint lleva @ApiOperation({summary, description:'HU-xxx'}) y @ApiOkResponse/@ApiCreatedResponse/@ApiConflictResponse con un DTO tipado. Los DTOs son clases con class-validator y @ApiProperty (con ejemplo). Los errores siguen el formato uniforme ErrorDto {codigo, mensaje, campos?}. El frontend genera sus tipos desde /api/docs-json con openapi-typescript.

| Método | Ruta | Descripción | HUs |
|---|---|---|---|
| GET | `/api/v1/legal/documentos-vigentes` | Aviso de privacidad y términos vigentes (id, versión, URL o contenido). | HU-001 |
| POST | `/api/v1/registro` | Crea una cuenta de cliente en estado PENDIENTE_VERIFICACION y envía el correo de verificación. Responde 409 si el correo está duplicado. | HU-001 |
| POST | `/api/v1/registro/verificar-correo` | Consume el token de verificación: activa la cuenta y la vincula o crea el expediente de cliente. | HU-001 |
| POST | `/api/v1/registro/reenviar-verificacion` | Reenvía el enlace de verificación, con límite de frecuencia y respuesta neutra. | HU-001 |
| POST | `/api/v1/auth/login` | Correo y contraseña. Devuelve accessToken, usuario, rol y rutaInicial, y pone el refresh token en una cookie httpOnly. | HU-002 |
| POST | `/api/v1/auth/refresh` | Rota el refresh token (cookie) y emite un nuevo access token. | HU-002 |
| POST | `/api/v1/auth/logout` | Revoca la sesión actual y borra la cookie. | HU-002 |
| GET | `/api/v1/auth/me` | Perfil y rol del usuario autenticado. | HU-002 |
| POST | `/api/v1/auth/password/solicitar` | Envía el enlace de restablecimiento. Siempre responde 202 con un mensaje neutro. | HU-003 |
| GET | `/api/v1/auth/password/token/{token}` | Indica si el enlace está vigente, usado o expirado. | HU-003 |
| POST | `/api/v1/auth/password/restablecer` | Recibe el token y la nueva contraseña. Actualiza el hash, marca el token como usado y revoca las sesiones. | HU-003 |
| GET | `/api/health` | Healthcheck (fuera de /v1 y excluido de Swagger). | — |

### Estructura de carpetas

```
apps/backend/
  README.md
  Dockerfile              # producción
  Dockerfile.dev
  nest-cli.json  package.json  tsconfig.json  .env.example
  prisma/
    schema.prisma
    migrations/
    seed.ts               # roles, documentos legales, usuario admin
  src/
    main.ts               # prefijo /api, ValidationPipe, Swagger, cookie-parser, helmet
    app.module.ts
    config/               # esquema de variables de entorno validado (zod/joi)
    common/               # filtros de error, ErrorDto, decoradores @Roles/@Public, guards
    prisma/               # PrismaModule, PrismaService
    modules/
      auth/        {auth.controller.ts, auth.service.ts, jwt.strategy.ts, dto/}
      registro/    {registro.controller.ts, registro.service.ts, dto/}
      password-recovery/ {…}
      usuarios/    {usuarios.repository.ts, domain/}
      clientes/    {clientes.service.ts, clientes.repository.ts}
      tokens/      {tokens.service.ts}
      notificaciones/ {mailer.port.ts, smtp.adapter.ts, console.adapter.ts, templates/}
      legal/  auditoria/  health/
  test/                   # e2e con Jest + supertest
  src/**/*.spec.ts        # pruebas unitarias con Jest
```

### Persistencia

PostgreSQL (Cloud SQL) con Prisma y migraciones versionadas (`prisma migrate deploy` en el arranque o en un job). Hay índices únicos sobre Usuario.correoNormalizado (en minúsculas y sin espacios) y Cliente.correoNormalizado/celular (parciales, NULL permitido), que impiden duplicados aunque haya carreras entre peticiones. La verificación ocurre en una sola transacción: consumir el token (UPDATE … WHERE usadoEn IS NULL AND expiraEn > now()), activar el usuario y vincular o crear el Cliente. El restablecimiento ocurre también en una sola transacción: consumir el token, actualizar el hash e invalidar los tokens de restablecimiento pendientes y las sesiones. Los tokens y refresh tokens se guardan solo como hash.

### Seguridad

JWT de acceso HS256 (15 min) con claims sub, rol y sesionId. El refresh token es opaco, rota en cada uso y vive en una cookie httpOnly, Secure y SameSite=Strict con path /api/v1/auth. Si se reutiliza un refresh token ya rotado, se revoca toda la familia. JwtAuthGuard es global y @Public() marca las rutas abiertas; RolesGuard aplica @Roles(). Roles iniciales: CLIENTE, RECEPCION, ADMIN (a confirmar). Contraseñas con argon2id y una política de dominio compartida por el frontend. El login responde con un mensaje genérico ante credenciales inválidas y no permite el acceso si la cuenta está pendiente de verificación o inactiva. Tanto el login como la solicitud de restablecimiento y el reenvío tienen límite de frecuencia (@nestjs/throttler) y respuestas neutras que no revelan si el correo existe. Se usan helmet y CORS restringido al origen del frontend. Los secretos vienen de Secret Manager. La auditoría (EventoAuditoria) registra IP, user-agent, resultado y usuario, sin datos sensibles.

### Convenciones

- Código en inglés para la infraestructura técnica y en español para el dominio (Usuario, Cliente), de forma consistente. Las rutas de la API van en español.
- Un módulo de Nest por cada módulo lógico. Solo se importa lo que el módulo exporta explícitamente; sin ciclos (auth, registro y password-recovery → usuarios, clientes, tokens, notificaciones, auditoria).
- Cada operación de escritura multi-entidad corre dentro de prisma.$transaction en la capa application.
- Pruebas: unitarias con Jest para los services y el dominio, y e2e con supertest sobre una base de datos de pruebas. Cada criterio de aceptación de una HU tiene al menos un test.
- Los errores de negocio usan códigos estables (p. ej. CORREO_DUPLICADO, TOKEN_EXPIRADO, CUENTA_NO_VERIFICADA) que el frontend traduce a mensajes.

## Modelo de datos

### Usuario

**Atributos:** id uuid, correo, correoNormalizado único, passwordHash, nombres, apellidos, celular (10 dígitos), rol enum(CLIENTE,RECEPCION,ADMIN), estado enum(PENDIENTE_VERIFICACION,ACTIVA,BLOQUEADA,INACTIVA), correoVerificadoEn?, intentosFallidos, ultimoLoginEn?, creadoEn, actualizadoEn

**Relaciones:** 1–0..1 Cliente (solo si el rol es CLIENTE), 1–N TokenUnUso, 1–N Sesion, 1–N AceptacionLegal

_HUs: HU-001, HU-002, HU-003_

### Cliente (expediente)

**Atributos:** id, nombres, apellidos, correoNormalizado? único parcial, celular? indexado, origen enum(RECEPCION,AUTORREGISTRO), usuarioId? único, creadoEn

**Relaciones:** 0..1–1 Usuario

_HUs: HU-001_

### TokenUnUso

**Atributos:** id, usuarioId, tipo enum(VERIFICACION_CORREO,RESTABLECER_PASSWORD), tokenHash único, expiraEn, usadoEn?, creadoEn

**Relaciones:** N–1 Usuario

_HUs: HU-001, HU-003_

### Sesion

**Atributos:** id, usuarioId, familiaId, refreshTokenHash único, expiraEn, revocadaEn?, ip, userAgent, creadoEn

**Relaciones:** N–1 Usuario

_HUs: HU-002, HU-003_

### DocumentoLegal

**Atributos:** id, tipo enum(AVISO_PRIVACIDAD,TERMINOS), version, url/contenido, vigenteDesde, vigente bool

**Relaciones:** 1–N AceptacionLegal

_HUs: HU-001_

### AceptacionLegal

**Atributos:** id, usuarioId, documentoLegalId, aceptadoEn, ip

**Relaciones:** N–1 Usuario, N–1 DocumentoLegal

_HUs: HU-001_

### EventoAuditoria

**Atributos:** id, usuarioId?, tipo (REGISTRO, VERIFICACION, VINCULACION, LOGIN_OK, LOGIN_FALLIDO, LOGOUT, RESET_SOLICITADO, RESET_COMPLETADO), resultado, ip, userAgent, metadata json, creadoEn

**Relaciones:** N–0..1 Usuario

_HUs: HU-001, HU-002, HU-003_

## Frontend

### Estructura de carpetas

```
apps/frontend/
  README.md
  Dockerfile              # producción: build + nginx
  Dockerfile.dev
  nginx.conf              # fallback SPA, /healthz, escucha en $PORT
  package.json  vite.config.ts  tsconfig.json  .env.example
  src/
    main.tsx  App.tsx
    app/          {router.tsx, theme.ts, queryClient.ts, providers.tsx}
    api/          {http.ts (fetch + refresh automático), schema.d.ts (generado con openapi-typescript)}
    auth/         {AuthContext.tsx, RequireAuth.tsx, RequireRole.tsx, rutaInicialPorRol.ts}
    features/
      registro/   {pages/, components/, hooks/}
      login/
      password-recovery/
      cliente/    {MisVehiculosPage.tsx (placeholder)}
      interno/    {InicioInternoPage.tsx (placeholder)}
    shared/       {components/, validation/ (reglas de contraseña, celular de 10 dígitos)}
    test/         setup de Vitest + Testing Library, MSW
```

### Módulos y pantallas

- **registro** — Crear cuenta (formulario con aceptación del aviso de privacidad y los términos), Revisa tu correo (con reenvío), Resultado de verificación (/verificar-correo?token=) _(HUs: HU-001)_
- **login** — Iniciar sesión, Menú de usuario con Cerrar sesión _(HUs: HU-002)_
- **password-recovery** — Olvidé mi contraseña, Restablecer contraseña (/restablecer?token=) con estados de enlace vigente, expirado o usado _(HUs: HU-003)_
- **cliente (shell)** — Mis vehículos (placeholder, destino del login de CLIENTE) _(HUs: HU-002)_
- **interno (shell)** — Inicio del personal interno (placeholder según rol) _(HUs: HU-002)_

### Estado y acceso a datos

TanStack Query para todo el estado del servidor (useMutation en registro, login y restablecimiento; useQuery en /auth/me y en los documentos legales). El access token vive solo en memoria (AuthContext). Al recargar la página se llama a /auth/refresh usando la cookie. El cliente HTTP reintenta una vez tras un 401 pasando por refresh. Al hacer logout se limpia la caché de Query. Los formularios usan react-hook-form + zod, con reglas equivalentes a las del backend. Los tipos de la API se generan desde /api/docs-json.

### Convenciones

- Organización por features. Las páginas solo componen, y los hooks useXxxMutation encapsulan las llamadas.
- Las rutas protegidas usan RequireAuth/RequireRole. Tras el login se redirige a la rutaInicial que devuelve el backend (CLIENTE → /mis-vehiculos).
- Los mensajes de error se traducen desde los códigos de negocio del backend en un único mapa.
- Pruebas con Vitest + Testing Library + MSW para cada escenario de las HUs.
- Solo componentes MUI con un theme central, sin CSS suelto.

## Despliegue

Se despliegan dos servicios en Cloud Run desde el monorepo, más Cloud SQL (PostgreSQL) y Secret Manager.

1) **Backend** (itz-agenda-api)
- Dockerfile de producción: `apps/backend/Dockerfile`.
- Construcción multi-stage: primero `node:20-alpine` como build (npm ci, prisma generate, nest build); luego `node:20-alpine` como runtime con dependencias de producción, dist y prisma, ejecutado con usuario no root.
- Puerto: `PORT=8080`.
- Healthcheck: `GET /api/health`, usado como startup y liveness probe.
- Arranque: `npx prisma migrate deploy && node dist/main.js`, o bien las migraciones como Cloud Run Job.
- Variables de entorno: `DATABASE_URL` (socket de Cloud SQL, desde un secreto), `JWT_ACCESS_SECRET` (secreto), `JWT_ACCESS_TTL=15m`, `REFRESH_TTL_DAYS`, `VERIFICACION_TTL_HORAS`, `RESET_TTL_MINUTOS`, `FRONTEND_URL` (para CORS y para los enlaces de los correos), `MAIL_ADAPTER` (smtp|console), `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` (secreto), `MAIL_FROM`, `NODE_ENV`.

2) **Frontend** (itz-agenda-web)
- Dockerfile de producción: `apps/frontend/Dockerfile`.
- Construcción multi-stage: `node:20-alpine` ejecuta `npm ci` y `vite build`; luego `nginx:1.27-alpine` sirve dist con fallback SPA.
- Puerto: 8080.
- Healthcheck: `GET /healthz` (lo responde nginx).
- Variables de entorno: `VITE_API_BASE_URL` se inyecta en el build. Se recomienda el mismo dominio vía Load Balancer (/api → backend) para que la cookie SameSite=Strict funcione.

Además, cada app tiene un `Dockerfile.dev` y hay un `docker-compose.yml` en la raíz (postgres, mailpit, api, web) para desarrollo local.

**CI (GitHub Actions)**
- En cada PR, por app afectada: lint, typecheck, pruebas con Jest (backend, con un servicio postgres para e2e) y Vitest (frontend), `prisma validate` y build de las imágenes Docker.
- En main: build y push a Artifact Registry con el tag del SHA, y `gcloud run deploy` de ambos servicios con autenticación Workload Identity Federation.

Raíz del repo: `README.md`, `docker-compose.yml`, `.github/workflows/`, `apps/backend/README.md`, `apps/frontend/README.md` y `docs/adr/`.

## Decisiones

### Estilo arquitectónico

**Decisión:** Monolito modular NestJS y SPA React en un monorepo (apps/backend, apps/frontend) con workspaces de npm.

**Por qué:** El stack exige 0 microservicios. El alcance de identidad es pequeño y conviene un solo despliegue de la API.

**Alternativas descartadas:** Microservicio de identidad separado; Nx/Turborepo (demasiado para dos apps).

### Sesión con JWT y logout real

**Decisión:** Access JWT de 15 min en memoria, y refresh opaco rotativo en cookie httpOnly guardado con hash en la tabla Sesion.

**Por qué:** HU-002 exige cerrar sesión para que nadie más la use. Un JWT puro no se puede revocar, y localStorage está expuesto a XSS.

**Alternativas descartadas:** JWT de larga duración en localStorage; lista negra de JWT; sesiones de servidor sin JWT.

### Tokens de verificación y restablecimiento

**Decisión:** Una sola tabla TokenUnUso por tipo, con hash SHA-256, expiración y consumo atómico (UPDATE condicional).

**Por qué:** HU-001 y HU-003 comparten el mismo patrón. El uso único y la expiración se garantizan en la base de datos.

**Alternativas descartadas:** JWT firmados como enlace (no se pueden invalidar tras usarse); tablas separadas por tipo.

### Vinculación al expediente

**Decisión:** Usuario (credenciales) y Cliente (expediente) son entidades separadas. La vinculación ocurre al verificar el correo, en una transacción, con índices únicos que impiden duplicados.

**Por qué:** HU-001 dice que recepción ya puede tener registrado al cliente sin cuenta. Vincular solo tras verificar el correo evita que alguien se apropie de un expediente ajeno.

**Alternativas descartadas:** Vincular al registrarse (antes de comprobar la propiedad del correo); fusionar Usuario y Cliente en una tabla.

### Correo

**Decisión:** Puerto MailerPort con un adaptador SMTP (proveedor configurable) y un adaptador de consola o Mailpit en desarrollo. Envío síncrono tras el commit.

**Por qué:** HU-001 y HU-003 dependen del correo, pero todavía no hay proveedor definido. Una cola sería excesiva para este volumen.

**Alternativas descartadas:** Pub/Sub con worker (más infraestructura); acoplarse ya a un SDK de un proveedor.

### Contrato de la API

**Decisión:** @nestjs/swagger con plugin CLI, UI en /api/docs, spec en /api/docs-json y tipos del frontend generados con openapi-typescript.

**Por qué:** El contrato es la única fuente de verdad entre backend y frontend y se documenta desde el primer paquete.

**Alternativas descartadas:** Tipos escritos a mano en el frontend; un paquete compartido de tipos en TypeScript.

### Despliegue

**Decisión:** Dos servicios en Cloud Run (api con Node y web con nginx), Cloud SQL Postgres y Secret Manager, idealmente detrás del mismo dominio.

**Por qué:** Cada servicio escala y se despliega de forma independiente, y el mismo origen simplifica cookies y CORS.

**Alternativas descartadas:** Servir la SPA desde NestJS (acopla los builds); Firebase Hosting (sale de la restricción de Cloud Run).

### Protección contra enumeración y abuso

**Decisión:** Respuestas neutras en login, solicitud de restablecimiento y reenvío, más throttler por IP y por correo, y auditoría de intentos.

**Por qué:** Buenas prácticas implícitas en HU-002 y HU-003 (correo no registrado) con un costo bajo.

**Alternativas descartadas:** Mensajes que revelan si el correo existe; CAPTCHA desde el inicio.

## Supuestos y preguntas abiertas

- Las HUs llegaron truncadas. Faltan escenarios de HU-001 (a partir de E2 en adelante), de HU-002 (desde I1) y de HU-003 (desde 'Correo no reg...'). Hay que confirmar los mensajes exactos y los casos de error.
- Criterio de vinculación al expediente (HU-001). ¿Se vincula por correo, por celular o por ambos? ¿Qué pasa si coincide el celular pero no el correo, o si hay varios expedientes candidatos? Supuesto: se vincula automáticamente solo si el correo coincide de forma única. Si solo coincide el celular, se crea uno nuevo y queda marcado para revisión de recepción (a confirmar).
- ¿Cuánto duran las vigencias? Supuesto: enlace de verificación 24 h, enlace de restablecimiento 60 min, refresh 7 días. ¿Existe bloqueo por intentos fallidos de login, y con qué umbral?
- Política de contraseña. Supuesto: mínimo 8 caracteres con letra y número. Confirmar las reglas exactas.
- Roles internos y sus pantallas iniciales. Supuesto: RECEPCION y ADMIN. Hace falta la lista de roles y la ruta inicial de cada uno. ¿Quién da de alta al personal interno? Supuesto: un seed o alta manual fuera de alcance.
- ¿Qué pasa si un usuario intenta iniciar sesión con la cuenta pendiente de verificación: se le bloquea con la opción de reenviar el correo? Supuesto: sí.
- Proveedor de correo y dominio remitente (SendGrid, SMTP de Google Workspace, etc.). Cambia las credenciales y la configuración de SPF/DKIM.
- Dominio de producción. ¿Frontend y API bajo el mismo dominio (Load Balancer) o en dominios de Cloud Run separados? Afecta la configuración de la cookie de refresh (SameSite) y de CORS.
- Textos y versiones del aviso de privacidad y de los términos: ¿quién los provee y hay que re-aceptarlos cuando cambian?
- 'Mis vehículos' queda como placeholder, porque su funcionalidad no está en estas HUs.
