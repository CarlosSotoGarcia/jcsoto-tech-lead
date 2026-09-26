---
hu_id: HU-002
fase: tcs_generados
total_tcs: 14
fecha_generacion: 2026-09-21
---

### TC-001 — deriva de: Dado que soy un usuario que olvidó su contraseña, cuando solicito recuperarla indicando mi correo, entonces el sistema me envía un mensaje a ese correo con el medio para restablecerla.

Given un usuario_final con cuenta activa registrada con su correo y en la página de login. When hace clic en '¿Olvidaste tu contraseña?', ingresa su correo registrado y envía el formulario. Then se muestra el mensaje de confirmación y se revisa el buzón de prueba.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se muestra el mensaje 'si el correo existe, recibirás instrucciones' y en el buzón del correo llega un único mensaje con un enlace de restablecimiento (HTTPS) en un plazo razonable (p. ej. < 1 min).


### TC-002 — deriva de: Dado que recibí el correo de recuperación, cuando sigo el procedimiento indicado y defino una nueva contraseña, entonces recupero el acceso a mi cuenta sin intervención del administrador.

Given un usuario_final que recibió el correo de recuperación con enlace vigente. When abre el enlace, ingresa una nueva contraseña válida y su confirmación idéntica y envía el formulario; luego va al login e ingresa con la nueva contraseña. Then accede a su cuenta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se muestra confirmación de cambio exitoso, el login con la nueva contraseña da acceso al panel de la cuenta y el login con la contraseña anterior es rechazado. No se requirió ninguna acción de administrador.


### TC-003 — deriva de: Dado un correo no registrado o cuenta inexistente, cuando solicito recuperación, entonces el sistema muestra el mismo mensaje genérico ('si el correo existe, recibirás instrucciones') para no revelar qué correos están registrados.

Given un invitado en el formulario de recuperación. When envía un correo con formato válido que no está registrado, y luego repite con un correo registrado. Then se comparan mensajes, comportamiento de pantalla y correos recibidos.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Ambas solicitudes muestran exactamente el mismo mensaje genérico, con la misma redirección/estado HTTP y sin diferencias visibles; no se envía ningún correo al correo no registrado.


### TC-004 — deriva de: Dado un correo con formato inválido o vacío, cuando envío la solicitud, entonces se muestra un error de validación y no se envía nada.

Given un invitado en el formulario de recuperación. When deja el campo de correo vacío y envía; luego repite con valores de formato inválido ('usuario', 'usuario@', 'a@b'). Then se observa la respuesta de UI y el buzón.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se muestra un mensaje de error de validación de correo en cada caso, no se muestra el mensaje genérico de éxito y no se envía ningún correo ni se genera token.


### TC-005 — deriva de: Dado que se generó un enlace/token de restablecimiento, cuando pasa su tiempo de vigencia, entonces deja de ser válido y se informa al usuario que debe solicitar uno nuevo.

Given un enlace de restablecimiento generado para un usuario_final y cuyo tiempo de vigencia configurado ya transcurrió (esperando o simulando el paso del tiempo en el entorno de prueba). When abre el enlace y trata de definir una nueva contraseña. Then se observa la respuesta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El sistema rechaza el enlace, no cambia la contraseña y muestra un mensaje indicando que el enlace expiró y que debe solicitar uno nuevo, con acceso al formulario de recuperación.


### TC-006 — deriva de: Dado un token ya utilizado, cuando intento usarlo de nuevo, entonces el sistema lo rechaza (uso único).

Given un usuario_final que ya restableció su contraseña con un enlace. When vuelve a abrir el mismo enlace e intenta definir otra contraseña. Then se observa la respuesta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El sistema rechaza el enlace por ya utilizado/inválido con mensaje claro, no permite cambiar la contraseña y la contraseña vigente sigue siendo la definida en el primer uso.


### TC-007 — deriva de: Dado que solicito un nuevo enlace, cuando ya existía uno vigente, entonces el anterior queda invalidado.

Given un usuario_final que solicitó recuperación y recibió el enlace A vigente. When solicita recuperación de nuevo, recibe el enlace B, y abre primero el enlace A y luego el enlace B. Then se observa el resultado de cada uno.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El enlace A es rechazado como inválido/expirado con mensaje para solicitar uno nuevo; el enlace B permite definir la nueva contraseña con éxito.


