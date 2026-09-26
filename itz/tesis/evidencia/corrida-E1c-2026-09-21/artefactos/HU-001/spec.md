---
id: HU-001
clasificacion: hu
fuente_tipo: jira
fuente_ref: ITZINV-12
fase: especificada
estado: pendiente
fecha_descubrimiento: 2026-09-21
tiene_supuestos: true
prototipo_ref: null
depende_de: []
---

# Iniciar sesión con correo y contraseña

Como usuario del sistema quiero iniciar sesión con mi correo y contraseña para acceder únicamente a la información que me corresponde. Intención de negocio: autenticar la identidad del usuario y, con ella, establecer una sesión que limite el acceso a los datos y funciones propios de su cuenta/rol (autenticación + base para la autorización).

## Criterios de aceptación explícitos

- Dado un usuario registrado con credenciales válidas (correo y contraseña), cuando envía el formulario de inicio de sesión, entonces el sistema lo autentica y le da acceso al sistema.
- Dado un usuario autenticado, cuando navega o consulta información, entonces solo puede ver/acceder a la información que le corresponde (la asociada a su cuenta/permisos), y no la de otros usuarios.

## Criterios de aceptación inferidos

- Dado un correo o contraseña incorrectos, cuando intenta iniciar sesión, entonces se rechaza el acceso con un mensaje genérico que no revela cuál de los dos datos falló (evita enumeración de usuarios).
- Dado un correo no registrado, cuando intenta iniciar sesión, entonces recibe el mismo mensaje que con contraseña incorrecta.
- Dado que el correo o la contraseña están vacíos, o el correo tiene formato inválido, cuando intenta enviar, entonces se muestra una validación de campo y no se procesa la autenticación.
- Dado que un usuario intenta acceder directamente a un recurso de otro usuario (por URL o API), cuando la solicitud llega, entonces el servidor la rechaza (403/404) y la autorización se valida en backend, no solo ocultando elementos en la interfaz.
- Dado un usuario no autenticado o con sesión expirada, cuando intenta acceder a una página o endpoint protegido, entonces es redirigido al inicio de sesión / recibe 401.
- Las contraseñas nunca se almacenan ni se transmiten en texto plano (hash con sal en almacenamiento, tráfico por HTTPS) y no aparecen en logs; el campo de contraseña se enmascara.
- Dado un inicio de sesión exitoso, cuando se crea la sesión/token, entonces este tiene vigencia limitada y se invalida al cerrar sesión.
- Dados varios intentos fallidos consecutivos, cuando se supera un umbral, entonces se aplica una protección contra fuerza bruta (bloqueo temporal, retardo o captcha).
- La comparación del correo no distingue mayúsculas/minúsculas y se ignoran espacios al inicio o final.
- Dado que el servicio de autenticación no está disponible, cuando el usuario intenta iniciar sesión, entonces ve un mensaje de error amigable sin perder lo escrito en el correo.
- Se registran los intentos de inicio de sesión (exitosos y fallidos) para auditoría.

## Supuestos y vacíos identificados

- No se define el modelo de autorización (por rol, por propietario de los datos, por organización/tenant). 'Información que me corresponde' admite varias interpretaciones; para cerrarlo hace falta la matriz de roles/permisos y qué datos ve cada uno.
- Se asume que el registro de usuarios ya existe o se gestiona en otra HU; el alcance no incluye registro, activación de cuenta ni verificación de correo.
- Fuera de alcance salvo confirmación: recuperación/restablecimiento de contraseña, 'recordarme', cierre de sesión como funcionalidad explícita, MFA/2FA e inicio de sesión social/SSO.
- Se desconocen las políticas de bloqueo (número de intentos, duración), la duración de la sesión y las reglas de complejidad de contraseña; los criterios inferidos las mencionan solo de forma genérica y requieren valores definidos por negocio/seguridad.
- No se especifica el comportamiento para cuentas desactivadas o bloqueadas (mensaje y si se distingue del error de credenciales).
- Se desconoce la plataforma (web, móvil, ambas) y a dónde se redirige tras un login exitoso.

## Notas

La HU mezcla dos preocupaciones: autenticación (login) y autorización/aislamiento de datos ('únicamente la información que me corresponde'). Se recomienda confirmar si la segunda se cubre aquí o en una HU aparte de control de acceso; si es aparte, esta HU quedaría acotada a autenticación y creación de sesión. Ausencia de criterios de aceptación en la fuente: los explícitos se derivaron del texto de la narrativa.
