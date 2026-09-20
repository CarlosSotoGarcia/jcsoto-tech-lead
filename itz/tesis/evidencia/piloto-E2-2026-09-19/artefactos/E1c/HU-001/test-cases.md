---
hu_id: HU-001
fase: tcs_generados
total_tcs: 21
fecha_generacion: 2026-09-19
---

### TC-001 — deriva de: Dado un usuario registrado, cuando ingresa su correo y contraseña correctos, entonces el sistema inicia su sesión y le da acceso al sistema.

Given un usuario registrado y activo está en la página de inicio de sesión. When escribe su correo y contraseña correctos y hace clic en 'Iniciar sesión'. Then se autentica.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El usuario es redirigido a la página principal del sistema, ve su nombre/cuenta en la interfaz y existe una cookie/token de sesión válido. No se muestra ningún mensaje de error.


### TC-002 — deriva de: Dado un usuario registrado, cuando ingresa su correo y contraseña correctos, entonces el sistema inicia su sesión y le da acceso al sistema.

Given un usuario registrado en el formulario de login. When ingresa credenciales correctas y presiona la tecla Enter en el campo de contraseña. Then se envía el formulario.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El inicio de sesión se completa igual que con el clic en el botón y el usuario accede a la página principal.


### TC-003 — deriva de: Dado un usuario autenticado, cuando consulta o navega por la información, entonces solo puede acceder a la información que le corresponde según su cuenta.

Given el usuario A ha iniciado sesión. When navega por todas las secciones y listados disponibles del sistema. Then se revisa la información mostrada.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Solo se muestran datos y opciones pertenecientes a la cuenta del usuario A; no aparece información de otros usuarios ni secciones no permitidas para su rol.


### TC-004 — deriva de: Dado un correo o contraseña incorrectos, cuando intenta iniciar sesión, entonces se rechaza el acceso y se muestra un mensaje genérico que no revela cuál de los dos datos falló.

Given un usuario registrado en la página de login. When ingresa su correo correcto y una contraseña incorrecta y envía el formulario. Then se rechaza el acceso.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Permanece en la página de login, no se crea sesión y se muestra un mensaje genérico (p. ej. 'Correo o contraseña incorrectos') sin indicar cuál dato falló. Los campos no exponen la contraseña.


### TC-005 — deriva de: Dado un correo o contraseña incorrectos, cuando intenta iniciar sesión, entonces se rechaza el acceso y se muestra un mensaje genérico que no revela cuál de los dos datos falló.

Given un usuario en la página de login. When ingresa un correo registrado en formato válido pero distinto al del titular de la contraseña, o ambos datos incorrectos, y envía. Then se rechaza.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se muestra exactamente el mismo mensaje genérico y no se inicia sesión.


### TC-006 — deriva de: Dado un correo que no está registrado, cuando intenta iniciar sesión, entonces se recibe el mismo mensaje genérico que con contraseña incorrecta.

Given un invitado en la página de login. When ingresa un correo con formato válido que no está registrado y cualquier contraseña y envía. Then se compara el mensaje con el de contraseña incorrecta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El texto del mensaje es idéntico al de contraseña incorrecta (mismo texto, mismo lugar en la interfaz, sin diferencias evidentes en el código de estado de la respuesta); no se revela que el correo no existe.


### TC-007 — deriva de: Dado que el correo o la contraseña están vacíos, cuando se intenta enviar el formulario, entonces se indica que los campos son obligatorios y no se realiza la autenticación.

Given un invitado en la página de login. When deja el correo vacío y la contraseña con valor y hace clic en 'Iniciar sesión'. Then se valida el formulario.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se muestra un mensaje de campo obligatorio para el correo, no se envía la petición de autenticación al servidor y no se crea sesión.


### TC-008 — deriva de: Dado que el correo o la contraseña están vacíos, cuando se intenta enviar el formulario, entonces se indica que los campos son obligatorios y no se realiza la autenticación.

Given un invitado en la página de login. When ingresa un correo válido, deja la contraseña vacía y envía. Then se valida el formulario.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se muestra un mensaje de campo obligatorio para la contraseña, no se realiza la autenticación y no se crea sesión.


### TC-009 — deriva de: Dado que el correo o la contraseña están vacíos, cuando se intenta enviar el formulario, entonces se indica que los campos son obligatorios y no se realiza la autenticación.

Given un invitado en la página de login. When deja ambos campos vacíos (o solo con espacios) y envía. Then se valida el formulario.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se indica que ambos campos son obligatorios, no hay llamada de autenticación y no se inicia sesión.


### TC-010 — deriva de: Dado un correo con formato inválido, cuando se intenta enviar, entonces se muestra un error de validación de formato.

Given un invitado en la página de login. When ingresa correos con formato inválido (p. ej. 'usuario', 'usuario@', 'usuario@dominio', 'a b@c.com') junto con una contraseña y envía. Then se valida el formato.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Para cada valor se muestra un error de validación de formato de correo, no se realiza la autenticación y no se crea sesión.


### TC-011 — deriva de: Dado un usuario no autenticado, cuando intenta acceder directamente a una URL o recurso protegido, entonces es redirigido al inicio de sesión y no ve información.

