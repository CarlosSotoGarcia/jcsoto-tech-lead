# Skill — Diagnóstico de avance existente

**Alias en diagramas:** `S1B` en [diagrama 02](../diagramas/02-skill-orquestador-y-skills-por-fase.md).

## Propósito

Ejecutar los TCs de `test-cases.md` contra el estado **actual** del ambiente de desarrollo, antes de
diseñar o descomponer nada, para distinguir qué criterios de aceptación ya están cubiertos (proyecto
con avance previo, ADR-0007) de los que realmente faltan. Cubre greenfield como caso particular: si no
existe nada, todos los TCs fallan y todos quedan pendientes — el mecanismo es el mismo en ambos casos.

Esta skill **es el mismo motor de ejecución de TCs** que usa `smoke testing` (S6, ADR-0006) más
adelante en el flujo — se documenta aquí en detalle y `S6` solo referencia esta ficha, para no
duplicar el diseño del mecanismo (ver Notas).

## Cuándo se invoca

Cuando una HU llega a la fase `tcs_generados` (salida de `skills/02-...md`).

## Entradas

- `test-cases.md` de la HU: TCs en formato Given/When/Then.
- Configuración del Proyecto (ADR-0005): URL del ambiente de desarrollo contra el que se corren los TCs
  (los repos de código no se tocan en esta fase — ver Notas sobre acceso).

## Salidas

- `evidencia/diagnostico-01.md` (numerado por corrida), con front-matter:

```yaml
hu_id: HU-001
tipo: diagnostico
fecha: 2026-09-14
tcs_totales: 5
tcs_pasan: [TC-002, TC-004]
tcs_fallan: [TC-001, TC-003, TC-005]
```

  Cuerpo: por cada TC, resultado (pasa/falla), evidencia (captura o descripción de lo observado), y si
  falló, por qué (funcionalidad inexistente vs. comportamiento distinto al esperado).

- Actualiza `test-cases.md`: cada TC queda marcado con su estado más reciente (`cubierto` /
  `pendiente`), que es lo que lee la skill de diseño de arquitectura (siguiente en el flujo) para saber
  qué falta.
- Deja la fase de la HU en `diagnosticada`.

## Qué hace (alto nivel)

1. Lee `test-cases.md` y la URL del ambiente de desarrollo configurado (ADR-0005).
2. Por cada TC, genera un script de Playwright (Python, ADR-0006) a partir de su Given/When/Then y lo
   ejecuta contra ese ambiente, como lo haría un usuario real.
3. Registra el resultado (pasa/falla) y la evidencia correspondiente.
4. Escribe `evidencia/diagnostico-01.md` y actualiza el estado de cobertura en `test-cases.md`.
5. Deja la fase en `diagnosticada` para que el orquestador continúe con diseño de arquitectura.

## Estado de implementación

Implementada — [ADR-0060](../decisiones/0060-diagnostico-de-avance-con-agente-de-navegador.md): el agente de navegador de la skill 08 prueba los TCs contra el ambiente existente, marca
cada uno `cubierto`, `pendiente` o `sin_evaluar`, y la skill 05 solo descompone lo que falta.

## ADRs relacionados

- [ADR-0060](../decisiones/0060-diagnostico-de-avance-con-agente-de-navegador.md) — implementación.

- [ADR-0006](../decisiones/0006-smoke-tests-con-playwright-y-bitacora-de-hus.md) — Playwright como
  motor de ejecución de TCs.
- [ADR-0007](../decisiones/0007-soporte-proyectos-con-avance-previo.md) — decisión de origen de esta
  skill.
- [ADR-0008](../decisiones/0008-adopcion-de-sdd-y-nombres-de-artefactos.md) — formato de `evidencia/`.
- [ADR-0016](../decisiones/0016-cuentas-de-prueba-por-rol-para-ejecucion-de-tcs.md) — selección de
  cuenta de prueba por rol declarado en cada TC.

## Criterios de éxito

Cada TC de `test-cases.md` tiene un resultado registrado (pasa/falla) con evidencia — incluyendo los
que fallan porque la funcionalidad todavía no existe (greenfield).

## Notas sobre acceso (relevante para no confundir con la skill de generación de código)

Esta skill **no necesita acceso de escritura a los repositorios** (no genera commits, no abre PRs) —
solo necesita poder **interactuar con el ambiente de desarrollo ya desplegado** (la URL configurada en
ADR-0005) como lo haría un usuario real, con el rol que cada TC declare (`rol_requerido`, ADR-0016) —
**no** una sola cuenta genérica: la configuración del Proyecto aporta un conjunto de cuentas de prueba,
una por rol relevante de la aplicación, y esta skill selecciona la que corresponda a cada TC. Esto es,
de cualquier forma, distinto de la cuenta de desarrollo con acceso a los repos que sí va a necesitar la
skill de generación de código (`skills/06-...md`) para hacer commit, push y abrir PRs (ADR-0013) — son
credenciales con alcances distintos y no deberían mezclarse.

## Pendientes propios de esta skill

- ~~Qué hacer con TCs que no se pueden evaluar de forma aislada porque dependen de un paquete de
  trabajo que todavía no existe~~ — resuelto en
  [ADR-0027](../decisiones/0027-prototipo-como-input-complementario.md): esta skill no necesita
  distinguir la causa del fallo. Simplemente marca el TC como `pendiente`; es la descomposición
  (`skills/05-...md`), informada por el prototipo cuando existe, la que genera todos los paquetes
  necesarios en ambas capas para cubrirlo por completo.
- Umbral entre "TC falla" (la funcionalidad no cumple el criterio) y "TC no se pudo ejecutar" (error
  técnico al correr el script, ambiente caído, etc.) — ¿cuentan igual para efectos de generar un
  paquete de trabajo?
- ~~Qué credencial de prueba usa esta skill~~ — resuelto en
  [ADR-0016](../decisiones/0016-cuentas-de-prueba-por-rol-para-ejecucion-de-tcs.md): un conjunto de
  cuentas por rol, seleccionada según el `rol_requerido` de cada TC.
