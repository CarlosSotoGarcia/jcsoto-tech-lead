# ADR-0015: Cuenta de desarrollo declarada explícitamente + revisión manual opcional antes de merge

## Estado

Aceptada. Concreta un pendiente de [ADR-0013](0013-cuenta-de-desarrollo-dedicada-para-acceso-a-repositorios.md)
y extiende el flujo de [ADR-0004](0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md)
y [ADR-0011](0011-supuestos-no-bloquean-se-resuelven-en-revision-de-codigo.md), sin reemplazarlos.

## Contexto

ADR-0013 ya decidió que el sistema opera con una cuenta de desarrollo dedicada, pero dejó pendiente
cómo se provee esa credencial. Además, aunque la skill de revisión de código (S5, ADR-0011) puede
aprobar un PR automáticamente cuando no hay observaciones ni supuestos sin resolver, algunos Proyectos
van a necesitar que una persona dé el visto bueno final antes de que el código llegue a `develop` —
sobre todo mientras se gana confianza en el sistema, o en repositorios sensibles.

## Decisión

1. La cuenta/credencial de desarrollo (ADR-0013) se **declara explícitamente** al dar de alta un
   Proyecto — no se infiere ni se crea por default.
2. La configuración de Proyecto (ADR-0009) incluye:
   - `requiere_revision_manual` (booleano): si un PR necesita aprobación humana además de la de la
     skill de revisión de código (S5).
   - `usuarios_autorizados_a_aprobar`: la lista de identidades humanas con permiso de dar ese visto
     bueno final, cuando `requiere_revision_manual` es `true`.
3. El flujo (ver [diagrama 01](../diagramas/01-flujo-pipeline-hu-a-desarrollo.md), a actualizar) gana un
   paso condicional entre "S5 aprueba sin observaciones" y `MERGE`:
   - Si `requiere_revision_manual` es `false`: se fusiona automáticamente en cuanto S5 aprueba (igual
     que hasta ahora).
   - Si es `true`: el PR espera la aprobación de alguno de los `usuarios_autorizados_a_aprobar` antes
     de fusionarse.

## Aclaración

`requiere_revision_manual` no es una decisión fija al dar de alta el Proyecto — es un flag que se puede
alternar en el tiempo según cómo cambien las necesidades del Proyecto (p. ej. exigirlo al principio
mientras el equipo gana confianza en el sistema, y desactivarlo más adelante).

`usuarios_autorizados_a_aprobar` se administra desde la plataforma de Telar (ADR-0012) — es una acción
de configuración/administración del Proyecto, no una acción sobre el pipeline en ejecución. Esto no
contradice que la plataforma sea "de solo lectura respecto al pipeline" (ADR-0012): esa restricción
aplica al estado de HUs/subtareas en curso, no a la configuración del Proyecto, que sí es administrable
desde ahí.

## Consecuencias

- La aprobación de S5 deja de ser sinónimo universal de "listo para merge": ahora significa "listo
  para merge, o listo para revisión humana final", según la configuración del Proyecto.
- Es el mecanismo concreto que faltaba para el principio ya establecido en `00-vision-general.md`
  ("una persona puede intervenir en cualquier fase"), aplicado específicamente al punto de merge.
- Pendiente de definir: si un supuesto sin resolver (ADR-0011) llega hasta este punto, ¿la revisión
  manual se vuelve obligatoria automáticamente sin importar `requiere_revision_manual`? Parece
  razonable, pero no está decidido.
- Pendiente: si `usuarios_autorizados_a_aprobar` aplica a nivel Proyecto completo o se puede afinar por
  repositorio o tipo de subtarea.
- Pendiente: mecanismo de notificación a esos usuarios — queda fuera del diseño de arquitectura, es
  detalle de implementación.