Given un usuario sin sesión iniciada. When escribe directamente en el navegador la URL de una página protegida (p. ej. el panel principal o perfil). Then se carga la ruta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Es redirigido a la página de inicio de sesión, no se muestra ningún dato de la página protegida (ni brevemente) y el recurso no se entrega.


### TC-012 — deriva de: Dado un usuario no autenticado, cuando intenta acceder directamente a una URL o recurso protegido, entonces es redirigido al inicio de sesión y no ve información.

Given un usuario sin sesión. When solicita directamente un endpoint de API protegido (sin cookie/token). Then se revisa la respuesta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El servidor responde 401/403 (o redirige al login) sin devolver datos del recurso.


### TC-013 — deriva de: Dado un usuario autenticado, cuando intenta acceder a un recurso o dato de otro usuario (por URL o API), entonces el acceso se deniega en el servidor (no solo se oculta en la interfaz).

Given el usuario A autenticado y conocido el identificador de un recurso del usuario B. When A navega directamente a la URL del recurso de B modificando el ID en la URL. Then se revisa la respuesta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El sistema muestra acceso denegado/no encontrado (403/404) y no muestra ningún dato del usuario B.


### TC-014 — deriva de: Dado un usuario autenticado, cuando intenta acceder a un recurso o dato de otro usuario (por URL o API), entonces el acceso se deniega en el servidor (no solo se oculta en la interfaz).

Given el usuario A autenticado (con su token de sesión). When realiza una petición API (GET y también PUT/DELETE) al recurso del usuario B usando la sesión de A. Then se revisa la respuesta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El servidor responde 403/404 sin devolver ni modificar datos del usuario B; los datos de B permanecen intactos.


### TC-015 — deriva de: La contraseña se transmite cifrada (HTTPS), se almacena con hash seguro y nunca se muestra en texto plano ni se registra en logs; el campo la enmascara.

Given un invitado en la página de login. When escribe caracteres en el campo de contraseña. Then se inspecciona el campo.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El campo es de tipo password y muestra los caracteres enmascarados; el valor no se expone en texto plano en la interfaz.


### TC-016 — deriva de: La contraseña se transmite cifrada (HTTPS), se almacena con hash seguro y nunca se muestra en texto plano ni se registra en logs; el campo la enmascara.

Given un invitado. When abre la página de login por HTTP (http://) y luego inicia sesión monitoreando la red. Then se revisan las peticiones.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** HTTP es redirigido a HTTPS; la petición de login se envía únicamente por HTTPS y la contraseña no viaja en la URL ni en query string.


### TC-017 — deriva de: La contraseña se transmite cifrada (HTTPS), se almacena con hash seguro y nunca se muestra en texto plano ni se registra en logs; el campo la enmascara.

Given intentos de login exitosos y fallidos realizados. When un administrador revisa los logs de la aplicación y los datos almacenados de la cuenta. Then se busca la contraseña usada.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** admin
- **Resultado esperado:** La contraseña en texto plano no aparece en logs ni en respuestas; en almacenamiento solo existe un hash seguro (bcrypt/argon2 o similar) con sal.


### TC-018 — deriva de: Dado un inicio de sesión exitoso, cuando expira la sesión por inactividad o el usuario cierra sesión, entonces se invalida la sesión y se exige autenticarse de nuevo.

Given un usuario con sesión iniciada. When hace clic en 'Cerrar sesión' y luego presiona el botón Atrás del navegador o intenta abrir una URL protegida. Then se revisa el acceso.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Es redirigido al login, no se muestra información protegida y el token/cookie anterior es rechazado por el servidor si se reutiliza.


### TC-019 — deriva de: Dado un inicio de sesión exitoso, cuando expira la sesión por inactividad o el usuario cierra sesión, entonces se invalida la sesión y se exige autenticarse de nuevo.

Given un usuario con sesión iniciada que permanece inactivo por el tiempo máximo configurado de inactividad. When intenta realizar una acción o navegar a otra página. Then se evalúa la sesión.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La sesión se considera expirada, se redirige al login (con aviso de sesión expirada) y se exige autenticarse de nuevo.


### TC-020 — deriva de: Dado que el correo se ingresa con distinta capitalización o espacios al inicio/fin, entonces se normaliza antes de validar.

Given un usuario registrado con correo 'usuario@ejemplo.com'. When ingresa '  Usuario@Ejemplo.COM  ' (mayúsculas y espacios al inicio/fin) con la contraseña correcta y envía. Then se valida.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El correo se normaliza (trim y minúsculas), no se muestra error de formato y el inicio de sesión es exitoso.


### TC-021 — deriva de: Dado que el correo se ingresa con distinta capitalización o espacios al inicio/fin, entonces se normaliza antes de validar.

Given un usuario registrado. When ingresa su correo con espacios al inicio/fin y una contraseña incorrecta (o con capitalización distinta en la contraseña). Then se envía.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El correo se normaliza pero la contraseña no: se rechaza el acceso con el mensaje genérico, confirmando que la contraseña sigue siendo sensible a mayúsculas.
