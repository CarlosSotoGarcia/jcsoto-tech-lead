---
id: HU-003
clasificacion: hu
fuente_tipo: jira
fuente_ref: ITZINV-14
fase: especificada
estado: pendiente
fecha_descubrimiento: 2026-09-21
tiene_supuestos: true
prototipo_ref: null
depende_de: []
---

# Cerrar sesión manualmente y expirar sesión por inactividad

Como usuario quiero poder cerrar mi sesión y que esta se cierre automáticamente tras un periodo de inactividad, para evitar accesos no autorizados cuando uso equipos compartidos. Problema de negocio: reducir el riesgo de uso indebido de sesiones abandonadas y cumplir buenas prácticas de seguridad.

## Criterios de aceptación explícitos

- Dado un usuario autenticado, cuando elige cerrar sesión (salir), entonces su sesión termina y ya no puede acceder a funciones protegidas.
- Dado un usuario autenticado sin actividad, cuando transcurre el periodo de inactividad definido, entonces la sesión se cierra automáticamente.
- Dado un equipo compartido, cuando la sesión se cerró (manual o por inactividad), entonces el siguiente usuario no puede ver información ni ejecutar acciones de la sesión anterior.

## Criterios de aceptación inferidos

- Al cerrar sesión, el token/sesión se invalida en el servidor (no solo en el cliente); reutilizarlo devuelve 401/no autorizado.
- Tras el cierre, el usuario es redirigido al inicio de sesión y el botón 'atrás' del navegador no muestra contenido protegido.
- Se eliminan los datos de sesión en el cliente (cookies, localStorage/sessionStorage, caché con datos sensibles).
- La actividad del usuario (clics, teclado, navegación, peticiones iniciadas por el usuario) reinicia el temporizador de inactividad.
- La expiración se valida también en el servidor: una petición con sesión vencida es rechazada aunque el cliente no haya cerrado la sesión.
- Si hay varias pestañas o ventanas abiertas, el cierre de sesión (manual o por expiración) se refleja en todas.
- Al expirar, se informa al usuario con un mensaje claro de que la sesión venció por inactividad y se le lleva al login.
- Cerrar sesión debe estar disponible desde cualquier pantalla autenticada y ser idempotente (cerrar una sesión ya cerrada no genera error).
- El cierre y la expiración de sesión quedan registrados en bitácora/auditoría.

## Supuestos y vacíos identificados

- El tiempo de inactividad no está definido en la fuente (p. ej. 5, 15 o 30 min); se requiere que negocio/seguridad lo fije y si es configurable.
- No se especifica si se muestra un aviso previo con opción de extender la sesión; se asume deseable pero se debe confirmar, pues cambia el alcance.
- No se aclara qué significa 'al salir': solo el botón cerrar sesión, o también cerrar pestaña/navegador; se debe confirmar si cerrar el navegador debe terminar la sesión.
- No se indica la plataforma (web, móvil, ambas); se asume web.
- No se define el tratamiento de trabajo no guardado (formularios en edición) al expirar la sesión.
- No se aclara si aplica a todos los roles o si algunos (p. ej. administradores) tienen tiempos distintos.

## Notas

Para cerrar los supuestos hace falta: valor y configurabilidad del tiempo de inactividad, decisión sobre aviso previo/extensión de sesión, definición de 'salir' (cierre de pestaña/navegador), plataformas cubiertas y política para datos no guardados.
