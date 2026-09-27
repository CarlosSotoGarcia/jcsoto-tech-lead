---
id: HU-002
clasificacion: hu
fuente_tipo: jira
fuente_ref: IAT-3
fase: especificada
estado: pendiente
fecha_descubrimiento: 2026-09-26
tiene_supuestos: true
prototipo_ref: null
depende_de: []
---

# Inicio y cierre de sesión con correo y contraseña, con redirección por rol

Como usuario del sistema (cliente o personal interno), quiero iniciar sesión con mi correo y contraseña y cerrarla cuando termine, para acceder solo a las funciones de mi rol y que nadie más use mi sesión. El objetivo de negocio es controlar el acceso según el rol (cliente → "Mis vehículos", personal → "Agenda del día"). También busca proteger las cuentas contra ataques de fuerza bruta y contra la enumeración de usuarios, y evitar que las sesiones abandonadas del personal queden abiertas en equipos compartidos.

## Criterios de aceptación explícitos

- E1 – Login correcto: Dado que tengo una cuenta activa, cuando ingreso un correo y una contraseña válidos, entonces accedo a la pantalla inicial de mi rol.
- E1a – Redirección de cliente (regla de negocio): Dado que soy un cliente con cuenta activa, cuando inicio sesión correctamente, entonces el sistema me lleva a "Mis vehículos".
- E1b – Redirección de personal (regla de negocio): Dado que soy personal interno con cuenta activa, cuando inicio sesión correctamente, entonces el sistema me lleva a "Agenda del día".
- E2 – Credenciales incorrectas: Dado que ingreso una contraseña errónea, cuando intento entrar, entonces veo un mensaje genérico que no revela si el correo existe.
- E3 – Bloqueo por intentos: Dado que fallé 5 veces seguidas, cuando intento de nuevo, entonces se muestra que la cuenta está bloqueada temporalmente y no se permite el acceso.
- E3a – Duración del bloqueo (regla de negocio): Dado que mi cuenta fue bloqueada por 5 intentos fallidos, cuando pasan 15 minutos, entonces puedo volver a intentar el inicio de sesión.
- E4 – Cierre de sesión: Dado que estoy autenticado, cuando selecciono "Cerrar sesión", entonces se invalida mi token y vuelvo a la pantalla de login.
- E5 – Expiración por inactividad (regla de negocio): Dado que soy personal interno autenticado, cuando pasan 30 minutos sin actividad, entonces mi sesión expira y debo volver a autenticarme.
- E6 – Cuentas no habilitadas (regla de negocio): Dado que mi cuenta está inactiva o pendiente de verificación, cuando ingreso credenciales correctas, entonces no se me permite el acceso.

## Criterios de aceptación inferidos

- I1 – Campos obligatorios: Dado que estoy en el login, cuando envío el formulario con el correo o la contraseña vacíos, entonces se muestra una validación junto al campo y no se envía la petición. La validación también se aplica en el backend, según la definición de terminado.
- I2 – Formato de correo: Dado que ingreso un correo con formato inválido, cuando intento entrar, entonces se indica que el formato es incorrecto y no cuenta como intento fallido de la cuenta.
- I3 – Correo inexistente: Dado que ingreso un correo que no está registrado, cuando intento entrar, entonces recibo el mismo mensaje genérico, con un tiempo de respuesta comparable al de una contraseña errónea.
- I4 – Reinicio del contador: Dado que tengo entre 1 y 4 intentos fallidos consecutivos, cuando inicio sesión correctamente, entonces el contador de intentos fallidos vuelve a cero.
- I5 – Bloqueo con credenciales correctas: Dado que mi cuenta está bloqueada, cuando ingreso las credenciales correctas antes de que pasen los 15 minutos, entonces sigo sin acceso y veo el mensaje de bloqueo temporal.
- I6 – Contraseña protegida: Dado que escribo mi contraseña, entonces el campo la oculta. Además, la contraseña nunca se guarda en texto plano ni aparece en logs o respuestas de la API.
- I7 – Token inválido tras logout: Dado que cerré sesión, cuando se reutiliza el token anterior (por ejemplo, con el botón "Atrás" del navegador o una llamada directa a la API), entonces el backend responde 401 y no se muestra contenido protegido.
- I8 – Expiración visible: Dado que mi sesión expiró por inactividad, cuando intento hacer cualquier acción, entonces me lleva al login con un mensaje de sesión expirada.
- I9 – Actividad renueva la sesión: Dado que soy personal interno, cuando hago una acción antes de cumplir 30 minutos de inactividad, entonces el contador de inactividad se reinicia.
- I10 – Permisos por rol: Dado que estoy autenticado con un rol, cuando intento acceder a una ruta o endpoint de otro rol, entonces el acceso se deniega (403 o redirección a mi pantalla inicial).
- I11 – Usuario ya autenticado: Dado que tengo una sesión válida, cuando entro a la pantalla de login, entonces me lleva a la pantalla inicial de mi rol.
- I12 – Auditoría: Dado cualquier intento de login (exitoso, fallido, bloqueado o a una cuenta no habilitada), un cierre de sesión o una expiración, entonces se registra un evento de auditoría con usuario/correo, fecha y hora, resultado e IP. Nunca se registra la contraseña.
- I13 – Comunicación segura: el envío de credenciales y tokens se hace solo por HTTPS.
- I14 – Documentación: los endpoints de login y logout, sus códigos de respuesta (200/401/403/423 o equivalentes) y sus mensajes quedan documentados en la API.

