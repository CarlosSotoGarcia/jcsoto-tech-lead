# Orquestador

No es una skill de fase como las demás (01-09): es el **despachador** que decide, para cada HU o
paquete de trabajo, cuál de esas 9 skills invocar a continuación — ninguna skill de fase llama a otra
directamente, siempre pasan por aquí (ver notas del [diagrama 02](../diagramas/02-skill-orquestador-y-skills-por-fase.md)).

## Propósito

Mantener el estado de cada HU/paquete de trabajo de un Proyecto y decidir, en cada momento, qué skill de fase
ejecutar — ya sea siguiendo el flujo secuencial completo (comportamiento por defecto, ADR-0004) o
despachando una sola fase bajo demanda (modo selectivo, ADR-0014). El orquestador **no hace el trabajo
especializado él mismo** (eso lo hacen las 9 skills) — solo lee estado, decide, despacha, y aplica los
gates que no son responsabilidad de ninguna skill de fase (revisión manual, merge).

## De dónde lee el estado

El orquestador **no mantiene una base de datos propia** — el estado ya vive en el front-matter de los
archivos SDD (`spec.md`, `test-cases.md`, `plan.md`, `tasks.md`, `paquetes/*.md`, `evidencia/*.md`,
ADR-0008) dentro del repositorio de control del Proyecto (ADR-0012). Para decidir el siguiente paso de
una HU o paquete de trabajo, el orquestador simplemente lee el campo `fase`/`estado` correspondiente.

## Tabla de transición (modo secuencial, por defecto)

| Fase/estado actual | Skill que despacha | Fase/estado resultante |
|---|---|---|
| (HU no descubierta) | `01` descubrimiento y especificación | `especificada` |
| `especificada` | `02` generación de TCs | `tcs_generados` |
| `tcs_generados` | `03` diagnóstico de avance existente | `diagnosticada` |
| `diagnosticada`, con TCs `pendiente` | `04` diseño de arquitectura | `planificada` |
| `diagnosticada`, todos los TCs `cubierto` | — | HU completa directo |
| `planificada` | `05` descomposición en paquetes de trabajo | `descompuesta` (crea N paquetes de trabajo `pendiente`, `ronda: 1`) |
| paquete de trabajo `pendiente` (sin `depende_de` sin resolver) | `06` generación de código | paquete de trabajo `en_revision` |
| paquete de trabajo `en_revision` | `07` revisión de código | con observaciones → vuelve a `06`; sin observaciones → gate de merge (ver abajo) |
| PR aprobado por `07` | *(el propio orquestador, ADR-0015)* | si `requiere_revision_manual`: espera aprobación humana; si no: merge directo → paquete de trabajo `fusionado` |
| paquete de trabajo `fusionado` | *(el propio orquestador, gate `RONDA`, ADR-0023)* | si quedan paquetes de trabajo de la misma `ronda` sin fusionar: espera (no se dispara `08`); si todos fusionados: pasa al gate `DEPLOY` |
| todos los paquetes de trabajo de la ronda `fusionado` | *(el propio orquestador, gate `DEPLOY`, ADR-0025)* | si el ambiente dev todavía no refleja el cambio: espera; si ya lo refleja: dispara `08` |
| ambiente dev actualizado | `08` smoke testing (todos los TCs de la HU) | todos pasan → HU y sus paquetes de trabajo quedan `completo`; alguno falla → `09` |
| TC fallido en smoke testing | `09` generación de fixes | crea paquete(s) de trabajo `tipo: fix` en `pendiente`, nueva `ronda` → vuelve a `06` |
| HU `completa` | — | fin |

**Camino reducido para Actividades (ADR-0026):** si `skills/01-...md` clasifica el elemento como
`clasificacion: actividad` (sin criterios de aceptación verificables), el orquestador salta `02` y `03`
directo a `04` (diseño/plan) → `05` (descomposición en paquetes de trabajo) → `06`/`07` (código y
revisión) → merge. Como no hay TCs asociados, tras el merge **no** se pasa por `RONDA`/`DEPLOY`/`08` —
la Actividad se marca completa directo al fusionarse, sin smoke testing.

## Responsabilidades que no son de ninguna skill de fase

- **El gate de revisión manual** (ADR-0015): tras la aprobación de `07`, el orquestador consulta
  `requiere_revision_manual` en la configuración del Proyecto. Si es `true`, deja el paquete de trabajo esperando
  la aprobación de alguno de los `usuarios_autorizados_a_aprobar` antes de continuar.
- **El merge en sí**: ninguna de las 9 skills lo ejecuta explícitamente — es el orquestador quien lo
  realiza (con la cuenta de desarrollo, ADR-0013), una vez que `07` aprobó y, si aplica, la revisión
  manual quedó satisfecha.
- **El gate `RONDA`** (ADR-0023): tras cada merge, el orquestador compara cuántos paquetes de trabajo
  tiene la ronda en curso (`tasks.md`) contra cuántos ya están `fusionado`. Solo cuando coinciden pasa
  al gate `DEPLOY` — ni la descomposición original ni una tanda de fixes disparan smoke testing por un
  paquete de trabajo suelto.
- **El gate `DEPLOY`** (ADR-0025): antes de despachar `08`, el orquestador verifica que el ambiente de
  desarrollo ya sirve el código recién fusionado — fusionar no es lo mismo que desplegar. El mecanismo
  concreto de verificación es detalle de implementación (ADR-0025).

