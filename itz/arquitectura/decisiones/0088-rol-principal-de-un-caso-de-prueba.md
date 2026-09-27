# ADR-0088: El rol de un caso de prueba se resuelve por su actor principal

## Estado

Aceptada. Ajusta la asignación de cuentas de prueba por rol del smoke testing ([ADR-0016](0016-cuentas-de-prueba-por-rol-para-ejecucion-de-tcs.md)).

## Contexto

Cada caso de prueba trae un `rol_requerido` que la skill 02 escribe en texto libre, y el smoke testing buscaba la cuenta de prueba con ese texto exacto (normalizado). En el piloto E1c (Inventarios) los casos usaron solo tres roles (`usuario_final`, `invitado`, `admin`) y todos coincidieron con las cuentas configuradas.

En el piloto E3c (Agenda Taller), los 101 casos usaron 32 roles distintos: además de nombres simples (`cliente`, `usuario_final`, `personal_interno`, `cliente_bloqueable`), combinaciones que describen varios actores y precondiciones, como «invitado (sin sesión); admin para verificar» o «recepcion (precondición); invitado→cliente; admin (auditoría)». Con tres cuentas configuradas (`admin`, `cliente`, `usuario_inactivo`), la primera corrida de smoke de la HU-001 dejó 33 de 35 casos bloqueados por «no hay cuenta para el rol», incluidos casos de invitado que no necesitan ninguna.

## Decisión

1. **Actor principal.** El rol se resuelve primero por el texto completo y, si no hay cuenta, por su actor principal: lo que va antes del primer paréntesis, punto y coma, coma, `+`, flecha o multiplicador (`x2`). «invitado (sin sesión); admin para verificar» → `invitado`.
2. **Roles públicos.** Un caso no requiere cuenta si su texto completo o su actor principal es un rol público (`invitado`, `anonimo`, `publico`, `sin sesion`, `ninguno`…).
3. **Las cuentas siguen siendo por rol.** Si el actor principal no tiene cuenta, el caso queda bloqueado como antes, con el rol en el motivo. Configurar una cuenta por cada rol que usan los casos sigue siendo trabajo de la persona en la pestaña Implementación.

## Consecuencias

- En el E3c, con la regla nueva, 39 casos quedan como de invitado y el resto se reparte en ocho roles principales (`cliente`, `usuario_final`, `personal_interno`, `cliente_bloqueable`, `recepcion`, `admin`, `cuenta_inactiva`, `cuenta_pendiente_verificacion`); se configuró una cuenta para cada uno.
- Los actores secundarios del texto («admin para verificar») no reciben cuenta propia: el guion de smoke corre con una sola cuenta por caso. Los pasos de verificación que dependen de otro rol pueden quedar sin comprobar.
- Pendiente: que la skill 02 genere los casos con los roles configurados en el Proyecto (más `invitado`) en lugar de texto libre. Se deja fuera de este piloto para no cambiar la generación de casos entre escenarios del mismo experimento.
