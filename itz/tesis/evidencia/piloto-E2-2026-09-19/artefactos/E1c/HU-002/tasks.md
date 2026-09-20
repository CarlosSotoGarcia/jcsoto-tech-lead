---
hu_id: HU-002
fase: descompuesta
total_paquetes: 3
fecha_descomposicion: 2026-09-19
---

# Paquetes de trabajo — HU-002: Recuperar contraseña olvidada por correo electrónico

- **PT-01** (backend, loom-piloto-e1c-claude-cli) — Backend: solicitud de recuperación de contraseña (POST /auth/password/forgot) · depende de BASE/PT-02 · cubre TC-001, TC-003, TC-004, TC-005, TC-009, TC-013, TC-014, TC-015, TC-017
- **PT-02** (backend, loom-piloto-e1c-claude-cli) — Backend: restablecimiento de contraseña con token (POST /auth/password/reset) · depende de BASE/PT-02, PT-01 · cubre TC-002, TC-006, TC-007, TC-008, TC-010, TC-011, TC-012, TC-014, TC-016, TC-017
- **PT-03** (frontend, loom-piloto-e1c-claude-cli) — Frontend: pantallas de recuperación de contraseña y acceso desde login · depende de BASE/PT-04, PT-01, PT-02 · cubre TC-001, TC-002, TC-003, TC-005, TC-006, TC-007, TC-008, TC-010, TC-011, TC-015, TC-018
