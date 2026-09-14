# ADR-0019: Contrato común de adaptadores de fuente de HUs

## Estado

Aceptada

## Contexto

[ADR-0009](0009-proyecto-como-entidad-de-configuracion-y-fuente-de-hus-pluggable.md) y
[ADR-0010](0010-agregar-github-como-fuente-de-hus.md) establecieron que la fuente de HUs es pluggable
(Jira, Markdown, GitHub) pero no definieron qué interfaz deben cumplir esos adaptadores para que la
skill de descubrimiento (`skills/01-...md`) los use de forma uniforme. Implementar cada adaptador es
trabajo de código, fuera del alcance de esta fase de documentación — lo que sí corresponde definir aquí
es el contrato que los une.

## Decisión

Todo adaptador de fuente de HUs (Jira, Markdown, GitHub, o cualquiera que se agregue después — Azure
DevOps, Notion, etc., discutidos como candidatas futuras) expone una operación equivalente a
`listar_elementos_procesables()`, que devuelve una lista de elementos del backlog, cada uno normalizado
a:

- `id_fuente`: identificador único en la fuente original.
- `tipo`: `epica` | `tarea` | `subtarea`, según la jerarquía de la fuente (ADR-0009).
- `titulo`
- `descripcion`
- `criterios_aceptacion`: lista; puede venir vacía si la fuente no los trae explícitos — la skill 01
  los completa por inferencia (rol de analista de requerimientos).
- `padre`: `id_fuente` del elemento padre en la jerarquía, si aplica.
- `metadatos_fuente`: cualquier dato adicional específico de la fuente que no encaje arriba (labels,
  estado, comentarios relevantes) — se preserva para el cuerpo de `spec.md`, no se descarta.

La skill 01 consume únicamente este contrato — no conoce el modelo de datos interno de Jira, Markdown o
GitHub.

## Consecuencias

- Agregar una fuente nueva en el futuro requiere solo escribir un adaptador que cumpla este contrato,
  sin tocar `skills/01-...md` ni ninguna skill posterior.
- El diseño concreto de cada adaptador (mapeo exacto de campos de Jira, convención de Markdown,
  resolución de sub-issues/labels de GitHub) sigue pendiente como trabajo de implementación — este ADR
  fija la interfaz común, no las implementaciones.
- Refuerza el carácter agnóstico de Telar al nivel de la fuente de HUs, igual que ya lo era a nivel de
  repositorios objetivo (ADR-0005).
- Este contrato es **solo de lectura** (descubrir HUs desde la fuente). La capacidad complementaria de
  **escritura** hacia la fuente — crear subtareas ahí cuando la plataforma lo soporta — se define por
  separado en [ADR-0024](0024-creacion-de-subtareas-en-la-fuente-via-mcp.md), porque no todas las
  fuentes la tienen (Jira y GitHub sí; Markdown no).
