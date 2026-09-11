# Perfil Técnico — Juan Carlos Soto

**Rol:** Tech Lead / Arquitecto de Software — Plataforma de crédito estructurado
**Organización:** CXC · Plataforma **LenderHub / Nuevos Negocios** (`suite.cxc.com.mx`)
**Contacto:** jsoto@cxc.com.mx
**Periodo evidenciado:** febrero 2025 — septiembre 2026 (19 meses, 391 días con actividad)
**Documento generado:** 10 de septiembre de 2026

---

## Resumen profesional

Ingeniero de software full-stack con perfil de **liderazgo técnico y arquitectura de plataforma**. Opero
el ciclo completo de un producto financiero B2B multi-lender: diseño la solución, escribo código en las
tres capas (backend Python, frontend Angular, infraestructura Terraform), integro el trabajo del resto
del equipo y sostengo la operación en producción.

La huella de trabajo combina dos ejes que rara vez coinciden en la misma persona:

- **Autoría concentrada en backend e infraestructura.** Mi código propio es mayoritariamente
  **Python/FastAPI (39%) e Infraestructura como Código (23%)**: soy el autor principal de cuatro de los
  siete microservicios y de prácticamente todo el Terraform de la plataforma. El frontend aparece en mi
  autoría de forma acotada (9%) pero constante, sobre las seis aplicaciones Angular.
- **Responsabilidad de integración y entrega, transversal a todo el producto.** He integrado
  **3,612 merge requests** en 22 proyectos de GitLab — incluidos ~1,540 en los repositorios frontend —
  gobernando el flujo `develop → staging → prod` de siete microservicios y seis aplicaciones Angular.
  Soy el punto por el que pasa el código del equipo antes de llegar a producción, también en las capas
  donde no soy el autor principal.

A eso se suma un tercer eje creciente desde 2026: **automatización del propio proceso de ingeniería**
(tooling interno de revisión, QA automatizado, reporting de actividad y agentes de IA aplicados a code
review), construido como producto interno y no como scripts desechables.

---

## Competencias principales

### Backend — Python / FastAPI

Diseño y mantenimiento de **siete microservicios** en producción, sobre dos generaciones de despliegue
(AWS Lambda heredado y Cloud Run actual).

- **FastAPI** con arquitectura por capas (`controllers` / `services` / `repository` / `schemas`) y por
  *vertical slices* (`features/<feature>/`), según el servicio.
- **Pydantic** para contratos y validación; **pytest** como suite de referencia (una migración que lideré
  cerró con 2,741 pruebas en verde).
- **MongoDB** — modelado, agregaciones, estrategia de índices y ajuste de *timeouts* de cliente.
  Migración de `facilities-api` al **driver asíncrono nativo de PyMongo (`AsyncMongoClient`)**, incluyendo
  un *gate* de CI que bloquea llamadas async sin `await` para impedir la regresión en ramas cortadas
  antes de la migración.
- **DynamoDB** en los servicios de identidad y notificaciones (AWS Lambda + Mangum + Serverless Framework).
- **BigQuery** como destino analítico del worker de ETL.
- Integraciones entre servicios sobre HTTP con `X-Api-Key`, **AWS Cognito** para autenticación JWT y RBAC
  por permiso a nivel de ruta.
- Gestión de dependencias con **uv** y **Poetry**; lideré la migración de Poetry → uv y de
  `requirements.txt` → `pyproject.toml`.

### Frontend — Angular 18 / Module Federation

Seis aplicaciones en una arquitectura de **micro-frontends**: un *shell* anfitrión que carga cuatro
remotos en tiempo de ejecución, más una librería compartida. Mi participación aquí es mixta: autoría
acotada pero sostenida (≈670 archivos `.ts`/`.html` propios, concentrados en `shell-mfe` y
`shell-admin-mfe`) y responsabilidad plena de integración y revisión (~1,540 MRs).

- **Angular 18** con componentes *standalone*, **Signals** como modelo de estado (sin NgRx), `inject()` y
  `OnPush`.
- **Module Federation** — configuración del host, resolución de remotos por entorno y depuración de
  fallos de carga cruzada.
- **PrimeNG 18 + Tailwind**; cadena de interceptores HTTP (caché → autorización → API key → loader →
  reintento → error → analítica) y caché opt-in con `@ngneat/cashew`.
- Librerías compartidas `@cxc/core` y `@cxc/ui-kit`, publicadas a un **Artifact Registry privado** de GCP
  y consumidas por los cinco micro-frontends.
- **Jest** (`jest-preset-angular`) para pruebas unitarias.

### Infraestructura — Terraform / GCP

