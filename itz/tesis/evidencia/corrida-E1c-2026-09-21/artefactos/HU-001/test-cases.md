---
hu_id: HU-001
fase: tcs_generados
total_tcs: 14
fecha_generacion: 2026-09-21
---

### TC-001 — deriva de: Dado un usuario registrado con credenciales válidas (correo y contraseña), cuando envía el formulario de inicio de sesión, entonces el sistema lo autentica y le da acceso al sistema.

Given un usuario registrado con correo y contraseña válidos y la página de login abierta. When ingresa ambos datos y pulsa 'Iniciar sesión'. Then se procesa la autenticación.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El usuario es redirigido a la página principal/dashboard, se muestra su nombre o indicador de sesión activa y no aparece mensaje de error.


### TC-002 — deriva de: Dado un usuario autenticado, cuando navega o consulta información, entonces solo puede ver/acceder a la información que le corresponde (la asociada a su cuenta/permisos), y no la de otros usuarios.

Given usuario_final A autenticado y existen datos de usuario B. When navega por las secciones y listados del sistema (perfil, pedidos, etc.). Then se revisa la información mostrada.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Solo se muestran datos asociados a la cuenta de A; ningún dato de B aparece en pantallas, listados ni búsquedas.


### TC-003 — deriva de: Dado un correo o contraseña incorrectos, cuando intenta iniciar sesión, entonces se rechaza el acceso con un mensaje genérico que no revela cuál de los dos datos falló (evita enumeración de usuarios).

Given un correo registrado y la página de login. When ingresa el correo correcto con una contraseña incorrecta y envía el formulario. Then se evalúa la respuesta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se rechaza el acceso, permanece en login y se muestra un mensaje genérico (p. ej. 'Correo o contraseña incorrectos') sin indicar cuál dato falló.


### TC-004 — deriva de: Dado un correo no registrado, cuando intenta iniciar sesión, entonces recibe el mismo mensaje que con contraseña incorrecta.

Given un correo que no existe en el sistema. When ingresa ese correo con cualquier contraseña y envía. Then se compara el mensaje con el del caso de contraseña incorrecta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El mensaje mostrado es idéntico en texto (y sin diferencias apreciables de estructura) al de contraseña incorrecta; el acceso es rechazado.


### TC-005 — deriva de: Dado que el correo o la contraseña están vacíos, o el correo tiene formato inválido, cuando intenta enviar, entonces se muestra una validación de campo y no se procesa la autenticación.

Given la página de login. When intenta enviar (a) con correo vacío, (b) con contraseña vacía, (c) con correo 'usuario@' de formato inválido. Then se observa la interfaz y las peticiones de red.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Para cada caso se muestra un mensaje de validación junto al campo correspondiente, no se envía petición de autenticación y no se inicia sesión.


### TC-006 — deriva de: Dado que un usuario intenta acceder directamente a un recurso de otro usuario (por URL o API), cuando la solicitud llega, entonces el servidor la rechaza (403/404) y la autorización se valida en backend, no solo ocultando elementos en la interfaz.

Given usuario_final A autenticado y el identificador de un recurso de B. When escribe manualmente la URL del recurso de B en el navegador y también solicita el endpoint de API correspondiente con la sesión de A. Then se revisa la respuesta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El servidor responde 403 o 404 en ambos casos, no se muestran datos de B y se ve una página/mensaje de acceso denegado o no encontrado.


### TC-007 — deriva de: Dado un usuario no autenticado o con sesión expirada, cuando intenta acceder a una página o endpoint protegido, entonces es redirigido al inicio de sesión / recibe 401.

Given un visitante sin sesión. When navega directamente a una URL protegida y consulta un endpoint protegido sin credenciales. Then se observa la respuesta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** La página redirige al login y el endpoint responde 401; no se muestra contenido protegido.


### TC-008 — deriva de: Dado un usuario no autenticado o con sesión expirada, cuando intenta acceder a una página o endpoint protegido, entonces es redirigido al inicio de sesión / recibe 401.

Given usuario_final autenticado cuya sesión/token ha expirado (esperando la vigencia o invalidando la cookie). When recarga o navega a una página protegida. Then se observa el resultado.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Es redirigido a la página de inicio de sesión y las llamadas a la API responden 401; no se muestra contenido protegido.


### TC-009 — deriva de: Las contraseñas nunca se almacenan ni se transmiten en texto plano (hash con sal en almacenamiento, tráfico por HTTPS) y no aparecen en logs; el campo de contraseña se enmascara.

Given la página de login cargada. When escribe una contraseña en el campo y envía el formulario, inspeccionando el campo y el tráfico de red. Then se verifica el enmascaramiento y el protocolo.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El campo es type=password (caracteres enmascarados), la URL de la página y la petición usan HTTPS, y la contraseña no aparece en la URL ni en query params. (El hash con sal y los logs se verifican por revisión de backend fuera de UI.)


### TC-010 — deriva de: Dado un inicio de sesión exitoso, cuando se crea la sesión/token, entonces este tiene vigencia limitada y se invalida al cerrar sesión.

Given usuario_final autenticado con cookie/token de sesión. When pulsa 'Cerrar sesión' y luego intenta volver a una página protegida con el botón Atrás o reutilizando el token anterior. Then se observa el acceso.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La sesión se cierra, se redirige al login y el token anterior es rechazado (401); la cookie/token tiene fecha de expiración definida.


### TC-011 — deriva de: Dados varios intentos fallidos consecutivos, cuando se supera un umbral, entonces se aplica una protección contra fuerza bruta (bloqueo temporal, retardo o captcha).

Given un correo registrado. When realiza intentos fallidos consecutivos por encima del umbral configurado (p. ej. 5) y luego intenta con la contraseña correcta. Then se observa la respuesta.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Tras superar el umbral se muestra bloqueo temporal, retardo o captcha y el intento con contraseña correcta durante el bloqueo no concede acceso; el mensaje no revela si la cuenta existe.


### TC-012 — deriva de: La comparación del correo no distingue mayúsculas/minúsculas y se ignoran espacios al inicio o final.

Given un usuario registrado con correo 'usuario@ejemplo.com'. When ingresa '  USUARIO@Ejemplo.COM  ' con su contraseña válida y envía. Then se evalúa el resultado.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La autenticación es exitosa y accede al sistema como el mismo usuario.


### TC-013 — deriva de: Dado que el servicio de autenticación no está disponible, cuando el usuario intenta iniciar sesión, entonces ve un mensaje de error amigable sin perder lo escrito en el correo.

Given la página de login y el servicio de autenticación simulado como caído (interceptando la petición con error 503/timeout). When escribe correo y contraseña y envía. Then se observa la interfaz.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Se muestra un mensaje amigable de error temporal (sin detalles técnicos), el campo de correo conserva el valor escrito y no se inicia sesión.


### TC-014 — deriva de: Se registran los intentos de inicio de sesión (exitosos y fallidos) para auditoría.

Given un usuario registrado. When realiza un inicio de sesión fallido y luego uno exitoso. Then un admin consulta el registro de auditoría.

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** admin
- **Resultado esperado:** El registro de auditoría contiene ambas entradas con fecha/hora, correo, resultado (fallido/exitoso) y origen; ninguna entrada contiene la contraseña.
