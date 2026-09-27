---
hu_id: HU-002
fase: tcs_generados
total_tcs: 39
fecha_generacion: 2026-09-26
---

### TC-001 — deriva de: E1 – Login correcto: Dado que tengo una cuenta activa, cuando ingreso un correo y una contraseña válidos, entonces accedo a la pantalla inicial de mi rol.

Given una cuenta activa de cliente sin intentos fallidos y el navegador en la pantalla de login sin sesión
When escribo el correo y la contraseña válidos y pulso "Iniciar sesión"
Then se sale de la pantalla de login y se muestra la pantalla inicial del rol

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente
- **Resultado esperado:** La URL ya no es la de login, el formulario de login no está visible y aparece un elemento propio de la sesión (p. ej., el botón "Cerrar sesión"). La petición de login responde 200.


### TC-002 — deriva de: E1a – Redirección de cliente (regla de negocio): Dado que soy un cliente con cuenta activa, cuando inicio sesión correctamente, entonces el sistema me lleva a "Mis vehículos".

Given una cuenta activa de cliente y el navegador en la pantalla de login
When inicio sesión con credenciales válidas
Then el sistema me redirige a "Mis vehículos"

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente
- **Resultado esperado:** La URL corresponde a la ruta de "Mis vehículos" y el encabezado visible dice "Mis vehículos". No se muestra "Agenda del día".


### TC-003 — deriva de: E1b – Redirección de personal (regla de negocio): Dado que soy personal interno con cuenta activa, cuando inicio sesión correctamente, entonces el sistema me lleva a "Agenda del día".

Given una cuenta activa de personal interno y el navegador en la pantalla de login
When inicio sesión con credenciales válidas
Then el sistema me redirige a "Agenda del día"

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** personal_interno
- **Resultado esperado:** La URL corresponde a la ruta de "Agenda del día" y el encabezado visible dice "Agenda del día". No se muestra "Mis vehículos".


### TC-004 — deriva de: E2 – Credenciales incorrectas: Dado que ingreso una contraseña errónea, cuando intento entrar, entonces veo un mensaje genérico que no revela si el correo existe.

Given una cuenta activa registrada y el navegador en la pantalla de login
When ingreso el correo correcto con una contraseña errónea y pulso "Iniciar sesión"
Then se muestra un mensaje de error genérico y sigo en la pantalla de login

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente
- **Resultado esperado:** Aparece un mensaje genérico (p. ej., "Correo o contraseña incorrectos") que no menciona si el correo existe ni cuál campo está mal. La URL sigue siendo la de login, la API responde 401 y no se guarda ningún token en cookies ni en el storage.


### TC-005 — deriva de: E3 – Bloqueo por intentos: Dado que fallé 5 veces seguidas, cuando intento de nuevo, entonces se muestra que la cuenta está bloqueada temporalmente y no se permite el acceso.

Given una cuenta activa de uso exclusivo para esta prueba con el contador de intentos fallidos en 0
When envío 5 veces seguidas una contraseña errónea y después intento entrar una sexta vez
Then se indica que la cuenta está bloqueada temporalmente y no se permite el acceso

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente_bloqueable
- **Resultado esperado:** En el sexto intento aparece un mensaje de bloqueo temporal, distinto del mensaje genérico de credenciales incorrectas. La API responde 423 (o el código de bloqueo documentado), la URL sigue siendo la de login y no se emite ningún token.


### TC-006 — deriva de: E3 – Bloqueo por intentos: Dado que fallé 5 veces seguidas, cuando intento de nuevo, entonces se muestra que la cuenta está bloqueada temporalmente y no se permite el acceso.

Given una cuenta activa de uso exclusivo para esta prueba con el contador de intentos fallidos en 0
When envío 4 veces seguidas una contraseña errónea y después intento entrar una quinta vez con contraseña errónea
Then el quinto intento todavía muestra el mensaje genérico (caso límite) y a partir del siguiente se muestra el bloqueo

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente_bloqueable
- **Resultado esperado:** Los intentos 1 a 4 muestran solo el mensaje genérico, sin mensaje de bloqueo. Al completar el quinto fallo la cuenta queda bloqueada: ese mismo intento, o el sexto según la especificación, muestra el mensaje de bloqueo temporal. El número exacto de intentos queda confirmado.