La segunda área por volumen de contribución propia, después del backend: **1,370 archivos** de IaC
modificados (`.tf`, `.tfvars`, `.hcl`), repartidos entre las dos capas de los siete servicios y el
balanceador compartido.

- **Terraform** con patrón de **dos capas** `setup` (una vez por entorno: cuentas de servicio, Artifact
  Registry, triggers) → `app` (gestionada por CI/CD: Cloud Run, secretos), enlazadas por
  `terraform_remote_state` sobre GCS. Módulos versionados por tag desde un catálogo compartido.
- **GCP**: Cloud Run, Cloud Build, Cloud Tasks, Cloud Scheduler, **Cloud Workflows** (orquestación del ETL
  de fideicomisos), Pub/Sub, Firestore, Cloud Storage, Artifact Registry, Firebase Hosting, Secret Manager
  y un **balanceador de carga HTTPS compartido** que da ingreso a toda la suite.
- **Gestión de secretos con SOPS + AGE**: diseñé y ejecuté la migración de credenciales en texto plano a
  secretos cifrados en repositorio para los cinco servicios de la plataforma, con llaves servidas desde
  Secret Manager hacia Cloud Build.
- **Migración AWS → GCP** de la plataforma de Portfolio Monitoring (épica propia), conviviendo durante la
  transición con las rutas heredadas (EKS, CodeBuild/CodePipeline, Serverless Framework).
- **FinOps**: optimización de costos de Cloud Run (piso de instancias mínimas, dimensionamiento) y
  etiquetado de negocio (`team_info`) como requisito de despliegue.

### CI/CD y gobierno del repositorio

- **GitLab CI** y **Cloud Build** — pipelines de lint, pruebas, escaneo de seguridad, build de imagen
  (Kaniko) y despliegue por entorno.
- **Estrategia de ramas gitflow** con nomenclatura distinta por repositorio; gobierno de
  `develop`/`staging`/`prod`/`qa`/`master` y ramas de release versionadas.
- **Conventional Commits**, `gitlint`, `commitizen`, `pre-commit`, `gitleaks`, `semantic-release`.
- Protección de ramas, políticas de squash diferenciadas (nunca en *merges* de ancestría, siempre en
  `feature/* → develop`) y plantillas de MR con checklist de cumplimiento.

### Calidad, QA y seguridad

- **Playwright + Behave (Gherkin)** para automatización de UI contra entornos desplegados, con
  sincronización de casos verdes hacia **Squash TM**.
- Cobertura de pruebas exigida al 100% en los servicios backend, sin `pragma: no cover`.
- Revisión de seguridad sistemática sobre cada cambio: exposición de información, manejo de secretos,
  autenticación y autorización.
- Endurecimiento operativo: **logging estructurado** con `correlation_id` y `stack_trace`, códigos de
  estado correctos (404/422 en lugar de 500), `maxTimeMS` en agregaciones pesadas, eliminación de
  `reload=True` en producción y prevención de volcado del `.env` en trazas de pipeline.

### Automatización e IA aplicada a ingeniería

Construí herramienta interna propia para el proceso del equipo, no scripts aislados:

- **Tablero de vigilancia de Merge Requests** — seguimiento del estado de cada MR del equipo, con estado
  persistido en MongoDB contenerizado, reintento ante errores transitorios de GitLab y un *gate* de CI
  previo al despacho.
- **Reporte de actividad por ingeniero** — histórico semanal y visualización de tendencia.
- **Generación asistida de pruebas de humo QA** a partir de historias de Jira, con validación contra el
  entorno de staging antes de sincronizar.
- **Catálogo de *skills* de Claude Code** para el equipo: revisión automatizada de MR con criterio de
  arquitecto (incluyendo validación de migraciones de esquema y convenciones de Terraform), revisión de
  producción, generación de documentos de release a partir de una versión de Jira, documentación de
  arquitectura y reportes de actividad.

---

## Logros destacados

**Programa de remediación de rendimiento de la plataforma (2026)**
Diagnóstico y ejecución de una auditoría transversal que se tradujo en ~50 tareas etiquetadas
`performance-audit`, organizadas en cuatro frentes: backend (BE-01…BE-21), frontend (FE-01…FE-11),
infraestructura (INF) y defectos de producto (PRD-01…PRD-11). Incluyó indexación de siete colecciones de
snapshots, paginación y desanidado de endpoints de gráficas, caché en `charts/v2`, eliminación de
peticiones duplicadas y de componentes muertos que generaban tráfico real, y corrección de cálculos
financieros erróneos visibles para el cliente (overcollateralization en cero, sellos de cumplimiento
contra umbral incorrecto, datos cruzados entre lenders).

