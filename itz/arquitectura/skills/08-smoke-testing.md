# Skill — Smoke testing

**Alias en diagramas:** `S6` en [diagrama 02](../diagramas/02-skill-orquestador-y-skills-por-fase.md).

## Propósito

Confirmar, contra el ambiente de desarrollo real, que una HU completa no rompe nada — no basta con que
cada PR haya pasado revisión de código (`skills/07-...md`), hace falta validar el comportamiento del
código ya integrado. **Es el mismo motor de ejecución de TCs que
`skills/03-diagnostico-de-avance-existente.md`** (Playwright, cuentas de prueba por rol — ADR-0016);
esta ficha documenta solo lo que es distinto: cuándo se invoca y qué pasa con el resultado. Para el
mecanismo de ejecución en sí, ver `skills/03-...md`.

## Cuándo se invoca

**No por cada paquete de trabajo fusionado** — se dispara cuando **todos los paquetes de trabajo de la ronda en curso**
(la descomposición original de `skills/05-...md`, o la tanda de fixes más reciente de
`skills/09-...md`) llegan a `estado: fusionado` (ADR-0023). El gate `RONDA` del
[diagrama 01](../diagramas/01-flujo-pipeline-hu-a-desarrollo.md) es responsabilidad del orquestador
(`skills/00-...md`), no de esta skill — esta skill solo se ejecuta una vez que el orquestador determina
que ya toca.

Correr smoke testing con paquetes de trabajo de la misma ronda todavía sin fusionar produciría fallos que no son
errores reales, solo trabajo incompleto (ADR-0023) — de ahí la espera. Además, el orquestador verifica
primero que el ambiente de desarrollo ya sirve el código recién fusionado (ADR-0025) — fusionar no es
lo mismo que desplegar; sin esa verificación, esta skill podría correr contra un ambiente todavía
desactualizado.

## Entradas

- **Todos los TCs de `test-cases.md` de la HU** (ADR-0020): cada corrida es una prueba de regresión
  completa, no una verificación puntual de un cambio aislado.
- Configuración del Proyecto: URL del ambiente de desarrollo (ADR-0005) y cuentas de prueba por rol
  (ADR-0016).

## Salidas

- `evidencia/smoke-0N.md` (numerado por corrida — mismo formato que `evidencia/diagnostico-01.md` de
  `skills/03-...md`, con `tipo: smoke`). Junto con las corridas anteriores, es el historial de
  regresión de la HU (ADR-0020), no solo evidencia de una corrida aislada.
- Si todos los TCs pasan: la HU se marca completa (y, con ella, todos sus paquetes de trabajo fusionados
  pasan de `fusionado` a `completo`).
- Si alguno falla: señala al orquestador para que dispare la skill de generación de fixes
  (`skills/09-...md`), que arranca una nueva ronda — ver el ciclo `RESULT → FIXSUB → DEV` del
  [diagrama 01](../diagramas/01-flujo-pipeline-hu-a-desarrollo.md).

## Qué hace (alto nivel)

Idéntico al mecanismo de `skills/03-...md` (generar script Playwright por TC, ejecutar con la cuenta de
prueba del rol correspondiente, registrar resultado y evidencia), aplicado sobre **todos los TCs de la
HU** una vez que el orquestador confirma que la ronda en curso está completa (ADR-0023).

## Estado de implementación

Implementada — [ADR-0059](../decisiones/0059-smoke-testing-por-hu-con-script-generado-desde-el-codigo.md): la IA lee el código del frontend y escribe un script de
Playwright por HU; se valida y ejecuta en un proceso aparte con cuentas de prueba por rol; un agente de navegador verifica los fallos; las corridas quedan como regresión repetible sin IA.
Sin generación de fixes (skill 09) ni verificación del despliegue (ADR-0025) todavía.

## ADRs relacionados

- [ADR-0059](../decisiones/0059-smoke-testing-por-hu-con-script-generado-desde-el-codigo.md) — implementación.

- [ADR-0004](../decisiones/0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md) — smoke
  testing como fase posterior al merge.
- [ADR-0006](../decisiones/0006-smoke-tests-con-playwright-y-bitacora-de-hus.md) — Playwright como
  motor de ejecución.
- [ADR-0007](../decisiones/0007-soporte-proyectos-con-avance-previo.md) — mismo mecanismo que el
  diagnóstico de avance.
- [ADR-0016](../decisiones/0016-cuentas-de-prueba-por-rol-para-ejecucion-de-tcs.md) — selección de
  cuenta de prueba por rol.
- [ADR-0020](../decisiones/0020-smoke-testing-corre-todos-los-tcs-como-regresion.md) — alcance completo
  (todos los TCs de la HU) y versionado de cada corrida como regresión.
- [ADR-0023](../decisiones/0023-smoke-testing-espera-a-toda-la-hu-no-por-subtarea.md) — disparador por
  ronda completa, no por paquete de trabajo individual.
- [ADR-0025](../decisiones/0025-verificacion-de-despliegue-antes-de-smoke-testing.md) — el orquestador
  verifica que el ambiente ya refleja el cambio antes de invocar esta skill.
- [ADR-0026](../decisiones/0026-vocabulario-unificado-hu-actividad-paquete-de-trabajo.md) — vocabulario
  "paquete de trabajo".

## Criterios de éxito

Cada TC de la HU tiene un resultado registrado (pasa/falla) con evidencia en la corrida más reciente, y
el resultado agregado decide correctamente si la HU queda completa o se dispara una nueva ronda de fix.

## Pendientes propios de esta skill

Comparte los pendientes de `skills/03-...md` (umbral falla vs. error técnico, TC sin rol configurado).
Específico de esta skill:

- Si un TC falla en smoke testing pero había pasado en una corrida anterior (regresión introducida por
  el propio cambio) — ¿se trata igual que cualquier TC fallido, o amerita una señal distinta (algo se
  rompió, no que algo nunca se hizo)? Se vuelve más relevante ahora que cada corrida es comparable
  contra la anterior (ADR-0020).
- Cómo se representa en el front-matter de `evidencia/smoke-0N.md` la comparación contra la corrida
  anterior (ADR-0020, pendiente).
