---
hu_id: HU-003
fase: tcs_generados
total_tcs: 16
fecha_generacion: 2026-09-21
---

### TC-001 — deriva de: Dado un usuario autenticado, cuando elige cerrar sesión (salir), entonces su sesión termina y ya no puede acceder a funciones protegidas.

Given un usuario_final autenticado en el dashboard. When hace clic en 'Cerrar sesión' y luego intenta navegar por URL directa a una ruta protegida (p. ej. /perfil). Then el sistema no le permite acceder.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La sesión termina, se muestra la pantalla de login y al abrir /perfil se redirige al login sin mostrar contenido protegido.


### TC-002 — deriva de: Dado un usuario autenticado sin actividad, cuando transcurre el periodo de inactividad definido, entonces la sesión se cierra automáticamente.

Given un usuario_final autenticado en una pantalla protegida. When no realiza ninguna interacción durante el periodo de inactividad configurado (T). Then la sesión se cierra automáticamente.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Al cumplirse T sin actividad, la UI redirige al login y las rutas protegidas ya no son accesibles.


### TC-003 — deriva de: Dado un usuario autenticado sin actividad, cuando transcurre el periodo de inactividad definido, entonces la sesión se cierra automáticamente.

Given un usuario autenticado inactivo durante un tiempo ligeramente menor a T (T-10 s). When observa la pantalla sin interactuar y se verifica el estado antes de T. Then la sesión sigue activa.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** No hay cierre de sesión antes de T; la pantalla protegida sigue visible y funcional.


### TC-004 — deriva de: Dado un equipo compartido, cuando la sesión se cerró (manual o por inactividad), entonces el siguiente usuario no puede ver información ni ejecutar acciones de la sesión anterior.

Given un equipo compartido donde el usuario A cerró sesión manualmente. When el usuario B abre el navegador en la misma ventana, visita la URL de la app y prueba abrir rutas de A (historial, /perfil). Then no ve datos de A.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se muestra solo el login; ninguna pantalla, campo autocompletado ni dato de A es visible y no se puede ejecutar ninguna acción de A.


### TC-005 — deriva de: Dado un equipo compartido, cuando la sesión se cerró (manual o por inactividad), entonces el siguiente usuario no puede ver información ni ejecutar acciones de la sesión anterior.

Given un equipo compartido donde la sesión de A expiró por inactividad. When el usuario B inicia sesión con sus credenciales. Then ve únicamente sus propios datos.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** B ve solo su información; no aparece ningún dato, filtro, formulario en borrador ni estado de A.


### TC-006 — deriva de: Al cerrar sesión, el token/sesión se invalida en el servidor (no solo en el cliente); reutilizarlo devuelve 401/no autorizado.

Given un usuario autenticado cuyo token/cookie de sesión fue capturado. When cierra sesión desde la UI y luego se reenvía una petición autenticada a un endpoint protegido con el token capturado. Then el servidor rechaza la petición.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El servidor responde 401 (no autorizado) al reutilizar el token; no se devuelven datos protegidos.


### TC-007 — deriva de: Tras el cierre, el usuario es redirigido al inicio de sesión y el botón 'atrás' del navegador no muestra contenido protegido.

Given un usuario autenticado que navegó por varias pantallas protegidas. When cierra sesión y pulsa el botón 'atrás' del navegador varias veces. Then no se muestra contenido protegido.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Tras cerrar sesión se muestra el login; al ir atrás se muestra el login o se redirige a él, nunca contenido protegido (ni desde caché/bfcache).


### TC-008 — deriva de: Se eliminan los datos de sesión en el cliente (cookies, localStorage/sessionStorage, caché con datos sensibles).

Given un usuario autenticado con cookies de sesión y datos en localStorage/sessionStorage/caché. When cierra sesión y se inspeccionan el almacenamiento del navegador. Then los datos de sesión no existen.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Cookies de sesión eliminadas, localStorage y sessionStorage sin tokens ni datos de usuario, y caché sin respuestas con datos sensibles.


### TC-009 — deriva de: La actividad del usuario (clics, teclado, navegación, peticiones iniciadas por el usuario) reinicia el temporizador de inactividad.

Given un usuario autenticado que lleva casi T de inactividad. When realiza una acción (clic, pulsación de tecla, navegación o acción que dispara petición) y después espera un tiempo menor a T. Then la sesión sigue activa.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El temporizador se reinicia con cada tipo de actividad; la sesión no expira hasta que pasa T completo desde la última actividad.


### TC-010 — deriva de: La expiración se valida también en el servidor: una petición con sesión vencida es rechazada aunque el cliente no haya cerrado la sesión.

Given un usuario autenticado cuya sesión superó T en el servidor, con el cliente sin haber ejecutado el cierre (temporizador cliente detenido/pestaña suspendida). When realiza una acción protegida. Then el servidor rechaza la petición.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El servidor responde 401 y la UI redirige al login con el aviso de sesión vencida; no se ejecuta la acción.


### TC-011 — deriva de: Si hay varias pestañas o ventanas abiertas, el cierre de sesión (manual o por expiración) se refleja en todas.

Given un usuario autenticado con dos pestañas abiertas en pantallas protegidas. When cierra sesión manualmente en la pestaña 1. Then la pestaña 2 refleja el cierre.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La pestaña 2 redirige al login (inmediatamente o al siguiente evento) y no permite acciones protegidas.


### TC-012 — deriva de: Si hay varias pestañas o ventanas abiertas, el cierre de sesión (manual o por expiración) se refleja en todas.

Given un usuario autenticado con dos pestañas abiertas y sin actividad en ninguna. When transcurre T. Then ambas pestañas cierran sesión.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Ambas pestañas muestran el login; la actividad en una pestaña reinicia el temporizador para ambas antes de T.


### TC-013 — deriva de: Al expirar, se informa al usuario con un mensaje claro de que la sesión venció por inactividad y se le lleva al login.

Given un usuario autenticado inactivo. When transcurre T y la sesión expira. Then se le informa y se le lleva al login.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se muestra el login con un mensaje visible como 'Tu sesión venció por inactividad', distinto de un cierre manual.


### TC-014 — deriva de: Cerrar sesión debe estar disponible desde cualquier pantalla autenticada y ser idempotente (cerrar una sesión ya cerrada no genera error).

Given un usuario autenticado. When navega por cada pantalla autenticada principal (dashboard, perfil, listados, configuración). Then la opción 'Cerrar sesión' está visible y funciona.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El control de cerrar sesión está presente y operativo en todas las pantallas autenticadas.


### TC-015 — deriva de: Cerrar sesión debe estar disponible desde cualquier pantalla autenticada y ser idempotente (cerrar una sesión ya cerrada no genera error).

Given un usuario con dos pestañas donde la sesión ya fue cerrada en la pestaña 1. When en la pestaña 2 (aún mostrando la pantalla) hace clic en 'Cerrar sesión', o se invoca el endpoint de logout de nuevo. Then no ocurre error.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** No se muestra error ni respuesta 5xx; el endpoint responde de forma exitosa/idempotente y el usuario queda en el login.


### TC-016 — deriva de: El cierre y la expiración de sesión quedan registrados en bitácora/auditoría.

Given un usuario_final que cierra sesión manualmente y otro cuya sesión expira por inactividad. When un admin consulta la bitácora de auditoría. Then aparecen ambos eventos.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** admin
- **Resultado esperado:** Hay un registro por cada evento, con usuario, fecha/hora y tipo (cierre manual vs. expiración por inactividad).
