---
hu_id: HU-001
fase: descompuesta
total_paquetes: 2
fecha_descomposicion: 2026-09-19
---

# Paquetes de trabajo — HU-001: Iniciar sesión con correo y contraseña

- **PT-01** (backend, loom-piloto-e1c-claude-cli) — Backend: módulo users + auth login, /users/me, seguridad JWT y auditoría · depende de BASE/PT-02 · cubre TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021
- **PT-02** (frontend, loom-piloto-e1c-claude-cli) — Frontend: pantalla de login, guard de rutas, interceptor JWT y home protegida · depende de BASE/PT-04, PT-01 · cubre TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021