### TC-007 — deriva de: E3a – Duración del bloqueo (regla de negocio): Dado que mi cuenta fue bloqueada por 5 intentos fallidos, cuando pasan 15 minutos, entonces puedo volver a intentar el inicio de sesión.

Given una cuenta bloqueada por 5 intentos fallidos
When pasan 15 minutos desde el bloqueo (espera real o reloj del servidor adelantado en el entorno de prueba) e ingreso las credenciales correctas
Then el inicio de sesión funciona

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente_bloqueable
- **Resultado esperado:** Ya no aparece el mensaje de bloqueo, la API responde 200 y se redirige a "Mis vehículos".


### TC-008 — deriva de: E3a – Duración del bloqueo (regla de negocio): Dado que mi cuenta fue bloqueada por 5 intentos fallidos, cuando pasan 15 minutos, entonces puedo volver a intentar el inicio de sesión.

Given una cuenta bloqueada por 5 intentos fallidos
When pasan 14 minutos (justo antes del límite) e intento entrar con las credenciales correctas
Then sigo bloqueado

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente_bloqueable
- **Resultado esperado:** Se muestra el mensaje de bloqueo temporal, la API responde 423 (o el código de bloqueo documentado) y la URL sigue siendo la de login.


### TC-009 — deriva de: E4 – Cierre de sesión: Dado que estoy autenticado, cuando selecciono "Cerrar sesión", entonces se invalida mi token y vuelvo a la pantalla de login.

Given un cliente autenticado en "Mis vehículos"
When pulso "Cerrar sesión"
Then vuelvo a la pantalla de login y se borra la sesión en el cliente

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente
- **Resultado esperado:** La URL es la de login y se ve el formulario. La petición de logout responde 200 (o 204). El token o la cookie de sesión ya no está en el storage ni en las cookies.


### TC-010 — deriva de: E4 – Cierre de sesión: Dado que estoy autenticado, cuando selecciono "Cerrar sesión", entonces se invalida mi token y vuelvo a la pantalla de login.

Given personal interno autenticado en "Agenda del día"
When pulso "Cerrar sesión"
Then vuelvo a la pantalla de login

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** personal_interno
- **Resultado esperado:** La URL es la de login, el formulario está visible y la cookie o el token de sesión ya no existe.


### TC-011 — deriva de: E5 – Expiración por inactividad (regla de negocio): Dado que soy personal interno autenticado, cuando pasan 30 minutos sin actividad, entonces mi sesión expira y debo volver a autenticarme.

Given personal interno autenticado en "Agenda del día"
When pasan 30 minutos sin actividad (con page.clock y/o el reloj del servidor adelantado) y después recargo o navego a "Agenda del día"
Then la sesión ha expirado y me pide autenticarme de nuevo

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** personal_interno
- **Resultado esperado:** Se redirige al login. Las peticiones con el token anterior responden 401 y no se muestra contenido de la agenda.


### TC-012 — deriva de: E5 – Expiración por inactividad (regla de negocio): Dado que soy personal interno autenticado, cuando pasan 30 minutos sin actividad, entonces mi sesión expira y debo volver a autenticarme.

Given personal interno autenticado en "Agenda del día"
When pasan 29 minutos sin actividad (justo antes del límite) y navego dentro de la agenda
Then la sesión sigue activa

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** personal_interno
- **Resultado esperado:** La navegación funciona sin redirigir al login, la API responde 200 y no aparece el mensaje de sesión expirada.


### TC-013 — deriva de: E6 – Cuentas no habilitadas (regla de negocio): Dado que mi cuenta está inactiva o pendiente de verificación, cuando ingreso credenciales correctas, entonces no se me permite el acceso.