## Modo selectivo (Proyecto en modo `avanzado`, ADR-0014)

En vez de determinar automáticamente la siguiente fase según la tabla de transición, el orquestador
puede recibir una invocación explícita: "ejecutar la skill X sobre estas HUs/paquetes de trabajo" (p.
ej. "solo `07` sobre todos los paquetes de trabajo en `en_revision`", o "solo `08` sobre los ya
fusionados"). En este modo:

- No se sigue la secuencia completa — se ejecuta únicamente lo pedido, actualizando el estado igual que
  en modo secuencial.
- Requiere que la HU/paquete de trabajo objetivo ya tenga los archivos SDD que la skill pedida necesita como
  entrada (p. ej. no se puede pedir "solo revisión de código" sobre algo que nunca tuvo `plan.md`) — si
  no existen porque el trabajo se hizo fuera de Telar antes de adoptarlo, hace falta reconstruirlos
  primero (pendiente, ver ADR-0014).
- Cada fase exige solo *su propia* configuración de Proyecto, no toda — las 9 skills se agrupan en 4
  fases de desarrollo (Requerimientos, Diseño, Desarrollo, Implementación) con su config mínima
  documentada en [ADR-0034](../decisiones/0034-fases-de-desarrollo-y-configuracion-minima-por-fase.md).
  Si se pide despachar una fase sin su config lista, el orquestador falla señalando específicamente qué
  le falta a esa fase, no un checklist del Proyecto completo.

## Modo fundacional (Proyecto en modo `nuevo`, ADR-0014)

Antes de procesar la primera HU de un repositorio objetivo vacío, el orquestador despacha `04` en su
modo fundacional (una sola vez por repositorio, no por HU) para establecer la arquitectura base.

## ADRs relacionados

Prácticamente todos — el orquestador es el punto donde convergen: [ADR-0004](../decisiones/0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md),
[ADR-0005](../decisiones/0005-solucion-configurable-repositorios-y-ambiente-dev.md),
[ADR-0008](../decisiones/0008-adopcion-de-sdd-y-nombres-de-artefactos.md),
[ADR-0009](../decisiones/0009-proyecto-como-entidad-de-configuracion-y-fuente-de-hus-pluggable.md),
[ADR-0012](../decisiones/0012-plataforma-de-visualizacion-y-reportes.md),
[ADR-0013](../decisiones/0013-cuenta-de-desarrollo-dedicada-para-acceso-a-repositorios.md),
[ADR-0014](../decisiones/0014-modo-de-arranque-de-proyecto-y-ejecucion-selectiva-por-fase.md),
[ADR-0015](../decisiones/0015-revision-manual-opcional-antes-de-merge.md),
[ADR-0020](../decisiones/0020-smoke-testing-corre-todos-los-tcs-como-regresion.md),
[ADR-0022](../decisiones/0022-repos-fuera-de-configuracion-o-de-alcance.md),
[ADR-0023](../decisiones/0023-smoke-testing-espera-a-toda-la-hu-no-por-subtarea.md),
[ADR-0024](../decisiones/0024-creacion-de-subtareas-en-la-fuente-via-mcp.md),
[ADR-0025](../decisiones/0025-verificacion-de-despliegue-antes-de-smoke-testing.md),
[ADR-0026](../decisiones/0026-vocabulario-unificado-hu-actividad-paquete-de-trabajo.md),
[ADR-0028](../decisiones/0028-ciclo-automatizado-de-calidad-como-mecanismo-suficiente.md),
[ADR-0029](../decisiones/0029-orden-secuencial-de-paquetes-de-trabajo-dependientes.md),
[ADR-0030](../decisiones/0030-paralelismo-entre-hus-con-dependencias.md).

## Criterios de éxito

Toda HU/paquete de trabajo de un Proyecto activo tiene, en todo momento, una fase/estado consistente con los
archivos SDD que existen para ella; el orquestador nunca despacha una skill cuya entrada no está
disponible; el merge solo ocurre cuando corresponde según `07` y, si aplica, la aprobación manual.

## Pendientes propios del orquestador

- Mecanismo de reconstrucción de `spec.md`/`plan.md`/`tasks.md` para HUs/paquetes de trabajo que ya existían
  antes de adoptar Telar (modo `avanzado`, ADR-0014) — bloquea que el modo selectivo funcione sobre
  trabajo preexistente.
- Qué framework de agentes implementa al orquestador y a las skills (Claude Code Skills u otra
  alternativa) — pendiente general desde el inicio de `00-vision-general.md`.
- ~~Orden/paralelismo de paquetes de trabajo con `depende_de`~~ — resuelto en
  [ADR-0029](../decisiones/0029-orden-secuencial-de-paquetes-de-trabajo-dependientes.md): secuencial
  estricto, nunca en paralelo.
- ~~Si el orquestador procesa una HU a la vez o puede paralelizar~~ — resuelto en
  [ADR-0030](../decisiones/0030-paralelismo-entre-hus-con-dependencias.md): puede procesar varias HUs
  del mismo Proyecto en paralelo, salvo que una declare `depende_de` sobre otra a nivel HU.
- Cómo se declara `depende_de` entre HUs cuando la fuente no lo modela explícitamente (Jira sí tiene
  "issue links"; Markdown probablemente necesite declararlo a mano). *(ADR-0030)*
