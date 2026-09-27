---
hu_id: HU-003
fase: descompuesta
total_paquetes: 4
fecha_descomposicion: 2026-09-26
---

# Paquetes de trabajo — HU-003: Recuperación de contraseña mediante enlace enviado por correo

- **PT-01** (backend, loom-piloto-e3c-claude-cli) — Backend: solicitud de enlace de restablecimiento (POST /auth/password/solicitar) · depende de BASE/PT-02, BASE/PT-01, BASE/PT-05 · cubre TC-001, TC-007, TC-009, TC-010, TC-011, TC-012, TC-013, TC-020, TC-023, TC-024, TC-025, TC-027
- **PT-02** (backend, loom-piloto-e3c-claude-cli) — Backend: validación del enlace y restablecimiento de contraseña con revocación de sesiones · depende de BASE/PT-02, BASE/PT-01, BASE/PT-05, PT-01 · cubre TC-002, TC-003, TC-004, TC-005, TC-006, TC-008, TC-014, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021, TC-022, TC-025, TC-027
- **PT-03** (frontend, loom-piloto-e3c-claude-cli) — Frontend: pantalla 'Olvidé mi contraseña' · depende de BASE/PT-04, BASE/PT-01, BASE/PT-05, PT-01 · cubre TC-001, TC-007, TC-009, TC-011, TC-012, TC-013, TC-023, TC-024
- **PT-04** (frontend, loom-piloto-e3c-claude-cli) — Frontend: pantalla 'Restablecer contraseña' con estados del enlace · depende de BASE/PT-04, BASE/PT-01, BASE/PT-05, PT-02 · cubre TC-002, TC-003, TC-004, TC-005, TC-006, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-026
