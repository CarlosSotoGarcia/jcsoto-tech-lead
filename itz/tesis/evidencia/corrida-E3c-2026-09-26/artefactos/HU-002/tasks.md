---
hu_id: HU-002
fase: descompuesta
total_paquetes: 4
fecha_descomposicion: 2026-09-26
---

# Paquetes de trabajo — HU-002: Inicio y cierre de sesión con correo y contraseña, con redirección por rol

- **PT-01** (backend, loom-piloto-e3c-claude-cli) — Backend: login con correo y contraseña, bloqueo por intentos y auditoría de acceso · depende de BASE/PT-02, BASE/PT-01, BASE/PT-05 · cubre TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021, TC-022, TC-023, TC-024, TC-025, TC-026, TC-037, TC-038, TC-039
- **PT-02** (backend, loom-piloto-e3c-claude-cli) — Backend: sesión (refresh, logout, /me), expiración por inactividad del personal y permisos por rol · depende de BASE/PT-02, BASE/PT-01, BASE/PT-05, PT-01 · cubre TC-009, TC-010, TC-011, TC-012, TC-027, TC-028, TC-029, TC-030, TC-031, TC-032, TC-033, TC-034, TC-037, TC-038, TC-039
- **PT-03** (frontend, loom-piloto-e3c-claude-cli) — Frontend: pantalla de login con validación, mensajes de error y redirección por rol · depende de BASE/PT-04, BASE/PT-01, BASE/PT-05, PT-01 · cubre TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021, TC-022, TC-023, TC-024, TC-025, TC-035, TC-036, TC-038
- **PT-04** (frontend, loom-piloto-e3c-claude-cli) — Frontend: cierre de sesión, sesión expirada y rutas protegidas por rol · depende de BASE/PT-04, BASE/PT-01, BASE/PT-05, PT-02, PT-03 · cubre TC-009, TC-010, TC-011, TC-012, TC-027, TC-028, TC-029, TC-030, TC-031, TC-032, TC-033, TC-034
