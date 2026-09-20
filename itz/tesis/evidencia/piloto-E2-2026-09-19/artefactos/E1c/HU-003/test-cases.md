---
hu_id: HU-003
fase: tcs_generados
total_tcs: 19
fecha_generacion: 2026-09-19
---

### TC-001 — deriva de: Dado un usuario con sesión activa, cuando selecciona la opción de salir/cerrar sesión, entonces la sesión se cierra y ya no puede acceder a recursos protegidos sin autenticarse de nuevo.

Given un usuario autenticado en la aplicación. When hace clic en la opción 'Cerrar sesión' del menú de usuario y luego navega directamente por URL a una página protegida (p. ej. /dashboard). Then se le pide autenticarse.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Tras el clic, la sesión se cierra; al abrir /dashboard la aplicación no muestra contenido protegido y muestra la pantalla de inicio de sesión.


### TC-002 — deriva de: Dado un usuario con sesión activa, cuando transcurre el periodo de inactividad definido sin actividad, entonces la sesión expira automáticamente y se exige autenticación nuevamente para continuar.

Given un usuario autenticado y un periodo de inactividad configurado (p. ej. 1 minuto en entorno de prueba). When no realiza ninguna interacción ni petición durante ese periodo y después intenta navegar a otra sección protegida. Then se exige autenticación.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La sesión expira automáticamente; al intentar continuar se muestra la pantalla de inicio de sesión y no se accede al contenido protegido hasta autenticarse de nuevo.


### TC-003 — deriva de: Al cerrar sesión (manual o por expiración) el token/cookie de sesión se invalida en el servidor, no solo en el cliente.

Given un usuario autenticado del que se capturó la cookie/token de sesión. When cierra sesión manualmente y luego se reenvía una petición a un endpoint protegido con la cookie/token capturado (p. ej. vía request de Playwright con la cookie restaurada en un contexto nuevo). Then el servidor lo rechaza.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El servidor responde 401 (o redirige a login) al usar el token/cookie anterior; no se devuelve información protegida.


### TC-004 — deriva de: Al cerrar sesión (manual o por expiración) el token/cookie de sesión se invalida en el servidor, no solo en el cliente.

Given un usuario autenticado con token/cookie capturado. When transcurre el periodo de inactividad y la sesión expira, y se reutiliza el token capturado en un contexto de navegador nuevo hacia un recurso protegido. Then el servidor lo rechaza.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El servidor rechaza el token expirado con 401 o redirección a login; no se devuelve contenido protegido.


### TC-005 — deriva de: Tras cerrar sesión, usar el botón 'atrás' del navegador o reutilizar el token anterior no da acceso a información protegida.

Given un usuario que visitó una página protegida y cerró sesión. When pulsa el botón 'atrás' del navegador. Then no ve la información protegida.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La página no muestra datos protegidos (ni desde caché/bfcache); se redirige a la pantalla de inicio de sesión o se muestra un estado no autenticado.


### TC-006 — deriva de: Tras cerrar sesión, usar el botón 'atrás' del navegador o reutilizar el token anterior no da acceso a información protegida.

Given un usuario que cerró sesión y conserva el token anterior. When se realiza una petición a la API protegida con el token anterior en la cabecera Authorization. Then se deniega el acceso.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La API responde 401/403 sin datos protegidos en el cuerpo.


### TC-007 — deriva de: Tras cerrar sesión o expirar, el usuario es redirigido a la pantalla de inicio de sesión.

Given un usuario autenticado. When cierra sesión manualmente. Then es redirigido.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La URL cambia a la de login y se muestra el formulario de inicio de sesión.


### TC-008 — deriva de: Tras cerrar sesión o expirar, el usuario es redirigido a la pantalla de inicio de sesión.

Given un usuario autenticado y con sesión expirada por inactividad. When realiza cualquier acción en la página o se dispara la comprobación de expiración. Then es redirigido.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El usuario termina en la pantalla de inicio de sesión.


### TC-009 — deriva de: Cualquier actividad del usuario (interacción o petición a la API) reinicia el contador de inactividad.

Given un usuario autenticado con inactividad configurada de 1 minuto. When a los ~40 s realiza una interacción de UI (clic/navegación), espera otros ~40 s (total >1 min desde el inicio, <1 min desde la interacción) y navega a otra página protegida. Then la sesión sigue activa.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La sesión no expira y la página protegida se muestra con normalidad; el contador se reinició con la interacción.


