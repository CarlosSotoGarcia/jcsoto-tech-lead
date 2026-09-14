# ADR-0018: Framework de agentes (Claude Code Skills) y análisis de código bajo demanda

## Estado

Aceptada

## Contexto

Faltaba decidir con qué framework de agentes se implementan el orquestador y las 9 skills de fase, y
cómo se representa/indexa el código de un repositorio para que la skill de diseño de arquitectura
(`skills/04-...md`) y la de revisión de código (`skills/07-...md`) puedan analizarlo — ambas ya
dependen de esto como entrada sin que existiera una decisión tomada.

## Decisión

1. El orquestador y las 9 skills de fase se implementan sobre **Claude Code Skills** (el Claude Agent
   SDK que lo sostiene), invocado de forma no interactiva/headless — el orquestador lo dispara
   programáticamente por HU/subtarea, sin que haga falta intervención manual en cada paso.
2. El análisis de código (skill 04 y skill 07) se hace **bajo demanda, en el momento**, con
   herramientas de búsqueda estructurada (grep/glob) y lectura directa de archivos — **no** se
   construye ni mantiene un índice persistente, ni de AST ni de embeddings.

## Consecuencias

- Consistente con [ADR-0002](0002-alcance-de-infraestructura-diseno-no-despliegue.md): ninguna de las
  dos decisiones introduce infraestructura desplegada/operada de forma persistente — Claude Code corre
  bajo demanda, y el análisis de código no depende de un índice que haya que mantener sincronizado con
  cada cambio.
- Reduce el trabajo de ingeniería: no hace falta construir parsers de AST por lenguaje ni un pipeline de
  embeddings/vector store.
- El costo/latencia de analizar un repositorio grande puede ser mayor que con un índice semántico
  precomputado — se acepta como limitación conocida y documentada, no resuelta con más infraestructura.
- La terminología "skill" usada desde [ADR-0004](0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md)
  deja de ser solo una metáfora: cada una de las 9 fichas en `skills/` es, en la práctica, una skill de
  Claude Code.
- Pendiente (detalle de implementación, no bloquea el diseño actual): cómo se acota el contexto de
  herramientas de cada skill dentro de un repo grande (todo el repo disponible vs. convenciones de
  carpetas relevantes).
