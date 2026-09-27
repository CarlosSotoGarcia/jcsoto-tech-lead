---
hu_id: HU-001
tipo: smoke
corrida: 3
modo: completo
fecha: 2026-09-27
ambiente: https://taller-web-118746543308.us-central1.run.app
proveedor_ia: claude_cli
tcs_totales: 35
tcs_pasan: [TC-001, TC-002, TC-003, TC-004, TC-005, TC-007, TC-008, TC-009, TC-010, TC-012, TC-013, TC-014, TC-015, TC-017, TC-018, TC-019, TC-021, TC-022, TC-023, TC-024, TC-025, TC-026, TC-027, TC-028, TC-029, TC-030, TC-034, TC-035]
tcs_fallan: [TC-006, TC-016, TC-032, TC-033]
tcs_bloqueados: [TC-011, TC-020, TC-031]
porcentaje_pasan: 80%
porcentaje_fallan: 11%
porcentaje_bloqueados: 9%
regresiones: []
---

# Smoke testing — HU-001: Autorregistro de cliente en el portal del taller con verificación de correo y vinculación a expediente existente

Corrida 3 (completo). Script de la HU: `smoke-03/HU-001_smoke.py`.

## Resumen

| Resultado | Casos | % |
|---|---:|---:|
| ✅ Pasa | 28 | 80% |
| ❌ Falla | 4 | 11% |
| ⛔ Bloqueado | 3 | 9% |
| **Total** | **35** | **100%** |

## Casos

| TC | Rol | Resultado | Cómo se resolvió | Motivo |
|---|---|---|---|---|
| TC-001 | invitado (sin sesión) para registrarse; admin para verificar el estado | ✅ Pasa | script |  |
| TC-002 | invitado (sin sesión); admin para verificar | ✅ Pasa | script |  |
| TC-003 | invitado (sin sesión); admin para comprobar que no se duplicó | ✅ Pasa | script |  |
| TC-004 | cliente (cuenta recién registrada, sin verificar) | ✅ Pasa | script |  |
| TC-005 | cliente (cuenta sin verificar) | ✅ Pasa | script |  |
| TC-006 | recepcion (para la precondición); invitado→cliente (para registrarse); admin (para verificar) | ❌ Falla | agente (fallo confirmado) | Con la sesión de recepcion@pruebas.taller.test iniciada, /interno solo muestra «Agenda del día» (dice «Aquí verás las citas y servicios del día.») y el botón «M |
| TC-007 | invitado (sin sesión) | ✅ Pasa | script |  |
| TC-008 | invitado (sin sesión) | ✅ Pasa | script |  |
| TC-009 | invitado (sin sesión) | ✅ Pasa | script |  |
| TC-010 | cliente (cuenta sin verificar); admin para verificar el estado | ✅ Pasa | script |  |
| TC-011 | recepcion (precondición); invitado→cliente; admin (verificación) | ⛔ Bloqueado | agente (fallo confirmado) | Tras iniciar sesión con la cuenta de prueba, /interno no muestra la sección «Clientes». El menú de usuario solo trae «Cerrar sesión». Al entrar directo a /inter |
| TC-012 | invitado (sin sesión); admin para consultar | ✅ Pasa | script |  |
| TC-013 | invitado (sin sesión) | ✅ Pasa | script |  |
| TC-014 | invitado (sin sesión) | ✅ Pasa | script |  |
| TC-015 | invitado (sin sesión) | ✅ Pasa | script |  |
| TC-016 | admin | ❌ Falla | agente (fallo confirmado) | Se esperaba un módulo de Auditoría para el admin con los 3 eventos del usuario (alta, verificación y vinculación), y documentación de la API con los endpoints d |
| TC-017 | invitado (sin sesión) | ✅ Pasa | script |  |
| TC-018 | invitado (sin sesión) | ✅ Pasa | script |  |
| TC-019 | invitado (sin sesión) | ✅ Pasa | script |  |
| TC-020 | recepcion (precondición); invitado→cliente | ⛔ Bloqueado | agente (fallo confirmado) | Tras iniciar sesión con la cuenta de prueba, se abrió /interno, pero «Clientes» nunca apareció (se agotó el tiempo de espera de 8 s). La página solo muestra el  |
| TC-021 | invitado (sin sesión) | ✅ Pasa | script |  |
| TC-022 | invitado (sin sesión); admin para consultar | ✅ Pasa | script |  |
| TC-023 | invitado (sin sesión) | ✅ Pasa | script |  |
| TC-024 | invitado (sin sesión); admin | ✅ Pasa | script |  |
| TC-025 | invitado (sin sesión) x2; admin para verificar | ✅ Pasa | script |  |
| TC-026 | cliente (cuenta sin verificar) | ✅ Pasa | script |  |
| TC-027 | cliente (cuenta activa) | ✅ Pasa | script |  |
| TC-028 | invitado (sin sesión); admin para verificar | ✅ Pasa | script |  |
| TC-029 | cliente (cuenta sin verificar) | ✅ Pasa | script |  |
| TC-030 | cliente | ✅ Pasa | script |  |
| TC-031 | recepcion (precondición); invitado→cliente | ⛔ Bloqueado | agente (fallo confirmado) | Inicié sesión con la cuenta de recepción y la app redirigió a /interno. Aun así, no se puede ejecutar el caso completo. Hace falta verificar el correo de 'hist@ |
| TC-032 | recepcion (precondición); invitado→cliente; admin (auditoría) | ❌ Falla | agente (fallo confirmado) | La sesión de recepción (recepcion@pruebas.taller.test) se inicia bien, pero solo lleva a /interno, con el título «Agenda del día» y el texto «Aquí verás las cit |
| TC-033 | admin | ❌ Falla | agente (fallo confirmado) | El admin inició sesión y llegó a /interno, pero en ninguna parte aparece el texto ni una opción «Auditoría». La espera del texto se agotó a los 8 s y el menú de |
| TC-034 | invitado (sin sesión); admin para revisar la cuenta y el log | ✅ Pasa | script |  |
| TC-035 | invitado (sin sesión) | ✅ Pasa | script |  |

