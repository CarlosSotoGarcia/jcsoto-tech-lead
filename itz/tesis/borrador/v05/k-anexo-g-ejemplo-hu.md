@@ tesis_anexos+
CAPITULO: G
### Anexo G. Ejemplo completo de una HU

Recorre la HU-001 de la corrida E1c, «Iniciar sesión con correo y contraseña» (ITZINV-12 en Jira), por todos los artefactos que Loom generó para ella: la especificación, los casos de prueba, los paquetes de trabajo con sus Pull Requests, la primera revisión de cada paquete y el resultado de las pruebas de humo. Los textos son los que produjo Loom; solo se cambió el formato. Fuente: `evidencia/corrida-E1c-2026-09-21/datos/`.

### G.1 Especificación (spec.md)

Encabezado del archivo:
CODIGO:
id: HU-001
clasificacion: hu
fuente_tipo: jira
fuente_ref: ITZINV-12
fase: especificada
estado: pendiente
fecha_descubrimiento: 2026-09-21
tiene_supuestos: true
prototipo_ref: null
depende_de: []
FIN-CODIGO

*Iniciar sesión con correo y contraseña*
Como usuario del sistema quiero iniciar sesión con mi correo y contraseña para acceder únicamente a la información que me corresponde. Intención de negocio: autenticar la identidad del usuario y, con ella, establecer una sesión que limite el acceso a los datos y funciones propios de su cuenta/rol (autenticación + base para la autorización).
*Criterios de aceptación explícitos*
- Dado un usuario registrado con credenciales válidas (correo y contraseña), cuando envía el formulario de inicio de sesión, entonces el sistema lo autentica y le da acceso al sistema.
- Dado un usuario autenticado, cuando navega o consulta información, entonces solo puede ver/acceder a la información que le corresponde (la asociada a su cuenta/permisos), y no la de otros usuarios.
*Criterios de aceptación inferidos*
- Dado un correo o contraseña incorrectos, cuando intenta iniciar sesión, entonces se rechaza el acceso con un mensaje genérico que no revela cuál de los dos datos falló (evita enumeración de usuarios).
- Dado un correo no registrado, cuando intenta iniciar sesión, entonces recibe el mismo mensaje que con contraseña incorrecta.
- Dado que el correo o la contraseña están vacíos, o el correo tiene formato inválido, cuando intenta enviar, entonces se muestra una validación de campo y no se procesa la autenticación.
- Dado que un usuario intenta acceder directamente a un recurso de otro usuario (por URL o API), cuando la solicitud llega, entonces el servidor la rechaza (403/404) y la autorización se valida en backend, no solo ocultando elementos en la interfaz.
- Dado un usuario no autenticado o con sesión expirada, cuando intenta acceder a una página o endpoint protegido, entonces es redirigido al inicio de sesión / recibe 401.
- Las contraseñas nunca se almacenan ni se transmiten en texto plano (hash con sal en almacenamiento, tráfico por HTTPS) y no aparecen en logs; el campo de contraseña se enmascara.
- Dado un inicio de sesión exitoso, cuando se crea la sesión/token, entonces este tiene vigencia limitada y se invalida al cerrar sesión.
- Dados varios intentos fallidos consecutivos, cuando se supera un umbral, entonces se aplica una protección contra fuerza bruta (bloqueo temporal, retardo o captcha).
- La comparación del correo no distingue mayúsculas/minúsculas y se ignoran espacios al inicio o final.
- Dado que el servicio de autenticación no está disponible, cuando el usuario intenta iniciar sesión, entonces ve un mensaje de error amigable sin perder lo escrito en el correo.
- Se registran los intentos de inicio de sesión (exitosos y fallidos) para auditoría.
*Supuestos y vacíos identificados*
- No se define el modelo de autorización (por rol, por propietario de los datos, por organización/tenant). 'Información que me corresponde' admite varias interpretaciones; para cerrarlo hace falta la matriz de roles/permisos y qué datos ve cada uno.
- Se asume que el registro de usuarios ya existe o se gestiona en otra HU; el alcance no incluye registro, activación de cuenta ni verificación de correo.
- Fuera de alcance salvo confirmación: recuperación/restablecimiento de contraseña, 'recordarme', cierre de sesión como funcionalidad explícita, MFA/2FA e inicio de sesión social/SSO.
- Se desconocen las políticas de bloqueo (número de intentos, duración), la duración de la sesión y las reglas de complejidad de contraseña; los criterios inferidos las mencionan solo de forma genérica y requieren valores definidos por negocio/seguridad.
- No se especifica el comportamiento para cuentas desactivadas o bloqueadas (mensaje y si se distingue del error de credenciales).
- Se desconoce la plataforma (web, móvil, ambas) y a dónde se redirige tras un login exitoso.
*Notas*
La HU mezcla dos preocupaciones: autenticación (login) y autorización/aislamiento de datos ('únicamente la información que me corresponde'). Se recomienda confirmar si la segunda se cubre aquí o en una HU aparte de control de acceso; si es aparte, esta HU quedaría acotada a autenticación y creación de sesión. Ausencia de criterios de aceptación en la fuente: los explícitos se derivaron del texto de la narrativa.

