# ADR-0083: Procesos concurrentes con reglas de exclusión

## Estado

Aceptada e implementada. Amplía la actividad visible del [ADR-0080](0080-actividad-en-curso-visible-desde-cualquier-sesion.md).

## Contexto

Hoy el panel de actividad muestra un solo proceso por Proyecto y bloquea cualquier otro mientras corre uno. Un release o la generación de código de una HU no debería impedir, por ejemplo, especificar otra HU.

## Decisión

1. **Varios procesos a la vez por Proyecto.** El servidor registra cada proceso (skill, HUs sobre las que trabaja, estado `en_cola`, `corriendo`, `terminada`, `error` o `rechazada`, y sus eventos) y `GET /hus/actividad` devuelve la lista. El panel de actividad muestra una pestaña por proceso y el registro del seleccionado, sin importar quién lo lanzó.
2. **Alcance por proceso.** Cada endpoint declara sobre qué trabaja: una HU (`avanzar-hu`, generación, revisión y corrección de código, smoke, diagnóstico, fixes, cambios), las HUs sin casos de prueba (`generar-tcs`) o todo el Proyecto (arquitectura, descomponer, release, y lo que no indica HU).
3. **Reglas de exclusión, aplicadas en el servidor:**
   - Sobre la misma HU, o sobre todo el Proyecto, no pueden coincidir dos procesos: el segundo **se rechaza** al momento con el motivo (`ya está corriendo sobre lo mismo`).
   - Sobre HUs distintas sí pueden correr juntos (por ejemplo, casos de prueba de HU-005 mientras se construye HU-004).
   - **El release es exclusivo:** espera en cola a que terminen los demás procesos y, mientras corre, los demás esperan en cola. Un release en espera tiene prioridad sobre los procesos nuevos, para que no se quede sin turno.
4. **Cola visible:** la petición queda abierta y el panel muestra «En cola: …» con el motivo; al liberarse el turno arranca sola. El release que lanza Loom al completar una HU (ADR-0082) respeta la misma regla.
5. **La interfaz deshabilita «Avanzar con esta HU» y «Probar HU» solo para la HU ocupada**, no para todo el Proyecto.

## Consecuencias

- El registro vive en la memoria del backend: al reiniciarlo se pierde el historial de procesos, aunque un proceso lanzado por API sigue y termina en el servidor.
- Se conserva una ventana de los últimos 12 procesos por Proyecto y 400 eventos por proceso.
- El proceso que se rechaza no queda en la cola: hay que volver a lanzarlo cuando termine el otro.

## Verificación

Las reglas se probaron con un simulador (misma HU rechazada, HU distinta en paralelo, release que espera y bloquea, prioridad del release en espera) y la interfaz con datos simulados de cuatro procesos a la vez. No se ha probado todavía con dos procesos reales concurrentes.

## Pendiente

- Persistir el registro en Mongo y mostrar el historial de procesos.
- Cancelar un proceso desde el panel.
