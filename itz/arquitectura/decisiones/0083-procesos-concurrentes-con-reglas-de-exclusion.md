# ADR-0083: Procesos concurrentes con reglas de exclusión

## Estado

**Propuesta, sin implementar.** Amplía la actividad visible del [ADR-0080](0080-actividad-en-curso-visible-desde-cualquier-sesion.md).

## Contexto

Hoy el panel de actividad muestra un solo proceso por Proyecto y bloquea cualquier otro mientras corre uno. Un release o la generación de código de una HU no debería impedir, por ejemplo, especificar otra HU.

## Propuesta

1. **Varios procesos a la vez por Proyecto**, cada uno con su sección en el panel (pestañas con el nombre, la HU y el estado), su progreso y su registro.
2. **Reglas de exclusión, calculadas en el servidor:**
   - Una HU tiene un solo proceso a la vez sobre sus fases posteriores: mientras se genera, revisa, corrige o fusiona su código, no se puede volver a tocar su especificación, casos de prueba, arquitectura o paquetes.
   - Procesos sobre HUs distintas pueden correr juntos (por ejemplo, especificar y generar casos de prueba de HU-005 mientras HU-004 se construye).
   - Las fases del Proyecto entero (descubrir HUs, arquitectura, descomponer) esperan a que no haya procesos que dependan de ellas.
   - **El release es exclusivo:** mientras corre, nada que cambie el repositorio o el ambiente se ejecuta; lo que se pida se pone en cola y arranca al terminar. El smoke testing también espera a que termine el release.
3. **Cola visible:** el panel muestra qué espera y a qué.
4. **Cada proceso se puede consultar por separado** (`/actividad?corrida=`), en lugar de una sola corrida por Proyecto.

## Consecuencias

- Requiere un gestor de bloqueos por recurso (HU, Proyecto, ambiente) y un registro de corridas en lugar de una sola por Proyecto.
- El registro vive en memoria: convendría persistirlo antes de depender de la cola.

## Pendiente

Todo. Se decide con quien usa la plataforma antes de construirlo.