Given una cuenta en estado inactivo y el navegador en la pantalla de login
When ingreso su correo y su contraseña correctos
Then no se me permite el acceso

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cuenta_inactiva
- **Resultado esperado:** La URL sigue siendo la de login y se muestra un mensaje de cuenta no habilitada (según el texto definido). La API responde 403 (o el código documentado) y no se emite ningún token.


### TC-014 — deriva de: E6 – Cuentas no habilitadas (regla de negocio): Dado que mi cuenta está inactiva o pendiente de verificación, cuando ingreso credenciales correctas, entonces no se me permite el acceso.

Given una cuenta pendiente de verificación y el navegador en la pantalla de login
When ingreso su correo y su contraseña correctos
Then no se me permite el acceso

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cuenta_pendiente_verificacion
- **Resultado esperado:** La URL sigue siendo la de login y se muestra un mensaje de cuenta no habilitada o pendiente de verificación. La API responde 403 (o el código documentado) y no se emite ningún token.


### TC-015 — deriva de: I1 – Campos obligatorios: Dado que estoy en el login, cuando envío el formulario con el correo o la contraseña vacíos, entonces se muestra una validación junto al campo y no se envía la petición. La validación también se aplica en el backend, según la definición de terminado.

Given el navegador en la pantalla de login sin sesión
When dejo el correo vacío, relleno la contraseña y pulso "Iniciar sesión"
Then aparece una validación junto al campo de correo y no se envía la petición

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se ve un mensaje de campo obligatorio junto al correo. Playwright no registra ninguna petición al endpoint de login y la URL sigue siendo la de login.


### TC-016 — deriva de: I1 – Campos obligatorios: Dado que estoy en el login, cuando envío el formulario con el correo o la contraseña vacíos, entonces se muestra una validación junto al campo y no se envía la petición. La validación también se aplica en el backend, según la definición de terminado.

Given el navegador en la pantalla de login sin sesión
When relleno el correo, dejo la contraseña vacía y pulso "Iniciar sesión"
Then aparece una validación junto al campo de contraseña y no se envía la petición

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se ve un mensaje de campo obligatorio junto a la contraseña y no se registra ninguna petición al endpoint de login.


### TC-017 — deriva de: I1 – Campos obligatorios: Dado que estoy en el login, cuando envío el formulario con el correo o la contraseña vacíos, entonces se muestra una validación junto al campo y no se envía la petición. La validación también se aplica en el backend, según la definición de terminado.

Given un contexto de Playwright (APIRequestContext) sin sesión
When envío directamente al endpoint de login un cuerpo con el correo y/o la contraseña vacíos o sin incluir
Then el backend rechaza la petición

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** La respuesta es 400 (o 422) con un error de validación, no se emite ningún token y el intento no cuenta como fallido para ninguna cuenta.


### TC-018 — deriva de: I2 – Formato de correo: Dado que ingreso un correo con formato inválido, cuando intento entrar, entonces se indica que el formato es incorrecto y no cuenta como intento fallido de la cuenta.

Given el navegador en la pantalla de login
When escribo un correo con formato inválido (p. ej., "usuario@" o "usuario.dominio.com") y una contraseña, y pulso "Iniciar sesión"
Then se indica que el formato del correo es incorrecto

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Aparece un mensaje de formato de correo inválido junto al campo, que no es el mensaje genérico de credenciales. La URL sigue siendo la de login.


### TC-019 — deriva de: I2 – Formato de correo: Dado que ingreso un correo con formato inválido, cuando intento entrar, entonces se indica que el formato es incorrecto y no cuenta como intento fallido de la cuenta.

Given una cuenta activa con 4 intentos fallidos consecutivos
When envío un login con una variante de su correo con formato inválido y después envío un quinto intento con el correo correcto y una contraseña errónea
Then el intento con formato inválido no se sumó al contador

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente_bloqueable
- **Resultado esperado:** Tras el intento con formato inválido no aparece el mensaje de bloqueo. El bloqueo solo se activa después del quinto fallo real, lo que confirma que el intento con formato inválido no contó.