### TC-008 — deriva de: Dada la nueva contraseña, cuando no cumple la política de contraseñas vigente o la confirmación no coincide, entonces se rechaza con un mensaje claro y el token sigue siendo válido hasta su expiración.

Given un usuario_final con enlace vigente abierto. When ingresa una contraseña que incumple la política (p. ej. demasiado corta/sin complejidad) y envía; luego ingresa una contraseña válida con confirmación distinta y envía; finalmente ingresa una contraseña válida con confirmación coincidente. Then se observa cada respuesta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** En los dos primeros intentos se muestra un mensaje claro (requisitos de la política / las contraseñas no coinciden), la contraseña no cambia y el token sigue válido; en el tercer intento el cambio se completa con éxito.


### TC-009 — deriva de: Dado que se restableció la contraseña con éxito, entonces se invalidan las sesiones activas previas y se notifica por correo el cambio realizado.

Given un usuario_final con una sesión activa en el navegador A (contexto Playwright 1) y que restablece su contraseña desde el navegador B (contexto 2) con un enlace válido. When completa el restablecimiento y luego en el navegador A recarga o navega a una página protegida. Then se revisa la sesión y el buzón.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La sesión del navegador A es cerrada y redirige al login; el usuario recibe un correo notificando el cambio de contraseña (sin incluir la contraseña).


### TC-010 — deriva de: Dadas múltiples solicitudes repetidas, cuando se supera un límite razonable por correo/IP, entonces se aplica limitación de frecuencia (rate limiting) para evitar abuso y spam.

Given un invitado en el formulario de recuperación. When envía solicitudes repetidas consecutivas para el mismo correo (y luego con distintos correos desde la misma IP) superando el límite configurado. Then se observa la respuesta y el buzón.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Al superar el límite el sistema bloquea o ralentiza las solicitudes (mensaje de demasiados intentos / HTTP 429 o respuesta genérica sin envío), no se envían correos adicionales más allá del límite y tras la ventana de espera se puede solicitar de nuevo.


### TC-011 — deriva de: Dado que el token se almacena, entonces se guarda de forma segura (hash) y es no predecible; la comunicación se realiza sobre HTTPS.

Given un invitado que solicita recuperación varias veces con distintas cuentas de prueba. When se comparan los enlaces recibidos por correo, se inspecciona la URL del enlace y se intenta abrir la versión HTTP del formulario y del enlace. Then se revisan además los datos almacenados con acceso de consulta de prueba.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Los tokens de los enlaces son largos, distintos y sin patrón secuencial; los enlaces usan HTTPS y HTTP redirige a HTTPS o se rechaza; el token almacenado en base de datos es un hash y no coincide con el valor del enlace.


### TC-012 — deriva de: Dado un fallo en el envío del correo, entonces el error se registra y el usuario no recibe información que comprometa la seguridad.

Given un entorno de prueba con el servicio de correo configurado para fallar y una cuenta registrada. When un invitado solicita recuperación con el correo registrado. Then se observa la UI y los logs del sistema.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** La UI muestra el mismo mensaje genérico (sin detalles técnicos ni indicación de que el correo existe o de que falló el envío); el error queda registrado en los logs del sistema sin datos sensibles.


### TC-013 — deriva de: Dada una cuenta bloqueada/inactiva/deshabilitada, cuando se solicita recuperación, entonces no se permite el restablecimiento (comportamiento externo idéntico al genérico).

Given cuentas de prueba bloqueada, inactiva y deshabilitada. When un invitado solicita recuperación con el correo de cada una. Then se observan la UI y los buzones.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** En cada caso se muestra el mismo mensaje genérico que para un correo inexistente, no se envía enlace de restablecimiento y no es posible restablecer la contraseña de esas cuentas.


### TC-014 — deriva de: Los eventos de solicitud y restablecimiento quedan registrados en auditoría (sin incluir contraseñas ni tokens).

Given un admin con acceso al registro de auditoría y un usuario_final que realiza una solicitud de recuperación y un restablecimiento exitoso. When el admin consulta el registro de auditoría de esos eventos. Then se revisa el contenido de las entradas.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** admin
- **Resultado esperado:** Existen entradas de auditoría para la solicitud y para el restablecimiento con fecha/hora, tipo de evento e identificador de la cuenta/IP; ninguna entrada contiene la contraseña ni el token.
