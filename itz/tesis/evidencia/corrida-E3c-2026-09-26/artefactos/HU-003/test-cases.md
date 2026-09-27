---
hu_id: HU-003
fase: tcs_generados
total_tcs: 27
fecha_generacion: 2026-09-26
---

### TC-001 — deriva de: Escenario 1 – Solicitud: Dado que ingreso mi correo en la pantalla 'Olvidé mi contraseña', cuando envío la solicitud, entonces recibo un correo con un enlace de restablecimiento.

TC-01 Solicitud con correo registrado (camino feliz)
Given un usuario registrado con el correo qa.user01@test.local y la bandeja de pruebas (mail catcher) vacía
And estoy sin sesión en la pantalla 'Olvidé mi contraseña'
When escribo qa.user01@test.local en el campo de correo y pulso 'Enviar'
Then se muestra el mensaje genérico de confirmación
And en la bandeja de pruebas llega un correo para qa.user01@test.local

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final (cuenta registrada, sin sesión iniciada)
- **Resultado esperado:** Se ve el mensaje genérico de confirmación. En menos de 60 s llega a la bandeja de pruebas un solo correo para qa.user01@test.local con un enlace de restablecimiento que empieza por https:// y lleva un token.


### TC-002 — deriva de: Escenario 2 – Restablecimiento: Dado que abro un enlace vigente, cuando capturo una nueva contraseña válida, entonces se actualiza y puedo iniciar sesión con ella.

TC-02 Restablecimiento con enlace vigente (camino feliz)
Given qa.user01 pidió el restablecimiento hace menos de 1 hora y tengo el enlace de la bandeja de pruebas
When abro el enlace, escribo 'NuevaClave#2026' en 'Nueva contraseña' y en 'Confirmar contraseña' y pulso 'Guardar'
And voy a la pantalla de inicio de sesión y entro con qa.user01@test.local / 'NuevaClave#2026'
Then el inicio de sesión funciona

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Al guardar se muestra un mensaje de contraseña actualizada. Después, el inicio de sesión con la nueva contraseña lleva al área autenticada (p. ej. se ve el dashboard o el menú de usuario).


### TC-003 — deriva de: Escenario 3 – Enlace vencido: Dado que el enlace se generó hace más de 1 hora, cuando lo abro, entonces el sistema indica que expiró y me permite solicitar uno nuevo.

TC-03 Abrir un enlace vencido y pedir uno nuevo
Given un enlace de restablecimiento de qa.user01 generado hace 61 minutos (con el reloj del entorno de pruebas adelantado o con una fixture de token vencido)
When abro el enlace
Then se muestra un mensaje de enlace expirado y la opción 'Solicitar un nuevo enlace'
When pulso esa opción y envío la solicitud con qa.user01@test.local
Then llega un correo nuevo con otro enlace

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** No aparece el formulario de nueva contraseña. Se ve un mensaje que dice que el enlace expiró y la opción para pedir uno nuevo, que lleva a 'Olvidé mi contraseña'. Al pedirlo llega un correo nuevo con un token distinto, y ese enlace abre el formulario de nueva contraseña.


### TC-004 — deriva de: Regla – Un solo uso: Dado que ya usé un enlace para cambiar mi contraseña, cuando intento usarlo otra vez, entonces se rechaza como no válido.

TC-04 Volver a usar un enlace ya consumido
Given qa.user01 ya cambió su contraseña con el enlace E1
When abro otra vez el enlace E1 en una pestaña nueva
Then el sistema lo rechaza como no válido

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** No aparece el formulario de nueva contraseña. Se ve el mensaje de enlace no válido o ya utilizado y la contraseña sigue siendo la del primer cambio (el inicio de sesión con ella sigue funcionando).


### TC-005 — deriva de: Regla – Vigencia: Dado un enlace generado, cuando pasa 1 hora desde que se generó, entonces deja de ser válido.

TC-05 Límite de vigencia: el enlace sigue valiendo antes de 1 hora
Given un enlace de qa.user01 generado hace 59 minutos (reloj del entorno controlado)
When abro el enlace y guardo una contraseña válida
Then el cambio se acepta

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El formulario de nueva contraseña aparece y el cambio se guarda con el mensaje de éxito.


### TC-006 — deriva de: Regla – Vigencia: Dado un enlace generado, cuando pasa 1 hora desde que se generó, entonces deja de ser válido.

TC-06 Límite de vigencia: el enlace deja de valer al pasar 1 hora
Given un enlace de qa.user01 generado hace 60 minutos y 1 segundo (reloj del entorno controlado)
When abro el enlace
Then se trata como vencido

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se muestra el mensaje de enlace expirado con la opción de pedir uno nuevo, y no aparece el formulario de nueva contraseña.


