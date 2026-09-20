---
hu_id: HU-002
fase: tcs_generados
total_tcs: 7
fecha_generacion: 2026-09-19
---

### TC-001 — deriva de: Dado que el usuario se encuentra en la pantalla de inicio de sesión, cuando selecciona la opción de recuperar contraseña e ingresa su correo electrónico registrado, entonces el sistema debe enviar un correo electrónico con las instrucciones/enlace para restablecer la contraseña sin requerir asistencia manual de un administrador.

Given que un usuario no autenticado está en la pantalla de inicio de sesión y hace clic en '¿Olvidaste tu contraseña?'
When ingresa su correo electrónico registrado 'usuario_valido@ejemplo.com' en el campo correspondiente y presiona el botón 'Enviar'
Then el sistema envía de forma automática un correo electrónico con el enlace único de restablecimiento y confirma la acción en la interfaz de usuario sin requerir aprobación o asistencia de un administrador.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se envía el correo con el enlace de recuperación al correo registrado y se notifica al usuario en pantalla.


### TC-002 — deriva de: Dado que el usuario solicita la recuperación e ingresa un correo electrónico (sea existente o no en el sistema), cuando presiona enviar, entonces el sistema muestra un mensaje genérico (ej. 'Si el correo está registrado, recibirás las instrucciones') para evitar la enumeración de usuarios/correos.

Given que un usuario no autenticado navega al formulario de recuperación de contraseña
When ingresa un correo electrónico que no existe en el sistema ('no_registrado@ejemplo.com') y presiona el botón 'Enviar'
Then el sistema muestra exactamente el mismo mensaje genérico 'Si el correo está registrado, recibirás las instrucciones' que muestra para correos válidos, evitando revelar la inexistencia de la cuenta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** La interfaz muestra el mensaje genérico de confirmación sin revelar el estado del correo en la base de datos ni generar ningún correo.


### TC-003 — deriva de: Dado que el usuario recibe el correo de recuperación, cuando hace clic en el enlace dentro del tiempo límite de validez (ej. 15 minutos), entonces es redirigido a un formulario seguro para ingresar la nueva contraseña.

Given que el usuario cuenta con un correo de recuperación cuyo token de acceso tiene menos de 15 minutos de haber sido generado
When hace clic en el enlace de restablecimiento contenido en el correo
Then el navegador lo redirige exitosamente a la página segura de restablecimiento de contraseña, donde se muestran los campos 'Nueva contraseña' y 'Confirmar nueva contraseña'.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se carga la pantalla de restablecimiento de contraseña de forma segura con los campos correspondientes habilitados.


### TC-004 — deriva de: Dado que el enlace de recuperación ya fue utilizado o ha expirado, cuando el usuario intenta ingresar a través de él, entonces el sistema le muestra un mensaje informando que el enlace no es válido y le ofrece la opción de solicitar uno nuevo.

Given que un usuario posee un enlace de recuperación emitido hace más de 15 minutos (expirado)
When ingresa a la aplicación mediante dicho enlace
Then el sistema impide la visualización del formulario de restablecimiento, muestra el mensaje 'El enlace no es válido o ha expirado' y despliega el botón 'Solicitar un nuevo enlace'.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El sistema bloquea el acceso al formulario, muestra la notificación de enlace vencido e incluye un botón o enlace funcional para iniciar un nuevo proceso.


### TC-005 — deriva de: Dado que el enlace de recuperación ya fue utilizado o ha expirado, cuando el usuario intenta ingresar a través de él, entonces el sistema le muestra un mensaje informando que el enlace no es válido y le ofrece la opción de solicitar uno nuevo.

Given que un usuario ya utilizó exitosamente su enlace de recuperación para actualizar su contraseña previamente
When intenta abrir nuevamente el mismo enlace en el navegador
Then el sistema detecta que el token ya fue consumido, muestra el mensaje 'El enlace no es válido o ya fue utilizado' y le ofrece la opción de solicitar uno nuevo.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El token previamente utilizado es rechazado, se muestra el mensaje de error correspondiente y se da la opción de reiniciar la solicitud.


### TC-006 — deriva de: Dado que el usuario ingresa su nueva contraseña en el formulario de restablecimiento, cuando la contraseña cumple con las políticas de complejidad (longitud, caracteres) y coincide con la confirmación, entonces el sistema actualiza la credencial, invalida el token utilizado y permite el inicio de sesión con la nueva clave.

Given que el usuario se encuentra en el formulario seguro de restablecimiento con un token válido
When ingresa una contraseña que cumple las políticas de complejidad (ej. 'Password123!') en el campo 'Nueva contraseña', la repite idénticamente en 'Confirmar contraseña' y presiona 'Guardar'
Then el sistema actualiza la clave en la base de datos, invalida el token de recuperación, redirige al inicio de sesión y permite ingresar exitosamente utilizando la nueva contraseña.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La credencial es actualizada, el token queda inservible y el usuario puede autenticarse de inmediato con la nueva clave.


### TC-007 — deriva de: Dado que el usuario ingresa su nueva contraseña en el formulario de restablecimiento, cuando la contraseña cumple con las políticas de complejidad (longitud, caracteres) y coincide con la confirmación, entonces el sistema actualiza la credencial, invalida el token utilizado y permite el inicio de sesión con la nueva clave.

Given que el usuario está en la pantalla de restablecimiento de contraseña
When ingresa una nueva contraseña que no cumple la política de complejidad (ej. '12345') o ingresa contraseñas no coincidentes entre ambos campos y presiona 'Guardar'
Then el sistema no procesa el cambio, muestra un mensaje explícito de error en los campos de la interfaz y no actualiza la credencial del usuario.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se visualizan alertas de error de validación en la interfaz y la contraseña actual de la cuenta permanece inalterada.
