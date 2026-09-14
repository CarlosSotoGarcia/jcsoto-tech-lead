# Skill — Diseño de arquitectura

**Alias en diagramas:** `S2` en [diagrama 02](../diagramas/02-skill-orquestador-y-skills-por-fase.md).

## Propósito

A partir de los TCs marcados como `pendiente` por el diagnóstico de avance (`skills/03-...md`), diseñar
**cómo** se va a construir lo que falta — respetando y extendiendo la arquitectura y convenciones que
ya existen en el/los repositorio(s) objetivo, no proponiendo una solución nueva ignorando lo que hay
(ADR-0007). Es el "plan" de Spec-Driven Development (ADR-0008): el puente entre "qué falta" (TCs
pendientes) y "en qué paquetes de trabajo se va a partir el trabajo" (siguiente skill).

Esta skill opera en **dos modos**, según el modo de arranque del Proyecto (ADR-0014):

- **Modo extensión** (Proyecto `avanzado` o con código ya existente): el comportamiento descrito abajo
  — analiza lo que ya existe y extiende sus patrones.
- **Modo fundacional** (Proyecto `nuevo`, ADR-0014): no hay nada que analizar ni extender. La skill
  **define** la arquitectura inicial del repositorio objetivo — elección de stack/framework (si no
  viene ya fijada por el tipo de Proyecto, ADR-0009), estructura de carpetas, capas y convenciones de
  partida. Ese resultado es lo que las HUs siguientes van a encontrar como "lo ya existente" y podrán
  extender en modo normal. Se ejecuta **una sola vez por repositorio objetivo**, no por cada HU.
- Proyecto en modo `con_arquitectura` (ADR-0014): esta skill **no se invoca** — se asume una
  arquitectura ya definida por humanos, aportada al sistema por otro medio (pendiente de definir en
  ADR-0014).

## Cuándo se invoca

En modo extensión: cuando una HU llega a la fase `diagnosticada` (salida de `skills/03-...md`) y tiene
al menos un TC marcado `pendiente`. Si todos los TCs ya están `cubierto`, la HU se da por completa sin
pasar por esta skill (todo lo pedido ya existe).

En modo fundacional: una vez, al dar de alta un repositorio objetivo de un Proyecto en modo `nuevo`
(ADR-0014), antes de procesar su primera HU.

## Entradas

- `test-cases.md`: qué TCs quedaron `pendiente` tras el diagnóstico (los `cubierto` no generan trabajo).
- `spec.md`: criterios de aceptación asociados a cada TC pendiente, y cualquier supuesto marcado
  (`tiene_supuestos`, ADR-0011) que afecte el diseño.
- **Código actual del/los repositorio(s) objetivo** (ADR-0005): estructura, convenciones, patrones ya
  presentes — vía el mecanismo de indexación de código (ADR-0002, todavía sin detallar como skill
  propia).

## Salidas

*(Lo siguiente describe el modo extensión, ligado a una HU. El modo fundacional produce un artefacto
de arquitectura base a nivel de repositorio, no de HU — formato pendiente de definir junto con
ADR-0014.)*

`plan.md`, con front-matter:

```yaml
hu_id: HU-001
fase: planificada
tcs_cubiertos_por_plan: [TC-001, TC-003, TC-005]   # los que test-cases.md marcó pendiente
repos_involucrados: [backend-principal, frontend-admin]
fecha_plan: 2026-09-14
```

Cuerpo:

- **Resumen del enfoque**: qué se va a construir y por qué esa aproximación, en términos de la
  arquitectura ya existente (qué capa/módulo/patrón se extiende, no se reinventa).
- **Repositorios afectados**: de los N configurados (ADR-0005), cuáles necesita tocar esta HU y por
  qué — insumo directo para que la skill de generación de código sepa dónde generar cada cosa.
