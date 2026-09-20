---
id: HU-002
clasificacion: hu
fuente_tipo: jira
fuente_ref: ITZINV-13
fase: especificada
estado: pendiente
fecha_descubrimiento: 2026-09-19
tiene_supuestos: true
prototipo_ref: null
depende_de: []
---

# Recuperar contraseña olvidada por correo electrónico

Como usuario registrado que olvidó su contraseña, quiero solicitar y completar un restablecimiento mediante un enlace/código enviado a mi correo, para recuperar el acceso a mi cuenta de forma autónoma sin depender del administrador.

## Criterios de aceptación explícitos

- Given un usuario que olvidó su contraseña, When solicita la recuperación indicando su correo, Then el sistema le envía un mensaje a ese correo con el mecanismo para restablecerla.
- Given un usuario que recibió el mensaje de recuperación, When completa el procedimiento y define una nueva contraseña, Then recupera el acceso a su cuenta sin intervención del administrador.

## Criterios de aceptación inferidos

- Given un correo no registrado o cuenta inactiva, When se solicita la recuperación, Then el sistema muestra el mismo mensaje genérico ('si el correo existe, recibirás instrucciones') para no revelar qué cuentas existen, y no envía correo (o no permite el restablecimiento).
- Given un formato de correo inválido o campo vacío, When se envía la solicitud, Then se muestra un error de validación sin procesar la solicitud.
- Given un enlace/token de recuperación, When se usa, Then es de un solo uso y expira tras un tiempo limitado; un token expirado, ya usado o inválido muestra un error claro y permite solicitar uno nuevo.
- Given que se genera un nuevo token, When existía uno anterior pendiente, Then el anterior queda invalidado.
- Given la pantalla de nueva contraseña, When el usuario la ingresa, Then se valida contra la política de contraseñas vigente y se exige confirmación coincidente; si no cumple, se muestran los motivos.
- Given un restablecimiento exitoso, When se guarda la nueva contraseña, Then se invalidan las sesiones activas previas y se notifica por correo al titular del cambio.
- Given solicitudes repetidas de recuperación, When se supera un umbral por cuenta/IP/tiempo, Then se limita la frecuencia (rate limiting) para prevenir abuso y spam de correos.
- Given el token y la contraseña, When se almacenan o registran, Then el token se guarda con hash, la contraseña con hash seguro, y ninguno aparece en logs; la comunicación es sobre HTTPS.
- Given un fallo en el envío del correo (servicio caído), When ocurre, Then el error se registra y el usuario puede reintentar sin que se exponga información sensible.
- Given una cuenta bloqueada por intentos fallidos, When se restablece la contraseña con éxito, Then se aplica la política definida para el desbloqueo (ver supuestos).
- Los eventos de solicitud y restablecimiento quedan registrados en auditoría (fecha, cuenta, IP) sin datos sensibles.
- La pantalla de login incluye un acceso visible a '¿Olvidaste tu contraseña?'.

## Supuestos y vacíos identificados

- Se asume que el usuario ya tiene cuenta con un correo registrado y verificado; no cubre usuarios sin correo asociado. Para cerrar: confirmar si existen cuentas sin correo o con correo compartido.
- El mecanismo no está definido: enlace con token vs. código numérico (OTP). Para cerrar: decidir con negocio/seguridad.
- Vigencia del token no especificada (típico 15–60 min). Para cerrar: definir con seguridad.
- Política de contraseñas (longitud, complejidad, historial/no reutilizar) no especificada. Para cerrar: confirmar la política corporativa vigente.
- No se define si las cuentas bloqueadas o deshabilitadas por el administrador pueden recuperar acceso por este flujo (podría eludir un bloqueo intencional). Para cerrar: definir la regla con negocio/seguridad.
- No se especifica si aplica MFA/segundo factor adicional en el restablecimiento. Para cerrar: confirmar requisitos de seguridad.
- Alcance de plataformas (web, móvil, ambas) y plantilla/idioma del correo no definidos. Para cerrar: confirmar canales e idiomas.
- No se define el límite exacto de rate limiting ni si el usuario es redirigido al login o autenticado automáticamente tras el cambio. Para cerrar: definir con UX/seguridad.

## Notas

La HU es breve pero clara en intención: autoservicio de recuperación de acceso, reduciendo carga del administrador. Los criterios explícitos son solo el flujo feliz; la mayor parte del alcance verificable (seguridad, expiración, anti-enumeración) es inferido y debe validarse con el equipo de seguridad antes de desarrollo. Los supuestos sobre cuentas bloqueadas y mecanismo (enlace vs. OTP) son los que más impactan el alcance.