**Migración a driver asíncrono en `facilities-api`**
Migración completa al driver nativo async de PyMongo con *gate* de CI que impide la regresión en ramas
cortadas antes del cambio. La migración y el gate aterrizaron en el mismo commit para no dejar ventana
de divergencia. Suite final: 2,741 pruebas en verde.

**Migración de secretos a SOPS (Fase 1)**
Traslado de credenciales de los cinco servicios a secretos cifrados en repositorio, con rotación de
credenciales incluida y verificación de referencias indexadas — un control derivado de un plan previo
fallido y convertido en checklist permanente.

**Migración de Portfolio Monitoring a GCP**
Épica propia de traslado de la plataforma desde AWS hacia Google Cloud, con convivencia controlada de
ambas rutas de despliegue durante la transición.

**Configuración de nuevos lenders**
Puesta en marcha de la plataforma para instituciones financieras (BBVA, PROMECAP, entre otras),
abarcando configuración, datos y validación de extremo a extremo.

---

## Métricas de actividad

| Indicador | Valor | Fuente |
|---|---|---|
| Periodo con actividad registrada | feb 2025 — sep 2026 (19 meses) | Historial git local |
| Días distintos con commits | 391 | Historial git local |
| Commits totales bajo mi autoría | 6,083 | Historial git local |
| — de los cuales, desarrollo propio | 2,152 | `--no-merges` |
| — de los cuales, integración de equipo | 3,931 | `--merges` |
| Merge Requests únicos integrados | 3,612 | Metadatos de merge commits |
| Proyectos de GitLab con MRs integrados | 22 | Metadatos de merge commits |
| Repositorios con contribución propia | 19 | Historial git local |
| Incidencias de Jira reportadas | 1,489 | Jira (`reporter = currentUser()`) |
| Incidencias de Jira asignadas | 698 | Jira (`assignee = currentUser()`) |
| — Épicas e Historias asignadas | 180 | Jira |
| Épicas de las que soy autor | 10 | Jira |
| Tickets referenciados en mis commits | 1,694 claves únicas | Mensajes de commit |

**Distribución de mi código propio por tecnología** — 6,001 archivos modificados en commits sin merge,
excluyendo el repositorio espejo `lender-hub-design`:

| Tecnología | Archivos | Peso |
|---|---|---|
| Python (FastAPI) | 2,361 | 39% |
| Terraform / HCL (`.tf`, `.tfvars`, `.hcl`) | 1,370 | 23% |
| CI/CD (`.yml`, `.yaml`) | 537 | 9% |
| TypeScript (Angular) | 535 | 9% |
| Documentación (`.md`) | 323 | 5% |
| JSON / configuración | 215 | 4% |
| HTML (plantillas Angular) | 138 | 2% |
| Shell (`.sh`) | 76 | 1% |
| Gherkin (`.feature`) | 28 | <1% |

El peso del frontend en esta tabla mide **autoría**, no involucramiento: sobre las seis aplicaciones
Angular integré ~1,540 merge requests y sostengo el gobierno de sus ramas y releases.

**Tipo de commit propio:** 786 `feat` · 437 `chore` · 246 `fix` · 51 `docs` · 33 `test` ·
27 `refactor` · 26 `ci` · 20 `perf`.

---

## Mapa de dominio

| Sistema | Mi rol | Commits propios | MRs integrados |
|---|---|---|---|
| `trust-scheduler-worker` — ETL de fideicomisos, GCP Workflows, BigQuery, OnBase | Autor principal | 662 | 403 |
| `facilities-api` — operaciones de trust, analítica de portafolio | Autor principal | 273 | 417 |
| `data-studio-api` — estados financieros, extracción con IA vía Pub/Sub | Autor principal | 269 | 477 |
| `companies-api` — datos maestros de empresas y contactos | Autor principal | 206 | 280 |
| `shell-mfe` — host de Module Federation del portal | Integrador + desarrollo | 127 | 532 |
| `financials-api` — matriz financiera, covenants, gráficas | Desarrollo + integración | 96 | 245 |
| `shell-admin-mfe` — administración de usuarios y plantillas | Desarrollo + integración | 85 | 120 |
| `data-studio-mfe`, `financials-mfe`, `companies-mfe` | Integración + desarrollo | 199 | 801 |
| `identity-api`, `notifications-api` — Lambda/DynamoDB | Mantenimiento + migración | 58 | 130 |
| `ngx-new-business` — librerías `@cxc/core` y `@cxc/ui-kit` | Integrador | 5 | 83 |
| `load-balancer` — ingreso HTTPS compartido | Infraestructura | 5 | 3 |
| `lender-hub-develop` — tooling interno propio | Autor y dueño | 71 | 27 |
| `lender-hub` — automatización QA con Playwright/Behave | Desarrollo | 33 | 20 |