### G.2 Casos de prueba (test-cases.md)

La *skill* 2 generó 14 casos; cada uno guarda el criterio del que deriva (apartado 5.2.15).

TABLA: Casos de prueba de la HU-001 de E1c
| Caso | Escenario | Rol | Resultado esperado |
| TC-001 | Given un usuario registrado con correo y contraseña válidos y la página de login abierta. When ingresa ambos datos y pulsa 'Iniciar sesión'. Then se procesa la autenticación. | usuario_final | El usuario es redirigido a la página principal/dashboard, se muestra su nombre o indicador de sesión activa y no aparece mensaje de error. |
| TC-002 | Given usuario_final A autenticado y existen datos de usuario B. When navega por las secciones y listados del sistema (perfil, pedidos, etc.). Then se revisa la información mostrada. | usuario_final | Solo se muestran datos asociados a la cuenta de A; ningún dato de B aparece en pantallas, listados ni búsquedas. |
| TC-003 | Given un correo registrado y la página de login. When ingresa el correo correcto con una contraseña incorrecta y envía el formulario. Then se evalúa la respuesta. | invitado | Se rechaza el acceso, permanece en login y se muestra un mensaje genérico (p. ej. 'Correo o contraseña incorrectos') sin indicar cuál dato falló. |
| TC-004 | Given un correo que no existe en el sistema. When ingresa ese correo con cualquier contraseña y envía. Then se compara el mensaje con el del caso de contraseña incorrecta. | invitado | El mensaje mostrado es idéntico en texto (y sin diferencias apreciables de estructura) al de contraseña incorrecta; el acceso es rechazado. |
| TC-005 | Given la página de login. When intenta enviar (a) con correo vacío, (b) con contraseña vacía, (c) con correo 'usuario@' de formato inválido. Then se observa la interfaz y las peticiones de red. | invitado | Para cada caso se muestra un mensaje de validación junto al campo correspondiente, no se envía petición de autenticación y no se inicia sesión. |
| TC-006 | Given usuario_final A autenticado y el identificador de un recurso de B. When escribe manualmente la URL del recurso de B en el navegador y también solicita el endpoint de API correspondiente con la sesión de A. Then se revisa la respuesta. | usuario_final | El servidor responde 403 o 404 en ambos casos, no se muestran datos de B y se ve una página/mensaje de acceso denegado o no encontrado. |
| TC-007 | Given un visitante sin sesión. When navega directamente a una URL protegida y consulta un endpoint protegido sin credenciales. Then se observa la respuesta. | invitado | La página redirige al login y el endpoint responde 401; no se muestra contenido protegido. |
| TC-008 | Given usuario_final autenticado cuya sesión/token ha expirado (esperando la vigencia o invalidando la cookie). When recarga o navega a una página protegida. Then se observa el resultado. | usuario_final | Es redirigido a la página de inicio de sesión y las llamadas a la API responden 401; no se muestra contenido protegido. |
| TC-009 | Given la página de login cargada. When escribe una contraseña en el campo y envía el formulario, inspeccionando el campo y el tráfico de red. Then se verifica el enmascaramiento y el protocolo. | invitado | El campo es type=password (caracteres enmascarados), la URL de la página y la petición usan HTTPS, y la contraseña no aparece en la URL ni en query params. (El hash con sal y los logs se verifican por revisión de backend fuera de UI.) |
| TC-010 | Given usuario_final autenticado con cookie/token de sesión. When pulsa 'Cerrar sesión' y luego intenta volver a una página protegida con el botón Atrás o reutilizando el token anterior. Then se observa el acceso. | usuario_final | La sesión se cierra, se redirige al login y el token anterior es rechazado (401); la cookie/token tiene fecha de expiración definida. |
| TC-011 | Given un correo registrado. When realiza intentos fallidos consecutivos por encima del umbral configurado (p. ej. 5) y luego intenta con la contraseña correcta. Then se observa la respuesta. | invitado | Tras superar el umbral se muestra bloqueo temporal, retardo o captcha y el intento con contraseña correcta durante el bloqueo no concede acceso; el mensaje no revela si la cuenta existe. |
| TC-012 | Given un usuario registrado con correo 'usuario@ejemplo.com'. When ingresa '  USUARIO@Ejemplo.COM  ' con su contraseña válida y envía. Then se evalúa el resultado. | usuario_final | La autenticación es exitosa y accede al sistema como el mismo usuario. |
| TC-013 | Given la página de login y el servicio de autenticación simulado como caído (interceptando la petición con error 503/timeout). When escribe correo y contraseña y envía. Then se observa la interfaz. | invitado | Se muestra un mensaje amigable de error temporal (sin detalles técnicos), el campo de correo conserva el valor escrito y no se inicia sesión. |
| TC-014 | Given un usuario registrado. When realiza un inicio de sesión fallido y luego uno exitoso. Then un admin consulta el registro de auditoría. | admin | El registro de auditoría contiene ambas entradas con fecha/hora, correo, resultado (fallido/exitoso) y origen; ninguna entrada contiene la contraseña. |