### TC-020 — deriva de: I3 – Correo inexistente: Dado que ingreso un correo que no está registrado, cuando intento entrar, entonces recibo el mismo mensaje genérico, con un tiempo de respuesta comparable al de una contraseña errónea.

Given el navegador en la pantalla de login
When ingreso un correo con formato válido que no está registrado y cualquier contraseña
Then recibo el mismo mensaje genérico que con una contraseña errónea

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El texto del mensaje es idéntico al de E2 y la API responde con el mismo código (401) y un cuerpo equivalente al de una contraseña errónea.


### TC-021 — deriva de: I3 – Correo inexistente: Dado que ingreso un correo que no está registrado, cuando intento entrar, entonces recibo el mismo mensaje genérico, con un tiempo de respuesta comparable al de una contraseña errónea.

Given una cuenta registrada y un correo no registrado
When mido con Playwright el tiempo de respuesta del endpoint de login en N intentos (p. ej., 10) con el correo inexistente y en N intentos con el correo existente y una contraseña errónea
Then los tiempos son comparables

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** La diferencia entre las medianas de ambos grupos está dentro del umbral acordado (p. ej., menos de 100 ms). Nota: la cuenta existente debe restablecerse para que los intentos de medición no la bloqueen.


### TC-022 — deriva de: I4 – Reinicio del contador: Dado que tengo entre 1 y 4 intentos fallidos consecutivos, cuando inicio sesión correctamente, entonces el contador de intentos fallidos vuelve a cero.

Given una cuenta activa con 4 intentos fallidos consecutivos
When inicio sesión correctamente, cierro sesión y después fallo 4 veces más con una contraseña errónea
Then la cuenta no queda bloqueada

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente_bloqueable
- **Resultado esperado:** El login correcto redirige a "Mis vehículos". Los 4 fallos siguientes muestran solo el mensaje genérico, sin mensaje de bloqueo, y un login correcto posterior sigue funcionando.


### TC-023 — deriva de: I4 – Reinicio del contador: Dado que tengo entre 1 y 4 intentos fallidos consecutivos, cuando inicio sesión correctamente, entonces el contador de intentos fallidos vuelve a cero.

Given una cuenta activa con 1 intento fallido (límite inferior)
When inicio sesión correctamente, cierro sesión y después fallo 4 veces seguidas
Then la cuenta no queda bloqueada

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente_bloqueable
- **Resultado esperado:** No aparece el mensaje de bloqueo después de los 4 fallos, que en total serían 5 si el contador no se hubiera reiniciado.


### TC-024 — deriva de: I5 – Bloqueo con credenciales correctas: Dado que mi cuenta está bloqueada, cuando ingreso las credenciales correctas antes de que pasen los 15 minutos, entonces sigo sin acceso y veo el mensaje de bloqueo temporal.

Given una cuenta bloqueada por 5 intentos fallidos hace menos de 15 minutos
When ingreso el correo y la contraseña correctos
Then sigo sin acceso

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente_bloqueable
- **Resultado esperado:** Se muestra el mensaje de bloqueo temporal, la API responde 423 (o el código de bloqueo documentado), no se emite ningún token y la URL sigue siendo la de login.


### TC-025 — deriva de: I6 – Contraseña protegida: Dado que escribo mi contraseña, entonces el campo la oculta. Además, la contraseña nunca se guarda en texto plano ni aparece en logs o respuestas de la API.

Given el navegador en la pantalla de login
When escribo una contraseña en el campo correspondiente
Then el campo oculta los caracteres

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El input de contraseña tiene el atributo type="password" y el texto escrito no aparece en claro en la página.


### TC-026 — deriva de: I6 – Contraseña protegida: Dado que escribo mi contraseña, entonces el campo la oculta. Además, la contraseña nunca se guarda en texto plano ni aparece en logs o respuestas de la API.

