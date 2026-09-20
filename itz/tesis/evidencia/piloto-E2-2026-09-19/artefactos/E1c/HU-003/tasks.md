---
hu_id: HU-003
fase: descompuesta
total_paquetes: 3
fecha_descomposicion: 2026-09-19
---

# Paquetes de trabajo — HU-003: Cerrar sesión manualmente y por expiración por inactividad

- **PT-01** (backend, loom-piloto-e1c-claude-cli) — Backend: refresh deslizante por inactividad, logout con revocación y auditoría de sesión · depende de BASE/PT-02 · cubre TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-009, TC-010, TC-011, TC-016, TC-017, TC-018, TC-019
- **PT-02** (frontend, loom-piloto-e1c-claude-cli) — Frontend: cierre de sesión manual, redirección y limpieza local de datos · depende de BASE/PT-04, PT-01 · cubre TC-001, TC-005, TC-006, TC-007, TC-008, TC-011, TC-012, TC-013, TC-014, TC-015
- **PT-03** (frontend, loom-piloto-e1c-claude-cli) — Frontend: IdleService con detección de actividad y expiración por inactividad · depende de BASE/PT-04, PT-01, PT-02 · cubre TC-002, TC-007, TC-008, TC-009, TC-010, TC-012, TC-013, TC-019
