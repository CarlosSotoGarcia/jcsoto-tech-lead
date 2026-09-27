---
hu_id: HU-001
tipo: smoke
corrida: 2
modo: completo
fecha: 2026-09-27
ambiente: https://taller-web-118746543308.us-central1.run.app
proveedor_ia: claude_cli
tcs_totales: 35
tcs_pasan: [TC-030]
tcs_fallan: [TC-033]
tcs_bloqueados: [TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021, TC-022, TC-023, TC-024, TC-025, TC-026, TC-027, TC-028, TC-029, TC-031, TC-032, TC-034, TC-035]
porcentaje_pasan: 3%
porcentaje_fallan: 3%
porcentaje_bloqueados: 94%
regresiones: []
---

# Smoke testing — HU-001: Autorregistro de cliente en el portal del taller con verificación de correo y vinculación a expediente existente

Corrida 2 (completo). Script de la HU: `smoke-02/HU-001_smoke.py`.

## Resumen

| Resultado | Casos | % |
|---|---:|---:|
| ✅ Pasa | 1 | 3% |
| ❌ Falla | 1 | 3% |
| ⛔ Bloqueado | 33 | 94% |
| **Total** | **35** | **100%** |

## Casos

| TC | Rol | Resultado | Cómo se resolvió | Motivo |
|---|---|---|---|---|
| TC-001 | invitado (sin sesión) para registrarse; admin para verificar el estado | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión) para registrarse; admin para verificar el estado» (pestaña Implementación). |
| TC-002 | invitado (sin sesión); admin para verificar | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión); admin para verificar» (pestaña Implementación). |
| TC-003 | invitado (sin sesión); admin para comprobar que no se duplicó | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión); admin para comprobar que no se duplicó» (pestaña Implementación). |
| TC-004 | cliente (cuenta recién registrada, sin verificar) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «cliente (cuenta recién registrada, sin verificar)» (pestaña Implementación). |
| TC-005 | cliente (cuenta sin verificar) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «cliente (cuenta sin verificar)» (pestaña Implementación). |
| TC-006 | recepcion (para la precondición); invitado→cliente (para registrarse); admin (para verificar) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «recepcion (para la precondición); invitado→cliente (para registrarse); admin (para verificar)» (pestaña Implementación). |
| TC-007 | invitado (sin sesión) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación). |
| TC-008 | invitado (sin sesión) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación). |
| TC-009 | invitado (sin sesión) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación). |
| TC-010 | cliente (cuenta sin verificar); admin para verificar el estado | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «cliente (cuenta sin verificar); admin para verificar el estado» (pestaña Implementación). |
| TC-011 | recepcion (precondición); invitado→cliente; admin (verificación) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «recepcion (precondición); invitado→cliente; admin (verificación)» (pestaña Implementación). |
| TC-012 | invitado (sin sesión); admin para consultar | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión); admin para consultar» (pestaña Implementación). |
| TC-013 | invitado (sin sesión) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación). |
| TC-014 | invitado (sin sesión) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación). |
| TC-015 | invitado (sin sesión) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación). |
| TC-016 | admin | ⛔ Bloqueado | agente (fallo confirmado) | Se inició sesión dos veces con la cuenta admin (pasos 11-13 y 16-18). Después, al abrir /interno/auditoria o /, la aplicación terminó en /login y nunca apareció |
| TC-017 | invitado (sin sesión) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación). |
| TC-018 | invitado (sin sesión) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación). |
| TC-019 | invitado (sin sesión) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación). |
| TC-020 | recepcion (precondición); invitado→cliente | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «recepcion (precondición); invitado→cliente» (pestaña Implementación). |
| TC-021 | invitado (sin sesión) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación). |
| TC-022 | invitado (sin sesión); admin para consultar | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión); admin para consultar» (pestaña Implementación). |
| TC-023 | invitado (sin sesión) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación). |
| TC-024 | invitado (sin sesión); admin | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión); admin» (pestaña Implementación). |
| TC-025 | invitado (sin sesión) x2; admin para verificar | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión) x2; admin para verificar» (pestaña Implementación). |
| TC-026 | cliente (cuenta sin verificar) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «cliente (cuenta sin verificar)» (pestaña Implementación). |
| TC-027 | cliente (cuenta activa) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «cliente (cuenta activa)» (pestaña Implementación). |
| TC-028 | invitado (sin sesión); admin para verificar | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión); admin para verificar» (pestaña Implementación). |
| TC-029 | cliente (cuenta sin verificar) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «cliente (cuenta sin verificar)» (pestaña Implementación). |
| TC-030 | cliente | ✅ Pasa | script |  |
| TC-031 | recepcion (precondición); invitado→cliente | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «recepcion (precondición); invitado→cliente» (pestaña Implementación). |
| TC-032 | recepcion (precondición); invitado→cliente; admin (auditoría) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «recepcion (precondición); invitado→cliente; admin (auditoría)» (pestaña Implementación). |
| TC-033 | admin | ❌ Falla | agente (fallo confirmado) | Inicié sesión como admin y la app me llevó a /interno, pero no hay ninguna entrada «Auditoría». Esperé el texto «Auditoría» y no apareció en 8 segundos. Abrí el |
| TC-034 | invitado (sin sesión); admin para revisar la cuenta y el log | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión); admin para revisar la cuenta y el log» (pestaña Implementación). |
| TC-035 | invitado (sin sesión) | ⛔ Bloqueado | sin cuenta | No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación). |

