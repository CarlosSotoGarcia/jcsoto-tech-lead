# ADR-0020: Smoke testing corre todos los TCs de la HU y versiona cada corrida como regresión

## Estado

Aceptada. Cierra un pendiente de [ADR-0004](0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md)
y de `skills/08-smoke-testing.md`/`skills/09-generacion-de-fixes.md`.

## Contexto

Quedaba sin decidir si, tras un fix (`skills/09-...md`), smoke testing (`skills/08-...md`) debía volver
a correr solo los TCs que habían fallado, o el conjunto completo de TCs de la HU.

## Decisión

Cada vez que se ejecuta smoke testing sobre una subtarea — incluyendo después de un fix — se corren
**todos los TCs de la HU**, no solo los que fallaron ni solo los asociados a esa subtarea puntual. Cada
ejecución se versiona (numerada, `evidencia/smoke-0N.md`, ya establecido en ADR-0008): el conjunto de
esas ejecuciones a lo largo del tiempo **es** el historial de regresión de la HU, no solo evidencia de
una corrida aislada.

## Consecuencias

- El diagnóstico de avance existente (`skills/03-...md`) y smoke testing (`skills/08-...md`) — que ya
  compartían el mismo motor de ejecución — ahora comparten también el mismo alcance: correr el conjunto
  completo de TCs de la HU en cada invocación.
- El costo de ejecución crece con el número de TCs acumulados de una HU conforme se agregan subtareas y
  fixes — se acepta conscientemente a cambio de trazabilidad y detección temprana de regresiones.
- `evidencia/smoke-0N.md` deja de ser solo "evidencia de una corrida puntual": junto con las corridas
  anteriores, es el historial de regresión de la HU. Pendiente de detallar: que el front-matter permita
  comparar una corrida contra la inmediata anterior (qué TC cambió de estado).
- Refuerza la utilidad de la plataforma de reportes (ADR-0012): puede mostrar la evolución de TCs en
  verde/rojo a través de las corridas, no solo el estado más reciente.
- Actualiza `skills/08-...md` y `skills/09-...md`: donde decían "TCs asociados a la subtarea", debe
  leerse "todos los TCs de la HU".

## Pendiente

Si el alcance de "todos los TCs" debe quedarse a nivel HU o ampliarse a todo el Proyecto (regresión
cruzada entre HUs distintas) — por ahora se limita a la HU; ampliarlo es trabajo futuro si el costo de
ejecución lo permite.