### TC-007 — deriva de: Regla – Respuesta uniforme: Dado que envío una solicitud con un correo registrado o no registrado, cuando el sistema responde, entonces el mensaje en pantalla y la respuesta de la API son iguales en los dos casos (no se revela si el correo existe).

TC-07 Misma respuesta para correo registrado y no registrado
Given estoy en 'Olvidé mi contraseña' y Playwright intercepta la petición al endpoint de solicitud
When envío la solicitud con qa.user01@test.local (registrado) y guardo el texto en pantalla y la respuesta de la API (código HTTP, cuerpo y cabeceras que no cambian por naturaleza)
And repito con no.existe.9f3a@test.local (no registrado)
Then comparo las dos respuestas

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado (sin sesión; se usa un correo de usuario_final registrado y otro que no existe)
- **Resultado esperado:** El texto en pantalla es idéntico en los dos casos. La API devuelve el mismo código HTTP y el mismo cuerpo JSON. Solo pueden cambiar las cabeceras que cambian por naturaleza (fecha, id de petición). Ni la pantalla ni la respuesta dicen si el correo existe.


### TC-008 — deriva de: Regla – Cierre de sesiones: Dado que tengo sesiones abiertas en uno o más dispositivos, cuando restablezco la contraseña, entonces todas esas sesiones se invalidan y tengo que volver a iniciar sesión.

TC-08 Las sesiones abiertas se invalidan al restablecer
Given qa.user01 tiene sesión iniciada en dos contextos de navegador aislados (A = Chromium, B = WebKit) y los dos cargan el área autenticada
When en un tercer contexto C restablezco la contraseña de qa.user01 con un enlace vigente
And en A y en B recargo la página o hago una acción autenticada
Then las dos sesiones quedan invalidadas

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** En A y en B la acción autenticada se rechaza: la app redirige a inicio de sesión o la API responde 401. Para volver a entrar hay que iniciar sesión con la nueva contraseña.


### TC-009 — deriva de: Correo no registrado: Dado un correo que no existe, cuando envío la solicitud, entonces no se manda ningún correo y se muestra el mismo mensaje genérico de confirmación.

TC-09 Solicitud con correo no registrado
Given no.existe.9f3a@test.local no está registrado y la bandeja de pruebas está vacía
When envío la solicitud en 'Olvidé mi contraseña' con ese correo
Then se muestra el mensaje genérico de confirmación
And reviso la bandeja de pruebas después de 2 minutos

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El mensaje en pantalla es el mismo texto que se ve con un correo registrado (TC-01). Después de 2 minutos no hay ningún correo para no.existe.9f3a@test.local en la bandeja de pruebas.


### TC-010 — deriva de: Tiempo de respuesta uniforme: la API tarda un tiempo parecido exista o no el correo, para que no se pueda saber por el tiempo si está registrado (el envío del correo se hace de forma asíncrona o con un tiempo equivalente).

TC-10 Tiempo de respuesta parecido para correo registrado y no registrado
Given Playwright mide la duración de la petición al endpoint de solicitud desde la UI
When hago 20 solicitudes con correos registrados y 20 con correos no registrados, intercaladas y con correos distintos para no llegar al límite de peticiones (o con el límite desactivado en el entorno de pruebas)
Then comparo la mediana y el percentil 95 de los dos grupos

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** La diferencia entre las medianas de los dos grupos está dentro del margen acordado (propuesta: ≤ 50 ms o ≤ 10 %, lo que sea mayor; hay que confirmarlo con el equipo) y las distribuciones se solapan. Con los tiempos no se puede saber si el correo existe.


### TC-011 — deriva de: Formato de correo: Dado que escribo un correo con formato inválido o dejo el campo vacío, cuando envío, entonces se muestra un error de validación en frontend y backend y no se procesa la solicitud.

TC-11 Campo de correo vacío (frontend)
Given estoy en 'Olvidé mi contraseña' y Playwright escucha las peticiones de red
When dejo el campo vacío y pulso 'Enviar'
Then se muestra un error de validación junto al campo

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Aparece un mensaje de campo obligatorio junto al campo de correo, no se hace ninguna petición al endpoint de solicitud y no se muestra el mensaje de confirmación.


### TC-012 — deriva de: Formato de correo: Dado que escribo un correo con formato inválido o dejo el campo vacío, cuando envío, entonces se muestra un error de validación en frontend y backend y no se procesa la solicitud.

