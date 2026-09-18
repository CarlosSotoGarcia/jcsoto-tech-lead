# ADR-0036: El ambiente de desarrollo se pide hasta Fase 4, no en Fase 2

## Estado

Aceptada. Corrige la tabla de configuración mínima de [ADR-0034](0034-fases-de-desarrollo-y-configuracion-minima-por-fase.md):
el ambiente de desarrollo dejaba de pedirse en Fase 2 y en Fase 4 a la vez — se queda solo en Fase 4.

## Contexto

ADR-0034 exigía el ambiente de desarrollo tanto en Fase 2 (Diseño: para que la skill 03 —
diagnóstico — corra los TCs contra el estado actual, ADR-0007) como en Fase 4 (Implementación: para
smoke testing de HUs ya terminadas, ADR-0006). En la práctica esto bloqueaba de forma artificial la
Fase 2 completa:

- La skill 02 (generación de TCs, ya implementada) no usa el ambiente para nada — solo lee
  `spec.md` y genera casos de prueba.
- Para `modo_arranque: nuevo` no puede existir un ambiente real todavía (no hay código que
  desplegar) — pedirlo ahí es un problema de huevo y gallina, no una casilla olvidada.
- El uso real y concreto del ambiente — evaluar cambios ya aplicados de HUs terminadas (smoke
  testing) — ocurre en **Fase 4**, no en Fase 2.

## Decisión

El ambiente de desarrollo se exige **únicamente en Fase 4** (Implementación). Fase 2 deja de
pedirlo por completo, para cualquier `modo_arranque`:

| Fase | Config mínima (corrige ADR-0034) |
|---|---|
| 2. Diseño | Repos objetivo — el ambiente ya **no** es prerrequisito aquí. |
| 3. Desarrollo | Repos objetivo + cuenta de desarrollo. |
| 4. Implementación | Cuenta de desarrollo + **ambiente de desarrollo** + cuentas de prueba (pendiente de implementar) + repositorio de control (ya no aplica, ADR-0035). |

Cuando se implemente la skill 03 (diagnóstico), es responsabilidad de esa skill validar por su
cuenta si tiene un ambiente configurado antes de intentar correr TCs contra él — el mismo patrón
que ya usan las skills 01 y 02 (cada una valida sus propios prerrequisitos al invocarse, ADR-0034
"Pendiente"), no un gate global de fase. Si no hay ambiente configurado, la skill 03 puede saltarse
sin bloquear el resto de la Fase 2 (coherente con el caso greenfield de ADR-0007: sin ambiente que
diagnosticar, todos los criterios quedan pendientes igual, sin necesidad de intentar una conexión
real).

## Consecuencias

- `models/proyecto.py`: `fases_configuradas` dejar de acoplar Fase 2 y Fase 4 al mismo campo — cada
  una se evalúa con su propio requisito, en cascada (Fase 2 → Fase 3 → Fase 4).
- Deja sin efecto la distinción por `modo_arranque` que se había considerado para este mismo
  problema — ya no hace falta: el ambiente simplemente no es parte de la Fase 2 para ningún modo.
- Cuando se implemente la skill 03, debe manejar la ausencia de ambiente configurado como una
  validación propia (mensaje claro, no un crash), no asumir que el gate de la plataforma ya la
  garantizó.

## Pendiente

- Igual que ADR-0034 ya dejaba pendiente: cuando existan más acciones por fase en la plataforma,
  cada una implementa su propia validación de prerrequisitos — esto aplica también a la futura
  skill 03 respecto al ambiente de desarrollo.
