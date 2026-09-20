---
proyecto: PILOTO E2 ITZ Inventarios (Gemini)
repositorio: https://github.com/CarlosSotoGarcia/loom-piloto-e2-gemini
tipo_repositorio: fullstack
modo: fundacional
fase: arquitectura_definida
fecha: 2026-09-19
hus_analizadas: 3
---

# Arquitectura — loom-piloto-e2-gemini

Monolito modular en monorepo que implementa el control de acceso, autenticación con JWT, recuperación autónoma de contraseña y cierre de sesión por inactividad para el sistema PILOTO E2 ITZ Inventarios. El backend está construido en Java con Spring Boot, Spring Security, JPA y Flyway, exponiendo una API documentada con Swagger/OpenAPI. El frontend está desarrollado con Angular, PrimeNG y Tailwind CSS, y el despliegue se automatiza mediante contenedores Docker en GCP Cloud Run.

## Backend

### Capas

- **Controlador (REST API)** — Recepción de peticiones HTTP, validación de DTOs y mapeo de respuestas con OpenAPI.
- **Servicio (Negocio)** — Lógica de negocio, autenticación, generación/validación de JWT y envío de correos.
- **Persistencia (Repositorio)** — Interfaces Spring Data JPA para acceso a la base de datos relacional.
- **Dominio (Entidades y DTOs)** — Modelos de datos persistentes mapeados con JPA/Hibernate y DTOs transformados con MapStruct.

### Módulos

- **Auth** — Gestión de inicio de sesión, emisión y revocación de tokens JWT, e invalidación de sesión. _(HUs: HU-001, HU-003)_
- **Usuarios** — Administración de información de usuarios, roles y permisos de acceso. _(HUs: HU-001)_
- **Notificaciones** — Generación de tokens de restablecimiento y envío de correos transaccionales para recuperación de clave. _(HUs: HU-002)_

### API y Swagger/OpenAPI

- **Herramienta:** springdoc-openapi-starter-webmvc-ui
- **UI de Swagger:** `/swagger-ui.html`
- **Especificación OpenAPI:** `/v3/api-docs`
- **Convención:** Controladores anotados con @Tag, @Operation y @ApiResponse. DTOs anotados con @Schema y validaciones Jakarta Bean Validation (@NotBlank, @Email).

| Método | Ruta | Descripción | HUs |
|---|---|---|---|
| POST | `/api/v1/auth/login` | Autentica usuario con email y contraseña, retornando token JWT y datos de perfil | HU-001 |
| POST | `/api/v1/auth/logout` | Invalida el token JWT activo del usuario cerrando la sesión explícitamente | HU-003 |
| POST | `/api/v1/auth/forgot-password` | Solicita el restablecimiento de contraseña enviando token por correo electrónico | HU-002 |
| POST | `/api/v1/auth/reset-password` | Restablece la contraseña del usuario utilizando el token recibido por correo | HU-002 |
| GET | `/api/v1/users/me` | Obtiene la información del perfil del usuario autenticado actual | HU-001 |

### Estructura de carpetas

```
/
├── README.md
├── backend/
│   ├── README.md
│   ├── pom.xml
│   └── src/
│       ├── main/
│       │   ├── java/com/itz/inventarios/
│       │   │   ├── Application.java
│       │   │   ├── auth/
│       │   │   │   ├── controller/
│       │   │   │   ├── service/
│       │   │   │   ├── dto/
│       │   │   │   └── repository/
│       │   │   ├── users/
│       │   │   │   ├── controller/
│       │   │   │   ├── service/
│       │   │   │   ├── entity/
│       │   │   │   └── repository/
│       │   │   ├── notifications/
│       │   │   │   └── service/
│       │   │   └── config/
│       │   │       ├── SecurityConfig.java
│       │   │       └── OpenApiConfig.java
│       │   └── resources/
│       │       ├── application.yml
│       │       └── db/migration/
│       │           └── V1__init_schema.sql
│       └── test/
└── frontend/
    ├── README.md
    └── ...
```

### Persistencia

Spring Data JPA con ORM Hibernate y migraciones de esquema gestionadas mediante Flyway.

### Seguridad

Spring Security Stateless basado en tokens JWT. Incluye filtro de autenticación personalizado, cifrado de contraseñas con BCrypt y lista de revocación de tokens para logout explícito.

### Convenciones

- Inyección de dependencias por constructor utilizando Lombok @RequiredArgsConstructor.
- Uso de MapStruct para la conversión bidireccional entre entidades de dominio y DTOs.
- Manejo centralizado de excepciones con @RestControllerAdvice y ResponseEntityExceptionHandler.
- Nombres de tablas en plural minúscula y columnas en snake_case.

## Modelo de datos

### Usuario

**Atributos:** id (UUID), email (String, Unique), password_hash (String), nombre (String), activo (Boolean), fecha_creacion (Timestamp)

**Relaciones:** Rol (ManyToOne)