## TC-001 — ✅ Pasa



![captura](smoke-03/TC-001.png)

## TC-002 — ✅ Pasa



![captura](smoke-03/TC-002.png)

## TC-003 — ✅ Pasa



![captura](smoke-03/TC-003.png)

## TC-004 — ✅ Pasa



![captura](smoke-03/TC-004.png)

## TC-005 — ✅ Pasa



![captura](smoke-03/TC-005.png)

## TC-006 — ❌ Falla

Con la sesión de recepcion@pruebas.taller.test iniciada, /interno solo muestra «Agenda del día» (dice «Aquí verás las citas y servicios del día.») y el botón «Menú de usuario». No aparece ninguna opción de Clientes. Al abrir /interno/clientes directamente, la página solo ofrecía el enlace «Ir al inicio», así que la ruta no existe. Por eso no se pudo dar de alta a 'Ana Ruiz' con sus vehículos ABC-123 y XYZ-987. Tampoco se pudo comprobar que la búsqueda de 'ana.ruiz@test.com' devuelva un solo expediente con la cuenta de portal vinculada. El resultado esperado necesita la vista Clientes de recepción/admin, y esa funcionalidad no existe. · Script: AssertionError: Page URL expected to be 're.compile('/mis-vehiculos')' Actual value: https://taller-web-118746543308.us-central1.run.app/int

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Clientes» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
7. clic button «Menú de usuario» — ok: clic
8. presionar «Escape» — ok: presionó Escape
9. ir a /interno/clientes — ok: abrió https://taller-web-118746543308.us-central1.run.app/interno/clientes
10. clic link «Ir al inicio» — ok: clic
11. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
12. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
13. clic button «Iniciar sesión» — ok: clic
14. esperar texto «Clientes» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.

![captura](smoke-03/TC-006.png)

## TC-007 — ✅ Pasa



![captura](smoke-03/TC-007.png)

## TC-008 — ✅ Pasa



![captura](smoke-03/TC-008.png)

## TC-009 — ✅ Pasa



![captura](smoke-03/TC-009.png)

## TC-010 — ✅ Pasa



![captura](smoke-03/TC-010.png)

