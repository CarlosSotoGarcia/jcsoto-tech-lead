---
hu_id: HU-001
fase: descompuesta
total_paquetes: 2
fecha_descomposicion: 2026-09-21
---

# Paquetes de trabajo — HU-001: Iniciar sesión con correo y contraseña

- **PT-01** (backend, loom-piloto-e1c-claude-cli) — Backend: modelo de datos, login JWT, /users/me y auditoría · depende de BASE/PT-02, BASE/PT-01, BASE/PT-05 · cubre TC-001, TC-002, TC-003, TC-004, TC-006, TC-007, TC-009, TC-010, TC-011, TC-012, TC-014
- **PT-02** (frontend, loom-piloto-e1c-claude-cli) — Frontend: pantalla de login, sesión, interceptor y guard · depende de BASE/PT-04, BASE/PT-01, BASE/PT-05, PT-01 · cubre TC-001, TC-002, TC-003, TC-004, TC-005, TC-007, TC-008, TC-009, TC-013
