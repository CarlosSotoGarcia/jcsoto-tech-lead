# ADR-0021: Convención de nombre de rama basada en el identificador de la fuente

## Estado

Aceptada. Aplica el contrato de [ADR-0019](0019-contrato-comun-de-adaptadores-de-fuente-de-hus.md).

## Contexto

`skills/06-generacion-de-codigo.md` dejaba pendiente la convención de nombre de rama al crear una nueva
rama por subtarea.

## Decisión

El nombre de rama es `hu/{id_fuente}/{subtarea_id}`, donde `id_fuente` es el campo que todo adaptador
de fuente de HUs ya devuelve por contrato (ADR-0019):

- **Jira / GitHub**: el identificador del ticket/issue tal como está dado de alta en la fuente (p. ej.
  `PROY-123` o `456`).
- **Markdown**: el identificador propio del documento si lo trae (p. ej. un ID declarado en su
  front-matter); si no lo trae, el adaptador de Markdown genera uno y lo asigna de forma estable —
  queda como `id_fuente` para todo efecto posterior, igual que si hubiera venido de Jira o GitHub.

## Consecuencias

- No hace falta inventar un identificador nuevo para la rama: se reutiliza el mismo `id_fuente` que ya
  circula por `spec.md` y el resto de los archivos SDD (ADR-0008) desde que la skill de descubrimiento
  (`skills/01-...md`) lo asigna.
- La rama queda trazable directamente al ticket de origen, sin importar de qué fuente vino.
- Pendiente de detallar (implementación, no bloquea el diseño): el algoritmo exacto de generación de
  `id_fuente` para Markdown sin identificador propio (p. ej. slug del título, hash del contenido).
