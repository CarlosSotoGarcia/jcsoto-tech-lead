---
hu_id: BASE
fase: descompuesta
total_paquetes: 5
fecha_descomposicion: 2026-09-21
---

# Paquetes de trabajo — BASE: Esqueleto del aplicativo

- **PT-01** (infra, loom-piloto-e1c-claude-cli) — Entorno de desarrollo dockerizado (compose, Dockerfiles dev, .env.example, README raíz)
- **PT-02** (backend, loom-piloto-e1c-claude-cli) — Base del backend: Spring Boot, config, Flyway, Swagger y README · depende de PT-01
- **PT-03** (backend, loom-piloto-e1c-claude-cli) — Seguridad base del backend: Spring Security stateless y CORS · depende de PT-02
- **PT-04** (frontend, loom-piloto-e1c-claude-cli) — Shell del frontend Angular: layout, rutas, cliente HTTP y README · depende de PT-01
- **PT-05** (infra, loom-piloto-e1c-claude-cli) — Despliegue: Dockerfiles de producción y CI con GitHub Actions · depende de PT-01, PT-02, PT-03, PT-04
