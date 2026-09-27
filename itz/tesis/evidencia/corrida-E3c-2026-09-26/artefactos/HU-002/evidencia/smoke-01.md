---
hu_id: HU-002
tipo: smoke
corrida: 1
modo: completo
fecha: 2026-09-27
ambiente: https://taller-web-118746543308.us-central1.run.app
proveedor_ia: claude_cli
tcs_totales: 39
tcs_pasan: [TC-001, TC-002, TC-003, TC-004, TC-005, TC-009, TC-010, TC-013, TC-014, TC-015, TC-016, TC-018, TC-019, TC-020, TC-021, TC-025, TC-027, TC-032, TC-037]
tcs_fallan: [TC-033, TC-035, TC-036, TC-039]
tcs_bloqueados: [TC-006, TC-007, TC-008, TC-011, TC-012, TC-017, TC-022, TC-023, TC-024, TC-026, TC-028, TC-029, TC-030, TC-031, TC-034, TC-038]
porcentaje_pasan: 49%
porcentaje_fallan: 10%
porcentaje_bloqueados: 41%
regresiones: []
---

# Smoke testing — HU-002: Inicio y cierre de sesión con correo y contraseña, con redirección por rol

Corrida 1 (completo). Script de la HU: `smoke-01/HU-002_smoke.py`.

## Resumen

| Resultado | Casos | % |
|---|---:|---:|
| ✅ Pasa | 19 | 49% |
| ❌ Falla | 4 | 10% |
| ⛔ Bloqueado | 16 | 41% |
| **Total** | **39** | **100%** |

## Casos