### G.3 Paquetes de trabajo

*PT-01, Backend: modelo de datos, login JWT, /users/me y auditoría* (capa backend). Pull Request: https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/pull/37. Casos que cubre: TC-001, TC-002, TC-003, TC-004, TC-006, TC-007, TC-009, TC-010, TC-011, TC-012, TC-014. Depende de: BASE/PT-02, BASE/PT-01, BASE/PT-05.
Entregables:
- backend/src/main/resources/db/migration/V1__auth.sql (tablas user, role, user_role, revoked_token, password_reset_token, auth_event + seed inicial de roles y usuarios)
- config/SecurityConfig (stateless, CORS al origen del frontend, BCrypt, @EnableMethodSecurity), config/JwtProperties, config/OpenApiConfig (bearerAuth global)
- user/domain (User, Role), user/repository (UserRepository, RoleRepository), user/mapper (UserMapper MapStruct)
- auth/domain (AuthEvent), auth/repository (AuthEventRepository, RevokedTokenRepository)
- auth/service (AuthService, JwtService con jti y expiración 15 min, LoginAttemptService con rate limit/bloqueo temporal, AuthEventService), JwtAuthenticationFilter
- auth/web (AuthController POST /api/v1/auth/login con LoginRequest/LoginResponse records validados con Bean Validation), user/web (UserController GET /api/v1/users/me con UserResponse)
- common/error (@RestControllerAdvice con ProblemDetail: 400 validación, 401 mensaje genérico, 429 fuerza bruta)
- Swagger/OpenAPI documentado (@Tag, @Operation, @ApiResponse, @Schema) para POST /api/v1/auth/login (público, @SecurityRequirements vacío) y GET /api/v1/users/me
- Pruebas JUnit 5: AuthServiceTest, JwtServiceTest, LoginAttemptServiceTest, AuthControllerTest y UserControllerTest (slice), pruebas de filtro JWT (401 sin token/expirado, acceso solo a /me propio, 403/404 a recursos ajenos), prueba de que la contraseña no aparece en logs ni respuestas
- backend/README.md actualizado (variables JWT_SECRET, JWT_ACCESS_TTL_MINUTES, CORS_ALLOWED_ORIGINS, DB_*, seed de usuarios, ejecución de pruebas, Swagger en /swagger-ui.html)

*PT-02, Frontend: pantalla de login, sesión, interceptor y guard* (capa frontend). Pull Request: https://github.com/CarlosSotoGarcia/loom-piloto-e1c-claude-cli/pull/38. Casos que cubre: TC-001, TC-002, TC-003, TC-004, TC-005, TC-007, TC-008, TC-009, TC-013. Depende de: BASE/PT-04, BASE/PT-01, BASE/PT-05, PT-01.
Entregables:
- src/app/core/auth.service.ts (BehaviorSubject de sesión, login, carga de /users/me), core/token.storage.ts (sessionStorage), core/auth.interceptor.ts (Bearer + 401 limpia sesión y redirige a /login), core/auth.guard.ts
- src/app/features/auth/login (componente standalone con formulario reactivo, PrimeNG + Tailwind, validación de correo obligatorio/formato y contraseña obligatoria, campo password enmascarado, mensaje genérico de credenciales inválidas, mensaje amigable ante 429 o servicio no disponible conservando el correo escrito)
- src/app/features/home (pantalla protegida inicial con datos de /users/me, carga lazy)
- src/app/app.routes.ts y app.config.ts (rutas /login y home protegida por guard, registro del interceptor), src/environments/
- Pruebas Jest: auth.service.spec, auth.interceptor.spec, auth.guard.spec, login.component.spec, home.component.spec
- frontend/README.md actualizado (API_BASE_URL, ejecución de lint y jest)

