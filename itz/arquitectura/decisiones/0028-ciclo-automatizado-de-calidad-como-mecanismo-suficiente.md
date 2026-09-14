# ADR-0028: El ciclo automatizado código→revisión→corrección es el mecanismo de calidad documentado

## Estado

Aceptada. Cierra el pendiente de [ADR-0011](0011-supuestos-no-bloquean-se-resuelven-en-revision-de-codigo.md)/[ADR-0015](0015-revision-manual-opcional-antes-de-merge.md)
sobre si un supuesto sin resolver debe forzar revisión manual.

## Contexto

Quedaba abierto si un supuesto sin resolver (`tiene_supuestos`, ADR-0011) debía forzar
`requiere_revision_manual` (ADR-0015) automáticamente, sin importar la configuración del Proyecto —
por el riesgo de dejar pasar una interpretación del LLM sin que nadie la confirme.

## Decisión

No se fuerza. Cuando `requiere_revision_manual` es `false`, el PR igual pasa por un ciclo real de
calidad antes de aceptarse: **generación de código → revisión de código (`skills/07-...md`) →
corrección (`skills/06-...md`) → aceptación** — nunca "generar y fusionar directo". Este ciclo:

- Es el mismo ciclo `CR ↔ APLICA` ya documentado en el [diagrama 01](../diagramas/01-flujo-pipeline-hu-a-desarrollo.md).
- Queda documentado explícitamente: `rondas_revision` en `paquetes/PT-0N.md` y los comentarios del PR
  son evidencia de que hubo una revisión real, no solo generación de código sin control.
- Trata un supuesto sin resolver como observación bloqueante (ADR-0011) dentro de ese mismo ciclo — no
  necesita un gate adicional de revisión humana para considerarse atendido.

Es decir: el ciclo automatizado de calidad **es** el mecanismo, con o sin revisión manual — la revisión
manual (ADR-0015) es una capa *adicional* para cuando el Proyecto la pida, no un requisito para que
exista control de calidad en absoluto.

## Consecuencias

- No se agrega una regla especial que fuerce `requiere_revision_manual` por tener supuestos — la
  responsabilidad sigue en `skills/07-...md`, consistente con ADR-0011.
- Refuerza el valor de `rondas_revision` y los comentarios del PR como evidencia de auditoría: un
  Proyecto sin revisión manual todavía puede demostrar que cada cambio pasó por un ciclo de revisión,
  no que se generó y fusionó a ciegas.
- Si en el futuro se decide que ciertos supuestos sí ameritan forzar revisión humana (p. ej. por
  severidad), eso sería una decisión nueva y explícita, no un default implícito de este ADR.
