# ADR-0023: Smoke testing espera a que toda la HU esté fusionada, no se dispara por cada subtarea

## Estado

Aceptada. Modifica el disparador de `skills/08-smoke-testing.md` establecido en ADR-0004/ADR-0020, sin
contradecir el alcance (todos los TCs de la HU) que ADR-0020 ya había fijado.

## Contexto

El diseño original (ADR-0004, [diagrama 01](../diagramas/01-flujo-pipeline-hu-a-desarrollo.md)) disparaba
smoke testing inmediatamente después de cada merge individual de subtarea. Esto genera falsos negativos:
muchos TCs de una HU solo se pueden evaluar de forma representativa cuando varias subtareas relacionadas
(p. ej. backend + frontend) están completas a la vez — correr smoke testing tras fusionar solo la
primera subtarea casi garantiza fallos que no son errores reales, sino trabajo todavía incompleto.

Además, la visibilidad de avance por subtarea (PR abierto, en revisión, fusionado) ya la cubre la
plataforma (ADR-0012) con su log/timeline continuo — no hace falta que la validación funcional
(smoke testing) sea también incremental para dar esa visibilidad; son dos cosas distintas.

## Decisión

Smoke testing (`skills/08-...md`) se dispara **una vez que todas las subtareas de la construcción
original de la HU están fusionadas** — no después de cada una individualmente — y corre sobre todos los
TCs de la HU (ADR-0020).

Si algún TC falla, se genera una subtarea de fix (`skills/09-...md`). A partir de ahí, **cada fix
fusionado sí dispara smoke testing de inmediato**: ya no hay más subtareas "en construcción" esperando
— la HU entera está completa y cualquier fix es una corrección puntual sobre trabajo ya terminado, no
una pieza faltante del rompecabezas original.

El estado de una subtarea (`subtareas/ST-0N.md`) pasa de `en_revision` a **`fusionada`** al hacer
merge — ya no a `completa`. `completa` (de la subtarea y de la HU) solo se alcanza cuando el smoke
testing de la HU pasa.

## Consecuencias

- Reduce falsos negativos de smoke testing causados por trabajo incompleto de otras subtareas
  relacionadas de la misma HU.
- Separa explícitamente "reportar avance" (continuo, por subtarea, vía la plataforma — ADR-0012) de
  "validar comportamiento" (una vez, a nivel HU, salvo en el ciclo de fixes).
- El criterio "todas las subtareas fusionadas" se resuelve comparando el total de `tasks.md` contra
  cuántas subtareas están en `fusionada` — no requiere mecanismo nuevo.
- Actualiza: [diagrama 01](../diagramas/01-flujo-pipeline-hu-a-desarrollo.md) (gate nuevo antes de
  `SMOKE`), `skills/05-...md` (estado `fusionada`), `skills/08-...md` (disparador) y `skills/09-...md`
  (tras un fix sí se dispara de inmediato).

## Pendiente

Si una subtarea de la construcción original queda bloqueada indefinidamente (nunca se fusiona), la HU
nunca llega a smoke testing — mismo tipo de pendiente que el "límite de rondas antes de escalar a
humano" ya señalado en otras skills; no se resuelve aquí.
