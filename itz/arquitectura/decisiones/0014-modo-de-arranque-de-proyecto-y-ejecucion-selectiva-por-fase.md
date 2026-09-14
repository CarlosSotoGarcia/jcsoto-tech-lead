# ADR-0014: Modo de arranque de Proyecto y ejecución selectiva por fase

## Estado

Aceptada. Extiende [ADR-0009](0009-proyecto-como-entidad-de-configuracion-y-fuente-de-hus-pluggable.md)
y [ADR-0004](0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md), no los reemplaza.

## Contexto

No todos los Proyectos arrancan desde cero ni necesitan correr el pipeline completo de punta a punta.
Al dar de alta un Proyecto pueden darse al menos tres situaciones distintas:

1. **Nuevo de verdad**: no existe arquitectura, solo hay HUs (backlog). El pipeline completo aplica tal
   cual, pero el diseño de arquitectura (`skills/04-...md`) no tiene nada que extender — tiene que
   *establecer* la base.
2. **HUs y arquitectura ya definidas** (por humanos, fuera del sistema, antes de adoptarlo): existe
   tanto backlog como un diseño de arquitectura ya decidido. El pipeline no necesita pasar por diseño de
   arquitectura — puede arrancar directo en descomposición en subtareas.
3. **Proyecto avanzado, con necesidad de entrar en cualquier fase**: se quiere usar el sistema para
   implementar HUs nuevas (pipeline completo), o **solo** hacer revisión de código de HUs/subtareas ya
   existentes, o **solo** generar/correr smoke tests — sin pasar necesariamente por las fases previas.

ADR-0007 ya resolvía una versión acotada de esto (greenfield vs. brownfield, a nivel del diagnóstico de
avance), pero no cubre que el **punto de entrada al pipeline** pueda ser distinto por Proyecto, ni que
se pueda invocar **una sola fase** bajo demanda en vez de siempre el flujo completo.

## Decisión

1. La configuración de Proyecto (ADR-0009) incluye un **modo de arranque**, uno de:
   - `nuevo` — sin arquitectura previa; la skill de diseño de arquitectura (`skills/04-...md`) opera en
     modo fundacional (ver Consecuencias) en vez de modo "extender lo existente".
   - `con_arquitectura` — HUs y arquitectura ya definidas; las HUs descubiertas entran directo en fase
     `descompuesta` o `planificada` (según qué tan detallado sea lo ya definido), sin pasar por
     `skills/04-...md`.
   - `avanzado` — no se asume ningún punto de entrada fijo; cada invocación especifica qué fase(s)
     ejecutar sobre qué HUs/subtareas.
2. El **orquestador** (pendiente de documentar como skill propia) deja de ser exclusivamente "un
   despachador de flujo secuencial fijo de HU nueva a HU completa" (ADR-0004) y gana un **modo de
   despacho selectivo**: se le puede pedir que ejecute una fase puntual (p. ej. "solo revisión de código
   sobre todas las subtareas en `en_revision`", o "solo smoke testing sobre las ya mergeadas") sin
   recorrer las fases anteriores. El flujo secuencial completo de ADR-0004 sigue siendo el
   comportamiento por defecto cuando el modo de arranque es `nuevo`.

## Consecuencias

- La skill de diseño de arquitectura (`skills/04-...md`) necesita un **modo fundacional** explícito para
  el caso `nuevo`: en vez de "analizar código existente y extender sus patrones", **define** la
  arquitectura inicial (stack, estructura base, convenciones de partida) — se documenta como ajuste a
  esa ficha, no como una skill aparte.
- Para el modo `con_arquitectura`, hace falta definir cómo se aporta esa arquitectura ya decidida al
  sistema (¿un `plan.md` inicial escrito a mano?, ¿una carpeta de referencia?) para que la skill de
  descomposición (`skills/05-...md`) tenga de dónde partir sin pasar por diseño de arquitectura.
- Para el modo `avanzado`, el orquestador necesita poder ubicar el estado de HUs/subtareas que **no**
  pasaron por el flujo normal del sistema (código y PRs preexistentes, escritos antes de adoptar el
  sistema) — probablemente requiere una forma de "reconstruir" `spec.md`/`plan.md`/`tasks.md` a partir
  de lo que ya existe, en vez de generarlos desde cero. Pendiente de detallar.
- El modelo de fases de ADR-0004 (secuencial, siempre de principio a fin) pasa a ser **un modo posible**
  del orquestador, no el único — esto debe reflejarse cuando se documente el orquestador como skill.

## Pendiente de definir

- Cómo se declara y valida el modo de arranque al dar de alta un Proyecto (parte de la configuración de
  ADR-0009).
- Formato de la "arquitectura ya definida" que se aporta en modo `con_arquitectura`.
- Mecanismo de reconstrucción de `spec.md`/`plan.md`/`tasks.md` para HUs/código preexistentes en modo
  `avanzado`, cuando se pide revisión o smoke testing sobre algo que el sistema nunca generó.