## Supuestos y vacíos identificados

- S1 – Expiración para clientes: la regla de 30 minutos solo menciona al personal interno. Falta definir si la sesión del cliente expira (por inactividad, con una duración absoluta del token o nunca) y en cuánto tiempo. Para cerrarlo hace falta una decisión del Product Owner o del área de seguridad.
- S2 – Mensaje de bloqueo frente a enumeración: decir "cuenta bloqueada" revela que el correo existe, lo que contradice el espíritu del escenario 2. Hay que definir si el mensaje de bloqueo también debe ser genérico o si se acepta ese riesgo. Lo decide seguridad o el Product Owner.
- S3 – Cuentas inactivas o pendientes: no se sabe qué mensaje se muestra. Puede ser genérico o específico (por ejemplo, "verifica tu correo" con opción de reenviar la verificación). Las dos opciones son válidas y cambian el alcance. Se necesita decisión del Product Owner y del equipo de UX.
- S4 – Alcance del conteo de intentos: se asume que se cuenta por cuenta (correo), no por IP ni por dispositivo. Tampoco está definido si un intento durante el bloqueo reinicia o alarga los 15 minutos. Se necesita confirmación.
- S5 – Qué cuenta como "actividad": no está claro si solo cuentan las peticiones al backend o también la interacción en la interfaz, ni si se avisa antes de expirar. Se necesita definición de UX o técnica.
- S6 – Alcance del cierre de sesión: se asume que solo se invalida la sesión del dispositivo actual. Falta definir si se permiten varias sesiones a la vez y si existe la opción "cerrar en todos los dispositivos".
- S7 – Subroles del personal: se asume que todo el personal interno (por ejemplo, administradores y mecánicos) llega a "Agenda del día". Si algún subrol, como administrador, tiene otra pantalla inicial, hay que especificarlo.
- S8 – Fuera de alcance: se asume que la recuperación y el cambio de contraseña, el "recordarme", el registro, la verificación de correo, el MFA y el desbloqueo manual por un administrador son historias aparte.
- S9 – Invalidación del token: se asume que el backend puede revocar tokens (por ejemplo, con una lista de revocación o sesiones guardadas en el servidor). Si se usan JWT sin estado, hace falta definir la estrategia técnica.

## Notas

Se clasifica como HU porque describe un comportamiento de usuario verificable, con escenarios claros y reglas de negocio que se pueden probar. Las reglas de negocio no tenían escenario Given/When/Then propio (expiración a los 30 minutos, redirección por rol, cuentas inactivas o pendientes y duración del bloqueo). Se estructuraron como criterios explícitos porque vienen en la fuente. El título incluye el cierre de sesión aunque la narrativa solo menciona el inicio; el escenario 4 lo deja dentro del alcance. Antes de pasar a desarrollo conviene cerrar primero S1, S2 y S3, porque afectan directamente los mensajes, la seguridad y el alcance de las pruebas de QA. La definición de terminado pide auditoría y documentación de API, y eso se reflejó en I12 e I14.
