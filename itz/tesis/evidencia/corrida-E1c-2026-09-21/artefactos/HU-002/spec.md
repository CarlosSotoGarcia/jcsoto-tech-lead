---
id: HU-002
clasificacion: hu
fuente_tipo: jira
fuente_ref: ITZINV-13
fase: especificada
estado: pendiente
fecha_descubrimiento: 2026-09-21
tiene_supuestos: true
prototipo_ref: null
depende_de: []
---

# Recuperar contraseña olvidada por correo electrónico

Como usuario registrado que olvidó su contraseña, quiero solicitar un restablecimiento mediante un enlace/código enviado a mi correo, para recuperar el acceso a mi cuenta de forma autónoma sin depender del administrador. Problema de negocio: reducir la carga de soporte/administración y el tiempo de indisponibilidad del usuario, manteniendo la seguridad de la cuenta.

## Criterios de aceptación explícitos

- Dado que soy un usuario que olvidó su contraseña, cuando solicito recuperarla indicando mi correo, entonces el sistema me envía un mensaje a ese correo con el medio para restablecerla.
- Dado que recibí el correo de recuperación, cuando sigo el procedimiento indicado y defino una nueva contraseña, entonces recupero el acceso a mi cuenta sin intervención del administrador.

## Criterios de aceptación inferidos

- Dado un correo no registrado o cuenta inexistente, cuando solicito recuperación, entonces el sistema muestra el mismo mensaje genérico ('si el correo existe, recibirás instrucciones') para no revelar qué correos están registrados.
- Dado un correo con formato inválido o vacío, cuando envío la solicitud, entonces se muestra un error de validación y no se envía nada.
- Dado que se generó un enlace/token de restablecimiento, cuando pasa su tiempo de vigencia, entonces deja de ser válido y se informa al usuario que debe solicitar uno nuevo.
- Dado un token ya utilizado, cuando intento usarlo de nuevo, entonces el sistema lo rechaza (uso único).
- Dado que solicito un nuevo enlace, cuando ya existía uno vigente, entonces el anterior queda invalidado.
- Dada la nueva contraseña, cuando no cumple la política de contraseñas vigente o la confirmación no coincide, entonces se rechaza con un mensaje claro y el token sigue siendo válido hasta su expiración.
- Dado que se restableció la contraseña con éxito, entonces se invalidan las sesiones activas previas y se notifica por correo el cambio realizado.
- Dadas múltiples solicitudes repetidas, cuando se supera un límite razonable por correo/IP, entonces se aplica limitación de frecuencia (rate limiting) para evitar abuso y spam.
- Dado que el token se almacena, entonces se guarda de forma segura (hash) y es no predecible; la comunicación se realiza sobre HTTPS.
- Dado un fallo en el envío del correo, entonces el error se registra y el usuario no recibe información que comprometa la seguridad.
- Dada una cuenta bloqueada/inactiva/deshabilitada, cuando se solicita recuperación, entonces no se permite el restablecimiento (comportamiento externo idéntico al genérico).
- Los eventos de solicitud y restablecimiento quedan registrados en auditoría (sin incluir contraseñas ni tokens).

## Supuestos y vacíos identificados

- No se especifica el mecanismo: enlace con token o código numérico (OTP). Se asume enlace, pero requiere confirmación.
- No se define la vigencia del token (se sugiere 15–60 min); falta que negocio la fije.
- No se define la política de contraseñas (longitud, complejidad, historial/no reutilizar las últimas N); se asume la política existente del sistema.
- No se indica si aplica a cuentas con SSO/login externo o MFA; se asume que solo aplica a cuentas con contraseña local y que MFA, si existe, se mantiene tras el restablecimiento.
- No se especifica si el usuario se identifica por correo o por nombre de usuario; se asume correo.
- No se define si se requiere verificación adicional (pregunta de seguridad/MFA) para cuentas de alto privilegio.
- Se desconoce el proveedor/plantilla de correo, idioma y canal de envío; se asume que existe infraestructura de correo transaccional.
- No se define si se hace login automático tras el restablecimiento; se asume que no, redirigiendo al inicio de sesión.

## Notas

Para cerrar los supuestos hace falta: decisión de producto sobre enlace vs. OTP, vigencia del token, política de contraseñas, alcance respecto a SSO/MFA y umbrales de rate limiting. Los criterios de seguridad inferidos (respuesta genérica, uso único, expiración) son estándar y se consideran parte del alcance mínimo.
