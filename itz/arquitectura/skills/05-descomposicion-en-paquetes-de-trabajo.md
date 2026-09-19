# Skill — Descomposición en paquetes de trabajo

**Alias en diagramas:** `S3` en [diagrama 02](../diagramas/02-skill-orquestador-y-skills-por-fase.md).

## Propósito

A partir de `plan.md` (el enfoque de diseño) y los TCs pendientes, partir el trabajo en **paquetes de
trabajo** lo bastante acotados para que cada uno resulte en un Pull Request propio y revisable. Es la
skill que produce los "paquetes de trabajo" que ADR-0004 describe generando código — un término
distinto de cualquier elemento del backlog que venga ya de la fuente (ADR-0009/ADR-0026): un paquete de
trabajo es siempre interno a Telar, nunca algo leído de Jira/GitHub/Markdown.

## Cuándo se invoca

Cuando una HU llega a la fase `planificada` (salida de `skills/04-...md`). No aplica a elementos
clasificados como Actividad (ADR-0026) — una Actividad no tiene TCs que descomponer en paquetes de
trabajo validables por smoke testing; su plan se implementa directo (ver `skills/04-...md`).

## Entradas

- `plan.md`: enfoque de diseño y repositorios involucrados.
- `test-cases.md`: TCs marcados `pendiente` que el plan debe cubrir.
- **Prototipo, si existe** (`prototipo_ref` en `spec.md`, ADR-0027): usado para asegurar que la
  descomposición cubra **ambos lados** (back y front) sin dejar huecos, contra lo que el diagnóstico
  (`skills/03-...md`) ya marcó como existente.

## Salidas

`tasks.md`, con front-matter:

```yaml
hu_id: HU-001
fase: descompuesta
total_paquetes: 3
fecha_descomposicion: 2026-09-14
```

Cuerpo: lista de paquetes de trabajo planeados, cada uno con su ID, repositorio objetivo, y qué TCs
cubre.

Más un archivo `paquetes/PT-0N.md` por cada paquete de trabajo, con front-matter:

```yaml
id: PT-01
hu_id: HU-001
repo: backend-principal        # exactamente uno de los repos configurados (ADR-0005)
estado: pendiente               # pendiente | en_revision | fusionado — no "completo" (ADR-0023)
ronda: 1                        # 1 = descomposición original; 2+ = rondas de fix (ADR-0023)
tcs_asociados: [TC-001, TC-003]
pr: null
rondas_revision: 0
depende_de: []                  # IDs de otros paquetes de trabajo que deben completarse antes
id_externo: null                 # ID del paquete/sub-issue creado en la fuente, si aplica (ADR-0024)
```

*(`estado: fusionado` es el final de este paquete de trabajo individualmente — ya no `completo`: la HU
y sus paquetes de trabajo solo se dan por completos cuando smoke testing pasa a nivel HU, ADR-0023.)*

**Creación en la plataforma de origen (ADR-0024):** si la fuente de HUs de este Proyecto es Jira o
GitHub (plataformas con gestión nativa de subtareas), esta skill además crea el paquete correspondiente
ahí, vía MCP, y guarda su referencia en `id_externo`. Si la fuente es Markdown, no hay plataforma
externa equivalente — `id_externo` queda `null` y `paquetes/PT-0N.md` en el repo de control es la
única representación que existe.

## Qué hace (alto nivel)

1. Lee `plan.md` y los TCs `pendiente` de `test-cases.md`.
2. Agrupa esos TCs en unidades de trabajo coherentes y acotadas. **Cada paquete de trabajo toca
   exactamente un repositorio** de los configurados (ADR-0005) — si el plan requiere un cambio
   coordinado en más de uno (p. ej. un contrato de API que afecta backend y frontend), se generan
   paquetes de trabajo separados, uno por repositorio, relacionados por `depende_de`.
3. Determina el orden/dependencias entre paquetes de trabajo cuando uno depende del resultado de otro.
4. Escribe `tasks.md` (resumen) y un `paquetes/PT-0N.md` por cada paquete de trabajo, en el repositorio
   de control (ADR-0012) — esto ocurre siempre, sin importar la fuente de HUs.
