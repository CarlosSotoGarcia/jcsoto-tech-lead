# ADR-0008: Adopción de Spec-Driven Development (SDD) y nombres de artefactos por HU

## Estado

Aceptada. Confirma y cierra la propuesta que quedó abierta en `00-vision-general.md` ("En discusión
ahora") sobre documentación en Markdown con front-matter y adopción de SDD.

## Contexto

ADR-0004 define el flujo (HU → TCs → arquitectura → subtareas → código), y quedaba pendiente decidir
con qué disciplina y en qué archivos se documenta cada fase, de forma que sea legible para humanos y
parseable por el orquestador sin depender de JSON. Se evaluó adoptar **Spec-Driven Development (SDD)**
como metodología: la generación de código ("vibecoding") se hace siempre contra una especificación
concreta, no un prompt suelto — y da un marco citable para la tesis.

## Decisión

Se adopta SDD como metodología para las fases de especificación/diseño/planeación del flujo. Cada HU
tiene una carpeta con estos archivos, todos en Markdown con front-matter YAML (estado/fase parseable,
cuerpo legible):

| Archivo | Fase de ADR-0004 (extendida por ADR-0007) | Contenido |
|---|---|---|
| `spec.md` | Lectura de HU + criterios | HU, escenarios, criterios de aceptación |
| `test-cases.md` | Generación de TCs | TCs derivados de los criterios |
| `plan.md` | Diseño de arquitectura | Plan técnico para esta HU, a partir del diagnóstico de avance |
| `tasks.md` | Descomposición en subtareas | Lista de subtareas planeadas (solo lo pendiente, ADR-0007) |
| `subtareas/ST-0N.md` | Desarrollo por subtarea | Seguimiento de ejecución: PR, estado, rondas de revisión |
| `evidencia/*.md` | Diagnóstico inicial y smoke testing | Resultado de cada corrida de TCs (ADR-0006, ADR-0007) |

## Consecuencias

- Ningún componente del sistema depende de JSON para su estado operativo; todo es Markdown con
  front-matter, versionable y legible directamente.
- El historial de `git log` sobre estos archivos es, por construcción, la auditoría de cada transición
  de fase — no se necesita un mecanismo de logging aparte para eso.
- SDD da un marco metodológico citable para la sección de metodología de la tesis.
- Sigue abierto (ver ADR-0009): de dónde viene la HU que origina el `spec.md` de cada carpeta — esta
  carpeta es el espacio de trabajo *del sistema*, no necesariamente la fuente original de la HU.
