---
hu_id: HU-002
fase: tcs_generados
total_tcs: 18
fecha_generacion: 2026-09-19
---

### TC-001 — deriva de: Given un usuario que olvidó su contraseña, When solicita la recuperación indicando su correo, Then el sistema le envía un mensaje a ese correo con el mecanismo para restablecerla.

Given un usuario activo registrado en la pantalla '¿Olvidaste tu contraseña?'; When ingresa su correo registrado y pulsa 'Enviar'; Then se muestra el mensaje de confirmación genérico y se consulta el buzón de prueba.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se muestra el mensaje genérico de confirmación y en el buzón del correo llega un mensaje con un enlace/token de restablecimiento válido.


### TC-002 — deriva de: Given un usuario que recibió el mensaje de recuperación, When completa el procedimiento y define una nueva contraseña, Then recupera el acceso a su cuenta sin intervención del administrador.

Given un usuario con correo de recuperación recibido; When abre el enlace, ingresa una nueva contraseña válida con confirmación coincidente y envía; Then inicia sesión en la pantalla de login con la nueva contraseña.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se muestra confirmación de restablecimiento, el login con la nueva contraseña es exitoso y llega al área autenticada; la contraseña anterior ya no funciona; sin intervención de un administrador.


### TC-003 — deriva de: Given un correo no registrado o cuenta inactiva, When se solicita la recuperación, Then el sistema muestra el mismo mensaje genérico ('si el correo existe, recibirás instrucciones') para no revelar qué cuentas existen, y no envía correo (o no permite el restablecimiento).

Given un correo con formato válido no registrado; When se solicita la recuperación desde la pantalla pública; Then se revisa el mensaje mostrado y el buzón correspondiente.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se muestra exactamente el mismo mensaje genérico que para un correo registrado (mismo texto, mismo tipo de respuesta) y no se envía ningún correo.


### TC-004 — deriva de: Given un correo no registrado o cuenta inactiva, When se solicita la recuperación, Then el sistema muestra el mismo mensaje genérico ('si el correo existe, recibirás instrucciones') para no revelar qué cuentas existen, y no envía correo (o no permite el restablecimiento).

Given una cuenta inactiva/deshabilitada existente; When se solicita la recuperación con su correo; Then se revisa el mensaje y el buzón.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se muestra el mismo mensaje genérico, no se envía correo de restablecimiento y no es posible restablecer la contraseña de esa cuenta.


### TC-005 — deriva de: Given un formato de correo inválido o campo vacío, When se envía la solicitud, Then se muestra un error de validación sin procesar la solicitud.

Given la pantalla de recuperación; When se envía el campo vacío, y luego valores con formato inválido ('usuario', 'a@', 'a@b'); Then se observa la respuesta de la UI y el buzón.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se muestra un error de validación claro en cada caso, no se muestra el mensaje de éxito genérico, no se procesa la solicitud ni se envía correo.


### TC-006 — deriva de: Given un enlace/token de recuperación, When se usa, Then es de un solo uso y expira tras un tiempo limitado; un token expirado, ya usado o inválido muestra un error claro y permite solicitar uno nuevo.

Given un enlace de recuperación ya utilizado con éxito; When se abre nuevamente el mismo enlace; Then se observa la pantalla.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se muestra un error claro de enlace ya usado/no válido, no permite definir contraseña y ofrece opción visible para solicitar un nuevo enlace.


### TC-007 — deriva de: Given un enlace/token de recuperación, When se usa, Then es de un solo uso y expira tras un tiempo limitado; un token expirado, ya usado o inválido muestra un error claro y permite solicitar uno nuevo.

Given un enlace de recuperación cuyo tiempo de vigencia configurado ya transcurrió (o expirado por entorno de prueba); When se abre el enlace e intenta restablecer; Then se observa el resultado.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se muestra error claro de enlace expirado, no se cambia la contraseña y se ofrece solicitar un nuevo enlace.


### TC-008 — deriva de: Given un enlace/token de recuperación, When se usa, Then es de un solo uso y expira tras un tiempo limitado; un token expirado, ya usado o inválido muestra un error claro y permite solicitar uno nuevo.

Given un enlace con el token alterado/inventado; When se abre en el navegador; Then se observa la pantalla.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se muestra error claro de enlace inválido, sin formulario de nueva contraseña, con opción de solicitar uno nuevo.


### TC-009 — deriva de: Given que se genera un nuevo token, When existía uno anterior pendiente, Then el anterior queda invalidado.

Given un usuario que solicitó recuperación dos veces seguidas y recibió dos correos; When abre primero el enlace del primer correo (anterior) y después el del segundo; Then se observan ambos resultados.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El enlace del primer correo muestra error de token inválido/expirado; el del segundo correo permite restablecer la contraseña.


