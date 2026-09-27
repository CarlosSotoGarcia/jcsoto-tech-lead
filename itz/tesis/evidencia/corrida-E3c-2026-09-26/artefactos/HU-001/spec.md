---
id: HU-001
clasificacion: hu
fuente_tipo: jira
fuente_ref: IAT-2
fase: especificada
estado: pendiente
fecha_descubrimiento: 2026-09-26
tiene_supuestos: true
prototipo_ref: null
depende_de: []
---

# Autorregistro de cliente en el portal del taller con verificación de correo y vinculación a expediente existente

Como cliente del taller, quiero crear mi propia cuenta en el portal con mis datos de contacto, verificar mi correo y, si recepción ya me tenía registrado, quedar vinculado a mi expediente existente (sin duplicados), para agendar citas y dar seguimiento en línea a mis vehículos. Intención de negocio: pasar a autoservicio digital sin perder la calidad de los datos. Se busca evitar clientes duplicados entre el alta de recepción y el autorregistro, asegurar que el contacto sea real (correo verificado) y cumplir con la ley de protección de datos al registrar cuándo se aceptó el aviso de privacidad.

## Criterios de aceptación explícitos

- E1 – Registro exitoso: DADO que ingreso nombre(s), apellidos, correo, celular a 10 dígitos y contraseña válidos, y acepto el aviso de privacidad y los términos, CUANDO presiono "Crear cuenta", ENTONCES se crea la cuenta en estado "Pendiente de verificación" y recibo un correo con un enlace de verificación.
- E2 – Correo duplicado: DADO que el correo capturado ya tiene una cuenta en el sistema, CUANDO intento registrarme, ENTONCES no se crea otra cuenta, veo el mensaje "Este correo ya tiene una cuenta" y se me ofrece la opción de recuperar contraseña.
- E3 – Verificación de correo: DADO que recibí un enlace de verificación con menos de 24 h de emitido, CUANDO lo abro, ENTONCES mi cuenta pasa de "Pendiente de verificación" a "Activa" y puedo iniciar sesión.
- E4 – Cliente preexistente (por correo): DADO que recepción me dio de alta antes con el mismo correo, CUANDO completo mi registro, ENTONCES mi cuenta se vincula a mi expediente de cliente existente (no se crea un cliente nuevo) y veo mis vehículos ya registrados.
- RN – Política de contraseña: DADO que capturo una contraseña de menos de 8 caracteres, o sin al menos una mayúscula, una minúscula y un número, CUANDO intento crear la cuenta, ENTONCES el registro se rechaza y se indica qué regla no se cumple.
- RN – Vigencia del enlace: DADO que el enlace de verificación tiene más de 24 h de emitido, CUANDO lo abro, ENTONCES la cuenta no se activa y sigue en "Pendiente de verificación".
- RN – Vinculación por teléfono: DADO que recepción me dio de alta antes con el mismo teléfono celular, CUANDO completo mi registro, ENTONCES la cuenta se vincula al cliente existente en lugar de duplicarlo (ver supuestos sobre conflictos y seguridad).
- RN – Aviso de privacidad: DADO que acepto el aviso de privacidad y los términos, CUANDO se crea la cuenta, ENTONCES queda guardada la fecha (y hora) de aceptación ligada al cliente.
- RN – Campos obligatorios: DADO que falta cualquiera de estos datos (nombre(s), apellidos, correo, celular, contraseña o la aceptación del aviso y los términos), CUANDO intento crear la cuenta, ENTONCES no se permite el registro. WhatsApp es opcional.
- DoD – Las validaciones se aplican en frontend y backend, hay permisos por rol, se registra la auditoría del alta, la verificación y la vinculación, y se actualiza la documentación de la API.

## Criterios de aceptación inferidos

- El botón "Crear cuenta" no envía nada (o el backend rechaza la solicitud) si no están marcadas las casillas del aviso de privacidad y de los términos. Se muestra un mensaje junto a esas casillas.
- El correo se compara sin distinguir mayúsculas y minúsculas, y quitando espacios al inicio y al final, tanto para revisar si es único como para vincular. Por ejemplo, Juan@Mail.com y juan@mail.com son el mismo correo.
- Se valida el formato del correo. Si es inválido, se muestra un error en el campo y no se crea la cuenta.
- El celular solo acepta 10 dígitos numéricos (se quitan espacios y guiones al normalizarlo). Si tiene otra longitud o caracteres no numéricos, se rechaza con un mensaje en el campo.
- La contraseña se guarda con un hash seguro (por ejemplo bcrypt o argon2) y nunca en texto plano. Tampoco aparece en logs ni en la auditoría.
- La unicidad del correo también se valida en el backend y en la base de datos (restricción única), para que dos registros simultáneos con el mismo correo no creen dos cuentas.
- Una cuenta en "Pendiente de verificación" no puede iniciar sesión. Si lo intenta, ve un mensaje que le indica verificar su correo.
- El enlace de verificación se usa una sola vez: si se abre otra vez después de activar la cuenta, no hace ningún cambio y muestra un mensaje de "cuenta ya verificada" o lleva al inicio de sesión.
- Si el enlace es inválido o fue alterado (token inexistente), no se activa ninguna cuenta y aparece un mensaje genérico de enlace inválido.
- Si el enlace venció, el usuario ve un mensaje claro de "enlace expirado".
- La cuenta recibe el rol "Cliente", con acceso solo a su expediente, sus vehículos y sus citas. No puede ver datos de otros clientes.
- En la vinculación (E4), los vehículos y el historial existentes del cliente quedan asociados a la cuenta. Se ven después de verificar el correo, no antes.
- Si el registro coincide con un expediente existente, no se sobrescriben en silencio los datos que capturó recepción (nombre, teléfono). Cualquier diferencia se deja en la auditoría.
- La auditoría guarda el alta de la cuenta, la verificación, la vinculación a un expediente existente (con su identificador), la fecha de aceptación del aviso y el origen del registro (autorregistro en el portal).
- Si falla el envío del correo de verificación, la cuenta se crea igual en estado pendiente, el error queda en el log y el usuario tiene forma de pedir que se le reenvíe (ver supuesto sobre reenvío).
- Los datos capturados (salvo la contraseña) se conservan en el formulario cuando hay errores de validación, para no volver a escribirlos.

