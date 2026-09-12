# Diagrama — flujo de una HU a través del pipeline

Flujo end-to-end por historia de usuario, según [ADR-0004](../decisiones/0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md).
Incluye los dos ciclos del sistema: revisión de código (hasta que un PR queda limpio) y smoke testing
(hasta que los TCs de la subtarea pasan).

```mermaid
flowchart TD
    HU["Historia de usuario\n+ criterios de aceptación"]
    TC["Generar casos de prueba (TCs)"]
    ARQ["Diseñar arquitectura de la solución"]
    SUB["Descomponer en subtareas"]
    DEV["Generar código de la subtarea"]
    PR["Abrir Pull Request"]
    CR{"Revisión de código"}
    APLICA["Aplicar observaciones\nsubir nueva versión"]
    MERGE["Merge a develop"]
    SMOKE["Ejecutar smoke tests\n(Playwright, contra ambiente dev)"]
    RESULT{"¿TCs de la subtarea\nen verde?"}
    FIXSUB["Generar subtarea de fix"]
    DONE["Subtarea completa"]
    ALL{"¿Todas las subtareas\nde la HU completas?"}
    HUDONE["HU completa"]

    HU --> TC --> ARQ --> SUB --> DEV --> PR --> CR
    CR -- hay observaciones --> APLICA --> CR
    CR -- sin observaciones --> MERGE --> SMOKE --> RESULT
    RESULT -- sí --> DONE --> ALL
    RESULT -- no --> FIXSUB --> DEV
    ALL -- no --> DEV
    ALL -- sí --> HUDONE
```

## Notas

- El ciclo de revisión de código (`CR` ↔ `APLICA`) se repite hasta que un PR no tiene observaciones
  pendientes — solo entonces avanza a `MERGE`.
- El ciclo de smoke testing (`RESULT` → `FIXSUB` → `DEV`) genera una subtarea de fix nueva, que
  atraviesa de nuevo generación de código, PR y revisión — no se edita directamente el código ya
  fusionado.
- `ALL` es el criterio de cierre de la HU: todas sus subtareas con PR fusionado y smoke tests en verde.
- Pendiente de ADR: cómo se decide qué subconjunto de TCs vuelve a correr tras un fix (¿solo los que
  fallaron, o todos los de la subtarea?).
