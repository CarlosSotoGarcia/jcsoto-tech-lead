---
hu_id: HU-003
fase: tcs_generados
total_tcs: 7
fecha_generacion: 2026-09-19
---

### TC-001 — deriva de: Dado que el usuario se encuentra con una sesión activa en la plataforma, cuando selecciona la opción de cerrar sesión, entonces su sesión finaliza inmediatamente y se evita el acceso no autorizado a su cuenta.

GIVEN el usuario "usuario_final" ha iniciado sesión y se encuentra en el panel principal
WHEN hace clic en el avatar de usuario y selecciona la opción "Cerrar sesión"
THEN el sistema cierra la sesión inmediatamente y redirige a la pantalla de inicio de sesión.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El usuario es redirigido a la pantalla de login y su sesión queda terminada sin acceso a rutas privadas.


### TC-002 — deriva de: Dado que el usuario tiene una sesión activa y no realiza ninguna acción en la plataforma durante un periodo de inactividad, cuando se alcanza el límite de tiempo configurado, entonces el sistema cierra automáticamente la sesión para proteger la cuenta en equipos compartidos.

GIVEN el usuario "usuario_final" ha iniciado sesión en la plataforma
WHEN transcurre el tiempo límite de inactividad configurado sin que el usuario realice ninguna acción
THEN el sistema cierra la sesión automáticamente y finaliza la sesión activa.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La sesión del usuario se destruye automáticamente tras alcanzar el tiempo límite de inactividad.


### TC-003 — deriva de: Dado que la sesión expiró por inactividad, cuando el sistema realiza el cierre automático, entonces redirige al usuario a la pantalla de login y muestra una notificación/mensaje claro indicando que la sesión se cerró por inactividad.

GIVEN la sesión del usuario finalizó automáticamente por inactividad
WHEN el sistema efectúa la redirección a la pantalla de inicio de sesión
THEN la pantalla de login muestra un mensaje o banner de notificación indicando "Su sesión ha expirado por inactividad".

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se visualiza un mensaje explícito en la pantalla de login informando la causa del cierre de sesión por inactividad.


### TC-004 — deriva de: Dado que la sesión finalizó (por acción del usuario o inactividad), cuando el usuario intenta navegar hacia atrás usando el botón del navegador o acceder directamente a URLs protegidas, entonces el sistema deniega el acceso y lo redirige a la pantalla de inicio de sesión.

GIVEN el usuario ha finalizado su sesión previa en la plataforma
WHEN intenta hacer clic en el botón atrás del navegador o ingresa directamente una URL protegida (ej: "/dashboard")
THEN el sistema deniega el acceso a la ruta protegida y redirige automáticamente al formulario de login.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Acceso denegado a la ruta protegida y redirección inmediata al login sin mostrar contenido privado en caché o estado anterior.


### TC-005 — deriva de: Dado que el usuario realiza interacciones en la plataforma (movimiento de cursor, tecleo, clics o peticiones HTTP/API) antes de que expire el tiempo límite, cuando detecta actividad, entonces el temporizador de inactividad se reinicia a cero.

GIVEN el usuario tiene una sesión activa y ha transcurrido parte del tiempo de inactividad
WHEN el usuario realiza una interacción en la plataforma (movimiento de cursor, presionar teclas, clic o petición API) antes de alcanzar el tiempo límite
THEN el temporizador de inactividad se reinicia a cero y la sesión permanece activa sin cerrarse.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La sesión no expira y el contador de inactividad vuelve al estado inicial de 0.


### TC-006 — deriva de: Dado que la sesión se cierra (voluntaria o por expiración), cuando se procesa la solicitud de cierre, entonces el servidor invalida completamente los tokens de acceso/cookies de sesión (HttpOnly) impidiendo su reutilización en peticiones futuras (respuesta HTTP 401 Unauthorized).

GIVEN la sesión del usuario ha sido cerrada (voluntariamente o por expiración)
WHEN se intenta realizar una nueva petición HTTP/API reutilizando el token o cookie de sesión previamente emitido
THEN el servidor responde con un código HTTP 401 Unauthorized e invalida la petición.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Respuesta HTTP 401 Unauthorized confirmando la invalidación total del token/cookie en el backend.


### TC-007 — deriva de: Dado que el usuario tiene la aplicación abierta en múltiples pestañas del mismo navegador, cuando cierra sesión o esta expira en una de las pestañas, entonces la sesión se invalida sincrónicamente en todas las demás pestañas abiertas.

GIVEN el usuario tiene la aplicación abierta con sesión activa en dos pestañas del mismo navegador
WHEN cierra la sesión o esta expira en la primera pestaña
THEN la segunda pestaña detecta la invalidación de la sesión en tiempo real y redirige sincrónicamente a la pantalla de inicio de sesión.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Redirección automática a la pantalla de inicio de sesión en todas las pestañas abiertas del mismo navegador.
