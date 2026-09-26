---
hu_id: HU-003
fase: descompuesta
total_paquetes: 2
fecha_descomposicion: 2026-09-21
---

# Paquetes de trabajo — HU-003: Cerrar sesión manualmente y expirar sesión por inactividad

- **PT-01** (backend, loom-piloto-e1c-claude-cli) — Backend: logout con revocación de jti, refresh deslizante y expiración validada en servidor · depende de BASE/PT-02, BASE/PT-01, BASE/PT-05 · cubre TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-009, TC-010, TC-014, TC-015, TC-016
- **PT-02** (frontend, loom-piloto-e1c-claude-cli) — Frontend: cierre de sesión manual, expiración por inactividad y sincronización entre pestañas · depende de BASE/PT-04, BASE/PT-01, BASE/PT-05, PT-01 · cubre TC-001, TC-002, TC-003, TC-004, TC-005, TC-007, TC-008, TC-009, TC-011, TC-012, TC-013, TC-014, TC-015
