# Skill — Descubrimiento y especificación de HU

**Alias en diagramas:** `S0` en [diagrama 02](../diagramas/02-skill-orquestador-y-skills-por-fase.md).

## Propósito

Leer una historia de usuario desde la fuente configurada del Proyecto (Jira, Markdown o GitHub —
ADR-0009, ADR-0010) e
**interpretarla como lo haría un analista de requerimientos senior** — no solo extraer texto — para
producir su especificación normalizada: `spec.md`, en el formato interno del sistema (SDD, ADR-0008).
Es el punto de entrada único del pipeline: sin importar si la HU vino de un issue de Jira o de un
archivo Markdown, todo lo que pasa después (generación de TCs, diagnóstico, arquitectura, código)
trabaja siempre sobre el mismo `spec.md`, nunca contra la fuente original directamente.

## Rol: analista de requerimientos (LLM)

Esta skill corre sobre un LLM con buena capacidad de análisis, con el mismo criterio que aplicaría un
analista de negocio/requerimientos experimentado al recibir una HU antes de pasarla a desarrollo:

- **Interpreta la intención real** detrás de la HU, no solo el texto literal — qué problema de negocio
  resuelve, no nada más qué dice la redacción.
- **Detecta criterios de aceptación implícitos** que la HU no menciona explícitamente pero que un
  analista experimentado asumiría como parte del alcance (manejo de errores, casos límite,
  validaciones, permisos) — y los hace explícitos.
- **Estructura los criterios de aceptación en un formato consistente y verificable** (Given/When/Then o
  equivalente), incluso si la fuente los trae en prosa libre o desordenados.
- **Distingue inferencia razonable de ambigüedad real.** Cuando el vacío es inferible con confianza
  (un detalle que casi cualquier analista completaría igual), lo completa. Cuando el vacío cambia el
  alcance o admite más de una interpretación válida, **no inventa silenciosamente** — lo deja marcado
  como supuesto o pregunta abierta (ver Salidas).
- **Clasifica el elemento como HU o Actividad** (ADR-0026): si tiene o se le pueden inferir criterios
  de aceptación verificables, es una **HU** y sigue el pipeline completo; si es trabajo de arquitectura
  o preparación sin comportamiento de usuario verificable (por lo regular así son los elementos que la
  fuente tipa como "Tarea"), es una **Actividad** y sigue un pipeline reducido — sin TCs ni smoke
  testing (ver Salidas y Qué hace).

Esto es explícitamente distinto de un parser: la misma HU puede llegar incompleta o ambigua desde la
fuente, y esta skill hace el trabajo de análisis, no solo de transcripción.

## Cuándo se invoca

- Al dar de alta un Proyecto, para el recorrido inicial completo del backlog configurado.
- Ante una HU nueva o modificada en la fuente (re-descubrimiento incremental).

*Pendiente: si el recorrido es "una corrida completa bajo demanda" o si hay un modo continuo/polling —
ver Pendientes.*

## Entradas

- Configuración del Proyecto (ADR-0009, ADR-0010): tipo de fuente (`jira` | `markdown` | `github`) y
  sus parámetros de conexión (proyecto de Jira; ubicación/repositorio de los archivos Markdown; o
  repositorio de GitHub del que se leen Issues).
- Un **elemento del backlog** (ADR-0009, ADR-0026) identificado durante el recorrido de la fuente —
  antes de saber si es una HU o una Actividad (eso lo determina esta misma skill, ver abajo).

## Salidas

Un archivo `spec.md` por HU, con este contrato:

**Front-matter:**

```yaml
id: HU-001                # identificador interno, asignado por esta skill (o AC-001 si es Actividad)
clasificacion: hu          # hu | actividad — ADR-0026
fuente_tipo: jira          # jira | markdown | github
fuente_ref: PROY-123       # ID del issue de Jira, o ruta del archivo Markdown original — trazabilidad
fase: especificada
estado: pendiente
fecha_descubrimiento: 2026-09-13
tiene_supuestos: true       # true si el análisis tuvo que asumir o marcar algo como ambiguo
prototipo_ref: null          # referencia al prototipo entregado junto con la HU, si existe (ADR-0027)
depende_de: []               # IDs de otras HUs de las que esta depende, si aplica (ADR-0030)
```

**Cuerpo (Markdown libre, legible):**

- Título de la HU.
- Descripción / narrativa (el "como usuario quiero... para...", tal como la interpretó el análisis, no
  necesariamente copiada literal de la fuente).
- **Criterios de aceptación explícitos de la fuente** — los que ya venían dados, estructurados en
  formato verificable.
- **Criterios de aceptación inferidos** — los que el análisis agregó por juicio de analista, marcados
  como tales (no se mezclan sin distinción con los explícitos).
- **Supuestos y vacíos identificados** — ambigüedades reales que no se resolvieron por inferencia,
  cada una con una nota de qué se necesitaría para cerrarla.
- Notas de la fuente original que no encajen en lo anterior (p. ej. comentarios relevantes de Jira).

## Qué hace (alto nivel)

1. Lee la configuración del Proyecto y determina qué adaptador de lectura usar (Jira, Markdown o
   GitHub).
2. Recorre el backlog de la fuente (vía el contrato de ADR-0019) para identificar elementos
   procesables.
