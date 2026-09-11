# Perfil técnico — Carlos Soto García

**Tech Lead · Arquitecto full-stack y cloud-native · Fundador de Novex Dynamics**

- **Ubicación:** Ciudad de México · Zacatecas
- **GitHub:** [CarlosSotoGarcia](https://github.com/CarlosSotoGarcia)
- **Idiomas de trabajo:** Español · Inglés técnico

> Perfil elaborado a partir del análisis del código, la documentación y la configuración de despliegue de los 19 repositorios de la cuenta `CarlosSotoGarcia` en GitHub (corte: 11 de septiembre de 2026). Los estados de cada proyecto se infieren de sus archivos de release, scripts de despliegue y documentación.

---

## Resumen

Diseña y construye **plataformas SaaS multi-tenant** de punta a punta: desde el PRD y los ADRs hasta el despliegue en **Google Cloud Run + Firebase Hosting**. Su stack de referencia es **FastAPI + Angular + MongoDB/PostgreSQL**, con experiencia adicional en **Java/Spring WebFlux con actores Pekko** y en integraciones de **IA generativa (Gemini)**, WhatsApp y pagos. Documenta con rigor, automatiza releases y forma a otros desarrolladores.

| | |
|---|---|
| Repositorios analizados | 19 |
| Productos SaaS en producción | 2 (Zity, Signalink) |
| Estrategias multi-tenant implementadas | 3 |
| Nubes públicas | 2 (GCP · AWS) |

---

## Habilidades técnicas

### Backend · Python — *stack principal, 12 repos*
FastAPI · Pydantic v2 · Motor / PyMongo · SQLAlchemy 2 async · Alembic (multi-schema) · Beanie ODM · APScheduler · PyJWT / python-jose · bcrypt · Authlib (OAuth) · slowapi · WebSockets · pytest + httpx · ruff · uv

### Backend · Java — *proyecto Monou (chat en tiempo real)*
Java 21 · Spring Boot 3 · WebFlux · Apache Pekko (actores) · Event sourcing · Cluster sharding · Distributed Pub/Sub · Maven · PostgreSQL / JDBC

### Frontend — *Angular 17 → 21, componentes standalone*
Angular 20/21 · TypeScript 5 · Signals · PrimeNG (Aura) · NgRx · Angular Material · RxJS · Tailwind CSS · Guards · Interceptors · Angular 14 libraries · React 19 + Vite · Chart.js

### Móvil — *distribución nativa y PWA de la misma base Angular*
Capacitor 8 (Android / iOS) · PWA · Service Worker · Gradle / Android Studio · Xcode CI en macOS · ZXing (escáner QR)

### Cloud · GCP — *despliegues reales en producción*
Cloud Run · Firebase Hosting · Artifact Registry · Cloud Build · Firestore (Native + API Mongo) · Cloud SQL · Pub/Sub · Cloud Tasks · Cloud Storage · Memorystore · Terraform · gcloud CLI

### Cloud · AWS — *ecosistema Monou*
S3 (archivado) · RDS PostgreSQL · CodeCommit · CodeArtifact (librerías npm privadas)

### Datos — *diseño de modelo y aislamiento por tenant*
MongoDB 7 · PostgreSQL 15 · Redis 7 · Firestore · Índices compuestos por tenant · schema-per-tenant · search_path dinámico

### DevOps y calidad — *entornos reproducibles y releases con un comando*
Docker multi-stage · Docker Compose · nginx (SPA + proxy /api, /ws) · GitHub Actions · Emuladores GCP locales · Scripts de release (Python / Bash) · Playwright e2e · Karma / Jasmine · pre-commit

### IA aplicada — *integración de LLMs en producto*
Gemini API (texto · audio) · System prompts especializados · Selección dinámica de modelo · OpenAI gpt-image-1 · Google AI Studio · Claude Code (CLAUDE.md)

### Integraciones — *APIs de terceros*
WhatsApp · Meta Cloud API · Twilio WhatsApp · Stripe · Google OAuth · SMTP · Facebook Graph API · TikTok OAuth · QR firmados HMAC-SHA256

### Arquitectura y proceso
Multi-tenancy (3 estrategias) · Router → Service → Repository · ADRs · PRD · RF/RNF · historias de usuario · Matriz de trazabilidad · RBAC por rol · JWT access + refresh · Diagramas Mermaid · Monorepo

### Liderazgo técnico — *mentoría y estándares*
Capacitación de equipos (FastAPI + Docker) · Boilerplates y guías de arquitectura · Convenciones de nomenclatura · Reportes técnicos para QA/frontend · Planes de desarrollo por fases

---

## Proyectos

### Novex Dynamics · productos SaaS

#### Zity — gestión de colonias privadas con acceso por QR
`zity` · **En producción · v1.0.0** · 75 commits · última actividad ago 2026 · Python + TypeScript · 40+ tests de integración

**Objetivo:** plataforma SaaS multi-tenant para administrar fraccionamientos: invitaciones con QR dinámico firmado, escáner para vigilantes, bitácora de accesos, viviendas, usuarios, pagos de mantenimiento, multas, incidencias, áreas comunes, notificaciones y solicitudes de alta. Cuatro roles: super admin, admin de colonia, residente y vigilante.

- Backend FastAPI + Motor con patrón Router → Service → Repository; multi-tenancy por `tenant_id` en cada documento y middleware que lo resuelve desde el JWT o el header.
- QR firmados con HMAC-SHA256, tokens de un solo uso, JWT con access (15 min) y refresh (7 días), correo SMTP fire-and-forget.
- Frontend Angular 20 + PrimeNG con signals, rutas lazy por tenant (`/:tenantSlug/*`) y detección de tenant por subdominio.
- Móvil: PWA con service worker y app nativa Android/iOS con Capacitor 8; CI de build iOS en GitHub Actions (macOS runner).
- Producción en GCP: Cloud Run + Artifact Registry, Firebase Hosting con rewrite `/api/**`, Firestore con API compatible MongoDB, dominio wildcard por tenant; script `release.py` para setup y deploy completo.
- Documentación: 9 documentos de arquitectura/API/seguridad, 20 guías HTML de usuario y material de marketing por canal.

*Stack:* FastAPI · Motor · MongoDB / Firestore · PyJWT · qrcode · Angular 20 · PrimeNG · Capacitor 8 · PWA · ZXing · Cloud Run · Firebase Hosting · GitHub Actions · pytest

#### FluxV2 — agendas y fidelización para negocios de servicios
`fluxv2` · **En desarrollo** · 9 commits · última actividad may 2026 · Python + TypeScript + HCL

**Objetivo:** SaaS multi-tenant para barberías, consultorios, gimnasios y salones: reservas online, notificaciones automáticas por WhatsApp (confirmación, T-24h, T-1h, agradecimiento), membresías y tarjetas de servicio, billetera digital, motor de promociones por recurrencia, CRM básico y walk-ins.

- Multi-tenancy **schema-per-tenant** en PostgreSQL 15: middleware que resuelve el slug y fija `search_path`; Alembic con migraciones separadas para el esquema público y para cada tenant.
- SQLAlchemy 2 async + asyncpg, Redis para disponibilidad en tiempo real, APScheduler para el despacho de notificaciones, Stripe para pagos, OTP por WhatsApp para clientes.
- Arquitectura orientada a eventos con Pub/Sub y Cloud Tasks; para desarrollo local escribió un **emulador propio de Cloud Tasks** en FastAPI y orquestó emuladores de Pub/Sub y GCS en Compose.
- Infraestructura como código con Terraform; dos apps Angular (panel admin con NgRx, portal cliente con signals y SSR).
- Decisiones registradas en 4 ADRs y un PRD completo de 6 módulos.

*Stack:* FastAPI · SQLAlchemy 2 · PostgreSQL · Alembic · Redis · Pub/Sub · Cloud Tasks · Cloud Storage · Terraform · Stripe · Meta WhatsApp API · Angular 20 · NgRx · uv · ruff

#### Flux — reservas de espacios con verificación por WhatsApp
`flux` · **MVP funcional** · 10 commits · última actividad mar 2026 · Python + TypeScript

**Objetivo:** primera versión de la plataforma de reservas. Un admin aprueba hosts, el host crea venues con horarios y capacidad, y los invitados reservan desde un link público `/book/<slug>` verificando su lugar por WhatsApp; lista de espera y expiración automática de reservas pendientes.

- FastAPI + Beanie ODM sobre MongoDB, WebSockets nativos para actualizaciones en vivo, rate limiting con slowapi, Google OAuth con Authlib.
- WhatsApp con proveedor intercambiable (Twilio o Meta) y fallback a consola en desarrollo.
- Angular 17 + Angular Material; nginx sirve el SPA y proxea `/api` y `/ws`.
- Suite e2e con Playwright del flujo de onboarding y un pipeline que graba un **video demo MP4** del producto (Playwright + ffmpeg).

*Stack:* FastAPI · Beanie · MongoDB · WebSockets · Authlib · Twilio · APScheduler · Angular 17 · Angular Material · Playwright · nginx

#### Agendix — agendas para negocios sobre la base Novex
`Agendix` · **Arquitectura definida** · 3 commits · última actividad jul 2026 · Público

**Objetivo:** producto de citas y disponibilidad de staff (barberías, spas, consultorios) que reutiliza la arquitectura de Zity (multi-tenancy, capas, RBAC, convenciones Angular) pero diverge en persistencia: **Cloud Firestore Native Mode** por estar 100 % en GCP desde el inicio.

- 7 documentos: arquitectura, visión y actores, RF, RNF, historias de usuario con criterios Dado/Cuando/Entonces, matriz de trazabilidad y plan de implementación.
- Plan explícito de bajo costo (≈ $0/mes con free tiers) con triggers definidos para escalar.

*Stack:* FastAPI · Firestore Native · Angular 20 · PrimeNG · Cloud Run · Firebase Hosting

#### Novex Dynamics — sitio corporativo y hub de marketing
`novexlandig` · **En producción** · 20 commits · última actividad sep 2026 · HTML + Python

**Objetivo:** landing del estudio (novexdynamics.com) con páginas de estado, changelog, aviso de privacidad y términos, más la planeación de marketing de todas las marcas.

- HTML estático + Tailwind vía CDN sin build; sistema de design tokens en `novex-brand.css`; deploy a Firebase Hosting con script que pide confirmación.
- Pipeline de contenido: manifest JSON como fuente de verdad, generación de imágenes con OpenAI, programación de publicaciones vía Facebook Graph API y OAuth de TikTok; brief para un agente de navegador.

*Stack:* HTML · Tailwind · Firebase Hosting · Python · OpenAI Images · Facebook Graph API · TikTok API

#### Orix — plantilla full-stack FastAPI + Angular + Docker
`orix` · **Boilerplate** · 3 commits · última actividad feb 2026

**Objetivo:** punto de partida reutilizable con patrón repositorio, capa de servicios, Pydantic v2, Angular standalone con signals y control de flujo moderno, hot-reload con `docker compose watch` y guías de arquitectura para agentes de código. Incluye un módulo de agenda pública como ejemplo.

*Stack:* FastAPI · Motor · Angular 17 · Docker Compose

---

### Signalink · traductor de español a Lengua de Señas Mexicana

#### Signalink — monolito full-stack
`signalink_monolitic` · **Desplegado en GCP** · 18 commits · última actividad dic 2025 · Python + TypeScript

**Objetivo:** convertir texto (y audio) en español a **glosas de LSM** y mostrar el video de cada seña; incluye la administración del diccionario de glosas con su enlace de video.

- Servicio Gemini con prompt lingüístico especializado (orden Tema-Comentario, deletreo de nombres propios, eliminación de artículos) y **selección dinámica del mejor modelo disponible** para audio.
- Backend por capas controller/service/repository; frontend Angular 20 + PrimeNG + Tailwind.
- Deploy con un script a Cloud Build → Artifact Registry → Cloud Run (backend y frontend), que además reescribe la URL del API en el build del frontend; base de datos Firestore con API Mongo.

*Stack:* FastAPI · Gemini API · MongoDB · Angular 20 · PrimeNG · Tailwind · Cloud Build · Cloud Run

#### Evolución del producto en tres repos
`signalink_backv2` (18) · `signalink` (23) · `signalink_backend` (6) · nov–dic 2025

- **signalink_backend** — primer microservicio: Gemini 1.5 Flash con `system_instruction` para LSM, PyMongo con reconexión, historias de usuario por épicas (MVP, gestión de diccionario, post-MVP).
- **signalink_backv2** — reescritura con arquitectura limpia, documentos API.md / ARCHITECTURE.md / DEPLOY.md, script de pruebas y contenedor listo para Cloud Run.
- **signalink** — frontend Angular 20 independiente con `BackendService` genérico documentado.

*Stack:* FastAPI · PyMongo · Gemini 1.5 · Angular 20 · Docker

#### Programa de formación del equipo Signalink
`signalink_training` · **Capacitación** · 40 commits · última actividad oct 2025 · 5 participantes

**Objetivo:** onboarding técnico del equipo antes de construir el producto. Cada participante tiene su carpeta con el mismo ejercicio guiado — una API de personas con FastAPI, validaciones Pydantic, MongoDB y Docker Compose — y el flujo de trabajo con Git en rama `develop`.

*Stack:* FastAPI · PyMongo · Docker Compose · Git flow · Mentoría

---

### ZenStock · punto de venta e inventario

#### ZenStock — inventario, POS y corte de caja con proyección de ventas
`zenstock_monolitic` (3) · `inventorysmarth` (12) · `inventory_back` (14) · **Desplegable en GCP** · dic 2025 · Python + TypeScript

**Objetivo:** sistema para pequeños comercios: catálogo de productos con folio y stock mínimo, punto de venta, movimientos de inventario, dashboard y reporte de caja. Incluye un módulo de **proyección de demanda a 30 días con Gemini** (prompt estructurado que devuelve JSON con proyecciones, top productos y análisis).

- Backend FastAPI por capas (controller / service / repository / model) sobre MongoDB; frontend Angular 20 + Tailwind; primero como repos separados y después unificado en monolito.
- Diagramas Mermaid de despliegue, dominio y secuencia; script de deploy a Cloud Run con Cloud Build.

*Stack:* FastAPI · MongoDB · Angular 20 · Tailwind · Gemini · Cloud Run · Mermaid

---

### Monou · consultoría para plataforma de torneos gaming

#### Chat en tiempo real para torneos (repo-bot-back / repo-bot-front)
`monou` · **Documentación de proyecto** · 10 commits · última actividad sep 2026 · código en AWS CodeCommit

**Objetivo:** sistema de chat WebSocket para torneos de la plataforma Monou, con salas jerárquicas (torneo → partida → equipo), comandos slash, moderación (mute/ban), difusiones programadas, temporizadores, reportes con evidencia a S3 y **cierre automático 48 h después del torneo con respaldo ZIP en S3**.

- Backend Java 21 + Spring Boot 3 WebFlux con **Apache Pekko**: un actor por sala con event sourcing (journal en PostgreSQL, snapshots), cluster sharding y Distributed Pub/Sub en UAT, passivación por inactividad.
- Frontend como librería Angular 14 publicada en AWS CodeArtifact + app demo.
- Este repo reúne el contexto: contratos de endpoints, modelo de datos, reporte técnico del cierre/archivado y notas de reconexión.

*Stack:* Java 21 · Spring WebFlux · Apache Pekko · Event sourcing · PostgreSQL · AWS S3 · CodeArtifact · Angular 14

---

### Laboratorios y pruebas
`geminy-interface` · `testmusica` · `argus` · `labs_python_fastapi` · ago 2025 – ene 2026

- **geminy-interface** — interfaz de consultas a Gemini en React 19 + Vite con el SDK `@google/genai`.
- **testmusica** — prueba de Angular 20 + Tailwind (lista de canciones con calificación por estrellas) generada desde Google AI Studio.
- **argus** y **labs_python_fastapi** — repos inicializados sin contenido aún.

*Stack:* React 19 · Vite · @google/genai · Angular 20

---

## Patrones que se repiten en su código

- **Multi-tenancy como decisión consciente.** Ha implementado tres estrategias distintas y documentado por qué: discriminador `tenant_id` por documento (Zity), schema-per-tenant en PostgreSQL con `search_path` (FluxV2) y subcolección por tenant en Firestore (Agendix).
- **Documenta antes y durante.** PRD, requerimientos funcionales y no funcionales, historias de usuario, ADRs, matriz de trazabilidad y guías de usuario; cada repo importante trae un `CLAUDE.md` con la arquitectura para trabajar con agentes de código.
- **Release con un comando.** Scripts `release.py` / `deploy.sh` que habilitan APIs, construyen imágenes, despliegan a Cloud Run y publican el frontend; Dockerfiles multi-stage con usuario no root en producción.
- **Entorno local fiel a producción.** Docker Compose con healthchecks, hot-reload y emuladores de Pub/Sub, Cloud Tasks y GCS — incluido un emulador de Cloud Tasks escrito por él cuando no existía uno oficial.
- **Capas estrictas y tipado.** Router → Service → Repository en backend; modelos `*Create / *Update / *InDB / *Public`; Angular standalone con signals, guards e interceptors; TypeScript estricto.
- **IA integrada al dominio.** No usa LLMs de forma genérica: prompts con reglas gramaticales de LSM, salida JSON estricta para proyecciones de ventas, selección dinámica de modelo y fallbacks ante errores.

---

## Línea de tiempo

| Periodo | Hito |
|---|---|
| ago 2025 | Laboratorios FastAPI y arranque del programa de formación Signalink. |
| oct–dic 2025 | Signalink pasa de microservicio a monolito desplegado en GCP; ZenStock (POS e inventario) se construye en paralelo. |
| feb–mar 2026 | Orix como plantilla base y Flux como primera plataforma de reservas con WhatsApp y e2e en Playwright. |
| abr–may 2026 | FluxV2 reescribe el producto con PostgreSQL schema-per-tenant, eventos y Terraform; Zity alcanza v1.0.0 en producción (18 de mayo). |
| jun–ago 2026 | Zity suma pagos, multas, incidencias, áreas comunes y apps móviles; Agendix queda definido; consultoría Monou con Java/Pekko. |
| sep 2026 | Sitio de Novex Dynamics y hub de marketing multi-marca en producción. |
