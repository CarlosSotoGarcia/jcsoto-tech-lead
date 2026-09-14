# ADR-0010: Agregar GitHub (Issues) como tercera fuente de historias de usuario

## Estado

Aceptada. Extiende [ADR-0009](0009-proyecto-como-entidad-de-configuracion-y-fuente-de-hus-pluggable.md),
no lo reemplaza.

## Contexto

ADR-0009 dejó la fuente de HUs como pluggable, con Jira y Markdown como las dos implementadas
inicialmente. El sistema de todas formas necesita operar sobre GitHub para generación de código y PRs
(ADR-0004) cuando los repos objetivo viven ahí — reutilizar esa misma superficie para leer HUs evita una
integración y autenticación adicionales. Además, los propios repositorios públicos del autor (ver
`itz/documentación/`) son un caso de validación real y ya disponible con esta fuente.

## Decisión

Se agrega `github` como tercer valor de `fuente_tipo` (junto a `jira` y `markdown`, ADR-0009). El
adaptador de GitHub lee Issues del repositorio configurado como origen de HUs, y resuelve la jerarquía
épica → tarea → subtarea (ADR-0009) de dos formas posibles, según lo que use el repositorio:

- **Sub-issues nativos** de GitHub (relación padre/hijo entre issues), cuando el repositorio los usa.
- **Labels/milestones** como convención de respaldo (p. ej. un label `epic` y otro `subtarea`, o el
  milestone como agrupador), cuando el repositorio no usa sub-issues.

## Consecuencias

- No agrega superficie de autenticación nueva cuando el Proyecto ya usa GitHub para sus repos (ADR-0005)
  — las mismas credenciales sirven para leer Issues y para abrir/gestionar PRs.
- Los repositorios propios y públicos del autor quedan disponibles como candidatos de validación con
  esta fuente, sin depender de acceso a un Jira ajeno.
- Pendiente de definir (mismo tipo de trabajo que ya estaba pendiente para Jira en ADR-0009): mapeo
  exacto de campos de un Issue de GitHub (título, cuerpo, labels, sub-issues) al `spec.md` interno, y
  qué convención de labels/milestones se asume cuando no hay sub-issues nativos.
- Refuerza que el skill de descubrimiento y especificación de HU (`skills/01-...md`) debe tratar el
  contenido de un Issue de GitHub con el mismo criterio de "analista de requerimientos" que ya aplica a
  Jira y Markdown — un Issue puede llegar tan incompleto o ambiguo como un ticket de Jira.
