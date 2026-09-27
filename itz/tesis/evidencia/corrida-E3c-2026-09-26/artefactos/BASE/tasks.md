---
hu_id: BASE
fase: descompuesta
total_paquetes: 5
fecha_descomposicion: 2026-09-26
---

# Paquetes de trabajo — BASE: Esqueleto del aplicativo

- **PT-01** (infra, loom-piloto-e3c-claude-cli) — Entorno de desarrollo dockerizado del monorepo
- **PT-02** (backend, loom-piloto-e3c-claude-cli) — Base del backend NestJS: configuración, Prisma, Swagger y health · depende de PT-01
- **PT-03** (backend, loom-piloto-e3c-claude-cli) — Seguridad base y puertos transversales del backend · depende de PT-01, PT-02
- **PT-04** (frontend, loom-piloto-e3c-claude-cli) — Shell del frontend React + MUI · depende de PT-01
- **PT-05** (infra, loom-piloto-e3c-claude-cli) — Dockerfiles de producción y CI/CD a Cloud Run · depende de PT-01, PT-02, PT-03, PT-04