5. Si la fuente de HUs del Proyecto lo soporta (Jira, GitHub), crea además el paquete correspondiente
   ahí vía MCP y guarda su referencia en `id_externo` (ADR-0024). Si la fuente es Markdown, se omite
   este paso.
6. Deja la fase de la HU en `descompuesta` — el orquestador puede empezar a despachar paquetes de
   trabajo individuales a la skill de generación de código.

## Estado de implementación

Implementada para Proyectos en modo `nuevo` a partir de la arquitectura fundacional aprobada (no de un
`plan.md` por HU): planea el esqueleto (grupo `BASE`) y el orden de las HUs, y parte cada HU en
paquetes — ADR-0045. El modo extensión, las rondas de fixes y la creación en Jira/GitHub siguen
pendientes.

## Orden de las HUs

El orden de las HUs ([ADR-0048](../decisiones/0048-orden-de-implementacion-de-hus-y-avance-por-hu.md)): fija el orden de implementación de cada HU (`orden`): prioridad de negocio ajustada por dependencias reales.

## Esqueleto con entorno de desarrollo

El primer paquete del esqueleto deja el entorno de desarrollo dockerizado y el README
([ADR-0050](../decisiones/0050-entorno-de-desarrollo-dockerizado-y-readme-en-el-esqueleto.md)).

## README por servicio

El esqueleto crea el README de cada servicio ([ADR-0056](../decisiones/0056-un-readme-por-servicio.md)).

## ADRs relacionados

- [ADR-0045](../decisiones/0045-skill-05-descomposicion-desde-arquitectura-fundacional.md) — adaptación
  al flujo fundacional.

- [ADR-0004](../decisiones/0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md) —
  descomposición en paquetes de trabajo como fase del flujo.
- [ADR-0005](../decisiones/0005-solucion-configurable-repositorios-y-ambiente-dev.md) — cada paquete de
  trabajo se ancla a exactamente uno de los repos configurados.
- [ADR-0008](../decisiones/0008-adopcion-de-sdd-y-nombres-de-artefactos.md) — formato de `tasks.md` y
  `paquetes/`.
- [ADR-0023](../decisiones/0023-smoke-testing-espera-a-toda-la-hu-no-por-subtarea.md) — el estado final
  de un paquete de trabajo es `fusionado`, no `completo`; el campo `ronda` agrupa qué paquetes deben
  fusionarse juntos antes de que se dispare smoke testing.
- [ADR-0024](../decisiones/0024-creacion-de-subtareas-en-la-fuente-via-mcp.md) — creación adicional del
  paquete en la plataforma de origen (Jira/GitHub) vía MCP, cuando la fuente lo soporta.
- [ADR-0026](../decisiones/0026-vocabulario-unificado-hu-actividad-paquete-de-trabajo.md) — define
  "paquete de trabajo" como término único, y resuelve la colisión que antes existía con "subtarea".
- [ADR-0027](../decisiones/0027-prototipo-como-input-complementario.md) — el prototipo, cuando existe,
  asegura que la descomposición cubra ambas capas sin huecos.
- [ADR-0029](../decisiones/0029-orden-secuencial-de-paquetes-de-trabajo-dependientes.md) — paquetes con
  `depende_de` se generan en secuencia estricta, no en paralelo.

## Criterios de éxito

Todo TC `pendiente` queda cubierto por al menos un paquete de trabajo; cada paquete de trabajo
referencia exactamente un repositorio configurado; las dependencias entre paquetes de trabajo quedan
explícitas en `depende_de`.

## Pendientes propios de esta skill

- Qué tan grande puede ser un paquete de trabajo antes de considerarse que debería partirse más — falta
  un criterio de "tamaño de PR razonable" (hoy: 1 a 4 paquetes por HU, un solo objetivo cada uno).
- ~~Si `depende_de` implica orden estricto o generación en paralelo~~ — resuelto en
  [ADR-0029](../decisiones/0029-orden-secuencial-de-paquetes-de-trabajo-dependientes.md): orden
  estricto (p. ej. backend antes que frontend cuando el frontend depende de él).
- Qué hacer si falla la creación del paquete en la plataforma de origen (Jira/GitHub, ADR-0024) — no
  debería bloquear el control interno; ya resuelto en ADR-0024 que solo se advierte, con opción de
  reintentar desde la plataforma.
