---
hu_id: BASE
fase: descompuesta
total_paquetes: 5
fecha_descomposicion: 2026-09-19
---

# Paquetes de trabajo — BASE: Esqueleto del aplicativo

- **PT-01** (infra, loom-piloto-e1c-claude-cli) — Entorno de desarrollo dockerizado (compose, Dockerfiles dev, README raíz)
- **PT-02** (backend, loom-piloto-e1c-claude-cli) — Base del backend: proyecto Spring Boot, módulos, Flyway y Swagger · depende de PT-01
- **PT-03** (backend, loom-piloto-e1c-claude-cli) — Seguridad base del backend: SecurityFilterChain, CORS y utilidades de token · depende de PT-02
- **PT-04** (frontend, loom-piloto-e1c-claude-cli) — Shell del frontend Angular: layout, rutas lazy, cliente HTTP y tests · depende de PT-01
- **PT-05** (infra, loom-piloto-e1c-claude-cli) — Dockerfiles de producción y CI/CD por carpeta · depende de PT-01, PT-02, PT-04