TC-12 Correo con formato inválido (frontend)
Given estoy en 'Olvidé mi contraseña'
When escribo por turnos 'usuario', 'usuario@', '@dominio.com' y 'usu ario@dominio.com' y pulso 'Enviar' con cada uno
Then cada intento se rechaza en el cliente

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Con cada valor aparece un error de formato de correo inválido, no se hace ninguna petición al endpoint y no se muestra la confirmación.


### TC-013 — deriva de: Formato de correo: Dado que escribo un correo con formato inválido o dejo el campo vacío, cuando envío, entonces se muestra un error de validación en frontend y backend y no se procesa la solicitud.

TC-13 Validación del formato en backend (saltando el frontend)
Given Playwright manda peticiones directas al endpoint de solicitud (APIRequestContext), o cambia la petición del formulario con page.route
When envío email vacío, 'usuario@' y un email ausente del cuerpo
Then el backend rechaza cada petición

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** Cada petición recibe un error de validación (4xx, p. ej. 400 o 422) con el código de error documentado. No se manda ningún correo a la bandeja de pruebas y no queda registrada una solicitud de restablecimiento procesada.


### TC-014 — deriva de: Contraseña inválida: Dado un enlace vigente, cuando capturo una contraseña que no cumple la política vigente, entonces se rechaza con un mensaje que dice qué regla no se cumple, y el enlace sigue sirviendo hasta que se use o venza.

TC-14 Contraseña que no cumple la política
Given abrí un enlace vigente de qa.user01
When escribo en los dos campos una contraseña que incumple una regla concreta de la política (p. ej. 'abc' por longitud mínima, y otra sin mayúscula, sin número, etc., según la política vigente) y pulso 'Guardar'
Then se rechaza con un mensaje que dice la regla incumplida
When en el mismo enlace escribo después una contraseña válida y guardo
Then el cambio se acepta

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Por cada contraseña inválida se ve un mensaje que nombra la regla que no se cumple (p. ej. 'Debe tener al menos N caracteres') y la contraseña no cambia (la anterior sigue funcionando). Luego, el mismo enlace acepta una contraseña válida y se ve el mensaje de éxito.


### TC-015 — deriva de: Confirmación de contraseña: se pide escribir la nueva contraseña dos veces y, si no coinciden, no se guarda.

TC-15 La confirmación no coincide
Given abrí un enlace vigente de qa.user01 cuya contraseña actual es 'ClaveActual#1'
When escribo 'NuevaClave#2026' en 'Nueva contraseña' y 'NuevaClave#2027' en 'Confirmar contraseña' y pulso 'Guardar'
Then se muestra un error de que las contraseñas no coinciden

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Aparece el error de que las contraseñas no coinciden y no se guarda nada: con 'ClaveActual#1' se puede seguir entrando y con 'NuevaClave#2026' no. El formulario sigue disponible con el mismo enlace.


### TC-016 — deriva de: Enlace inválido o alterado: Dado un enlace con un token inexistente, mal formado o manipulado, cuando lo abro, entonces se muestra un mensaje genérico de enlace no válido y la opción de pedir uno nuevo.

TC-16 Token inexistente, mal formado o manipulado
Given tengo un enlace válido de qa.user01
When abro por turnos: (a) el enlace con un token aleatorio del mismo largo que no existe, (b) el enlace con el token vacío o con caracteres inválidos ('%%%<script>'), (c) el enlace con un solo carácter del token válido cambiado
Then en cada caso se muestra el mismo mensaje genérico

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** En los tres casos se ve el mismo mensaje genérico de enlace no válido y la opción 'Solicitar un nuevo enlace'. No aparece el formulario de nueva contraseña, no hay error 500 ni traza técnica, y no se ejecuta ningún script inyectado. Después, el enlace original sin cambios sigue funcionando.


### TC-017 — deriva de: Enlace ya usado: al abrir un enlace consumido se muestra un mensaje (no válido/ya utilizado) con la opción de pedir uno nuevo.

TC-17 Mensaje y opción al abrir un enlace consumido
Given el enlace E1 de qa.user01 ya se usó para cambiar la contraseña
When abro E1
Then se muestra el mensaje de enlace no válido o ya utilizado
When pulso 'Solicitar un nuevo enlace'
Then llego a la pantalla 'Olvidé mi contraseña'

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se ve el mensaje de enlace no válido o ya utilizado con la opción visible y funcional 'Solicitar un nuevo enlace', que lleva a 'Olvidé mi contraseña'.


