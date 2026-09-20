# ADR-0074: Avanzar con una HU de punta a punta

## Estado

Aceptada. Orquesta las skills de generación de código ([ADR-0046](0046-skill-06-generacion-de-codigo-agente-con-tdd.md)), revisión y corrección ([ADR-0049](0049-skill-07-revision-de-codigo-y-correcciones.md)) y la fusión de PR ([ADR-0051](0051-aceptar-y-fusionar-el-pr-desde-la-plataforma.md)), y dispara el release automático ([ADR-0072](0072-release-automatico-al-aceptar-un-pr.md)).

## Contexto

Completar una HU obligaba a repetir a mano, por cada paquete, cuatro acciones (generar, revisar, corregir, fusionar). En el piloto se resolvió con un script externo. El botón «Avanzar con esta HU» solo generaba el siguiente paquete.

## Decisión

1. **«Avanzar con esta HU» abre una confirmación** donde se elige el número de rondas de corrección por paquete (0 a 3, por omisión 1) y si se acepta el PR aunque queden observaciones bloqueantes (apagado por omisión).
2. **Un solo proceso en vivo** (`POST /hus/avanzar-hu`, SSE) recorre los paquetes pendientes de la HU en orden de dependencias. Por paquete: genera el código y abre el PR, lo revisa, aplica hasta N correcciones (revisando otra vez después de cada una; se detiene antes si la revisión aprueba) y fusiona el PR. Si una corrida se corta, la siguiente retoma el paquete que ya tiene PR.
3. **Se detiene ante lo bloqueante.** Si tras las rondas queda una observación bloqueante y no se marcó aceptar con bloqueantes, la corrida se detiene en ese paquete, deja el PR abierto y explica qué hacer. No se avanza a los paquetes dependientes con un bloqueante sin decidir.
4. **Al fusionar el último paquete de la HU se lanza el release automático**, si el proyecto lo tiene activo.
5. **Tope de 3 rondas** por paquete: más allá se pide criterio humano; también acota el costo.

## Consecuencias

- Una HU completa puede costar varias decenas de dólares y horas de agente (en el piloto, unos 14.8 USD por HU con dos paquetes y una ronda), por eso la confirmación muestra cuántos paquetes se van a completar.
- La corrida vive en la conexión SSE: si se cierra la pestaña, se corta; se retoma al volver a avanzar.
- La regla de detenerse ante bloqueantes corrige la práctica del piloto, donde el script fusionó paquetes con una observación bloqueante abierta.

## Pendiente

- Ejecutar la corrida como tarea en segundo plano con estado consultable, para que sobreviva al cierre de la pestaña.
