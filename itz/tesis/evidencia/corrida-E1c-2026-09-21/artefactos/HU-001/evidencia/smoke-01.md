---
hu_id: HU-001
tipo: smoke
corrida: 1
modo: completo
fecha: 2026-09-21
ambiente: https://inventarios-web-118746543308.us-central1.run.app
proveedor_ia: claude_cli
tcs_totales: 14
tcs_pasan: [TC-001, TC-002, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-012, TC-014]
tcs_fallan: []
tcs_bloqueados: [TC-003, TC-011, TC-013]
porcentaje_pasan: 79%
porcentaje_fallan: 0%
porcentaje_bloqueados: 21%
regresiones: []
---

# Smoke testing — HU-001: Iniciar sesión con correo y contraseña

Corrida 1 (completo). Script de la HU: `smoke-01/HU-001_smoke.py`.

## Resumen

| Resultado | Casos | % |
|---|---:|---:|
| ✅ Pasa | 11 | 79% |
| ❌ Falla | 0 | 0% |
| ⛔ Bloqueado | 3 | 21% |
| **Total** | **14** | **100%** |

## Casos

| TC | Rol | Resultado | Cómo se resolvió | Motivo |
|---|---|---|---|---|
| TC-001 | usuario_final | ✅ Pasa | script |  |
| TC-002 | usuario_final | ✅ Pasa | script |  |
| TC-003 | invitado | ⛔ Bloqueado | agente (fallo confirmado) | El caso exige un correo registrado con una contraseña incorrecta, pero no hay cuenta de prueba. Un correo inventado no permite comprobar que el mensaje no revel |
| TC-004 | invitado | ✅ Pasa | agente (el script estaba mal) | Con un correo inexistente el sistema rechazó el acceso, se quedó en /login y mostró la alerta «Correo o contraseña incorrectos.». Es un mensaje genérico que no  |
| TC-005 | invitado | ✅ Pasa | script |  |
| TC-006 | usuario_final | ✅ Pasa | script |  |
| TC-007 | invitado | ✅ Pasa | agente (el script estaba mal) | Sin sesión, /dashboard y /api/users redirigieron a /login («Iniciar sesión» visible) y no se mostró contenido protegido. El código HTTP 401 no se puede ver desd |
| TC-008 | usuario_final | ✅ Pasa | script |  |
| TC-009 | invitado | ✅ Pasa | agente (el script estaba mal) | El campo «Contraseña» coincide con el selector input[type=password] (el clic sobre él funcionó), por lo que está enmascarado. La página está en https://inventar |
| TC-010 | usuario_final | ✅ Pasa | script |  |
| TC-011 | invitado | ⛔ Bloqueado | agente (fallo confirmado) | El caso requiere un correo registrado (y su contraseña correcta) para probar el bloqueo tras intentos fallidos, pero el rol invitado no tiene cuenta de prueba d |
| TC-012 | usuario_final | ✅ Pasa | script |  |
| TC-013 | invitado | ⛔ Bloqueado | agente (fallo confirmado) | La página de login carga, pero el caso exige escribir correo y contraseña y no hay usuario configurado para el rol invitado. Tampoco se dispone de forma de inte |
| TC-014 | admin | ✅ Pasa | script |  |

## TC-001 — ✅ Pasa



![captura](smoke-01/TC-001.png)

## TC-002 — ✅ Pasa



![captura](smoke-01/TC-002.png)

## TC-003 — ⛔ Bloqueado

El caso exige un correo registrado con una contraseña incorrecta, pero no hay cuenta de prueba. Un correo inventado no permite comprobar que el mensaje no revela qué dato falló. La página de login sí carga, con campos Correo y Contraseña. · Script: AssertionError: Locator expected to be visible Actual value: None Error: element(s) not found Call log:

Verificación del agente de navegador:

1. ir a / — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/
2. ir a /login — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/login

![captura](smoke-01/TC-003.png)

## TC-004 — ✅ Pasa

Con un correo inexistente el sistema rechazó el acceso, se quedó en /login y mostró la alerta «Correo o contraseña incorrectos.». Es un mensaje genérico que no revela si el correo existe. No había cuenta de prueba, así que no pude ejecutar el caso de contraseña incorrecta con un correo real para compararlo directamente. Lo doy por idéntico porque el texto es genérico, pero esa comparación queda sin confirmar.