### TC-018 — deriva de: Vigencia también en backend: la expiración y el uso único se validan en el servidor al enviar la nueva contraseña, no solo al abrir el enlace (caso de un formulario que se abrió a los 59 minutos y se envió a los 61).

TC-18 El formulario se abre a los 59 minutos y se envía a los 61
Given un enlace de qa.user01 generado hace 59 minutos (reloj del servidor controlado)
When abro el enlace y aparece el formulario de nueva contraseña
And adelanto el reloj del servidor 2 minutos (el token tiene ahora 61 minutos)
And escribo una contraseña válida en los dos campos y pulso 'Guardar'
Then el servidor rechaza el cambio

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** La API de restablecimiento responde con el error de enlace expirado (código documentado) y la UI muestra el mensaje de expiración con la opción de pedir uno nuevo. La contraseña no cambia: la anterior sigue funcionando.


### TC-019 — deriva de: Vigencia también en backend: la expiración y el uso único se validan en el servidor al enviar la nueva contraseña, no solo al abrir el enlace (caso de un formulario que se abrió a los 59 minutos y se envió a los 61).

TC-19 Uso único validado al enviar (dos pestañas)
Given abrí el mismo enlace vigente de qa.user01 en dos pestañas, P1 y P2, y las dos muestran el formulario
When en P1 guardo 'NuevaClave#A1' con éxito
And en P2 guardo 'NuevaClave#B2'
Then el servidor rechaza el envío de P2

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** P2 recibe el error de enlace no válido o ya utilizado y la UI lo muestra. La contraseña que queda es 'NuevaClave#A1' (funciona) y 'NuevaClave#B2' no permite entrar.


### TC-020 — deriva de: Seguridad del token: el token es aleatorio, criptográficamente seguro y difícil de adivinar; se guarda como hash, no en texto plano.

TC-20 Tokens únicos, largos y no predecibles
Given el límite de peticiones está desactivado o es suficiente en el entorno de pruebas
When pido 20 enlaces seguidos para qa.user01 y para qa.user02 y saco el token de cada correo en la bandeja de pruebas
Then analizo los tokens

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Los 40 tokens son distintos. Cada uno tiene al menos 128 bits de entropía (p. ej. ≥ 22 caracteres base64url o ≥ 32 hex). No se ven patrones secuenciales, ni partes derivadas del correo, el id de usuario o la fecha. Aparte: que el token se guarda como hash no se puede ver desde la UI; hay que confirmarlo con una consulta a la base de datos (el valor guardado no coincide con el token del correo) o con revisión de código.


### TC-021 — deriva de: Almacenamiento de la contraseña: la nueva contraseña se guarda con un hash seguro y nunca aparece en logs ni en la auditoría.

TC-21 La contraseña nueva no se expone
Given un enlace vigente de qa.user01 y Playwright captura todo el tráfico de red (HAR)
When guardo la contraseña 'MarcaUnica#7Qz91' (un valor fácil de buscar)
And como admin abro la vista de auditoría y busco el evento de cambio de contraseña
Then busco 'MarcaUnica#7Qz91' en las respuestas del servidor y en la auditoría

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final (hace el cambio) + admin (revisa la auditoría)
- **Resultado esperado:** 'MarcaUnica#7Qz91' no aparece en ninguna respuesta del servidor ni en la vista de auditoría; solo aparece en el cuerpo de la petición de restablecimiento que envía el cliente. Aparte: el hash seguro (bcrypt/argon2/scrypt) y que no esté en los logs del servidor no se pueden ver desde la UI; hay que confirmarlo buscando el valor en la base de datos y en los logs.


### TC-022 — deriva de: Contraseña anterior: después del cambio, la contraseña anterior ya no permite iniciar sesión.

TC-22 La contraseña anterior deja de funcionar
Given qa.user01 tenía la contraseña 'ClaveActual#1' y la cambió a 'NuevaClave#2026' con un enlace vigente
When en la pantalla de inicio de sesión entro con qa.user01@test.local / 'ClaveActual#1'
Then el inicio de sesión se rechaza

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** Se muestra el error genérico de credenciales inválidas y el usuario sigue en la pantalla de inicio de sesión sin sesión. Con 'NuevaClave#2026' sí se puede entrar.


### TC-023 — deriva de: Protección contra abuso: las solicitudes se limitan por correo y por IP para evitar que se inunde a alguien de correos o se enumeren cuentas, y la respuesta visible sigue siendo la misma.

