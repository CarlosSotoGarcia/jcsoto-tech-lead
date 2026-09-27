---
hu_id: HU-001
fase: descompuesta
total_paquetes: 4
fecha_descomposicion: 2026-09-26
---

# Paquetes de trabajo — HU-001: Autorregistro de cliente en el portal del taller con verificación de correo y vinculación a expediente existente

- **PT-01** (backend, loom-piloto-e3c-claude-cli) — Backend: alta de cuenta de cliente (POST /registro) con documentos legales, política de contraseña y auditoría · depende de BASE/PT-02, BASE/PT-01, BASE/PT-05 · cubre TC-001, TC-002, TC-003, TC-007, TC-008, TC-009, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-021, TC-022, TC-023, TC-024, TC-025, TC-030, TC-034
- **PT-02** (backend, loom-piloto-e3c-claude-cli) — Backend: verificación de correo, reenvío del enlace y vinculación al expediente de cliente · depende de BASE/PT-02, BASE/PT-01, BASE/PT-05, PT-01 · cubre TC-004, TC-005, TC-006, TC-010, TC-011, TC-016, TC-020, TC-026, TC-027, TC-028, TC-029, TC-031, TC-032, TC-033, TC-034
- **PT-03** (frontend, loom-piloto-e3c-claude-cli) — Frontend: pantalla Crear cuenta y Revisa tu correo con reenvío · depende de BASE/PT-04, BASE/PT-01, BASE/PT-05, PT-01, PT-02 · cubre TC-001, TC-002, TC-003, TC-007, TC-008, TC-009, TC-013, TC-014, TC-015, TC-017, TC-018, TC-021, TC-023, TC-026, TC-034, TC-035
- **PT-04** (frontend, loom-piloto-e3c-claude-cli) — Frontend: pantalla Resultado de verificación (/verificar-correo?token=) · depende de BASE/PT-04, BASE/PT-01, BASE/PT-05, PT-02, PT-03 · cubre TC-004, TC-005, TC-010, TC-027, TC-028, TC-029
