---
hu_id: BASE
fase: descompuesta
total_paquetes: 4
fecha_descomposicion: 2026-09-19
---

# Paquetes de trabajo — BASE: Esqueleto del aplicativo

- **PT-01** (infra, loom-piloto-e2-gemini) — Entorno de desarrollo local dockerizado y orquestación base
- **PT-02** (backend, loom-piloto-e2-gemini) — Estructura base del backend, persistencia Flyway, seguridad base y Swagger UI · depende de PT-01
- **PT-03** (frontend, loom-piloto-e2-gemini) — Shell base del frontend, PrimeNG, Tailwind CSS y estado de autenticación · depende de PT-01
- **PT-04** (infra, loom-piloto-e2-gemini) — Dockerfiles de producción y Pipeline de Integración Continua (CI) · depende de PT-02, PT-03
