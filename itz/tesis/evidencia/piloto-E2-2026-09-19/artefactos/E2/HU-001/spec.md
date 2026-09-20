---
id: HU-001
clasificacion: hu
fuente_tipo: jira
fuente_ref: ITZINV-12
fase: especificada
estado: pendiente
fecha_descubrimiento: 2026-09-19
tiene_supuestos: true
prototipo_ref: null
depende_de: []
---

# Iniciar sesión con correo electrónico y contraseña

Como usuario del sistema quiero autenticarme mediante mi correo electrónico y contraseña para acceder de manera segura a la plataforma y visualizar únicamente la información correspondiente a mi perfil.

## Criterios de aceptación explícitos

- Dado que un usuario registrado se encuentra en la pantalla de inicio de sesión, Cuando ingresa su correo electrónico y contraseña válidos y hace clic en "Iniciar sesión", Entonces el sistema autentica exitosamente al usuario y lo redirige a la plataforma, garantizando acceso únicamente a la información asociada a su cuenta y rol.

## Criterios de aceptación inferidos

- Dado que el usuario deja vacíos los campos de correo o contraseña, Cuando intenta iniciar sesión, Entonces el sistema impide el envío del formulario y muestra mensajes de validación indicando que los campos son obligatorios.
- Dado que el usuario ingresa un texto que no cumple con el formato estándar de correo electrónico, Cuando intenta iniciar sesión, Entonces el sistema muestra una validación de formato de correo inválido.
- Dado que el usuario ingresa credenciales incorrectas (correo no registrado o contraseña errónea), Cuando intenta iniciar sesión, Entonces el sistema muestra un mensaje de error genérico ("Correo o contraseña incorrectos") para evitar la divulgación de usuarios existentes.
- Dado que el usuario escribe su contraseña, Cuando interactúa con el campo de texto, Entonces los caracteres se muestran enmascarados/ocultos por defecto.
- Dado que una cuenta de usuario se encuentra en estado inactivo o suspendido, Cuando el usuario intenta iniciar sesión con credenciales válidas, Entonces el sistema deniega el acceso y muestra un mensaje indicando que la cuenta no está activa.

## Supuestos y vacíos identificados

- Se asume que la autenticación manejará sesiones seguras mediante tokens (ej. JWT o cookies HTTP-Only con flag de seguridad).
- Se asume que la creación y registro previo de usuarios, así como la recuperación de contraseña ("Olvidé mi contraseña"), corresponden a historias de usuario independientes fuera de este alcance.

## Notas

Se recomienda aclarar con el Product Owner / Equipo de Seguridad los siguientes puntos antes del desarrollo: 1) ¿Se requiere bloqueo automático de cuenta tras N intentos fallidos consecutivos? 2) ¿Cuál es el tiempo de expiración de sesión por inactividad? 3) ¿Se incluirá opción de visualización/ocultamiento de contraseña (ícono de ojo)?