### TC-010 — deriva de: Given la pantalla de nueva contraseña, When el usuario la ingresa, Then se valida contra la política de contraseñas vigente y se exige confirmación coincidente; si no cumple, se muestran los motivos.

Given la pantalla de nueva contraseña con token válido; When ingresa una contraseña que incumple la política (corta, sin complejidad requerida, igual a reciente si aplica); Then se envía el formulario.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** No se guarda la contraseña; se listan los motivos concretos del incumplimiento de la política y el token sigue vigente para reintentar.


### TC-011 — deriva de: Given la pantalla de nueva contraseña, When el usuario la ingresa, Then se valida contra la política de contraseñas vigente y se exige confirmación coincidente; si no cumple, se muestran los motivos.

Given la pantalla de nueva contraseña con token válido; When ingresa una contraseña válida y una confirmación distinta (o vacía); Then se envía el formulario.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se muestra error de que la confirmación no coincide, no se cambia la contraseña y el token no se consume.


### TC-012 — deriva de: Given un restablecimiento exitoso, When se guarda la nueva contraseña, Then se invalidan las sesiones activas previas y se notifica por correo al titular del cambio.

Given un usuario con sesión activa en un segundo navegador/contexto; When otro contexto completa el restablecimiento exitoso; Then en el contexto original se navega/recarga una página protegida y se revisa el buzón.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La sesión previa queda invalidada y redirige al login; llega al correo del titular una notificación de cambio de contraseña sin incluir la contraseña ni el token.


### TC-013 — deriva de: Given solicitudes repetidas de recuperación, When se supera un umbral por cuenta/IP/tiempo, Then se limita la frecuencia (rate limiting) para prevenir abuso y spam de correos.

Given la pantalla de recuperación; When se envían solicitudes consecutivas para el mismo correo superando el umbral configurado en el periodo definido; Then se observa la respuesta y el buzón.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Al superar el umbral se bloquea/limita la solicitud con mensaje de demasiados intentos (sin revelar existencia de cuenta), no se envían correos adicionales; tras el periodo se puede solicitar de nuevo.


### TC-014 — deriva de: Given el token y la contraseña, When se almacenan o registran, Then el token se guarda con hash, la contraseña con hash seguro, y ninguno aparece en logs; la comunicación es sobre HTTPS.

Given un flujo completo de recuperación ejecutado; When se inspeccionan la URL/tráfico del navegador, y (con acceso de prueba) la BD y los logs; Then se verifican los valores almacenados y registrados.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** admin
- **Resultado esperado:** Todas las páginas del flujo se sirven por HTTPS (HTTP redirige a HTTPS); en BD el token y la contraseña aparecen solo como hash; ni el token en claro ni la contraseña aparecen en logs.


### TC-015 — deriva de: Given un fallo en el envío del correo (servicio caído), When ocurre, Then el error se registra y el usuario puede reintentar sin que se exponga información sensible.

Given el servicio de correo simulado como caído; When un usuario solicita la recuperación con su correo; Then se observa la UI y luego se restablece el servicio y se reintenta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La UI muestra un mensaje genérico/de reintento sin detalles técnicos ni datos sensibles, el error queda registrado en logs, y al reintentar con el servicio activo el correo se envía.


### TC-016 — deriva de: Given una cuenta bloqueada por intentos fallidos, When se restablece la contraseña con éxito, Then se aplica la política definida para el desbloqueo (ver supuestos).

Given una cuenta bloqueada por intentos fallidos de login; When el titular completa el restablecimiento con éxito y luego intenta iniciar sesión; Then se observa el resultado.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se aplica la política de desbloqueo definida en los supuestos (p. ej. la cuenta queda desbloqueada y el login con la nueva contraseña es exitoso, o permanece bloqueada con mensaje acorde); el comportamiento coincide con dicha política.


### TC-017 — deriva de: Los eventos de solicitud y restablecimiento quedan registrados en auditoría (fecha, cuenta, IP) sin datos sensibles.

Given un administrador con acceso a auditoría; When un usuario realiza una solicitud y un restablecimiento y el admin consulta el registro de auditoría; Then se revisan las entradas.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** admin
- **Resultado esperado:** Existen entradas separadas para solicitud y restablecimiento con fecha, cuenta e IP, y sin contraseña ni token en claro.


### TC-018 — deriva de: La pantalla de login incluye un acceso visible a '¿Olvidaste tu contraseña?'.

Given la pantalla de login sin sesión; When se carga la página y se hace clic en '¿Olvidaste tu contraseña?'; Then se observa la navegación.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El enlace '¿Olvidaste tu contraseña?' es visible sin desplazamiento y al hacer clic lleva a la pantalla de solicitud de recuperación.