_HUs: HU-001, HU-002_

### Rol

**Atributos:** id (Long), codigo (String, Unique), descripcion (String)

**Relaciones:** Usuario (OneToMany)

_HUs: HU-001_

### TokenRestablecimiento

**Atributos:** id (UUID), token (String, Unique), usuario_id (UUID), fecha_expiracion (Timestamp), usado (Boolean)

**Relaciones:** Usuario (ManyToOne)

_HUs: HU-002_

### SesionRevocada

**Atributos:** id (UUID), token_identifier (String), fecha_revocacion (Timestamp)

**Relaciones:** —

_HUs: HU-003_

## Frontend

### Estructura de carpetas

```
frontend/
├── README.md
├── package.json
├── angular.json
├── tailwind.config.js
└── src/
    ├── app/
    │   ├── core/
    │   │   ├── guards/
    │   │   │   └── auth.guard.ts
    │   │   ├── interceptors/
    │   │   │   └── jwt.interceptor.ts
    │   │   └── services/
    │   │       ├── auth.service.ts
    │   │       └── inactivity.service.ts
    │   ├── features/
    │   │   └── auth/
    │   │       ├── pages/
    │   │       │   ├── login-page/
    │   │       │   ├── forgot-password-page/
    │   │       │   └── reset-password-page/
    │   │       └── components/
    │   │           └── login-form/
    │   └── shared/
    │       └── components/
    └── assets/
```

### Módulos y pantallas

- **AuthModule** — Pantalla de Iniciar Sesión, Pantalla de Solicitud de Recuperación de Contraseña, Pantalla de Restablecer Contraseña _(HUs: HU-001, HU-002, HU-003)_
- **CoreModule** — Navegación principal y Layout general con opción de Cierre de Sesión _(HUs: HU-001, HU-003)_

### Estado y acceso a datos

Estado de autenticación y datos de usuario mantenidos en AuthService con RxJS BehaviorSubject. Guardado de JWT en sessionStorage y monitoreo de eventos de usuario (mousemove, keydown) para temporizador de inactividad.

### Convenciones

- Arquitectura modular por características (Feature Modules / Standalone Components) con Lazy Loading.
- Manejo de estado reactivo mediante RxJS (BehaviorSubject) para la sesión del usuario.
- Estilos definidos con Tailwind CSS combinados con componentes de UI PrimeNG.
- Pruebas unitarias e integración de componentes desarrolladas con Jest.

## Despliegue

Despliegue en Google Cloud Platform (GCP) utilizando contenedores en Cloud Run. Monorepo con Dockerfiles independientes para Backend (Spring Boot / JVM) y Frontend (Angular servido mediante Nginx). Base de datos relacional alojada en GCP Cloud SQL con conexión segura.

## Decisiones

### Estilo Arquitectónico

**Decisión:** Monolito modular con límites de módulos bien definidos.

**Por qué:** Reduce la complejidad de despliegue y sobrecostos operativos para el alcance inicial del sistema.

**Alternativas descartadas:** Arquitectura de microservicios descentralizados.

### Documentación de API

**Decisión:** Springdoc OpenAPI integrado en el backend Spring Boot.

**Por qué:** Permite generar automáticamente la especificación OpenAPI v3 y la UI de Swagger desde las anotaciones del código.

**Alternativas descartadas:** Generación manual de documentación Postman o Swagger estático.

### Manejo de Autenticación y Sesión

**Decisión:** Autenticación Stateless mediante JWT con lista de revocación.

**Por qué:** Garantiza escalabilidad horizontal en Cloud Run y aislamiento total entre frontend y backend.

**Alternativas descartadas:** Sesiones de Spring Security con estado HTTP (JSESSIONID).

### Cierre de Sesión por Inactividad

**Decisión:** Servicio de detección de inactividad con temporizador en Angular (RxJS) e interceptor de expiración.

**Por qué:** Cumple con la HU-003 cerrando la sesión cliente tras inactividad del usuario en terminales compartidas.

**Alternativas descartadas:** Detección pasiva únicamente mediante la expiración del token JWT.

### Gestión de Base de Datos

**Decisión:** Uso de Flyway para el control de versiones de base de datos.

**Por qué:** Garantiza la trazabilidad y ejecución segura de scripts SQL en entornos de prueba y producción.

**Alternativas descartadas:** Creación y modificación automática del esquema con ddl-auto=update de Hibernate.

## Supuestos y preguntas abiertas

- El límite de inactividad antes de cerrar sesión automáticamente no está parametrizado en la HU-003; se asume un tiempo predeterminado de 15 minutos de inactividad en el cliente.
- Se asume la disponibilidad de un servicio de correo transaccional (SMTP o API de envío como SendGrid/Cloud Mail) para el correcto funcionamiento de la HU-002.
- Se asume que la base de datos será PostgreSQL o MySQL en GCP Cloud SQL dentro del mismo entorno de proyecto.
