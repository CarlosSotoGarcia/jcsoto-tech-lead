# ADR-0002: La infraestructura de indexación se documenta a nivel de diseño, no se despliega ni se opera

## Estado

Aceptada

## Contexto

El planteamiento original (ver propuesta aprobada y `00-vision-general.md` en su versión inicial)
incluía construir una infraestructura de indexación multi-repositorio y validarla empíricamente
operando sobre varios sistemas reales. Los asesores acotaron el alcance: el proyecto se evalúa por su
diseño e implementación del *skill*, no por operar infraestructura.

## Decisión

La indexación multi-repositorio se documenta a nivel de diseño (arquitectura, ADRs, diagramas), pero no
se despliega ni se opera como infraestructura persistente/productiva. La validación del sistema se hace
ejecutando el skill de forma puntual contra repositorios de prueba, no manteniendo un servicio de
indexación corriendo de forma continua.

## Consecuencias

- Queda fuera de alcance el trabajo de ingeniería de despliegue y operación (contenedores,
  orquestación, monitoreo de infraestructura) que antes implicaba "validar en producción".
- Mitiga directamente el riesgo de "tiempo limitado (proyecto ya en prórroga)" identificado en la
  propuesta.
- La evaluación sigue siendo posible: el skill puede ejecutarse ad hoc contra cada repositorio de
  validación sin necesitar infraestructura corriendo de forma permanente.
- El objetivo específico "diseñar un mecanismo de indexación multi-repositorio" se mantiene, pero se
  entiende como diseño, no como sistema desplegado.