## TC-011 — ⛔ Bloqueado

Tras iniciar sesión con la cuenta de prueba, /interno no muestra la sección «Clientes». El menú de usuario solo trae «Cerrar sesión». Al entrar directo a /interno/clientes solo aparece el enlace «Ir al inicio». Sin acceso a Clientes no se puede dar de alta al cliente 'Luis Mora' (5533334444, LMN-456) como recepción, ni revisar el expediente como admin. No se pudo comprobar la vinculación por teléfono. · Script: AssertionError: Page URL expected to be 're.compile('/mis-vehiculos')' Actual value: https://taller-web-118746543308.us-central1.run.app/int

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «ITZ» — ok: apareció «ITZ»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Clientes» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
7. clic button «Menú de usuario» — ok: clic
8. presionar «Escape» — ok: presionó Escape
9. ir a /interno/clientes — ok: abrió https://taller-web-118746543308.us-central1.run.app/interno/clientes
10. clic link «Ir al inicio» — ok: clic
11. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
12. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
13. clic button «Iniciar sesión» — ok: clic
14. esperar texto «Clientes» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
15. clic button «Menú de usuario» — ok: clic

![captura](smoke-03/TC-011.png)

## TC-012 — ✅ Pasa



![captura](smoke-03/TC-012.png)

## TC-013 — ✅ Pasa



![captura](smoke-03/TC-013.png)

## TC-014 — ✅ Pasa



![captura](smoke-03/TC-014.png)

## TC-015 — ✅ Pasa



![captura](smoke-03/TC-015.png)

## TC-016 — ❌ Falla

