# ADR-0025: Verificar que el despliegue se completó antes de ejecutar smoke tests

## Estado

Aceptada. Se inserta entre el gate `RONDA` (ADR-0023) y la invocación de `skills/08-smoke-testing.md`.

## Contexto

El gate `RONDA` (ADR-0023) determina cuándo todas las subtareas de una ronda están **fusionadas** a la
rama base. Pero fusionar código no significa que el ambiente de desarrollo configurado (ADR-0005) ya lo
refleje: normalmente existe un pipeline de build/despliegue entre el merge y que el cambio esté
realmente sirviendo en el ambiente — y eso toma tiempo, no es instantáneo. Ejecutar smoke testing antes
de que el despliegue termine produciría fallos falsos (ambiente desactualizado, no un error real del
código).

## Decisión

Antes de invocar `skills/08-...md`, el orquestador verifica explícitamente que el ambiente de
desarrollo ya refleja los cambios recién fusionados de la ronda en curso. El mecanismo concreto de esa
verificación (sondear un endpoint de versión/health-check, esperar un webhook de despliegue, consultar
el estado del pipeline de CI/CD del Proyecto, etc.) queda como decisión de implementación — lo que fija
esta ADR es que el chequeo **debe existir como paso explícito**, no asumirse con una espera arbitraria
de tiempo fijo.

## Consecuencias

- Se agrega un paso "verificar despliegue" entre `RONDA` y `SMOKE` en el
  [diagrama 01](../diagramas/01-flujo-pipeline-hu-a-desarrollo.md).
- Reduce falsos negativos de smoke testing causados por un ambiente todavía no actualizado, no por
  errores reales de código.
- La configuración de Proyecto (ADR-0009/0017) eventualmente necesita un dato más: cómo verificar que
  el despliegue terminó (endpoint de salud/versión, integración con el sistema de CI/CD, etc.) —
  pendiente de detallar, es información de configuración adicional, no parte de este ADR.
- Si la verificación de despliegue nunca se completa (falla el pipeline de CI/CD, por ejemplo), hace
  falta un umbral de espera máxima antes de escalar a un humano — mismo tipo de pendiente de "límite
  antes de escalar" ya señalado en otras skills.
