# ADR-0066: Propagar un cambio de HU a los casos de prueba, el código y el smoke testing

## Estado

Aceptada. Completa el [ADR-0065](0065-agregar-hus-por-etapas-con-historial-de-versiones.md) sobre HUs que cambian después de haber avanzado.

## Contexto

Si cambia la especificación de una HU, sus casos de prueba quedan atrás; si cambian los casos, el código que se planeó con los anteriores y el script de smoke testing generado a partir de ellos también. Loom no lo avisaba: al regenerar la especificación la HU volvía a «especificada» conservando los casos viejos, los paquetes seguían apuntando a casos que ya no existen y la regresión del smoke testing reutilizaba un script de casos anteriores, bloqueando en silencio los casos nuevos.

## Decisión

1. **Qué se detecta** (`GET /hus/desactualizados`, calculado, sin estado propio), por HU:
   - **Casos de prueba desactualizados:** la HU está en «especificada» y ya tiene casos (su especificación cambió y no se regeneraron).
   - **Código desactualizado:** algún paquete se planeó con una versión de los casos de prueba anterior a la vigente.
   - **Smoke desactualizado:** la última corrida se hizo con casos anteriores.
2. **Versión funcional de los casos de prueba.** Se cuenta la última versión de `test-cases.md` que cambió su contenido; el diagnóstico de avance (que solo agrega la cobertura) no cuenta. Cada paquete (y cada fix) guarda con qué versión se planeó (`tcs_version`) y cada corrida de smoke, con cuál se hizo. Lo anterior al registro se considera hecho con la versión 1.
3. **Qué cambió.** Cada versión nueva de los casos guarda la diferencia con la anterior por criterio de aceptación de origen (agregados, eliminados, con casos distintos), porque los ids TC-00N se reasignan al regenerar.
4. **Avisos.** Detalle de la HU (banner con lo pendiente y el resumen del cambio), lista de HUs (marcas «Desactualizados», «Código por actualizar», «Smoke por regenerar») y paso recomendado del proyecto, con prioridad sobre los demás.
5. **Smoke testing.** La regresión con el script guardado se niega si los casos cambiaron desde esa corrida y pide generar el script de nuevo, en lugar de omitir los casos nuevos.
6. **Regenerar los casos** ya funciona (solo de las HUs en «especificada»); regenerar el script de smoke, también. **Actualizar el código no se automatiza todavía:** el aviso lo señala y el ajuste se hace generando o corrigiendo paquetes a mano.

## Consecuencias

- Un cambio de especificación ya no pasa inadvertido en las etapas siguientes.
- La arquitectura solo sabe qué HUs consideró (ADR-0065), no si cambió el contenido de alguna; un cambio de fondo en una HU puede requerir regenerarla a mano.
- Los paquetes ya fusionados no se modifican solos: el aviso no dice qué archivos tocar.

## Pendiente

- Generar paquetes de cambio a partir de la diferencia de casos de prueba, con el mismo ciclo de código, revisión y smoke que un fix (ADR-0061).
- Marcar también la arquitectura cuando cambia el contenido de una HU.