Se esperaba un módulo de Auditoría para el admin con los 3 eventos del usuario (alta, verificación y vinculación), y documentación de la API con los endpoints de registro y verificación. Pero al iniciar sesión como admin no apareció el texto «Auditoría» (se agotó la espera). El menú de usuario, abierto tres veces, tampoco muestra ese módulo. Al ir directo a /auditoria solo se ofreció el enlace «Ir al inicio», al parecer una página no encontrada, y ese enlace llevó de vuelta a /login. Se abrieron /api/docs y /docs, pero no se comprobó que mostraran los endpoints de registro y verificación de correo. Como no existe la auditoría del alta, la verificación y la vinculación, el caso no se cumple. · Script: TimeoutError: Locator.click: Timeout 10000ms exceeded. Call log: - waiting for get_by_role("link", name=re.compile(r"Auditor[i�]a", re.IGNOR

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
12. ir a /api/docs — ok: abrió https://taller-web-118746543308.us-central1.run.app/api/docs
13. ir a /docs — ok: abrió https://taller-web-118746543308.us-central1.run.app/docs
14. ir a /auditoria — ok: abrió https://taller-web-118746543308.us-central1.run.app/auditoria
15. clic link «Ir al inicio» — ok: clic

![captura](smoke-03/TC-016.png)

## TC-017 — ✅ Pasa



![captura](smoke-03/TC-017.png)

## TC-018 — ✅ Pasa



![captura](smoke-03/TC-018.png)

## TC-019 — ✅ Pasa



![captura](smoke-03/TC-019.png)

## TC-020 — ⛔ Bloqueado

Tras iniciar sesión con la cuenta de prueba, se abrió /interno, pero «Clientes» nunca apareció (se agotó el tiempo de espera de 8 s). La página solo muestra el menú de usuario con «Cerrar sesión». Por eso no se puede dar de alta a 'maria@mail.com' con el vehículo 'QWE-111' como recepción. Además, el escenario pide verificar el correo ' MARIA@Mail.com', y no hay acceso a ese buzón. Sin estas precondiciones no se puede comprobar que la cuenta se vincule sin distinguir mayúsculas ni espacios. · Script: AssertionError: Page URL expected to be 're.compile('/mis-vehiculos')' Actual value: https://taller-web-118746543308.us-central1.run.app/int

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Clientes» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
7. clic button «Menú de usuario» — ok: clic
8. presionar «Escape» — ok: presionó Escape
9. clic button «Menú de usuario» — ok: clic

![captura](smoke-03/TC-020.png)

## TC-021 — ✅ Pasa



![captura](smoke-03/TC-021.png)

## TC-022 — ✅ Pasa



![captura](smoke-03/TC-022.png)

## TC-023 — ✅ Pasa



![captura](smoke-03/TC-023.png)

## TC-024 — ✅ Pasa



![captura](smoke-03/TC-024.png)

## TC-025 — ✅ Pasa



![captura](smoke-03/TC-025.png)

## TC-026 — ✅ Pasa



![captura](smoke-03/TC-026.png)

## TC-027 — ✅ Pasa



![captura](smoke-03/TC-027.png)

## TC-028 — ✅ Pasa



![captura](smoke-03/TC-028.png)

## TC-029 — ✅ Pasa



![captura](smoke-03/TC-029.png)

## TC-030 — ✅ Pasa



![captura](smoke-03/TC-030.png)

## TC-031 — ⛔ Bloqueado

Inicié sesión con la cuenta de recepción y la app redirigió a /interno. Aun así, no se puede ejecutar el caso completo. Hace falta verificar el correo de 'hist@test.com' y luego iniciar sesión como ese cliente, pero no hay acceso a ese buzón ni una cuenta de cliente de prueba. Sin ese paso no se puede comprobar el resultado esperado: que después de verificar se vean 'HIS-001' y la orden de servicio. Además, en /interno el árbol de accesibilidad solo mostró el menú de usuario con «Cerrar sesión», sin opciones para dar de alta al cliente. · Script: AssertionError: Page URL expected to be 're.compile('/mis-vehiculos')' Actual value: https://taller-web-118746543308.us-central1.run.app/int

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Cerrar sesión» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
7. clic button «Menú de usuario» — ok: clic
8. presionar «Escape» — ok: presionó Escape
9. clic button «Menú de usuario» — ok: clic

![captura](smoke-03/TC-031.png)

## TC-032 — ❌ Falla

La sesión de recepción (recepcion@pruebas.taller.test) se inicia bien, pero solo lleva a /interno, con el título «Agenda del día» y el texto «Aquí verás las citas y servicios del día.». No hay navegación a Clientes: el menú de usuario no la ofrece y /interno/clientes abrió una página cuya única opción era «Ir al inicio». Tampoco apareció el texto «Clientes», que se esperó dos veces hasta agotar el tiempo. Sin el módulo Clientes (vista recepción) no se puede dar de alta a 'Juan Pérez' ni revisar si el expediente conserva el nombre y el celular originales. Por eso no se pudo probar el autorregistro ni la auditoría de la vinculación. Se esperaba una sección Clientes para recepción. · Script: TimeoutError: Locator.click: Timeout 10000ms exceeded. Call log: - waiting for get_by_role("link", name=re.compile(r"^Clientes", re.IGNORECA

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Clientes» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
7. clic button «Menú de usuario» — ok: clic
8. presionar «Escape» — ok: presionó Escape
9. ir a /interno/clientes — ok: abrió https://taller-web-118746543308.us-central1.run.app/interno/clientes
10. clic link «Ir al inicio» — ok: clic
11. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
12. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
13. clic button «Iniciar sesión» — ok: clic
14. esperar texto «Clientes» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.

![captura](smoke-03/TC-032.png)

## TC-033 — ❌ Falla

El admin inició sesión y llegó a /interno, pero en ninguna parte aparece el texto ni una opción «Auditoría». La espera del texto se agotó a los 8 s y el menú de usuario solo ofrece «Cerrar sesión». Se esperaba poder abrir Auditoría, filtrar por la cuenta y ver los eventos de alta (con origen autorregistro y fecha de aceptación del aviso), de verificación y de vinculación con el identificador EX. La funcionalidad de Auditoría no está disponible. · Script: TimeoutError: Locator.click: Timeout 10000ms exceeded. Call log: - waiting for get_by_role("link", name=re.compile(r"Auditor[i�]a", re.IGNOR

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

![captura](smoke-03/TC-033.png)

## TC-034 — ✅ Pasa



![captura](smoke-03/TC-034.png)

## TC-035 — ✅ Pasa



![captura](smoke-03/TC-035.png)
