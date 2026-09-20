---
id: HU-003
clasificacion: hu
fuente_tipo: jira
fuente_ref: ITZINV-14
fase: especificada
estado: pendiente
fecha_descubrimiento: 2026-09-19
tiene_supuestos: true
prototipo_ref: null
depende_de: []
---

# Cerrar sesión manualmente y por expiración por inactividad

Como usuario quiero que mi sesión se cierre cuando yo elija salir o tras un periodo de inactividad, para evitar que otras personas accedan sin autorización a mi cuenta en equipos compartidos.

## Criterios de aceptación explícitos

- Dado un usuario con sesión activa, cuando selecciona la opción de salir/cerrar sesión, entonces la sesión se cierra y ya no puede acceder a recursos protegidos sin autenticarse de nuevo.
- Dado un usuario con sesión activa, cuando transcurre el periodo de inactividad definido sin actividad, entonces la sesión expira automáticamente y se exige autenticación nuevamente para continuar.

## Criterios de aceptación inferidos

- Al cerrar sesión (manual o por expiración) el token/cookie de sesión se invalida en el servidor, no solo en el cliente.
- Tras cerrar sesión, usar el botón 'atrás' del navegador o reutilizar el token anterior no da acceso a información protegida.
- Tras cerrar sesión o expirar, el usuario es redirigido a la pantalla de inicio de sesión.
- Cualquier actividad del usuario (interacción o petición a la API) reinicia el contador de inactividad.
- Si la sesión expira y el usuario intenta una acción o una petición, recibe un mensaje claro de sesión expirada y se le pide volver a iniciar sesión.
- Con varias pestañas o ventanas abiertas, el cierre o expiración de sesión se refleja en todas ellas.
- Se limpian los datos sensibles almacenados localmente (storage, caché) al cerrar sesión.
- El cierre de sesión y la expiración quedan registrados en logs de auditoría.
- El tiempo de inactividad es configurable y no depende solo del cliente; el servidor valida la expiración.

## Supuestos y vacíos identificados

- El valor del periodo de inactividad no está definido (p. ej. 15 o 30 min). Falta confirmación de negocio/seguridad para cerrarlo.
- No se indica si habrá aviso previo a la expiración con opción de extender la sesión. Requiere decisión de producto; no se incluye como criterio.
- 'Salir' se interpreta como la acción explícita de cerrar sesión; no está claro si cerrar la pestaña o el navegador también debe terminar la sesión. Requiere definición.
- No se especifica si aplica a todos los roles o canales (web, móvil, API) ni si el periodo varía por perfil.
- No se define qué ocurre con trabajo no guardado (formularios en curso) al expirar la sesión.
- No se indica si existe opción 'recordarme' que contradiga la expiración por inactividad.

## Notas

Para cerrar el alcance se necesita: tiempo de inactividad, política de aviso previo/extensión, comportamiento al cerrar pestaña/navegador, canales cubiertos y manejo de datos no guardados.
