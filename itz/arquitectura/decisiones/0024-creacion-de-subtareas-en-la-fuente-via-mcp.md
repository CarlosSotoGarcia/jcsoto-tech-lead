# ADR-0024: Creación de subtareas en la plataforma de origen vía MCP, cuando la fuente lo soporta

## Estado

Aceptada. Complementa el contrato de lectura de [ADR-0019](0019-contrato-comun-de-adaptadores-de-fuente-de-hus.md)
con una capacidad de escritura que ese ADR no cubría.

## Contexto

[ADR-0012](0012-plataforma-de-visualizacion-y-reportes.md) ya estableció que la documentación por HU
(incluidas las subtareas técnicas) vive siempre en el repositorio de control del Proyecto — eso sigue
siendo la fuente de verdad operativa del orquestador y no cambia. Pero cuando la fuente de HUs
(ADR-0009/0010) es una plataforma con gestión nativa de subtareas — **Jira** y **GitHub** la tienen
(sub-tickets, sub-issues); **Markdown** no —, las personas que trabajan directamente en esa plataforma,
sin pasar por Telar/Loom, no verían el desglose de subtareas que el sistema generó a menos que también
se refleje ahí.

## Decisión

1. El **control interno en el repositorio de control** (`subtareas/ST-0N.md`, ADR-0008/0012) sigue
   siendo **siempre** la fuente de verdad operativa, sin importar la fuente de HUs — esto no cambia.
2. Cuando la fuente de HUs es una plataforma con gestión nativa de subtareas (Jira, GitHub), la skill
   de descomposición en subtareas (`skills/05-...md`) **además crea las subtareas correspondientes en
   esa plataforma de origen**, usando una conexión **MCP** a ella (servidor MCP de Jira o de GitHub) —
   así, alguien que trabaje directamente ahí, sin pasar por Telar, también ve el desglose.
3. Cuando la fuente es **Markdown**, no existe una plataforma externa equivalente — el control interno
   del repositorio de control es la **única** representación de las subtareas; no hay nada que crear
   afuera.
4. `subtareas/ST-0N.md` gana un campo opcional `id_externo`: la referencia a la subtarea/sub-issue
   creada en la plataforma de origen, cuando aplica (vacío para fuente Markdown).

## Consecuencias

- Introduce una capacidad de **escritura** hacia la fuente de HUs que ADR-0019 no contemplaba (ese
  contrato era solo de lectura, `listar_elementos_procesables()`) — se necesita una capacidad adicional
  de "crear subtarea en la fuente", presente para Jira/GitHub y ausente para Markdown.
- Refuerza que Markdown, aunque es una fuente válida y más simple, no da la misma sincronización
  bidireccional que Jira/GitHub — es una diferencia real entre fuentes, documentada aquí explícitamente,
  no un descuido.
- MCP se convierte en el mecanismo elegido para integraciones de escritura hacia plataformas externas —
  consistente con que el framework de agentes ya es Claude Code Skills (ADR-0018), que soporta MCP de
  forma nativa.
- El control interno **no depende** de que la creación en la fuente tenga éxito — es la fuente de
  verdad real; la sincronización hacia Jira/GitHub es un reflejo adicional, no un requisito para que el
  pipeline avance.

## Resolución: falla de creación en la fuente

Si la creación de la subtarea en la plataforma de origen (vía MCP) falla, **solo se advierte — no
bloquea** el control interno ni el resto del pipeline. La advertencia queda registrada como un reporte
en la plataforma de Telar (ADR-0012), con la opción explícita de **volver a intentar** esa creación
manualmente desde ahí. Consistente con que el control interno (`subtareas/ST-0N.md`) es la fuente de
verdad real — la sincronización hacia Jira/GitHub es un reflejo adicional, no un requisito.

## Pendiente

- Si el alcance de esta sincronización vía MCP se limita a la creación de subtareas, o también debería
  reflejar actualizaciones de estado (PR abierto, en revisión, fusionado) hacia Jira/GitHub.
