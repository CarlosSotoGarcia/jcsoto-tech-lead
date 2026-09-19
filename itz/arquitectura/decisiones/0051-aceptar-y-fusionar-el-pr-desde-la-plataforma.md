# ADR-0051: Aceptar (fusionar) el PR de un paquete desde la plataforma

## Estado

Aceptada. Completa el ciclo de [ADR-0046](0046-skill-06-generacion-de-codigo-agente-con-tdd.md) y
[ADR-0049](0049-skill-07-revision-de-codigo-y-correcciones.md): hasta ahora la fusión se hacía a mano en GitHub y luego se
pulsaba «Sincronizar PRs».

## Decisión

1. **La persona acepta el PR desde la lista de paquetes.** Cada paquete con PR abierto (`en_revision`, `con_observaciones` o
   `aprobado`) tiene un botón «Fusionar». Abre una confirmación; si el paquete no está `aprobado` (o tiene observaciones), la
   confirmación lo advierte, pero la fusión sigue siendo decisión de la persona (ADR-0015).
2. **Cómo se fusiona.** `POST /proyectos/{id}/paquetes/fusionar?grupo=&pt=` usa la cuenta de desarrollo (ADR-0043) para fusionar el PR
   en GitHub con *squash* y borrar la rama (mejor esfuerzo). Si GitHub no lo permite (conflictos, revisiones o checks requeridos), se devuelve
   el motivo. El paquete pasa a `fusionado` y `paquetes/PT-0N.md` se actualiza, lo que libera a los paquetes que dependen de él (ADR-0029).
3. **Sincronizar PRs sigue existiendo** para fusiones hechas directamente en GitHub.
4. El «siguiente paso recomendado» ofrece «Fusionar PR» cuando hay un paquete aprobado.

## Consecuencias

- La cuenta de desarrollo necesita permiso de escritura sobre el repositorio (ya lo verifica «Probar conexión»); si la rama base está protegida,
  la fusión puede rechazarse y habrá que hacerla en GitHub.
- Se usa *squash*: la historia de la rama base queda con un commit por paquete.

## Pendiente

- Elegir el método de fusión por Proyecto (squash, merge, rebase).
- Fusionar en lote los paquetes aprobados y respetar el orden de dependencias.