TC-23 Límite de solicitudes por correo
Given el límite por correo está configurado en N solicitudes por ventana de tiempo (el valor de N y de la ventana hay que confirmarlo con el equipo) y la bandeja de pruebas está vacía
When envío N+3 solicitudes seguidas desde la UI para qa.user01@test.local
Then reviso el mensaje en pantalla de cada solicitud y la bandeja de pruebas

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado (sobre la cuenta de usuario_final qa.user01)
- **Resultado esperado:** Todas las solicitudes, también las que pasan el límite, muestran exactamente el mismo mensaje genérico en pantalla. En la bandeja de pruebas hay como mucho N correos para qa.user01. La respuesta de la API que ve el usuario no dice que se pasó el límite de forma distinta según el correo exista o no.


### TC-024 — deriva de: Protección contra abuso: las solicitudes se limitan por correo y por IP para evitar que se inunde a alguien de correos o se enumeren cuentas, y la respuesta visible sigue siendo la misma.

TC-24 Límite de solicitudes por IP (intento de enumeración)
Given el límite por IP está configurado en M solicitudes por ventana de tiempo (hay que confirmarlo) y todas las peticiones salen de la misma IP
When desde la UI envío M+5 solicitudes con correos distintos, mezclando registrados y no registrados
Then reviso el mensaje en pantalla y los correos recibidos

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado
- **Resultado esperado:** El mensaje en pantalla es idéntico en todas las solicitudes. Después de M solicitudes no llega ningún correo más a la bandeja de pruebas, aunque el correo esté registrado. Con la respuesta visible no se puede saber qué correos existen.


### TC-025 — deriva de: Auditoría (según la DoD): se registran la solicitud de restablecimiento, el cambio de contraseña hecho y el cierre de sesiones, con fecha y hora, usuario (si existe) e IP, sin guardar datos sensibles.

TC-25 Eventos de auditoría del flujo completo
Given qa.user01 tiene una sesión abierta y anoto la hora de inicio de la prueba
When como invitado pido el restablecimiento de qa.user01, y también el de no.existe.9f3a@test.local
And como usuario_final restablezco la contraseña de qa.user01 con el enlace
And como admin abro la vista de auditoría filtrando desde la hora de inicio
Then reviso los eventos registrados

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** admin (revisa la auditoría); invitado y usuario_final hacen las acciones
- **Resultado esperado:** Aparecen estos eventos: solicitud de restablecimiento (qa.user01), solicitud de restablecimiento con correo no registrado (sin usuario asociado), contraseña cambiada (qa.user01) y sesiones cerradas (qa.user01). Cada uno tiene fecha y hora de la ejecución, la IP de origen y el usuario cuando existe. En ningún evento aparecen la contraseña, el token o el enlace completo.


### TC-026 — deriva de: Transporte seguro: el enlace usa HTTPS y el token no se filtra a terceros (por ejemplo, con la cabecera Referrer-Policy en la página de restablecimiento).

TC-26 HTTPS y Referrer-Policy en la página de restablecimiento
Given tengo un enlace vigente de qa.user01 sacado de la bandeja de pruebas
When reviso la URL del enlace, la abro con Playwright y capturo las cabeceras de respuesta de la página
And capturo las peticiones a dominios de terceros que hace la página (analítica, CDN, fuentes) y las que salen de hacer clic en un enlace externo de la página, si hay alguno
Then verifico el esquema, la cabecera y las cabeceras Referer que se envían

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** usuario_final
- **Resultado esperado:** El enlace empieza por https://, y si se abre la versión http:// redirige a https://. La respuesta de la página de restablecimiento trae la cabecera Referrer-Policy con 'no-referrer' o 'same-origin'. Ninguna petición a terceros lleva el token en la cabecera Referer ni en la URL.


### TC-027 — deriva de: Documentación de API: los endpoints de solicitud y de restablecimiento quedan documentados con sus respuestas y códigos de error (según la DoD).

TC-27 Documentación de los endpoints
Given la documentación de la API (p. ej. Swagger/OpenAPI UI) está publicada en el entorno de pruebas
When la abro en el navegador y busco los endpoints de solicitud y de restablecimiento de contraseña
Then reviso lo que se documenta de cada uno

- **Tipo de verificación:** ui_playwright
- **Rol requerido:** invitado (o el rol con acceso a la documentación de la API, si está protegida)
- **Resultado esperado:** Los dos endpoints aparecen documentados con método, ruta, esquema del cuerpo de la petición, respuesta de éxito y códigos de error: validación de correo o contraseña (400/422), token no válido, expirado o ya usado, y límite de peticiones (429 o su equivalente). Lo documentado coincide con lo que se vio en TC-07, TC-13, TC-16, TC-18 y TC-23.