---

## Stack declarado

**Lenguajes** · Python · TypeScript · HCL/Terraform · Bash · SQL · Gherkin
**Backend** · FastAPI · Pydantic · pytest · uv · Poetry · Mangum · Serverless Framework
**Frontend** · Angular 18 · Module Federation · PrimeNG 18 · Tailwind · Angular Signals · RxJS · Jest
**Datos** · MongoDB · DynamoDB · BigQuery · Firestore
**Cloud (GCP)** · Cloud Run · Cloud Build · Cloud Workflows · Cloud Tasks · Cloud Scheduler · Pub/Sub ·
Secret Manager · Artifact Registry · Cloud Storage · Firebase Hosting · Load Balancing
**Cloud (AWS)** · Lambda · DynamoDB · Cognito · SES · EKS · CodeBuild/CodePipeline
**DevOps** · Terraform · Docker · GitLab CI · Cloud Build · SOPS + AGE · pre-commit · gitleaks ·
semantic-release · Kaniko
**QA** · Playwright · Behave · pytest · Jest · Squash TM
**Observabilidad** · Sentry · Prometheus · logging estructurado
**Metodología** · Gitflow · Conventional Commits · Code review · TDD · Arquitectura de microservicios ·
Micro-frontends · IaC · FinOps

---

## Perfil de trabajo

- **Opero de punta a punta.** Un mismo ticket puede llevarme del esquema de Mongo al componente Angular y
  al módulo de Terraform que lo despliega. No delego la capa que no me toca.
- **Trato la infraestructura como producto.** Convenciones escritas, módulos versionados por tag, secretos
  cifrados en repositorio y validaciones automatizadas antes del `apply`.
- **Integro más de lo que escribo.** Casi dos tercios de mi historial de commits son merges: el rol real es
  sostener la calidad de lo que entra a `develop` y a producción, no solo producir código propio.
- **Automatizo el proceso, no solo el producto.** Cuando la revisión de MRs se volvió un cuello de botella,
  construí el tablero y el pipeline de revisión asistida en lugar de absorber el costo manualmente.
- **Documento para que otros ejecuten.** Convenciones de rama, reglas de IaC, checklists de migración y
  guías de repositorio escritas como material operable por el equipo.

---

## Nota metodológica sobre las fuentes

Este perfil se construyó únicamente con evidencia verificable, recolectada el 10 de septiembre de 2026.

**Fuentes utilizadas**

- **Historial git local** de los 21 repositorios del workspace `c:\LenderHub`, filtrado por la identidad
  `jsoto@cxc.com.mx`. Cubre feb 2025 – sep 2026.
- **Metadatos de merge commits**, de los que se derivó la actividad de GitLab (ruta del proyecto, número de
  MR, rama origen y destino) sin necesidad de consultar la API.
- **Jira Cloud** (`cxcprojects.atlassian.net`), proyectos LEN (LenderHub), NN (Nuevos Negocios) y EM
  (Emisores), vía consultas JQL sobre la cuenta propia.
- **Historial local de sesiones de Claude Code** (`~/.claude/projects`): 428 sesiones, 269 con prompt
  recuperable.
- **Configuración personal de Claude Code**: 35 skills, 15 agentes, 8 hooks y 17 reglas instaladas.

**Limitaciones declaradas**

- **El historial de Claude en la web no es accesible** por vía programática; no se incorporó. Lo que aquí
  aparece proviene exclusivamente de las sesiones locales de Claude Code.
- **El historial local de Claude solo cubre agosto–septiembre de 2026** por la ventana de retención. De las
  269 sesiones con prompt, 231 son invocaciones automáticas (revisión de seguridad y revisión de MR) y
  solo 38 son instrucciones escritas directamente. La evidencia de uso de IA es por tanto de un mes, no
  del periodo completo.
- **No se consultó la API de GitLab.** El intento de obtener un token quedó bloqueado por la política local
  de credenciales, de modo que las cifras de MRs provienen de los merge commits ya presentes en los
  repositorios clonados. Esto subestima la actividad: no contabiliza MRs abiertos por mí que integró otra
  persona, ni comentarios de revisión, ni aprobaciones.
- Las cifras de archivos por tecnología **excluyen deliberadamente** el repositorio `lender-hub-design`,
  cuyo historial contiene copias masivas de los micro-frontends y distorsionaría el conteo.
- Los repositorios `claude-toolkit` y `claude-devkit` **no se atribuyen a este perfil**: su autoría
  corresponde a otra persona del equipo, aunque sus plugins están instalados en mi entorno.
