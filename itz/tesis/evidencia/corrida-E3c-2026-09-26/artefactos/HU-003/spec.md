---
id: HU-003
clasificacion: hu
fuente_tipo: jira
fuente_ref: IAT-4
fase: especificada
estado: pendiente
fecha_descubrimiento: 2026-09-26
tiene_supuestos: true
prototipo_ref: null
depende_de: []
---

# Recuperación de contraseña mediante enlace enviado por correo

Como usuario que olvidó su contraseña, quiero solicitar un enlace de restablecimiento a mi correo registrado y con él definir una contraseña nueva, para recuperar el acceso por mi cuenta sin tener que llamar al taller. Problema de negocio: bajar la carga de soporte del taller por bloqueos de acceso sin descuidar la seguridad de la cuenta (el enlace dura poco y sirve una sola vez, no se revela qué correos existen y se cierran las sesiones abiertas).

## Criterios de aceptación explícitos

- Escenario 1 – Solicitud: Dado que ingreso mi correo en la pantalla 'Olvidé mi contraseña', cuando envío la solicitud, entonces recibo un correo con un enlace de restablecimiento.
- Escenario 2 – Restablecimiento: Dado que abro un enlace vigente, cuando capturo una nueva contraseña válida, entonces se actualiza y puedo iniciar sesión con ella.
- Escenario 3 – Enlace vencido: Dado que el enlace se generó hace más de 1 hora, cuando lo abro, entonces el sistema indica que expiró y me permite solicitar uno nuevo.
- Regla – Un solo uso: Dado que ya usé un enlace para cambiar mi contraseña, cuando intento usarlo otra vez, entonces se rechaza como no válido.
- Regla – Vigencia: Dado un enlace generado, cuando pasa 1 hora desde que se generó, entonces deja de ser válido.
- Regla – Respuesta uniforme: Dado que envío una solicitud con un correo registrado o no registrado, cuando el sistema responde, entonces el mensaje en pantalla y la respuesta de la API son iguales en los dos casos (no se revela si el correo existe).
- Regla – Cierre de sesiones: Dado que tengo sesiones abiertas en uno o más dispositivos, cuando restablezco la contraseña, entonces todas esas sesiones se invalidan y tengo que volver a iniciar sesión.

## Criterios de aceptación inferidos

- Correo no registrado: Dado un correo que no existe, cuando envío la solicitud, entonces no se manda ningún correo y se muestra el mismo mensaje genérico de confirmación.
- Tiempo de respuesta uniforme: la API tarda un tiempo parecido exista o no el correo, para que no se pueda saber por el tiempo si está registrado (el envío del correo se hace de forma asíncrona o con un tiempo equivalente).
- Formato de correo: Dado que escribo un correo con formato inválido o dejo el campo vacío, cuando envío, entonces se muestra un error de validación en frontend y backend y no se procesa la solicitud.
- Contraseña inválida: Dado un enlace vigente, cuando capturo una contraseña que no cumple la política vigente, entonces se rechaza con un mensaje que dice qué regla no se cumple, y el enlace sigue sirviendo hasta que se use o venza.
- Confirmación de contraseña: se pide escribir la nueva contraseña dos veces y, si no coinciden, no se guarda.
- Enlace inválido o alterado: Dado un enlace con un token inexistente, mal formado o manipulado, cuando lo abro, entonces se muestra un mensaje genérico de enlace no válido y la opción de pedir uno nuevo.
- Enlace ya usado: al abrir un enlace consumido se muestra un mensaje (no válido/ya utilizado) con la opción de pedir uno nuevo.
- Vigencia también en backend: la expiración y el uso único se validan en el servidor al enviar la nueva contraseña, no solo al abrir el enlace (caso de un formulario que se abrió a los 59 minutos y se envió a los 61).
- Seguridad del token: el token es aleatorio, criptográficamente seguro y difícil de adivinar; se guarda como hash, no en texto plano.
- Almacenamiento de la contraseña: la nueva contraseña se guarda con un hash seguro y nunca aparece en logs ni en la auditoría.
- Contraseña anterior: después del cambio, la contraseña anterior ya no permite iniciar sesión.
- Protección contra abuso: las solicitudes se limitan por correo y por IP para evitar que se inunde a alguien de correos o se enumeren cuentas, y la respuesta visible sigue siendo la misma.
- Auditoría (según la DoD): se registran la solicitud de restablecimiento, el cambio de contraseña hecho y el cierre de sesiones, con fecha y hora, usuario (si existe) e IP, sin guardar datos sensibles.
- Transporte seguro: el enlace usa HTTPS y el token no se filtra a terceros (por ejemplo, con la cabecera Referrer-Policy en la página de restablecimiento).
- Documentación de API: los endpoints de solicitud y de restablecimiento quedan documentados con sus respuestas y códigos de error (según la DoD).

## Supuestos y vacíos identificados

- Varias solicitudes seguidas: no se define si pedir un enlace nuevo invalida los anteriores que siguen vigentes. Supuesto recomendado: sí, solo vale el más reciente. Lo tiene que confirmar el PO.
- Política de contraseñas: la HU dice 'contraseña válida' pero no da reglas (largo mínimo, complejidad, prohibir reutilizar las anteriores). Hay que remitir a la política vigente del sistema o que el PO la defina.
- Sesión después del cambio: no se sabe si el usuario entra automáticamente al terminar o si lo llevamos al login. El Escenario 2 ('puedo iniciar sesión') apunta a redirigir al login. Lo tiene que confirmar el PO o UX.
- Cierre de sesiones: se asume que incluye tokens de actualización / 'recordarme' y sesiones en apps móviles, si las hay. Hay que confirmarlo con arquitectura.
- Cuentas inactivas, bloqueadas o sin correo verificado: no se dice si pueden recuperar la contraseña. Afecta al alcance; lo tiene que definir el PO.
- Usuarios sin correo registrado (por ejemplo, clientes del taller dados de alta solo con teléfono): quedan fuera de esta HU; la recuperación por otro canal sería una HU aparte.
- Contenido y remitente del correo, idioma y plantilla: no se especifican. Hace falta el texto aprobado y el remitente.
- Notificación de seguridad: no se pide avisar al usuario por correo de que su contraseña cambió; es una buena práctica, pero amplía el alcance. Lo tiene que confirmar el PO.
- Límites de solicitudes: no se definen umbrales concretos (por ejemplo, 3 solicitudes por correo cada 15 minutos). Los tienen que definir seguridad o el PO.
- 'Permisos por rol' de la DoD: la función se usa sin iniciar sesión, así que no aplica un control por rol. Hay que confirmar si la recuperación aplica a todos los roles (clientes, empleados, administradores) o si alguno (por ejemplo, administradores) tiene otro flujo.

## Notas

Es una HU completa y verificable: tres escenarios explícitos más tres reglas de negocio que se pueden probar directamente. Faltan casos que se prueban explícitamente: enlace ya usado, token inválido, contraseña que no cumple la política y la respuesta uniforme para correos que no existen. Los agregué como inferidos. Lo que más riesgo tiene de estar abierto: (1) la política de contraseñas, (2) si un enlace nuevo invalida los anteriores y (3) qué pasa con cuentas bloqueadas o inactivas. Conviene cerrarlos con el PO antes del refinamiento. Varios puntos de la DoD (permisos por rol, auditoría) hay que adaptarlos a un flujo que se usa sin iniciar sesión.