### TC-010 — deriva de: Cualquier actividad del usuario (interacción o petición a la API) reinicia el contador de inactividad.

Given un usuario autenticado con inactividad de 1 minuto. When a los ~40 s se dispara una petición a la API autenticada (p. ej. acción que refresca datos), espera otros ~40 s y recarga una página protegida. Then la sesión sigue activa.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La petición a la API reinició el contador; la sesión sigue vigente y no se solicita login.


### TC-011 — deriva de: Si la sesión expira y el usuario intenta una acción o una petición, recibe un mensaje claro de sesión expirada y se le pide volver a iniciar sesión.

Given un usuario cuya sesión ha expirado por inactividad con la página protegida aún abierta. When hace clic en una acción que realiza una petición (p. ej. guardar o cargar datos). Then ve un mensaje.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se muestra un mensaje claro tipo 'Tu sesión ha expirado, inicia sesión de nuevo', la acción no se ejecuta y se ofrece/redirige al login.


### TC-012 — deriva de: Con varias pestañas o ventanas abiertas, el cierre o expiración de sesión se refleja en todas ellas.

Given un usuario autenticado con dos pestañas abiertas de la aplicación en el mismo contexto de navegador. When cierra sesión en la pestaña A. Then la pestaña B lo refleja.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La pestaña B pasa a la pantalla de login (o muestra sesión cerrada) automáticamente o al primer intento de acción, sin mostrar datos protegidos.


### TC-013 — deriva de: Con varias pestañas o ventanas abiertas, el cierre o expiración de sesión se refleja en todas ellas.

Given un usuario autenticado con dos pestañas abiertas y sin actividad en ninguna. When transcurre el periodo de inactividad. Then ambas pestañas reflejan la expiración.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Ambas pestañas muestran la pantalla de login/mensaje de sesión expirada y ninguna permite acceder a contenido protegido.


### TC-014 — deriva de: Se limpian los datos sensibles almacenados localmente (storage, caché) al cerrar sesión.

Given un usuario autenticado cuyo localStorage, sessionStorage, cookies y caché contienen datos de sesión/usuario. When cierra sesión. Then se inspecciona el almacenamiento del navegador.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** localStorage, sessionStorage y cookies ya no contienen token, datos personales ni información sensible; la caché no sirve contenido protegido.


### TC-015 — deriva de: Se limpian los datos sensibles almacenados localmente (storage, caché) al cerrar sesión.

Given un usuario cuya sesión expira por inactividad. When se muestra la pantalla de login tras la expiración. Then se inspecciona el almacenamiento del navegador.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** No permanecen tokens ni datos sensibles en storage/caché tras la expiración.


### TC-016 — deriva de: El cierre de sesión y la expiración quedan registrados en logs de auditoría.

Given un usuario autenticado y un auditor con acceso al log de auditoría. When el usuario cierra sesión manualmente y el auditor consulta el log de auditoría. Then aparece el evento.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** admin
- **Resultado esperado:** Existe un registro de cierre de sesión manual con usuario, fecha/hora y tipo de evento correctos.


### TC-017 — deriva de: El cierre de sesión y la expiración quedan registrados en logs de auditoría.

Given un usuario cuya sesión expira por inactividad y un admin con acceso a los logs de auditoría. When el admin consulta el log tras la expiración. Then aparece el evento.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** admin
- **Resultado esperado:** Existe un registro de expiración de sesión por inactividad con usuario, fecha/hora y motivo 'expiración' distinguible del cierre manual.


### TC-018 — deriva de: El tiempo de inactividad es configurable y no depende solo del cliente; el servidor valida la expiración.

Given un admin que cambia el tiempo de inactividad a un valor distinto (p. ej. 2 minutos) en la configuración, y un usuario autenticado. When el usuario permanece inactivo por ese nuevo periodo. Then la sesión expira según el nuevo valor.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** admin
- **Resultado esperado:** La sesión expira al cumplirse el nuevo tiempo configurado y no antes; el valor previo ya no se aplica.


### TC-019 — deriva de: El tiempo de inactividad es configurable y no depende solo del cliente; el servidor valida la expiración.

Given un usuario autenticado y con la sesión expirada en servidor por inactividad, pero con el temporizador del cliente manipulado/bloqueado (p. ej. temporizadores JS detenidos o reloj alterado). When envía una petición a un endpoint protegido. Then el servidor valida la expiración.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El servidor rechaza la petición con 401 o redirección a login aunque el cliente crea que la sesión sigue activa.
