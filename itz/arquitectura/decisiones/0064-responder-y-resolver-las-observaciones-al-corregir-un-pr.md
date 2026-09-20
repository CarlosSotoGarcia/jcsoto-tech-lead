# ADR-0064: Responder cada observación y resolver las conversaciones al corregir un PR

## Estado

Aceptada. Amplía la corrección de la skill 07 ([ADR-0049](0049-skill-07-revision-de-codigo-y-correcciones.md)).

## Contexto

Al corregir un PR, Loom subía el commit y borraba las observaciones de su registro, pero en GitHub las conversaciones de la revisión quedaban abiertas y sin respuesta: quien revisa no sabía qué se cambió para atender cada una.

## Decisión

1. **Guardar el comentario.** Al publicar la revisión, cada observación con archivo y línea guarda el id de su comentario en línea de GitHub (`comentario_id`).
2. **Responder una por una.** Tras subir la corrección, una llamada a la IA del Proyecto recibe las observaciones numeradas, el resumen de quien corrigió y **el diff del commit de corrección**, y responde cada observación con qué se cambió y un estado: `corregida`, `parcial` o `no_corregida`. Debe basarse solo en el diff. Una observación sin respuesta cuenta como no corregida.
3. **Dónde se publica.** La respuesta se pone en el hilo de cada comentario en línea y, además, un comentario general del PR lista todas las observaciones (incluidas las que no tenían ubicación en el código) con su estado.
4. **Resolver solo lo corregido.** Las conversaciones con estado `corregida` se marcan como resueltas en GitHub (GraphQL); las `parcial` y `no_corregida` quedan abiertas para la siguiente revisión.
5. **No bloquea.** Si algo de esto falla (permisos, red, líneas fuera del diff), la corrección ya está subida y el paso avisa «no se pudieron responder las observaciones en el PR».

## Consecuencias

- Una llamada más a la IA por corrección (pequeña: observaciones y diff).
- La respuesta puede equivocarse al valorar el diff; por eso solo se resuelven las que declara corregidas y la revisión siguiente vuelve a comprobar todo.
- Las observaciones sin ubicación (por ejemplo, supuestos sin confirmar) solo aparecen en el comentario general.
- Probado en un PR desechable de GitHub: hilos respondidos, uno resuelto y otro abierto. No se ha corrido con una corrección real del agente.
