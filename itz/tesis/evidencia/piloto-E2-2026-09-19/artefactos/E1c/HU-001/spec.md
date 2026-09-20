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

# Iniciar sesión con correo y contraseña

Como usuario del sistema quiero iniciar sesión con mi correo y contraseña para acceder únicamente a la información que me corresponde. Problema de negocio: autenticar la identidad del usuario y garantizar que, tras el ingreso, solo vea y opere sobre los datos autorizados para su cuenta (aislamiento de información y confidencialidad).

## Criterios de aceptación explícitos

- Dado un usuario registrado, cuando ingresa su correo y contraseña correctos, entonces el sistema inicia su sesión y le da acceso al sistema.
- Dado un usuario autenticado, cuando consulta o navega por la información, entonces solo puede acceder a la información que le corresponde según su cuenta.

## Criterios de aceptación inferidos

- Dado un correo o contraseña incorrectos, cuando intenta iniciar sesión, entonces se rechaza el acceso y se muestra un mensaje genérico que no revela cuál de los dos datos falló.
- Dado un correo que no está registrado, cuando intenta iniciar sesión, entonces se recibe el mismo mensaje genérico que con contraseña incorrecta.
- Dado que el correo o la contraseña están vacíos, cuando se intenta enviar el formulario, entonces se indica que los campos son obligatorios y no se realiza la autenticación.
- Dado un correo con formato inválido, cuando se intenta enviar, entonces se muestra un error de validación de formato.
- Dado un usuario no autenticado, cuando intenta acceder directamente a una URL o recurso protegido, entonces es redirigido al inicio de sesión y no ve información.
- Dado un usuario autenticado, cuando intenta acceder a un recurso o dato de otro usuario (por URL o API), entonces el acceso se deniega en el servidor (no solo se oculta en la interfaz).
- La contraseña se transmite cifrada (HTTPS), se almacena con hash seguro y nunca se muestra en texto plano ni se registra en logs; el campo la enmascara.
- Dado un inicio de sesión exitoso, cuando expira la sesión por inactividad o el usuario cierra sesión, entonces se invalida la sesión y se exige autenticarse de nuevo.
- Dado que el correo se ingresa con distinta capitalización o espacios al inicio/fin, entonces se normaliza antes de validar.

## Supuestos y vacíos identificados

- No se define el modelo de permisos: 'información que me corresponde' puede significar datos propios del usuario, de su organización/tenant o según su rol. Se requiere definir la regla de autorización exacta.
- No se especifica la política ante intentos fallidos (bloqueo temporal, CAPTCHA, límite de intentos). Se requiere decidir umbral y duración; no se inventa.
- No se indica si existen recuperación de contraseña, registro de usuarios, cierre de sesión, 'recordarme' o MFA; se asumen fuera del alcance de esta HU.
- No se define el tratamiento de usuarios inactivos, bloqueados o con correo sin verificar; falta confirmar el comportamiento y mensaje.
- No se especifica la duración de la sesión ni el mecanismo (cookie/token); se asume que se define técnicamente aparte.
- No se indica la pantalla o destino tras el inicio de sesión exitoso (p. ej., página de inicio o la URL solicitada originalmente).

## Notas

La fuente es muy breve: solo hay dos criterios explícitos implícitos en la narrativa. La parte de 'acceder únicamente a la información que me corresponde' es autorización y puede requerir su propia HU o criterios detallados una vez definido el modelo de permisos.
