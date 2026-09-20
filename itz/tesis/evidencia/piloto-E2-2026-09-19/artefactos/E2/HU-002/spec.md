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

# Recuperación de contraseña por correo electrónico

Como usuario registrado que no recuerda su contraseña, quiero solicitar el restablecimiento de mi clave de acceso a través de un enlace enviado a mi correo electrónico, para recuperar el acceso a la plataforma de forma autónoma sin depender del administrador.

## Criterios de aceptación explícitos

- Dado que el usuario se encuentra en la pantalla de inicio de sesión, cuando selecciona la opción de recuperar contraseña e ingresa su correo electrónico registrado, entonces el sistema debe enviar un correo electrónico con las instrucciones/enlace para restablecer la contraseña sin requerir asistencia manual de un administrador.

## Criterios de aceptación inferidos

- Dado que el usuario solicita la recuperación e ingresa un correo electrónico (sea existente o no en el sistema), cuando presiona enviar, entonces el sistema muestra un mensaje genérico (ej. 'Si el correo está registrado, recibirás las instrucciones') para evitar la enumeración de usuarios/correos.
- Dado que el usuario recibe el correo de recuperación, cuando hace clic en el enlace dentro del tiempo límite de validez (ej. 15 minutos), entonces es redirigido a un formulario seguro para ingresar la nueva contraseña.
- Dado que el enlace de recuperación ya fue utilizado o ha expirado, cuando el usuario intenta ingresar a través de él, entonces el sistema le muestra un mensaje informando que el enlace no es válido y le ofrece la opción de solicitar uno nuevo.
- Dado que el usuario ingresa su nueva contraseña en el formulario de restablecimiento, cuando la contraseña cumple con las políticas de complejidad (longitud, caracteres) y coincide con la confirmación, entonces el sistema actualiza la credencial, invalida el token utilizado y permite el inicio de sesión con la nueva clave.

## Supuestos y vacíos identificados

- Se asume que la plataforma dispone de un servicio de envío de correos transaccionales (SMTP/Servidor de correo) operativo e integrado.
- Se asume que el token de recuperación generado es de un solo uso y expiración temporal corta.
- Se asume que las políticas de complejidad de contraseñas son las mismas definidas a nivel global en el sistema.

## Notas

Falta definir con precisión el tiempo exacto de vigencia del token/enlace de recuperación (ej. 15, 30 o 60 minutos). También se recomienda definir si se aplicará un límite de tasa de peticiones (rate limiting) por IP o correo para prevenir spam/abuso del servicio de correo transactional, e indicar si se debe enviar una notificación por correo confirmando que la contraseña ha sido cambiada con éxito.
