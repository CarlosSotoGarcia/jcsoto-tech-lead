---
hu_id: HU-002
fase: descompuesta
total_paquetes: 3
fecha_descomposicion: 2026-09-21
---

# Paquetes de trabajo — HU-002: Recuperar contraseña olvidada por correo electrónico

- **PT-01** (backend, loom-piloto-e1c-claude-cli) — Backend: solicitud de recuperación de contraseña (POST /auth/password/forgot) · depende de BASE/PT-02, BASE/PT-01, BASE/PT-05 · cubre TC-001, TC-003, TC-004, TC-007, TC-010, TC-011, TC-012, TC-013, TC-014
- **PT-02** (backend, loom-piloto-e1c-claude-cli) — Backend: restablecer contraseña con token (POST /auth/password/reset) · depende de BASE/PT-02, BASE/PT-01, BASE/PT-05, PT-01 · cubre TC-002, TC-005, TC-006, TC-008, TC-009, TC-014
- **PT-03** (frontend, loom-piloto-e1c-claude-cli) — Frontend: pantallas Recuperar contraseña y Restablecer contraseña · depende de BASE/PT-04, BASE/PT-01, BASE/PT-05, PT-02 · cubre TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-008