### G.4 Primera revisión de cada paquete

*PT-01*: veredicto «con observaciones», 8 observaciones. Resumen del revisor: El PR implementa login JWT, /users/me, rate limit, auditoría, Swagger y pruebas amplias, en general alineado con la arquitectura. Hay defectos que conviene corregir antes de fusionar: la protección de fuerza bruta permite bloquear a cualquier usuario por correo (DoS) y falta tabla/comprobación coherente en algunos puntos. Además, el filtro JWT se registra antes de las reglas de CORS/CSRF y el seed de contraseñas por variable de entorno es riesgoso si se usa en producción.
- mayor, seguridad, `backend/src/main/java/com/itz/inventarios/auth/service/AuthService.java:45`: El bloqueo por fuerza bruta se clave solo por correo. Cualquier atacante puede provocar el bloqueo de 15 min de una cuenta legítima con 5 intentos fallidos (denegación de servicio dirigida). Además, el bloqueo se comprueba antes de validar credenciales, y no hay límite por IP.
- mayor, seguridad, `backend/src/main/java/com/itz/inventarios/user/service/SeedUserPasswordInitializer.java:30`: El SeedUserPasswordInitializer es un @Component sin @Profile: si SEED_PASSWORD se define en producción, todas las cuentas sembradas (incluido ADMIN) quedan con una contraseña conocida. Solo la documentación dice que no se defina en prod.
- mayor, seguridad, `backend/src/main/java/com/itz/inventarios/auth/web/AuthController.java:50`: Se usa http.getRemoteAddr() como IP de auditoría. Detrás de Cloud Run/proxy será siempre la IP del balanceador, por lo que auth_event.ip pierde valor (TC-014 pide origen).
- menor, criterio aceptacion, `backend/src/main/java/com/itz/inventarios/auth/service/AuthService.java:47`: Con bloqueo activo se registra LOGIN_FAIL con userId null y sin distinguir que fue por bloqueo; la auditoría pierde el usuario y el motivo.
- menor, buenas practicas, `backend/src/main/java/com/itz/inventarios/config/SecurityConfig.java:60`: JwtAuthenticationFilter se añade con new dentro de la cadena; es correcto para evitar doble registro, pero se registra antes de configurar csrf/cors y el filtro pasa a ejecutarse también en preflight OPTIONS sin necesidad.
- menor, buenas practicas, `backend/src/main/java/com/itz/inventarios/user/domain/User.java:57`: Uso de @ManyToMany EAGER sobre roles en cada carga de usuario, incluido cada /me. Aceptable ahora, pero costoso al crecer.
- menor, pruebas, `backend/src/test/java/com/itz/inventarios/auth/AuthFlowIntegrationTest.java:118`: Los tests de integración dependen del estado en memoria compartido de LoginAttemptService entre tests (correos únicos mitigan). La prueba de logs solo verifica el mensaje formateado, no el contenido de argumentos ni excepciones.
- menor, buenas practicas, `backend/src/main/java/com/itz/inventarios/user/web/UserController.java:36`: Se usa el nombre completo io.swagger...Schema inline en lugar de import; y falta documentar respuesta 403 y la ausencia de bearer en la operación.