## Supuestos y vacíos identificados

- Vinculación solo por teléfono (correo distinto): la regla dice "mismo correo/teléfono", pero E4 solo cubre el correo. Falta definir qué pasa si el teléfono coincide y el correo no: ¿se vincula sin más, se pide confirmar con un código por SMS o WhatsApp, o recepción lo revisa? Vincular solo por teléfono podría dejar a alguien ver los vehículos de otra persona (números reciclados, teléfonos compartidos). También falta decidir qué correo queda en el expediente. Hace falta que lo decida el Product Owner, con el visto bueno de seguridad.
- Coincidencias contradictorias: el correo coincide con un cliente A y el teléfono con otro cliente B, o el teléfono coincide con varios expedientes. No hay regla. Supongo que no se vincula automáticamente y se crea un caso para que recepción lo revise; el PO debe confirmarlo.
- Diferencia entre "correo registrado" (E2) y "cliente preexistente" (E4): entiendo que E2 aplica solo si ya existe una cuenta del portal con ese correo, y E4 si el correo solo existe en un expediente que capturó recepción, sin cuenta. Si no se distinguen así, E2 bloquearía E4. Hay que confirmarlo con el PO.
- Momento de la vinculación: supongo que el expediente se vincula (o sus datos se muestran) solo después de verificar el correo, para que nadie vea los vehículos de otro solo por escribir su correo. E4 dice "cuando completo mi registro", así que hay que confirmar si "completar" incluye la verificación.
- Reenvío del enlace de verificación: la HU no lo menciona. Supongo que al abrir un enlace vencido o desde el login de una cuenta pendiente se puede pedir uno nuevo, que anula el anterior. Si no entra en el alcance, un usuario con el enlace vencido se queda bloqueado, porque el correo ya aparece como registrado. Hay que confirmarlo con el PO.
- Cuentas pendientes que nunca se verifican: no se dice si se borran o liberan después de cierto tiempo, ni si E2 aplica igual cuando la cuenta existente sigue pendiente. Supongo que E2 aplica y que se ofrece reenviar la verificación además de recuperar la contraseña.
- WhatsApp opcional: no queda claro si es una casilla de "este celular tiene WhatsApp" o un segundo número. Supongo que es una casilla sobre el mismo celular. Si es otro número, hay que definir si también se valida a 10 dígitos.
- Unicidad del teléfono: la HU no dice si el celular debe ser único entre cuentas del portal. Supongo que no se exige (pueden existir números compartidos), pero esto afecta cómo funciona la vinculación por teléfono.
- Aviso de privacidad y términos: no queda claro si es una casilla o dos, ni si hay que guardar la versión del documento aceptado además de la fecha. Supongo casillas separadas y que se guarda fecha, hora y versión de cada una, que es lo normal para cumplir con la LFPDPPP. Hay que confirmarlo con el área legal o el PO.
- Mensaje de E2 y enumeración de cuentas: el mensaje "Este correo ya tiene una cuenta" deja saber qué correos están registrados. Se acepta porque es un requisito explícito, pero seguridad podría pedir limitar intentos o poner un captcha. No se incluye en el alcance hasta que se confirme.
- Confirmar contraseña y reglas del nombre (caracteres permitidos, acentos, longitud máxima): no se especifican. Supongo un campo para confirmar la contraseña y que el nombre acepta letras con acentos, ñ, espacios y guiones, pero hay que validarlo con UX.

## Notas

Se clasifica como HU porque tiene comportamiento de usuario claro y verificable (4 escenarios más las reglas de negocio). Antes de pasarla a desarrollo, lo más urgente es cerrar la vinculación por teléfono y el momento de la vinculación: afectan el alcance y la seguridad, porque se podrían exponer los vehículos de otra persona. Luego hay que definir qué distingue a E2 de E4 y si entra el reenvío del enlace. Sugiero agregar escenarios explícitos para: enlace vencido, intento de login con la cuenta pendiente, vinculación por teléfono (con la regla que se decida) y coincidencias contradictorias. La DoD pide \"permisos por rol\", pero la HU solo implica el rol Cliente. Conviene confirmar si recepción o un administrador necesitan ver o gestionar las cuentas pendientes o las vinculaciones que quedaron en conflicto.
