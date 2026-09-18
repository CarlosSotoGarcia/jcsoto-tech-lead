# ADR-0034: Fases de desarrollo agrupando las skills, y configuración mínima por fase

## Estado

Aceptada. Concreta el "modo selectivo" de [ADR-0014](0014-modo-de-arranque-de-proyecto-y-ejecucion-selectiva-por-fase.md):
antes quedaba abierto *qué* config exige cada fase para poder correrse sola. Cambia además el
criterio de "Proyecto activo" en la plataforma (ver Consecuencias).

## Contexto

Las 9 skills de fase se diseñaron como una secuencia, pero ADR-0014 ya establecía que el orquestador
puede despachar una sola fase bajo demanda, no siempre el flujo completo. Faltaba responder: si alguien
quiere correr *solo* descubrimiento hoy, ¿qué de la configuración de Proyecto (ADR-0017) le hace falta
tener lista, y qué puede quedar pendiente para más adelante? Sin esta respuesta, la plataforma no podía
distinguir "el Proyecto está listo para arrancar" de "el Proyecto está completo" — y terminaba exigiendo
todo de una vez, contradiciendo la idea de ir capturando la configuración por fase de desarrollo.

## Decisión

Las 9 skills se agrupan en **4 fases de desarrollo** (a la manera de un ciclo de vida clásico:
Requerimientos, Diseño, Desarrollo, Implementación), cada una con su propia configuración mínima:

| Fase | Skills que la implementan | Config que exige | Config que NO exige todavía |
|---|---|---|---|
| **1. Requerimientos** | 01 Descubrimiento | Fuente de HUs (tipo, URL/carpeta, credenciales) | Repos objetivo, repositorio de control, cuenta de desarrollo, ambiente, cuentas de prueba |
| **2. Diseño** (Arquitectura, Casos de Uso) | 02 TCs, 03 Diagnóstico, 04 Arquitectura | Repositorio de control (escribe `test-cases.md`/`plan.md`) + repos objetivo (03 y 04 analizan código, ADR-0018) + **ambiente de desarrollo** (03 corre los TCs contra él, ADR-0007) + cuentas de prueba por rol (ADR-0016) + modo de arranque (ADR-0014) | Cuenta de desarrollo (nada de commits/PRs todavía) |
| **3. Desarrollo** (Code, Code Review) | 05 Descomposición, 06 Código, 07 Revisión | Repositorio de control + repos objetivo + **cuenta de desarrollo** (push/PR, ADR-0013) | — |
| **4. Implementación** (incluye validar con Test/Smoke Test que la implementación quedó bien) | Orquestador (gate de revisión manual, merge, verificación de deploy — ADR-0015, ADR-0025) + 08 Smoke testing + 09 Fixes si algo falla | Cuenta de desarrollo (merge) + lista de aprobadores si aplica + ambiente de desarrollo + cuentas de prueba + repositorio de control (`evidencia/`) | — |

No hay una skill de fase para "Implementación" — el merge y la verificación de despliegue los hace el
orquestador directamente, no una de las 9 skills.

## Consecuencias

- **Activar un Proyecto en la plataforma deja de exigir toda la configuración de una vez** — solo
  exige lo mínimo de la Fase 1 (fuente de HUs). Repos objetivo, repositorio de control, cuenta de
  desarrollo y ambiente pasan a ser campos capturables en cualquier momento, sin bloquear el arranque.
  Esto reemplaza el criterio de completitud que tenía la plataforma (ver
  `especificacion-plataforma-telar.md` RF-01 a RF-09) — activar ya no significa "todo listo", significa
  "listo para al menos la fase 1".
- Cuando el orquestador (o la plataforma) despache una fase posterior (2, 3 o 4) sobre un Proyecto que
  no tiene la config de ESA fase, debe fallar con un mensaje específico de qué le falta a esa fase — no
  con el checklist completo del Proyecto.
- Refuerza que el diagnóstico (skill 03) es parte de "Diseño", no de "Test": corre antes de decidir la
  arquitectura, para saber qué ya está cubierto (ADR-0007) — aunque necesite el ambiente de desarrollo,
  igual que Test.
- Pendiente: cuando existan más acciones por fase en la plataforma (más allá de "Descubrir HUs"), cada
  una debe implementar su propia validación de prerrequisitos, replicando el patrón de
  `validar_completo_si_activo` pero acotado a su fase, no reutilizando un único gate global.