*PT-02*: veredicto «con observaciones», 5 observaciones. Resumen del revisor: El PT-02 implementa el login, la sesión, el interceptor, el guard y el home con buena cobertura de pruebas, y cubre en lo esencial los TCs asociados. Hay tres defectos reales: el guard solo comprueba que exista un token (no su validez ni caducidad), no se limpia el token en un 401 del login y el interceptor decide la exclusión con `endsWith`. Ninguno es bloqueante, pero conviene corregir los dos primeros antes de fusionar.
- mayor, criterio aceptacion, `frontend/src/app/core/auth.guard.ts:8`: El guard solo comprueba que exista un token en sessionStorage (`isAuthenticated()` = token !== null). Un token caducado o inválido deja entrar a /home; solo se redirige cuando /users/me responde 401. TC-008 (sesión expirada) depende de que esa llamada se dispare y se maneje. Además `AuthService.loadProfile()` no se invoca desde el guard, y HomeComponent solo lo llama si `currentUser` es null, así que el flujo funciona solo por accidente.
- menor, criterio aceptacion, `frontend/src/app/core/auth.service.ts:49`: `expiresAt` de LoginResponse se descarta: no se persiste ni se usa. Sin ello el cliente no conoce la vigencia limitada de la sesión.
- menor, buenas practicas, `frontend/src/app/core/auth.interceptor.ts:24`: La exclusión del 401 del login usa `req.url.endsWith(LOGIN_PATH)`, lo que es frágil (p. ej. coincidiría con cualquier URL que termine igual).
- menor, pruebas, `frontend/src/app/features/auth/login/login.component.spec.ts:40`: No hay prueba de que un login exitoso no vuelva a enviar mientras `loading` o de que el botón se deshabilite; tampoco se prueba el caso 4xx distinto de 401 (p. ej. 400/403), que hoy se clasifica como credenciales inválidas.
- menor, buenas practicas, `frontend/src/app/features/auth/login/login.component.ts:98`: El componente usa propiedades mutables (`loading`, `error`) y suscripción manual sin `takeUntilDestroyed`; en Angular 18 son preferibles signals y limpiar la suscripción. Además el mensaje de 429 no se distingue de un 5xx en el TC-013 más allá del texto, lo cual es correcto, pero el `Validators.email` cast con `{ value } as AbstractControl` es un truco de tipos poco legible.

### G.5 Pruebas de humo

La corrida de pruebas de humo de la HU-001 ejecutó 14 casos contra la aplicación desplegada: 11 aprobados, 0 fallidos y 3 bloqueados.

TABLA: Resultado de las pruebas de humo de la HU-001 de E1c
| Caso | Rol | Resultado | Motivo |
| TC-001 | usuario_final | Aprobado | — |
| TC-002 | usuario_final | Aprobado | — |
| TC-003 | invitado | Bloqueado | El caso exige un correo registrado con una contraseña incorrecta, pero no hay cuenta de prueba. Un correo inventado no permite comprobar que el mensaje no revela qué dato falló. La página de login sí carga, con campos Correo y Contraseña. · Script: AssertionError: Locator expected to be visible Actual value: None Error: element(s) not found Call log: |
| TC-004 | invitado | Aprobado | Con un correo inexistente el sistema rechazó el acceso, se quedó en /login y mostró la alerta «Correo o contraseña incorrectos.». Es un mensaje genérico que no revela si el correo existe. No había cuenta de prueba, así que no pude ejecutar el caso de contraseña incorrecta con un correo real para compararlo directamente. Lo doy por idéntico porque el texto es genérico, pero esa comparación queda sin confirmar. |
| TC-005 | invitado | Aprobado | — |
| TC-006 | usuario_final | Aprobado | — |
| TC-007 | invitado | Aprobado | Sin sesión, /dashboard y /api/users redirigieron a /login («Iniciar sesión» visible) y no se mostró contenido protegido. El código HTTP 401 no se puede ver desde el navegador. Solo se observó la redirección al login, así que el 401 queda sin confirmar. |
| TC-008 | usuario_final | Aprobado | — |
| TC-009 | invitado | Aprobado | El campo «Contraseña» coincide con el selector input[type=password] (el clic sobre él funcionó), por lo que está enmascarado. La página está en https://inventarios-web-118746543308.us-central1.run.app/login, es decir, HTTPS, y la URL no tiene query params ni contiene «TextoPrueba123» tras enviar el formulario. No se inspeccionó el tráfico de red directamente, y el hash con sal y los logs quedan para revisión de backend fuera de UI. |
| TC-010 | usuario_final | Aprobado | — |
| TC-011 | invitado | Bloqueado | El caso requiere un correo registrado (y su contraseña correcta) para probar el bloqueo tras intentos fallidos, pero el rol invitado no tiene cuenta de prueba disponible. No se puede ejecutar sin credenciales válidas. Solo se observó el formulario de login con Correo, Contraseña y enlace de recuperación. · Script: AssertionError: Locator expected to be visible Actual value: None Error: element(s) not found Call log: |
| TC-012 | usuario_final | Aprobado | — |
| TC-013 | invitado | Bloqueado | La página de login carga, pero el caso exige escribir correo y contraseña y no hay usuario configurado para el rol invitado. Tampoco se dispone de forma de interceptar la petición de autenticación con un 503. Por eso no se pudo comprobar el mensaje de error, la conservación del correo ni que no se inicie sesión. · Script: AssertionError: Locator expected to be visible Actual value: None Error: element(s) not found Call log: |
| TC-014 | admin | Aprobado | — |
