# ADR-0062: La descomposición no acepta una HU sin paquetes

## Estado

Aceptada. Corrige un defecto de la skill 05 ([ADR-0045](0045-skill-05-descomposicion-desde-arquitectura-fundacional.md)) encontrado en el piloto de la tesis con el proveedor «Claude (cuenta normal)».

## Contexto

Con el proveedor de CLI, el modelo devolvió a veces `paquetes: []` para una HU (llamadas «correctas», pero con muy pocos tokens de salida). Loom lo tomó por bueno: la HU quedó en fase `descompuesta` con **0 paquetes** y el paso se reportó como exitoso. En el piloto ocurrió en 2 de 3 HUs de una misma corrida y la HU habría quedado sin implementarse sin ningún aviso.

## Decisión

1. Una respuesta sin paquetes para una HU con casos de prueba pendientes **no es válida**: se reintenta hasta 3 veces en total y cada reintento se registra en las métricas (`reintento`, motivo `sin_paquetes`).
2. Si tras los 3 intentos sigue vacía, la descomposición termina con un error claro que nombra la HU, en lugar de guardar una HU sin paquetes. Las HUs ya procesadas de esa ejecución se conservan.

## Consecuencias

- Una corrida puede tardar más cuando el modelo devuelve vacíos; el costo extra queda visible en las métricas.
- El fallo es intermitente y depende del proveedor: no cambia el contrato de la skill, solo impide el éxito silencioso.
- Una HU cuyos TCs están todos cubiertos por el diagnóstico (ADR-0060) sigue sin generar paquetes: ese caso no pasa por esta validación.

## Pendiente

- Aplicar la misma comprobación a la planeación del esqueleto (grupo BASE) y a los fixes (ADR-0061).
