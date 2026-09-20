---
hu_id: HU-003
fase: descompuesta
total_paquetes: 2
fecha_descomposicion: 2026-09-19
---

# Paquetes de trabajo — HU-003: Cerrar sesión voluntariamente y expiración por inactividad

- **PT-01** (backend, loom-piloto-e2-gemini) — Backend - Endpoint de logout y revocación de tokens JWT · depende de BASE/PT-02 · cubre TC-001, TC-006
- **PT-02** (frontend, loom-piloto-e2-gemini) — Frontend - Temporizador de inactividad, logout, sincronización multipestaña y guardias de seguridad · depende de BASE/PT-03, PT-01 · cubre TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007