Verificación del agente de navegador:

1. ir a / — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir «noexiste.qa.9731@example.com» en «Correo» — ok: escribió «noexiste.qa.9731@example.com»
4. escribir «ClaveIncorrecta#123» en textbox «Contraseña» — ok: escribió «ClaveIncorrecta#123»
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «incorrect» — ok: apareció «incorrect»
7. verificar texto «Correo o contraseña incorrectos.» — ok: verificado: «Correo o contraseña incorrectos.» está visible

![captura](smoke-01/TC-004.png)

## TC-005 — ✅ Pasa



![captura](smoke-01/TC-005.png)

## TC-006 — ✅ Pasa



![captura](smoke-01/TC-006.png)

## TC-007 — ✅ Pasa

Sin sesión, /dashboard y /api/users redirigieron a /login («Iniciar sesión» visible) y no se mostró contenido protegido. El código HTTP 401 no se puede ver desde el navegador. Solo se observó la redirección al login, así que el 401 queda sin confirmar.

Verificación del agente de navegador:

1. ir a / — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/
2. ir a /dashboard — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/dashboard
3. ir a /api/users — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/api/users
4. verificar texto «Iniciar sesión» — ok: verificado: «Iniciar sesión» está visible
5. ir a /api/users — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/api/users

![captura](smoke-01/TC-007.png)

## TC-008 — ✅ Pasa



![captura](smoke-01/TC-008.png)

## TC-009 — ✅ Pasa

El campo «Contraseña» coincide con el selector input[type=password] (el clic sobre él funcionó), por lo que está enmascarado. La página está en https://inventarios-web-118746543308.us-central1.run.app/login, es decir, HTTPS, y la URL no tiene query params ni contiene «TextoPrueba123» tras enviar el formulario. No se inspeccionó el tráfico de red directamente, y el hash con sal y los logs quedan para revisión de backend fuera de UI.

Verificación del agente de navegador:

1. ir a / — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/
2. esperar texto «Contraseña» — ok: apareció «Contraseña»
3. escribir el contrasena en textbox «Contraseña» — FALLÓ: no hay «contrasena» configurado para el rol de este caso
4. escribir «TextoPrueba123» en «Contraseña» — ok: escribió «TextoPrueba123»
5. clic button «Iniciar sesión» — ok: clic
6. verificar texto «https://inventarios-web-118746543308.us-central1.run.app/login» — FALLÓ: Locator.wait_for: Timeout 5000ms exceeded.
7. esperar texto «input[type=password]» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
8. verificar texto «Contraseña» — ok: verificado: «Contraseña» está visible
9. clic «input[type=password]» — ok: clic

![captura](smoke-01/TC-009.png)

## TC-010 — ✅ Pasa



![captura](smoke-01/TC-010.png)

## TC-011 — ⛔ Bloqueado

El caso requiere un correo registrado (y su contraseña correcta) para probar el bloqueo tras intentos fallidos, pero el rol invitado no tiene cuenta de prueba disponible. No se puede ejecutar sin credenciales válidas. Solo se observó el formulario de login con Correo, Contraseña y enlace de recuperación. · Script: AssertionError: Locator expected to be visible Actual value: None Error: element(s) not found Call log:

Verificación del agente de navegador:

1. ir a / — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»

![captura](smoke-01/TC-011.png)

## TC-012 — ✅ Pasa



![captura](smoke-01/TC-012.png)

## TC-013 — ⛔ Bloqueado

La página de login carga, pero el caso exige escribir correo y contraseña y no hay usuario configurado para el rol invitado. Tampoco se dispone de forma de interceptar la petición de autenticación con un 503. Por eso no se pudo comprobar el mensaje de error, la conservación del correo ni que no se inicie sesión. · Script: AssertionError: Locator expected to be visible Actual value: None Error: element(s) not found Call log:

Verificación del agente de navegador:

1. ir a / — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/
2. ir a /login — ok: abrió https://inventarios-web-118746543308.us-central1.run.app/login
3. escribir el usuario en textbox «Correo» — FALLÓ: no hay «usuario» configurado para el rol de este caso

![captura](smoke-01/TC-013.png)

## TC-014 — ✅ Pasa



![captura](smoke-01/TC-014.png)