- **Decisiones de diseño puntuales** relevantes a esta HU (no arquitectura del sistema completo, solo
  lo que esta HU necesita: p. ej. "se agrega un nuevo endpoint siguiendo el patrón REST ya usado en
  `X`", "el nuevo componente de UI reutiliza el layout de `Y`").
- **Supuestos heredados de `spec.md`**, si los hay, con nota de cómo el diseño los interpretó (para que
  lleguen visibles hasta la revisión de código, ADR-0011).

## Qué hace (alto nivel)

1. Lee los TCs `pendiente` de `test-cases.md` y sus criterios asociados en `spec.md`.
2. Analiza el código actual de los repos involucrados (vía el mecanismo de indexación, ADR-0002) para
   identificar patrones y convenciones existentes relevantes a lo que falta construir.
3. Propone un enfoque que extiende esos patrones — no una arquitectura nueva en el vacío.
4. Identifica qué repositorio(s) de los configurados necesita tocar esta HU.
5. Escribe `plan.md` y deja la fase en `planificada`.

## ADRs relacionados

- [ADR-0002](../decisiones/0002-alcance-de-infraestructura-diseno-no-despliegue.md) — el mecanismo de
  indexación de código del que depende esta skill (diseño, no infraestructura desplegada).
- [ADR-0004](../decisiones/0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md) — el
  diseño de arquitectura como fase del flujo.
- [ADR-0007](../decisiones/0007-soporte-proyectos-con-avance-previo.md) — el diseño debe extender lo
  existente, no ignorarlo.
- [ADR-0008](../decisiones/0008-adopcion-de-sdd-y-nombres-de-artefactos.md) — `plan.md` como artefacto
  SDD.
- [ADR-0011](../decisiones/0011-supuestos-no-bloquean-se-resuelven-en-revision-de-codigo.md) — los
  supuestos de `spec.md` deben quedar visibles en `plan.md`.
- [ADR-0014](../decisiones/0014-modo-de-arranque-de-proyecto-y-ejecucion-selectiva-por-fase.md) — modo
  fundacional vs. modo extensión, según el modo de arranque del Proyecto.
- [ADR-0022](../decisiones/0022-repos-fuera-de-configuracion-o-de-alcance.md) — qué hacer cuando el
  enfoque de diseño necesita un repo fuera de la configuración del Proyecto, o un tipo de sistema fuera
  del alcance de Telar.

## Criterios de éxito

`plan.md` cubre todos los TCs marcados `pendiente` (ninguno queda sin un enfoque de diseño asociado),
identifica explícitamente qué repositorios toca, y no contradice patrones ya presentes en el código sin
justificarlo.

## Pendientes propios de esta skill

- ~~Cómo se implementa el mecanismo de indexación de código~~ — resuelto en
  [ADR-0018](../decisiones/0018-framework-de-agentes-e-indexacion-de-codigo.md): análisis bajo demanda
  con grep/glob, sin índice persistente.
- ~~Qué pasa si el enfoque de diseño requiere un repositorio fuera de configuración~~ — resuelto en
  [ADR-0022](../decisiones/0022-repos-fuera-de-configuracion-o-de-alcance.md): se marca en `plan.md`
  como pendiente de definir (recuperable, amplía config) o como fuera de alcance (si es un tipo de
  sistema no soportado) — la plataforma lo escala al humano en ambos casos.
- Nivel de detalle esperado en "decisiones de diseño puntuales": ¿alcanza con guiar a la skill de
  generación de código, o debe ser suficientemente detallado para que un humano lo revise como si fuera
  un mini-RFC?
- Si esta skill también debería registrar sus propias decisiones como ADRs del Proyecto (paralelo a
  cómo se documenta la arquitectura de este mismo sistema, ADR-0001) o si `plan.md` basta.
- Formato exacto del artefacto de arquitectura fundacional (modo fundacional, ADR-0014): ¿un `plan.md`
  especial a nivel de repositorio, o algo distinto?
- Cómo se decide el stack/framework en modo fundacional cuando el tipo de Proyecto (ADR-0009, solo
  "web" por ahora) no basta para elegirlo por sí solo (web se puede construir con muchas combinaciones
  de stack).