| TC | Rol | Resultado | Cómo se resolvió | Motivo |
|---|---|---|---|---|
| TC-001 | cliente | ✅ Pasa | script |  |
| TC-002 | cliente | ✅ Pasa | script |  |
| TC-003 | personal_interno | ✅ Pasa | script |  |
| TC-004 | cliente | ✅ Pasa | script |  |
| TC-005 | cliente_bloqueable | ✅ Pasa | script |  |
| TC-006 | cliente_bloqueable | ⛔ Bloqueado | agente (fallo confirmado) | Tras el primer intento con contraseña errónea («ClaveErronea#1») apareció el aviso «Tu cuenta está bloqueada temporalmente por demasiados intentos fallidos. Int |
| TC-007 | cliente_bloqueable | ⛔ Bloqueado | agente (fallo confirmado) | Ingresé con las credenciales correctas de cliente_bloqueable. La página se quedó en /login con la alerta «Tu cuenta está bloqueada temporalmente por demasiados  |
| TC-008 | cliente_bloqueable | ⛔ Bloqueado | agente (fallo confirmado) | Tras el primer intento fallido la página mostró la alerta de bloqueo temporal («Tu cuenta está bloqueada temporalmente por demasiados intentos fallidos…») y la  |
| TC-009 | cliente | ✅ Pasa | agente (el script estaba mal) | Resultado: pasa en lo que se pudo comprobar. Al pulsar «Cerrar sesión» se volvió a la pantalla de login y se verificó el texto «Ingresa con tu correo y contrase |
| TC-010 | personal_interno | ✅ Pasa | agente (el script estaba mal) | Se pulsó «Cerrar sesión» y apareció la pantalla de login; se verificó «Ingresa con tu correo y contraseña.». Luego, al abrir / de nuevo, la app redirigió a /log |
| TC-011 | personal_interno | ⛔ Bloqueado | agente (fallo confirmado) | Se inició sesión como personal interno y se llegó a «Agenda del día» (/interno). El escenario pide que pasen 30 minutos sin actividad adelantando page.clock o e |
| TC-012 | personal_interno | ⛔ Bloqueado | agente (fallo confirmado) | Inicié sesión como personal interno (recepcion@pruebas.taller.test) y llegué a «Agenda del día» (/interno). No pude seguir: la prueba pide 29 minutos sin activi |
| TC-013 | cuenta_inactiva | ✅ Pasa | agente (el script estaba mal) | La cuenta inactiva no pudo entrar con su correo y contraseña correctos. La URL siguió en /login y apareció el aviso «Tu cuenta no está habilitada. Comunícate co |
| TC-014 | cuenta_pendiente_verificacion | ✅ Pasa | agente (el script estaba mal) | Con credenciales correctas de la cuenta pendiente de verificación, la URL siguió en /login. Apareció la alerta «Tu cuenta aún no está activa: verifica tu correo |
| TC-015 | invitado | ✅ Pasa | script |  |
| TC-016 | invitado | ✅ Pasa | script |  |
| TC-017 | invitado | ⛔ Bloqueado | agente (fallo confirmado) | El escenario pide enviar al endpoint de login, sin sesión, cuerpos con el correo o la contraseña vacíos o sin incluir. Luego hay que comprobar tres cosas: que r |
| TC-018 | invitado | ✅ Pasa | script |  |
| TC-019 | cliente_bloqueable | ✅ Pasa | agente (el script estaba mal) | Con el correo 'correo-invalido' se vio solo «El correo no tiene un formato válido.» y ningún mensaje de bloqueo. Después, con el correo correcto y la contraseña |
| TC-020 | invitado | ✅ Pasa | agente (el script estaba mal) | Con un correo no registrado (noregistrado.tc020@example.com) y cualquier contraseña, la página mostró la alerta genérica «Correo o contraseña incorrectos.», que |
| TC-021 | invitado | ✅ Pasa | script |  |
| TC-022 | cliente_bloqueable | ⛔ Bloqueado | agente (fallo confirmado) | Se inició sesión con las credenciales correctas de la cuenta de prueba (cliente.bloqueable@pruebas.taller.test). No se redirigió a «Mis vehículos»: la página si |
| TC-023 | cliente_bloqueable | ⛔ Bloqueado | agente (fallo confirmado) | Después de apenas 1 intento fallido (el que servía para preparar la precondición), la página mostró «Tu cuenta está bloqueada temporalmente por demasiados inten |
| TC-024 | cliente_bloqueable | ⛔ Bloqueado | agente (fallo confirmado) | No se cumplió la precondición: la cuenta cliente_bloqueable no estaba bloqueada por 5 intentos fallidos en los últimos 15 minutos. Con el correo y la contraseña |
| TC-025 | invitado | ✅ Pasa | script |  |
| TC-026 | cliente | ⛔ Bloqueado | agente (fallo confirmado) | El inicio de sesión funcionó: la app redirigió a /mis-vehiculos y muestra el encabezado «Mis vehículos» y el menú de usuario con la cuenta cliente@pruebas.talle |
| TC-027 | cliente | ✅ Pasa | agente (el script estaba mal) | Con la sesión ya cerrada, pulsé "Atrás" (Alt+ArrowLeft). La URL quedó en /login, se ve el formulario "Iniciar sesión" y aparece el texto «Ingresa con tu correo  |
| TC-028 | cliente | ⛔ Bloqueado | agente (fallo confirmado) | El escenario pide capturar el token del cliente antes del logout y luego llamar directamente a un endpoint protegido (listado de vehículos) con APIRequestContex |
| TC-029 | personal_interno | ⛔ Bloqueado | agente (fallo confirmado) | Inicié sesión como personal interno y llegué a /interno («Agenda del día»). No pude probar la expiración por dos motivos. Primero, la página no ofrece forma de  |
| TC-030 | personal_interno | ⛔ Bloqueado | agente (fallo confirmado) | Inicié sesión como personal interno y llegué a «Agenda del día» sin problema. El caso pide dos esperas de 25 minutos, con una acción entre ellas, para comprobar |
| TC-031 | personal_interno | ⛔ Bloqueado | agente (fallo confirmado) | Se completó el login y el botón «Iniciar sesión» quedó deshabilitado mientras se procesaba. Para verificar el caso habría que hacer una acción en el minuto 25,  |
| TC-032 | cliente | ✅ Pasa | agente (el script estaba mal) | Con la sesión de cliente iniciada (se veía «Mis vehículos»), navegué directamente a /agenda. La aplicación mostró «Página no encontrada» («La dirección que busc |
| TC-033 | personal_interno | ❌ Falla | agente (fallo confirmado) | Personal interno autenticado (se vio «Agenda del día»). Al navegar por URL a /mis-vehiculos no se mostraron los vehículos del cliente, pero tampoco hubo redirec |
| TC-034 | cliente | ⛔ Bloqueado | agente (fallo confirmado) | No se pudo ejecutar el caso con este agente de navegador. Se enviaron las credenciales del cliente, pero la página seguía en /login con el botón «Iniciar sesión |
| TC-035 | cliente | ❌ Falla | agente (fallo confirmado) | Después de iniciar sesión como cliente (apareció «Mis vehículos»), entré directamente a /login. La URL final quedó en /login y se ve el formulario «Iniciar sesi |
| TC-036 | personal_interno | ❌ Falla | agente (fallo confirmado) | Esperado: si ya hay sesión, entrar a /login lleva a "Agenda del día" y no muestra el formulario. Observado: el login funcionó y apareció "Agenda del día". Despu |
| TC-037 | admin (acceso al registro de auditoría) | ✅ Pasa | script |  |
| TC-038 | cliente | ⛔ Bloqueado | agente (fallo confirmado) | El inicio de sesión, la navegación autenticada y el cierre de sesión se hicieron en https://taller-web-118746543308.us-central1.run.app. Después del login apare |
| TC-039 | invitado (o el rol con acceso a la documentación) | ❌ Falla | agente (fallo confirmado) | No encontré documentación de la API en el ambiente. Probé /swagger-ui/index.html, /swagger-ui.html, /v3/api-docs, /docs, /api-docs, /api/swagger-ui/index.html,  |

## TC-001 — ✅ Pasa



![captura](smoke-01/TC-001.png)

## TC-002 — ✅ Pasa



![captura](smoke-01/TC-002.png)

## TC-003 — ✅ Pasa



![captura](smoke-01/TC-003.png)

## TC-004 — ✅ Pasa



![captura](smoke-01/TC-004.png)

## TC-005 — ✅ Pasa



![captura](smoke-01/TC-005.png)

## TC-006 — ⛔ Bloqueado

Tras el primer intento con contraseña errónea («ClaveErronea#1») apareció el aviso «Tu cuenta está bloqueada temporalmente por demasiados intentos fallidos. Intenta de nuevo más tarde.». Se esperaba que los intentos 1 a 4 mostraran solo el mensaje genérico. Lo más probable es que la cuenta cliente.bloqueable ya estuviera bloqueada por ejecuciones anteriores, así que no cumple la precondición del caso (contador de intentos en 0). Como no se puede comprobar si el bloqueo ocurre en el 5.º o en el 6.º intento, hay que desbloquear o reiniciar la cuenta y volver a ejecutar el caso. Si la cuenta estaba realmente en 0, se trata de un defecto: el sistema bloquea desde el primer fallo. · Script: AssertionError: 

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir «ClaveErronea#1» en textbox «Contraseña» — ok: escribió «ClaveErronea#1»
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Ingresa con tu correo y contraseña.» — ok: apareció «Ingresa con tu correo y contraseña.»

![captura](smoke-01/TC-006.png)

## TC-007 — ⛔ Bloqueado

Ingresé con las credenciales correctas de cliente_bloqueable. La página se quedó en /login con la alerta «Tu cuenta está bloqueada temporalmente por demasiados intentos fallidos. Intenta de nuevo más tarde.» y no llevó a «Mis vehículos». No se sabe cuándo empezó el bloqueo. Además, en esta ejecución no hay forma de esperar 15 minutos reales ni de adelantar el reloj del servidor. Por eso no se puede comprobar el resultado esperado: que desaparezca el bloqueo, que la API responda 200 y que lleve a «Mis vehículos». Hay que volver a ejecutar la prueba en una de estas condiciones: (a) cuando se sepa que pasaron más de 15 minutos desde el bloqueo; (b) con el reloj del servidor adelantado. · Script: AssertionError: 

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Mis vehículos» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.

![captura](smoke-01/TC-007.png)

## TC-008 — ⛔ Bloqueado

Tras el primer intento fallido la página mostró la alerta de bloqueo temporal («Tu cuenta está bloqueada temporalmente por demasiados intentos fallidos…») y la URL siguió en /login. Eso indica que la cuenta ya estaba bloqueada por pruebas anteriores. Con esta herramienta no se pueden cumplir dos condiciones del caso: esperar exactamente 14 minutos desde el momento del bloqueo (no se sabe cuándo empezó ni se puede adelantar el reloj) y comprobar que la API responde 423, porque el árbol de accesibilidad no muestra códigos HTTP. Para ejecutarlo hace falta controlar el tiempo en el ambiente (reloj simulado o un bloqueo reciente con hora conocida) y poder ver la respuesta de la API. · Script: AssertionError: 

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir «ClaveIncorrecta#1» en textbox «Contraseña» — ok: escribió «ClaveIncorrecta#1»
5. clic button «Iniciar sesión» — ok: clic
6. escribir «ClaveIncorrecta#2» en textbox «Contraseña» — ok: escribió «ClaveIncorrecta#2»

![captura](smoke-01/TC-008.png)

## TC-009 — ✅ Pasa

Resultado: pasa en lo que se pudo comprobar. Al pulsar «Cerrar sesión» se volvió a la pantalla de login y se verificó el texto «Ingresa con tu correo y contraseña.». Después abrí / y la app redirigió a /login con el formulario visible (Correo, Contraseña, botón Iniciar sesión). Eso indica que la sesión en el cliente ya no está. No comprobé directamente dos puntos del resultado esperado, porque desde el navegador no se ven la red ni el storage: que la petición de logout responda 200 o 204, y que el token o la cookie ya no esté en el storage ni en las cookies.

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Mis vehículos» — ok: apareció «Mis vehículos»
7. clic button «Menú de usuario» — ok: clic
8. clic menuitem «Cerrar sesión» — ok: clic
9. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
10. verificar texto «Ingresa con tu correo y contraseña.» — ok: verificado: «Ingresa con tu correo y contraseña.» está visible
11. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
12. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»

![captura](smoke-01/TC-009.png)

## TC-010 — ✅ Pasa

Se pulsó «Cerrar sesión» y apareció la pantalla de login; se verificó «Ingresa con tu correo y contraseña.». Luego, al abrir / de nuevo, la app redirigió a /login con los campos Correo y Contraseña y el botón «Iniciar sesión» visibles. Esto indica que la sesión ya no es válida, aunque la cookie o el token no se revisaron directamente.

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Agenda del día» — ok: apareció «Agenda del día»
7. clic button «Menú de usuario» — ok: clic
8. clic menuitem «Cerrar sesión» — ok: clic
9. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
10. verificar texto «Ingresa con tu correo y contraseña.» — ok: verificado: «Ingresa con tu correo y contraseña.» está visible
11. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
12. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»

![captura](smoke-01/TC-010.png)

## TC-011 — ⛔ Bloqueado

Se inició sesión como personal interno y se llegó a «Agenda del día» (/interno). El escenario pide que pasen 30 minutos sin actividad adelantando page.clock o el reloj del servidor. Ninguna de las acciones disponibles controla el reloj, y esperar 30 minutos reales supera el límite de pasos. Por eso no se pudo comprobar la redirección al login, las respuestas 401 con el token anterior ni que la agenda deje de mostrarse. Para ejecutar el caso hace falta un harness que pueda manipular el reloj o un token de expiración corta en el ambiente. · Script: AssertionError: Locator expected to be visible Actual value: None Error: element(s) not found Call log:

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Agenda del día» — ok: apareció «Agenda del día»

![captura](smoke-01/TC-011.png)

## TC-012 — ⛔ Bloqueado

Inicié sesión como personal interno (recepcion@pruebas.taller.test) y llegué a «Agenda del día» (/interno). No pude seguir: la prueba pide 29 minutos sin actividad y el ejecutor no puede esperar tiempo ni cambiar el reloj o el vencimiento de la sesión. Por eso no se revisó si la navegación sigue sin ir al login, si la API responde 200 ni si falta el aviso de sesión expirada. Además, la agenda no muestra ningún elemento para navegar dentro de ella (solo el «Menú de usuario»). Hace falta configurar un tiempo de expiración más corto en el ambiente de prueba, poder cambiar el reloj, o hacer la prueba a mano. · Script: AssertionError: Locator expected to be visible Actual value: None Error: element(s) not found Call log:

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Agenda» — ok: apareció «Agenda»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Agenda del día» — ok: apareció «Agenda del día»

![captura](smoke-01/TC-012.png)

## TC-013 — ✅ Pasa

La cuenta inactiva no pudo entrar con su correo y contraseña correctos. La URL siguió en /login y apareció el aviso «Tu cuenta no está habilitada. Comunícate con el taller.», como se esperaba. No se puede confirmar desde la pantalla que la API responda 403 ni que no emita ningún token; eso hay que revisarlo en la red.

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «inactiva» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
7. verificar texto «Tu cuenta no está habilitada» — ok: verificado: «Tu cuenta no está habilitada» está visible

![captura](smoke-01/TC-013.png)

## TC-014 — ✅ Pasa

Con credenciales correctas de la cuenta pendiente de verificación, la URL siguió en /login. Apareció la alerta «Tu cuenta aún no está activa: verifica tu correo con el enlace que te enviamos para poder iniciar sesión.», con el enlace «Reenviar verificación». El acceso no se permitió. El código 403 de la API y la ausencia de token no se pueden comprobar desde el árbol de accesibilidad. Lo que se ve en pantalla coincide con eso.

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «verific» — ok: apareció «verific»
7. verificar texto «Tu cuenta aún no está activa: verifica tu correo con el enlace que te » — ok: verificado: «Tu cuenta aún no está activa: verifica tu correo con el enlace que te enviamos para poder iniciar sesión.» está visible

![captura](smoke-01/TC-014.png)

## TC-015 — ✅ Pasa



![captura](smoke-01/TC-015.png)

## TC-016 — ✅ Pasa



![captura](smoke-01/TC-016.png)

## TC-017 — ⛔ Bloqueado

El escenario pide enviar al endpoint de login, sin sesión, cuerpos con el correo o la contraseña vacíos o sin incluir. Luego hay que comprobar tres cosas: que responda 400 o 422 con error de validación, que no se emita ningún token y que el intento no cuente como fallido para ninguna cuenta. El ejecutor solo tiene acciones de navegador (ir_a, clic, escribir, etc.). Con ellas no puedo enviar peticiones HTTP a mano, ver el código de respuesta ni revisar el conteo de intentos fallidos. La página cargó, pero solo muestra el indicador "Cargando". El caso no se puede ejecutar con esta herramienta y hay que correrlo como prueba de API. · Script: AssertionError: ({'correo': '', 'password': 'ClaveCualquiera1'}, 429)

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/

![captura](smoke-01/TC-017.png)

## TC-018 — ✅ Pasa



![captura](smoke-01/TC-018.png)

## TC-019 — ✅ Pasa

Con el correo 'correo-invalido' se vio solo «El correo no tiene un formato válido.» y ningún mensaje de bloqueo. Después, con el correo correcto y la contraseña errónea, apareció «Tu cuenta está bloqueada temporalmente por demasiados intentos fallidos». Es lo esperado: el intento con formato inválido no contó y el bloqueo llegó con el quinto fallo real. Lo que no pude comprobar en pantalla es que la cuenta ya tuviera los 4 fallos previos del Given.

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir «correo-invalido» en textbox «Correo» — ok: escribió «correo-invalido»
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. verificar texto «El correo no tiene un formato válido.» — ok: verificado: «El correo no tiene un formato válido.» está visible
7. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
8. escribir «ClaveErronea123!» en textbox «Contraseña» — ok: escribió «ClaveErronea123!»
9. clic button «Iniciar sesión» — ok: clic
10. esperar texto «bloquead» — ok: apareció «bloquead»

![captura](smoke-01/TC-019.png)

## TC-020 — ✅ Pasa

Con un correo no registrado (noregistrado.tc020@example.com) y cualquier contraseña, la página mostró la alerta genérica «Correo o contraseña incorrectos.», que no revela si la cuenta existe. Como no hay cuenta de prueba, no se pudo reproducir E2 (contraseña errónea con correo registrado) para comparar el texto directamente. Desde la interfaz tampoco se pueden ver el código HTTP 401, el cuerpo de la respuesta ni el tiempo de respuesta: eso requiere revisar la red o la API.

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir «noregistrado.tc020@example.com» en textbox «Correo» — ok: escribió «noregistrado.tc020@example.com»
4. escribir «ClaveCualquiera123!» en textbox «Contraseña» — ok: escribió «ClaveCualquiera123!»
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «incorrect» — ok: apareció «incorrect»
7. verificar texto «Correo o contraseña incorrectos.» — ok: verificado: «Correo o contraseña incorrectos.» está visible

![captura](smoke-01/TC-020.png)

## TC-021 — ✅ Pasa



![captura](smoke-01/TC-021.png)

## TC-022 — ⛔ Bloqueado

Se inició sesión con las credenciales correctas de la cuenta de prueba (cliente.bloqueable@pruebas.taller.test). No se redirigió a «Mis vehículos»: la página sigue en /login y muestra «Tu cuenta está bloqueada temporalmente por demasiados intentos fallidos. Intenta de nuevo más tarde.» La cuenta ya estaba bloqueada antes de empezar el caso, probablemente por ejecuciones anteriores. No se cumple la precondición (una cuenta activa con 4 intentos fallidos consecutivos) y no se puede comprobar si el contador vuelve a cero. Antes de repetir el caso hay que desbloquear la cuenta o restablecer sus datos. · Script: AssertionError: 

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Mis vehículos» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.

![captura](smoke-01/TC-022.png)

## TC-023 — ⛔ Bloqueado

Después de apenas 1 intento fallido (el que servía para preparar la precondición), la página mostró «Tu cuenta está bloqueada temporalmente por demasiados intentos fallidos». Lo más probable es que la cuenta cliente.bloqueable ya estuviera bloqueada por ejecuciones anteriores. Por eso no se cumple la precondición «cuenta activa con 1 intento fallido» y no se pueden hacer el inicio de sesión correcto ni los 4 fallos siguientes. Hay que desbloquear o reiniciar la cuenta de prueba y volver a ejecutar el caso. · Script: AssertionError: 

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir «ClaveIncorrecta123!» en textbox «Contraseña» — ok: escribió «ClaveIncorrecta123!»
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»

![captura](smoke-01/TC-023.png)

## TC-024 — ⛔ Bloqueado

No se cumplió la precondición: la cuenta cliente_bloqueable no estaba bloqueada por 5 intentos fallidos en los últimos 15 minutos. Con el correo y la contraseña correctos se inició sesión sin problema: la página redirigió a /mis-vehiculos («Mis vehículos») y el menú de usuario muestra cliente.bloqueable@pruebas.taller.test. No apareció ningún mensaje de bloqueo. Se esperaba el mensaje de bloqueo temporal, respuesta 423, ningún token emitido y seguir en la URL de login. Como la cuenta no estaba bloqueada al empezar, este resultado no demuestra un defecto. Para ejecutar el caso hay que dejar la cuenta bloqueada antes: con 5 intentos fallidos justo antes de la prueba o con datos de prueba preparados. Nota: el clic en «Cerrar sesión» no sacó al usuario; la página sigue mostrando la sesión iniciada. · Script: AssertionError: 

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «bloquead» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
7. clic button «Menú de usuario» — ok: clic
8. clic menuitem «Cerrar sesión» — ok: clic

![captura](smoke-01/TC-024.png)

## TC-025 — ✅ Pasa



![captura](smoke-01/TC-025.png)

## TC-026 — ⛔ Bloqueado

El inicio de sesión funcionó: la app redirigió a /mis-vehiculos y muestra el encabezado «Mis vehículos» y el menú de usuario con la cuenta cliente@pruebas.taller.test. La URL no contiene la contraseña. El paso de esperar «Cerrar sesión» falló porque ese texto no se ve en pantalla; seguramente está dentro del «Menú de usuario», que sigue cerrado. Con mis acciones (clic, escribir, verificar texto, etc.) no puedo capturar ni leer cuerpos o cabeceras de respuestas de red, ni ver el contenido de localStorage, sessionStorage o las cookies. Eso es lo que exige el resultado esperado, así que no lo pude comprobar. Tampoco hice el inicio de sesión fallido. Para completar el caso hace falta un script de Playwright que registre las respuestas (page.on('response')) y lea el almacenamiento y las cookies (context.cookies(), page.evaluate sobre localStorage y sessionStorage), buscando la contraseña en claro o un campo "password". · Script: AssertionError: Locator expected to contain text 'Correo o contrase�a incorrectos' Actual value: Demasiados intentos. Espera un momento e in

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Cerrar sesión» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.

![captura](smoke-01/TC-026.png)

## TC-027 — ✅ Pasa

Con la sesión ya cerrada, pulsé "Atrás" (Alt+ArrowLeft). La URL quedó en /login, se ve el formulario "Iniciar sesión" y aparece el texto «Ingresa con tu correo y contraseña.». En el árbol de accesibilidad no hay contenido protegido ni datos de "Mis vehículos", como se esperaba. No pude comprobar desde la interfaz que las peticiones a la API respondan 401.

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Mis vehículos» — ok: apareció «Mis vehículos»
7. clic button «Menú de usuario» — ok: clic
8. clic menuitem «Cerrar sesión» — ok: clic
9. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
10. presionar «Alt+ArrowLeft» — ok: presionó Alt+ArrowLeft
11. verificar texto «Ingresa con tu correo y contraseña.» — ok: verificado: «Ingresa con tu correo y contraseña.» está visible

![captura](smoke-01/TC-027.png)

## TC-028 — ⛔ Bloqueado

El escenario pide capturar el token del cliente antes del logout y luego llamar directamente a un endpoint protegido (listado de vehículos) con APIRequestContext usando ese token. Con las acciones de navegador disponibles (ir_a, clic, escribir, etc.) no se puede leer el token ni enviar una petición HTTP con encabezado Authorization. Tampoco se puede ver el código de estado de la respuesta. Por eso no se puede comprobar el resultado esperado (401 sin datos protegidos). Hay que ejecutar este caso como prueba de API con Playwright APIRequestContext. La página inicial solo mostraba el indicador 'Cargando'. · Script: AssertionError: 

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/

![captura](smoke-01/TC-028.png)

## TC-029 — ⛔ Bloqueado

Inicié sesión como personal interno y llegué a /interno («Agenda del día»). No pude probar la expiración por dos motivos. Primero, la página no ofrece forma de simular el reloj o la inactividad de 30 minutos, que es la precondición del caso. Segundo, «Agenda del día» solo muestra un encabezado y el texto «Aquí verás las citas y servicios del día.», sin botones ni enlaces donde hacer clic; lo único disponible es «Menú de usuario». Por eso no pude comprobar si al expirar la sesión se redirige al login con un aviso de sesión expirada distinto del de credenciales incorrectas. Para ejecutar el caso hace falta un ambiente con reloj simulable y que la agenda tenga acciones. · Script: AssertionError: Locator expected to be visible Actual value: None Error: element(s) not found Call log:

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Agenda del día» — ok: apareció «Agenda del día»

![captura](smoke-01/TC-029.png)

## TC-030 — ⛔ Bloqueado

Inicié sesión como personal interno y llegué a «Agenda del día» sin problema. El caso pide dos esperas de 25 minutos, con una acción entre ellas, para comprobar que la actividad reinicia el contador de 30 minutos de inactividad. Sin embargo, no tengo ninguna acción para esperar un tiempo fijo ni para simular el paso del tiempo. Tampoco puedo ver las respuestas de la API. Además, la agenda no muestra elementos con los que operar; solo aparece «Menú de usuario». Este caso necesita una prueba manual o una forma de controlar el tiempo, como un tiempo de sesión configurable o un reloj simulado. · Script: AssertionError: 

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Agenda» — ok: apareció «Agenda»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Agenda del día» — ok: apareció «Agenda del día»

![captura](smoke-01/TC-030.png)

## TC-031 — ⛔ Bloqueado

Se completó el login y el botón «Iniciar sesión» quedó deshabilitado mientras se procesaba. Para verificar el caso habría que hacer una acción en el minuto 25, esperar 30 minutos sin actividad y confirmar que la app redirige al login con el mensaje de sesión expirada. El ejecutor no puede adelantar el reloj ni esperar unos 55 minutos reales dentro del límite de pasos. No se probó el comportamiento esperado. Para ejecutarlo se necesita poder manipular el tiempo o una configuración de expiración reducida en el ambiente de prueba. · Script: AssertionError: Locator expected to be visible Actual value: None Error: element(s) not found Call log:

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic

![captura](smoke-01/TC-031.png)

## TC-032 — ✅ Pasa

Con la sesión de cliente iniciada (se veía «Mis vehículos»), navegué directamente a /agenda. La aplicación mostró «Página no encontrada» («La dirección que buscas no existe o fue movida.») y un enlace «Ir al inicio». No apareció contenido de la agenda, así que el acceso quedó denegado. Observaciones: (1) la página es de tipo 404, no un 403 ni una redirección a «Mis vehículos» como indica el resultado esperado; (2) no se confirmó que /agenda sea la ruta real de «Agenda del día». Conviene repetir la prueba con la ruta confirmada (por ejemplo, con un usuario del rol que sí tiene acceso) para distinguir entre una ruta protegida y una ruta que no existe.

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Mis vehículos» — ok: apareció «Mis vehículos»
7. ir a /agenda — ok: abrió https://taller-web-118746543308.us-central1.run.app/agenda
8. verificar texto «Página no encontrada» — ok: verificado: «Página no encontrada» está visible

![captura](smoke-01/TC-032.png)

## TC-033 — ❌ Falla

Personal interno autenticado (se vio «Agenda del día»). Al navegar por URL a /mis-vehiculos no se mostraron los vehículos del cliente, pero tampoco hubo redirección a «Agenda del día» ni página 403: la sesión se perdió y se terminó en /login («Ingresa con tu correo y contraseña.»). Se esperaba una redirección a «Agenda del día» o un 403 con la sesión activa. Hay que revisar si la sesión se cierra al acceder a una ruta de otro rol o si no se mantiene al navegar por URL. · Script: AssertionError: Page URL expected to be 're.compile('/interno')' Actual value: https://taller-web-118746543308.us-central1.run.app/login Cal

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Agenda del día» — ok: apareció «Agenda del día»
7. ir a /cliente/vehiculos — ok: abrió https://taller-web-118746543308.us-central1.run.app/cliente/vehiculos
8. verificar texto «Página no encontrada» — ok: verificado: «Página no encontrada» está visible
9. ir a /vehiculos — ok: abrió https://taller-web-118746543308.us-central1.run.app/vehiculos
10. ir a /mis-vehiculos — ok: abrió https://taller-web-118746543308.us-central1.run.app/mis-vehiculos
11. esperar texto «Agenda del día» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
12. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
13. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
14. clic button «Iniciar sesión» — ok: clic
15. esperar texto «Agenda del día» — ok: apareció «Agenda del día»
16. ir a /cliente — ok: abrió https://taller-web-118746543308.us-central1.run.app/cliente
17. ir a /mis-vehiculos — ok: abrió https://taller-web-118746543308.us-central1.run.app/mis-vehiculos
18. esperar texto «Agenda del día» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
19. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
20. esperar texto «Agenda del día» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
21. verificar texto «Ingresa con tu correo y contraseña.» — ok: verificado: «Ingresa con tu correo y contraseña.» está visible

![captura](smoke-01/TC-033.png)

## TC-034 — ⛔ Bloqueado

No se pudo ejecutar el caso con este agente de navegador. Se enviaron las credenciales del cliente, pero la página seguía en /login con el botón «Iniciar sesión» deshabilitado, así que no se confirmó que la sesión se iniciara. El caso pide llamar con APIRequestContext y un token válido a un endpoint del personal interno (p. ej., el de la agenda), y revisar que responda 403 sin datos de la agenda. Este agente no puede enviar peticiones HTTP con un token, ni leer el código de estado o el cuerpo de la respuesta, y el caso no da la ruta exacta del endpoint. Hay que ejecutarlo como prueba de API (Playwright request) indicando el endpoint concreto. · Script: AssertionError: 404

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar» — ok: apareció «Iniciar»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic

![captura](smoke-01/TC-034.png)

## TC-035 — ❌ Falla

Después de iniciar sesión como cliente (apareció «Mis vehículos»), entré directamente a /login. La URL final quedó en /login y se ve el formulario «Iniciar sesión» con los campos Correo y Contraseña. Se esperaba que me llevara a «Mis vehículos» sin mostrar el login. Además, al entrar a / tampoco apareció «Mis vehículos», así que es posible que la sesión no se mantenga al navegar por URL. · Script: AssertionError: Page URL expected to be 're.compile('/mis-vehiculos')' Actual value: https://taller-web-118746543308.us-central1.run.app/log

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Mis vehículos» — ok: apareció «Mis vehículos»
7. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
8. esperar texto «Mis vehículos» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
9. ir a /login — ok: abrió https://taller-web-118746543308.us-central1.run.app/login
10. esperar texto «Mis vehículos» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.

![captura](smoke-01/TC-035.png)

## TC-036 — ❌ Falla

Esperado: si ya hay sesión, entrar a /login lleva a "Agenda del día" y no muestra el formulario. Observado: el login funcionó y apareció "Agenda del día". Después, al entrar a / y luego a /login, la URL se quedó en /login y se mostró el formulario "Iniciar sesión" con los campos Correo y Contraseña. "Agenda del día" no apareció en ninguno de los dos casos. Hay dos explicaciones posibles: no hay redirección desde /login, o la sesión no se conserva al navegar directamente a otra URL. · Script: AssertionError: Page URL expected to be 're.compile('/interno')' Actual value: https://taller-web-118746543308.us-central1.run.app/login Cal

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Agenda del día» — ok: apareció «Agenda del día»
7. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
8. esperar texto «Agenda del día» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
9. ir a /login — ok: abrió https://taller-web-118746543308.us-central1.run.app/login
10. esperar texto «Agenda del día» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.

![captura](smoke-01/TC-036.png)

## TC-037 — ✅ Pasa



![captura](smoke-01/TC-037.png)

## TC-038 — ⛔ Bloqueado

El inicio de sesión, la navegación autenticada y el cierre de sesión se hicieron en https://taller-web-118746543308.us-central1.run.app. Después del login apareció el «Menú de usuario», y el cierre de sesión llevó a /login por https. No pude verificar tres cosas que pide el resultado esperado: (1) el registro de todas las peticiones de red y sus URL, (2) el atributo Secure de las cookies de sesión y (3) la redirección de http:// a https://. Mi herramienta no tiene acceso al tráfico de red ni a las cookies, y el ambiente no deja navegar a http://. Hay que revisarlo con un script de Playwright que registre las peticiones (page.on('request')), que lea context.cookies() y que pruebe una petición a http://…/login. · Script: AssertionError: 

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
3. escribir el usuario en textbox «Correo» — ok: escribió el usuario de la cuenta de prueba
4. escribir el contrasena en textbox «Contraseña» — ok: escribió el contrasena de la cuenta de prueba
5. clic button «Iniciar sesión» — ok: clic
6. esperar texto «Cerrar sesión» — FALLÓ: Locator.wait_for: Timeout 8000ms exceeded.
7. clic button «Menú de usuario» — ok: clic
8. clic menuitem «Cerrar sesión» — ok: clic
9. esperar texto «Iniciar sesión» — ok: apareció «Iniciar sesión»
10. ir a http://taller-web-118746543308.us-central1.run.app/login — FALLÓ: solo se puede navegar dentro del ambiente de pruebas (https://taller-web-118746543308.us-central1.run.app)

![captura](smoke-01/TC-038.png)

## TC-039 — ❌ Falla

No encontré documentación de la API en el ambiente. Probé /swagger-ui/index.html, /swagger-ui.html, /v3/api-docs, /docs, /api-docs, /api/swagger-ui/index.html, /api/v3/api-docs, /api/docs y /openapi.json. En la última comprobé que la página muestra "Página no encontrada. La dirección que buscas no existe o fue movida." El resultado esperado era ver los endpoints de login y logout con sus códigos 200/401/403/423 y sus mensajes. Si la documentación está en otro host o en otra ruta, falta ese dato para volver a ejecutar el caso. · Script: AssertionError: Locator expected to be visible Actual value: None Error: element(s) not found Call log:

Verificación del agente de navegador:

1. ir a / — ok: abrió https://taller-web-118746543308.us-central1.run.app/
2. ir a /swagger-ui/index.html — ok: abrió https://taller-web-118746543308.us-central1.run.app/swagger-ui/index.html
3. ir a /v3/api-docs — ok: abrió https://taller-web-118746543308.us-central1.run.app/v3/api-docs
4. ir a /swagger-ui.html — ok: abrió https://taller-web-118746543308.us-central1.run.app/swagger-ui.html
5. ir a /docs — ok: abrió https://taller-web-118746543308.us-central1.run.app/docs
6. ir a /api-docs — ok: abrió https://taller-web-118746543308.us-central1.run.app/api-docs
7. ir a /api/swagger-ui/index.html — ok: abrió https://taller-web-118746543308.us-central1.run.app/api/swagger-ui/index.html
8. ir a /api/v3/api-docs — ok: abrió https://taller-web-118746543308.us-central1.run.app/api/v3/api-docs
9. ir a /api/docs — ok: abrió https://taller-web-118746543308.us-central1.run.app/api/docs
10. ir a /openapi.json — ok: abrió https://taller-web-118746543308.us-central1.run.app/openapi.json

![captura](smoke-01/TC-039.png)