Given una cuenta activa y Playwright capturando todas las respuestas de red
When inicio sesión (con éxito y con fallo) y navego por la pantalla inicial
Then ninguna respuesta de la API contiene la contraseña

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente
- **Resultado esperado:** Ningún cuerpo ni cabecera de respuesta contiene la contraseña usada, ni en claro ni como campo "password". La contraseña tampoco aparece en la URL, en localStorage, en sessionStorage ni en las cookies. Nota: comprobar que no se guarda en texto plano en la base de datos ni en los logs del servidor requiere revisión de backend, fuera del alcance de la UI.


### TC-027 — deriva de: I7 – Token inválido tras logout: Dado que cerré sesión, cuando se reutiliza el token anterior (por ejemplo, con el botón "Atrás" del navegador o una llamada directa a la API), entonces el backend responde 401 y no se muestra contenido protegido.

Given un cliente que inició sesión, navegó a "Mis vehículos" y luego cerró sesión
When pulso el botón "Atrás" del navegador (page.goBack)
Then no se muestra contenido protegido

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente
- **Resultado esperado:** No se muestran datos de "Mis vehículos" y se redirige al login. Cualquier petición a la API que se dispare responde 401.


### TC-028 — deriva de: I7 – Token inválido tras logout: Dado que cerré sesión, cuando se reutiliza el token anterior (por ejemplo, con el botón "Atrás" del navegador o una llamada directa a la API), entonces el backend responde 401 y no se muestra contenido protegido.

Given un cliente autenticado cuyo token se capturó antes de cerrar sesión
When, después del logout, llamo directamente con APIRequestContext a un endpoint protegido (p. ej., el listado de vehículos) usando el token anterior
Then el backend rechaza la petición

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente
- **Resultado esperado:** La respuesta es 401 y el cuerpo no contiene datos protegidos.


### TC-029 — deriva de: I8 – Expiración visible: Dado que mi sesión expiró por inactividad, cuando intento hacer cualquier acción, entonces me lleva al login con un mensaje de sesión expirada.

Given personal interno cuya sesión expiró tras 30 minutos de inactividad (con el reloj simulado)
When hago clic en cualquier acción de "Agenda del día"
Then me lleva al login con un aviso de sesión expirada

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** personal_interno
- **Resultado esperado:** La URL es la de login y se ve un mensaje explícito de sesión expirada, distinto del mensaje de credenciales incorrectas.


### TC-030 — deriva de: I9 – Actividad renueva la sesión: Dado que soy personal interno, cuando hago una acción antes de cumplir 30 minutos de inactividad, entonces el contador de inactividad se reinicia.

Given personal interno autenticado en "Agenda del día"
When pasan 25 minutos, hago una acción (p. ej., navegar u operar en la agenda) y luego pasan otros 25 minutos (50 en total, pero solo 25 desde la última actividad) y hago otra acción
Then la sesión sigue activa

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** personal_interno
- **Resultado esperado:** La segunda acción funciona sin redirigir al login, la API responde 200 y no aparece el mensaje de sesión expirada.


### TC-031 — deriva de: I9 – Actividad renueva la sesión: Dado que soy personal interno, cuando hago una acción antes de cumplir 30 minutos de inactividad, entonces el contador de inactividad se reinicia.

Given personal interno que hizo una acción en el minuto 25
When pasan 30 minutos más sin actividad y hago una acción
Then la sesión expira, porque el contador se reinició en el minuto 25 y no antes

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** personal_interno
- **Resultado esperado:** Se redirige al login con el mensaje de sesión expirada.


### TC-032 — deriva de: I10 – Permisos por rol: Dado que estoy autenticado con un rol, cuando intento acceder a una ruta o endpoint de otro rol, entonces el acceso se deniega (403 o redirección a mi pantalla inicial).

Given un cliente autenticado
When navego directamente con la URL a la ruta de "Agenda del día"
Then se deniega el acceso

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente
- **Resultado esperado:** Se redirige a "Mis vehículos" o se muestra una página de acceso denegado (403) y no se ve contenido de la agenda.


### TC-033 — deriva de: I10 – Permisos por rol: Dado que estoy autenticado con un rol, cuando intento acceder a una ruta o endpoint de otro rol, entonces el acceso se deniega (403 o redirección a mi pantalla inicial).