## TC-001 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión) para registrarse; admin para verificar el estado» (pestaña Implementación).


## TC-002 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión); admin para verificar» (pestaña Implementación).


## TC-003 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión); admin para comprobar que no se duplicó» (pestaña Implementación).


## TC-004 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «cliente (cuenta recién registrada, sin verificar)» (pestaña Implementación).


## TC-005 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «cliente (cuenta sin verificar)» (pestaña Implementación).


## TC-006 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «recepcion (para la precondición); invitado→cliente (para registrarse); admin (para verificar)» (pestaña Implementación).


## TC-007 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación).


## TC-008 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación).


## TC-009 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación).


## TC-010 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «cliente (cuenta sin verificar); admin para verificar el estado» (pestaña Implementación).


## TC-011 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «recepcion (precondición); invitado→cliente; admin (verificación)» (pestaña Implementación).


## TC-012 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión); admin para consultar» (pestaña Implementación).


## TC-013 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación).


## TC-014 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación).


## TC-015 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación).


## TC-016 — ⛔ Bloqueado

Se inició sesión dos veces con la cuenta admin (pasos 11-13 y 16-18). Después, al abrir /interno/auditoria o /, la aplicación terminó en /login y nunca apareció el texto «Auditoría». No se pudo entrar al módulo de Auditoría para filtrar por correo y comprobar los 3 eventos (alta de la cuenta, verificación y vinculación). La documentación de la API no se revisó porque ya no quedaban pasos para ejecutar el escenario completo. Parece un problema de sesión o de la cuenta de prueba, ajeno al caso. · Script: TimeoutError: Locator.click: Timeout 10000ms exceeded. Call log: - waiting for get_by_role("link", name=re.compile(r"Auditor[i�]a", re.IGNOR

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Auditoría» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
7. clic button «Menú de usuario» — ok: clic
8. ir a /interno/auditoria — ok: abrió https://taller-web-118746543308.us-central1.run.app/interno/auditoria
9. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
10. esperar texto «Auditoría» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
11. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
12. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
13. clic button «Iniciar sesión» — ok: clic
14. ir a /interno/auditoria — ok: abrió https://taller-web-118746543308.us-central1.run.app/interno/auditoria
15. clic link «Ir al inicio» — ok: clic
16. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
17. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
18. clic button «Iniciar sesión» — ok: clic
19. ir a /interno/auditoria — ok: abrió https://taller-web-118746543308.us-central1.run.app/interno/auditoria
20. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
21. esperar texto «Auditoría» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.

![captura](smoke-02/TC-016.png)

## TC-017 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación).


## TC-018 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación).


## TC-019 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación).


## TC-020 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «recepcion (precondición); invitado→cliente» (pestaña Implementación).


## TC-021 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación).


## TC-022 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión); admin para consultar» (pestaña Implementación).


## TC-023 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación).


## TC-024 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión); admin» (pestaña Implementación).


## TC-025 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión) x2; admin para verificar» (pestaña Implementación).


## TC-026 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «cliente (cuenta sin verificar)» (pestaña Implementación).


## TC-027 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «cliente (cuenta activa)» (pestaña Implementación).


## TC-028 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión); admin para verificar» (pestaña Implementación).


## TC-029 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «cliente (cuenta sin verificar)» (pestaña Implementación).


## TC-030 — ✅ Pasa



![captura](smoke-02/TC-030.png)

## TC-031 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «recepcion (precondición); invitado→cliente» (pestaña Implementación).


## TC-032 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «recepcion (precondición); invitado→cliente; admin (auditoría)» (pestaña Implementación).


## TC-033 — ❌ Falla

Inicié sesión como admin y la app me llevó a /interno, pero no hay ninguna entrada «Auditoría». Esperé el texto «Auditoría» y no apareció en 8 segundos. Abrí el menú de usuario tres veces y solo muestra «Cerrar sesión». Se esperaba que el admin pudiera abrir Auditoría, filtrar por la cuenta y ver tres eventos: el alta con origen 'autorregistro en el portal' y la fecha y hora de aceptación del aviso, la verificación con su fecha y hora, y la vinculación con el identificador EX. Como no encontré la sección, no pude comprobar ninguno. No probé abrir la sección escribiendo una URL directa. · Script: TimeoutError: Locator.click: Timeout 10000ms exceeded. Call log: - waiting for get_by_role("link", name=re.compile(r"Auditor[i�]a", re.IGNOR

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Auditoría» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
7. clic button «Menú de usuario» — ok: clic
8. presionar «Escape» — ok: presionó Escape
9. clic button «Menú de usuario» — ok: clic
10. presionar «Escape» — ok: presionó Escape
11. clic button «Menú de usuario» — ok: clic

![captura](smoke-02/TC-033.png)

## TC-034 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión); admin para revisar la cuenta y el log» (pestaña Implementación).


## TC-035 — ⛔ Bloqueado

No hay cuenta de prueba para el rol «invitado (sin sesión)» (pestaña Implementación).

