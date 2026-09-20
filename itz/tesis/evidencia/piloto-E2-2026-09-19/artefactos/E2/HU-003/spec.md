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

# Cerrar sesión voluntariamente y expiración por inactividad

Como usuario autenticado, quiero cerrar mi sesión explícitamente o que esta expire automáticamente tras un periodo de inactividad, para proteger mi cuenta y evitar accesos no autorizados en dispositivos compartidos o públicos.

## Criterios de aceptación explícitos

- Dado que el usuario se encuentra con una sesión activa en la plataforma, cuando selecciona la opción de cerrar sesión, entonces su sesión finaliza inmediatamente y se evita el acceso no autorizado a su cuenta.
- Dado que el usuario tiene una sesión activa y no realiza ninguna acción en la plataforma durante un periodo de inactividad, cuando se alcanza el límite de tiempo configurado, entonces el sistema cierra automáticamente la sesión para proteger la cuenta en equipos compartidos.

## Criterios de aceptación inferidos

- Dado que la sesión finalizó (por acción del usuario o inactividad), cuando el usuario intenta navegar hacia atrás usando el botón del navegador o acceder directamente a URLs protegidas, entonces el sistema deniega el acceso y lo redirige a la pantalla de inicio de sesión.
- Dado que la sesión expiró por inactividad, cuando el sistema realiza el cierre automático, entonces redirige al usuario a la pantalla de login y muestra una notificación/mensaje claro indicando que la sesión se cerró por inactividad.
- Dado que el usuario realiza interacciones en la plataforma (movimiento de cursor, tecleo, clics o peticiones HTTP/API) antes de que expire el tiempo límite, cuando detecta actividad, entonces el temporizador de inactividad se reinicia a cero.
- Dado que la sesión se cierra (voluntaria o por expiración), cuando se procesa la solicitud de cierre, entonces el servidor invalida completamente los tokens de acceso/cookies de sesión (HttpOnly) impidiendo su reutilización en peticiones futuras (respuesta HTTP 401 Unauthorized).
- Dado que el usuario tiene la aplicación abierta en múltiples pestañas del mismo navegador, cuando cierra sesión o esta expira en una de las pestañas, entonces la sesión se invalida sincrónicamente en todas las demás pestañas abiertas.

## Supuestos y vacíos identificados

- Umbral de tiempo de inactividad: Se asume un tiempo límite por defecto (ej. 15 o 30 minutos), pero requiere confirmación explícita con el PO/Negocio para alinearlo con las políticas de seguridad del sistema.
- Advertencia previa de expiración (Timeout Warning): Se asume que no hay aviso previo antes del cierre automático. Hace falta confirmar con UX/Negocio si se desea incluir un modal interactivo N minutos/segundos antes de expirar (ej. 'Tu sesión expira en 1 minuto, ¿deseas mantenerla activa?').
- Comportamiento con tareas en segundo plano o descargas: Se asume que la inactividad considera solo eventos de usuario explícitos (UI) y no llamadas periódicas pasivas (polling), a menos que Negocio defina lo contrario.

## Notas

Se recomienda sincronizar esta HU con el equipo de seguridad y backend para asegurar que la expiración no ocurra únicamente a nivel de cliente (UI/Frontend), sino que haya una invalidación efectiva de tokens/sesión en el servidor (ej. revocación de Refresh Tokens o TTL corto en Access Tokens).