Given personal interno autenticado
When navego directamente con la URL a la ruta de "Mis vehículos" del cliente
Then se deniega el acceso

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** personal_interno
- **Resultado esperado:** Se redirige a "Agenda del día" o se muestra una página de acceso denegado (403) y no se ven los vehículos del cliente.


### TC-034 — deriva de: I10 – Permisos por rol: Dado que estoy autenticado con un rol, cuando intento acceder a una ruta o endpoint de otro rol, entonces el acceso se deniega (403 o redirección a mi pantalla inicial).

Given un cliente autenticado con un token válido
When llamo con APIRequestContext a un endpoint exclusivo del personal interno (p. ej., el de la agenda)
Then el backend deniega el acceso

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente
- **Resultado esperado:** La respuesta es 403 y el cuerpo no contiene datos de la agenda.


### TC-035 — deriva de: I11 – Usuario ya autenticado: Dado que tengo una sesión válida, cuando entro a la pantalla de login, entonces me lleva a la pantalla inicial de mi rol.

Given un cliente con una sesión válida
When navego directamente a la URL de login
Then me lleva a "Mis vehículos"

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente
- **Resultado esperado:** La URL final es la de "Mis vehículos" y el formulario de login no se muestra.


### TC-036 — deriva de: I11 – Usuario ya autenticado: Dado que tengo una sesión válida, cuando entro a la pantalla de login, entonces me lleva a la pantalla inicial de mi rol.

Given personal interno con una sesión válida
When navego directamente a la URL de login
Then me lleva a "Agenda del día"

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** personal_interno
- **Resultado esperado:** La URL final es la de "Agenda del día" y el formulario de login no se muestra.


### TC-037 — deriva de: I12 – Auditoría: Dado cualquier intento de login (exitoso, fallido, bloqueado o a una cuenta no habilitada), un cierre de sesión o una expiración, entonces se registra un evento de auditoría con usuario/correo, fecha y hora, resultado e IP. Nunca se registra la contraseña.

Given se ejecutan, anotando la hora de cada uno: un login exitoso, un login con contraseña errónea, un intento sobre una cuenta bloqueada, un intento sobre una cuenta inactiva, un logout y una expiración por inactividad
When consulto el registro de auditoría (desde la vista de auditoría o, si no hay UI, con el endpoint o la consulta de soporte de QA)
Then hay un evento por cada acción

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** admin (acceso al registro de auditoría)
- **Resultado esperado:** Cada evento tiene el usuario o correo, la fecha y hora (coincidente con la ejecución), el resultado correcto (éxito, fallo, bloqueado, no habilitada, logout, expirada) y la IP de origen. Ningún evento contiene la contraseña usada. Nota: si no hay UI de auditoría, la verificación requiere acceso de backend.


### TC-038 — deriva de: I13 – Comunicación segura: el envío de credenciales y tokens se hace solo por HTTPS.

Given Playwright registrando todas las peticiones de red
When inicio sesión, navego como usuario autenticado y cierro sesión
Then todas las peticiones con credenciales o tokens usan HTTPS

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** cliente
- **Resultado esperado:** Todas las peticiones de login, las autenticadas y la de logout tienen URL https://. Las cookies de sesión tienen el atributo Secure. Al acceder a la URL de login por http:// se redirige a https:// antes de enviar el formulario.


### TC-039 — deriva de: I14 – Documentación: los endpoints de login y logout, sus códigos de respuesta (200/401/403/423 o equivalentes) y sus mensajes quedan documentados en la API.

Given la documentación de la API publicada (p. ej., Swagger/OpenAPI)
When abro en el navegador la página de documentación y busco los endpoints de login y logout
Then ambos están documentados con sus códigos y mensajes

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado (o el rol con acceso a la documentación)
- **Resultado esperado:** Aparecen los endpoints de login y logout. Para cada uno se listan los códigos 200, 401, 403 y 423 (o los equivalentes definidos), con un mensaje o esquema de respuesta que coincide con lo que devuelve la API en los TCs anteriores.