3. Por cada elemento encontrado, **analiza** su contenido — no solo lo normaliza — aplicando el rol de
   analista de requerimientos descrito arriba: interpreta intención, estructura criterios explícitos,
   infiere los implícitos razonables, marca como supuesto lo genuinamente ambiguo, y **clasifica el
   elemento como `hu` o `actividad`** según si termina teniendo criterios de aceptación verificables.
4. Escribe `spec.md` separando claramente lo explícito de lo inferido y de lo pendiente de aclarar.
5. Deja la fase en `especificada` para que el orquestador continúe: si `clasificacion: hu`, con la
   generación de TCs; si `clasificacion: actividad`, saltando directo a diseño/plan (sin TCs ni smoke
   testing, ADR-0026) — una HU con `tiene_supuestos: true` puede necesitar una regla especial de qué
   hacer con esos supuestos antes de avanzar (ver Pendientes).

## Paso adicional en Proyectos nuevos

Cuando `modo_arranque` es `nuevo`, al terminar de especificar todas las HUs la skill hace un último
análisis como arquitecto sobre lo leído y guarda una **propuesta de stack** (tecnología y
herramientas de backend y frontend, autenticación, estructura de repositorios, microservicios) con
su justificación, que la pantalla de Diseño precarga (ADR-0039). No genera archivos SDD; es estado
del Proyecto, y su falla no invalida el descubrimiento.

## Orden de las HUs

El orden de las HUs ([ADR-0048](../decisiones/0048-orden-de-implementacion-de-hus-y-avance-por-hu.md)): lee todas las HUs y guarda la posición de cada una en la fuente (Jira Rank) como prioridad de negocio (`orden_fuente`).

## ADRs relacionados

- [ADR-0039](../decisiones/0039-catalogo-de-stack-y-propuesta-del-arquitecto.md) — propuesta de
  stack al terminar el descubrimiento en Proyectos nuevos.
- [ADR-0008](../decisiones/0008-adopcion-de-sdd-y-nombres-de-artefactos.md) — formato y ubicación de
  `spec.md`.
- [ADR-0009](../decisiones/0009-proyecto-como-entidad-de-configuracion-y-fuente-de-hus-pluggable.md) —
  fuente pluggable y recorrido de la jerarquía del backlog.
- [ADR-0010](../decisiones/0010-agregar-github-como-fuente-de-hus.md) — GitHub Issues como tercera
  fuente soportada.
- [ADR-0011](../decisiones/0011-supuestos-no-bloquean-se-resuelven-en-revision-de-codigo.md) — qué pasa
  con una HU marcada `tiene_supuestos: true`.
- [ADR-0026](../decisiones/0026-vocabulario-unificado-hu-actividad-paquete-de-trabajo.md) — distinción
  HU vs. Actividad, y vocabulario general.
- [ADR-0027](../decisiones/0027-prototipo-como-input-complementario.md) — `prototipo_ref`, cuando se
  entrega un prototipo junto con la HU.
- [ADR-0030](../decisiones/0030-paralelismo-entre-hus-con-dependencias.md) — `depende_de` a nivel HU.

## Criterios de éxito

Existe un `spec.md` válido — con todos los campos de front-matter listados arriba, al menos un criterio
de aceptación explícito o inferido, y cualquier ambigüedad real registrada como supuesto en vez de
resuelta en silencio — por cada HU procesable encontrada en la fuente configurada.

## Pendientes propios de esta skill

- ~~Qué hace el orquestador con una HU marcada `tiene_supuestos: true`~~ — resuelto en
  [ADR-0011](../decisiones/0011-supuestos-no-bloquean-se-resuelven-en-revision-de-codigo.md): el
  pipeline avanza sin bloquear, y el supuesto se resuelve visiblemente en la revisión de código (S5).
- ~~Cómo se detectan HUs ya procesadas antes vs. nuevas/modificadas~~ — resuelto en
  [ADR-0040](../decisiones/0040-deteccion-de-cambios-en-la-fuente-y-regeneracion-selectiva.md): huella
  del título+descripción de la fuente; revisión sin LLM y regeneración solo de lo nuevo/modificado o
  de HUs puntuales. Sigue abierto el descubrimiento automático (polling/webhook).
- Formato mínimo esperado de un archivo Markdown de HU cuando la fuente es `markdown` — sigue abierto;
  fuente `markdown` todavía no está implementada (ADR-0033).
- ~~Mapeo exacto de campos de Jira... al `spec.md` interno~~ — resuelto en
  [ADR-0033](../decisiones/0033-primera-implementacion-skill-01-descubrimiento.md): resumen y
  descripción (aplanada desde Atlassian Document Format) se pasan al LLM, que hace el análisis
  completo — no hay mapeo campo-a-campo de criterios de aceptación, se infieren del texto.
- Mapeo exacto de un Issue de GitHub (título, cuerpo, labels, sub-issues) al `spec.md` interno, y qué
  convención de labels/milestones se asume cuando el repositorio no usa sub-issues nativos (ADR-0010).
- Modo de ejecución: ¿corrida bajo demanda sobre todo el backlog, o descubrimiento continuo/incremental
  (polling, webhook de Jira, etc.)?
- Qué tan "agresiva" debe ser la inferencia de criterios implícitos antes de que se considere que el
  análisis se está excediendo de su alcance (inventando requisitos, no infiriéndolos).
