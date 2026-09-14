# Skill — Generación de casos de prueba (TCs)

**Alias en diagramas:** `S1` en [diagrama 02](../diagramas/02-skill-orquestador-y-skills-por-fase.md).

## Propósito

A partir de `spec.md` (ya analizado por la skill de descubrimiento, `skills/01-...md`), generar los
casos de prueba (TCs) que verifican cada criterio de aceptación — explícito o inferido — de la HU. Los
TCs son el contrato que usan dos skills más adelante (diagnóstico de avance, ADR-0007, y smoke testing,
ADR-0006) para saber si algo "ya funciona" o "todavía falta".

## Cuándo se invoca

Cuando una HU llega a la fase `especificada` (salida de `skills/01-...md`) y no tiene supuestos sin
resolver que bloqueen continuar (ver el pendiente de la skill 01 sobre `tiene_supuestos: true`).

## Entradas

- `spec.md` de la HU: criterios de aceptación explícitos e inferidos, y cualquier supuesto ya aceptado.
- **Prototipo, si existe** (`prototipo_ref` en `spec.md`, ADR-0027): mockup, contrato de API o
  wireframe entregado como input a Telar junto con la HU. Cuando está presente, se usa junto con
  `spec.md` para generar TCs que cubran el comportamiento completo descrito, no solo lo que el texto de
  los criterios alcanza a especificar.

## Salidas

`test-cases.md`, con este contrato:

**Front-matter:**

```yaml
hu_id: HU-001
fase: tcs_generados
total_tcs: 5
fecha_generacion: 2026-09-13
```

**Cuerpo (un TC por criterio de aceptación, como mínimo):**

- **ID del TC** (p. ej. `TC-001`), y el criterio de aceptación del que se deriva (referencia directa al
  criterio en `spec.md`, explícito o inferido).
- **Escenario en formato Given/When/Then** (consistente con cómo `skills/01-...md` ya estructuró los
  criterios).
- **Tipo de verificación esperada**: por ahora, proyectos tipo web (ADR-0009) — el TC se piensa para
  ejecutarse como interacción de UI vía Playwright (ADR-0006), no como prueba unitaria de código.
- **Rol requerido** (`rol_requerido`): qué rol de la aplicación necesita la cuenta de prueba con la que
  se ejecuta este TC (p. ej. `admin`, `usuario_final`, `invitado`) — ver ADR-0016. Se infiere del
  criterio de aceptación en `spec.md` (quién realiza la acción descrita).
- **Resultado esperado** explícito (qué se debe observar si el TC pasa).

## Qué hace (alto nivel)

1. Lee `spec.md` y recorre cada criterio de aceptación (explícito e inferido).
2. Por cada criterio, deriva uno o más TCs — un criterio compuesto puede generar varios TCs si cubre
   más de un caso (camino feliz, casos límite, manejo de error), coherente con el nivel de detalle que
   la skill 01 ya dejó en el criterio.
3. Estructura cada TC en Given/When/Then con un resultado esperado verificable, pensado para que la
   skill de ejecución de TCs (diagnóstico/smoke testing) lo pueda convertir en un script de Playwright.
4. Escribe `test-cases.md` y deja la fase en `tcs_generados`.

## ADRs relacionados

- [ADR-0004](../decisiones/0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md) — TCs
  como segundo paso del flujo.
- [ADR-0006](../decisiones/0006-smoke-tests-con-playwright-y-bitacora-de-hus.md) — los TCs se ejecutan
  con Playwright (Python).
- [ADR-0007](../decisiones/0007-soporte-proyectos-con-avance-previo.md) — los mismos TCs alimentan el
  diagnóstico de avance existente, no solo el smoke testing final.
- [ADR-0008](../decisiones/0008-adopcion-de-sdd-y-nombres-de-artefactos.md) — formato de `test-cases.md`.
- [ADR-0011](../decisiones/0011-supuestos-no-bloquean-se-resuelven-en-revision-de-codigo.md) — un
  criterio con supuesto no resuelto igual genera TC; el supuesto se resuelve en revisión de código.
- [ADR-0016](../decisiones/0016-cuentas-de-prueba-por-rol-para-ejecucion-de-tcs.md) — cada TC declara
  el rol con el que debe ejecutarse.
- [ADR-0027](../decisiones/0027-prototipo-como-input-complementario.md) — el prototipo, cuando existe,
  informa la generación de TCs completos.

## Criterios de éxito

Cada criterio de aceptación de `spec.md` (explícito o inferido, no los supuestos sin resolver) tiene al
menos un TC en `test-cases.md`, en formato Given/When/Then con resultado esperado explícito.

## Pendientes propios de esta skill

- Cuántos TCs por criterio son razonables — ¿solo camino feliz, o también casos límite/error por
  defecto? Afecta directamente qué tan caro es correr el diagnóstico de avance (ADR-0007) y el smoke
  testing (ADR-0006).
- Cómo se referencia un TC de vuelta a su criterio de aceptación en `spec.md` de forma estable (¿un ID
  de criterio explícito desde la skill 01?) — necesario para que el diagnóstico pueda decir "este
  criterio ya está cubierto" con precisión.
- ~~Qué pasa con un criterio marcado como supuesto no resuelto~~ — resuelto en
  [ADR-0011](../decisiones/0011-supuestos-no-bloquean-se-resuelven-en-revision-de-codigo.md): se genera
  TC igual, usando la interpretación de la skill 01; el supuesto se resuelve visiblemente en la
  revisión de código (S5), no aquí.
- Esta skill asume proyectos tipo web (Playwright/UI). Si algún día se soporta tipo API (ADR-0009,
  fuera de alcance de esta tesis), un TC necesitaría otra forma de expresar la verificación esperada.
- Qué hacer cuando el criterio de aceptación no deja claro qué rol requiere el TC — ¿rol por default,
  o se marca para confirmación humana? (ADR-0016)
