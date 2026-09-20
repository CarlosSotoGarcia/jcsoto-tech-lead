---
hu_id: HU-001
fase: tcs_generados
total_tcs: 6
fecha_generacion: 2026-09-19
---

### TC-001 — deriva de: Dado que un usuario registrado se encuentra en la pantalla de inicio de sesión, Cuando ingresa su correo electrónico y contraseña válidos y hace clic en "Iniciar sesión", Entonces el sistema autentica exitosamente al usuario y lo redirige a la plataforma, garantizando acceso únicamente a la información asociada a su cuenta y rol.

Given que el usuario registrado se encuentra en la pantalla de inicio de sesión
When ingresa un correo electrónico válido y su contraseña correspondiente
And hace clic en el botón "Iniciar sesión"
Then el sistema autentica exitosamente al usuario y lo redirige al panel principal de la plataforma acorde a su rol

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El usuario es autenticado correctamente, redirigido a la plataforma y se visualiza únicamente la información y funcionalidades asociadas a su rol.


### TC-002 — deriva de: Dado que el usuario deja vacíos los campos de correo o contraseña, Cuando intenta iniciar sesión, Entonces el sistema impide el envío del formulario y muestra mensajes de validación indicando que los campos son obligatorios.

Given que el usuario se encuentra en la pantalla de inicio de sesión
When deja vacíos los campos de correo electrónico y contraseña
And hace clic en el botón "Iniciar sesión"
Then el sistema impide el envío del formulario
And muestra mensajes de error en la interfaz indicando que los campos son obligatorios

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El formulario de inicio de sesión no se envía y la UI muestra mensajes de campo obligatorio debajo de los campos vacíos.


### TC-003 — deriva de: Dado que el usuario ingresa un texto que no cumple con el formato estándar de correo electrónico, Cuando intenta iniciar sesión, Entonces el sistema muestra una validación de formato de correo inválido.

Given que el usuario se encuentra en la pantalla de inicio de sesión
When ingresa un texto con formato incorrecto de correo electrónico (ej. "usuario_sin_arroba")
And ingresa una contraseña
And hace clic en el botón "Iniciar sesión"
Then el sistema muestra un mensaje de validación indicando que el formato del correo electrónico no es válido

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Aparece un mensaje de error en la UI indicando que el correo electrónico no cumple con el formato estándar.


### TC-004 — deriva de: Dado que el usuario ingresa credenciales incorrectas (correo no registrado o contraseña errónea), Cuando intenta iniciar sesión, Entonces el sistema muestra un mensaje de error genérico ("Correo o contraseña incorrectos") para evitar la divulgación de usuarios existentes.

Given que el usuario se encuentra en la pantalla de inicio de sesión
When ingresa un correo no registrado o una contraseña errónea
And hace clic en el botón "Iniciar sesión"
Then el sistema muestra el mensaje de error genérico "Correo o contraseña incorrectos" sin especificar cuál de los dos datos falló

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se despliega en la interfaz el mensaje genérico "Correo o contraseña incorrectos" impidiendo el acceso a la plataforma.


### TC-005 — deriva de: Dado que el usuario escribe su contraseña, Cuando interactúa con el campo de texto, Entonces los caracteres se muestran enmascarados/ocultos por defecto.

Given que el usuario se encuentra en la pantalla de inicio de sesión
When escribe caracteres en el campo de texto de contraseña
Then los caracteres dentro del campo se muestran enmascarados/ocultos por defecto (input type="password")

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Los caracteres ingresados en la caja de texto de contraseña son ilegibles visualmente (enmascarados con puntos/asteriscos).


### TC-006 — deriva de: Dado que una cuenta de usuario se encuentra en estado inactivo o suspendido, Cuando el usuario intenta iniciar sesión con credenciales válidas, Entonces el sistema deniega el acceso y muestra un mensaje indicando que la cuenta no está activa.

Given que el usuario posee una cuenta registrada en estado inactivo o suspendido y se encuentra en la pantalla de inicio de sesión
When ingresa sus credenciales válidas (correo y contraseña)
And hace clic en el botón "Iniciar sesión"
Then el sistema deniega el acceso y muestra un mensaje indicando que la cuenta no se encuentra activa

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_inactivo
- **Resultado esperado:** El acceso es denegado y se visualiza en pantalla un mensaje notificando que la cuenta no está activa.
