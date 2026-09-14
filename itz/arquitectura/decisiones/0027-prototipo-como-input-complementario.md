# ADR-0027: El prototipo, cuando se entrega, es input complementario para TCs y descomposición completas

## Estado

Aceptada. Extiende [ADR-0004](0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md) y
resuelve el pendiente de `skills/03-diagnostico-de-avance-existente.md` sobre TCs que no se pueden
evaluar de forma aislada.

## Contexto

Un TC puede necesitar tanto un cambio de backend como uno de frontend para poder evaluarse de forma
representativa. Basarse solo en el texto de los criterios de aceptación de `spec.md` puede dejar
ambigüedad sobre qué tan completa debe quedar la solución en cada capa. Además, quedaba sin resolver
qué hacer cuando un TC del diagnóstico inicial (`skills/03-...md`) falla: ¿falla porque de verdad no
existe nada, o porque falta la otra mitad de la misma HU que todavía no se ha construido?

## Decisión

El **prototipo** (mockup, contrato de API, wireframe, o cualquier artefacto que describa el
comportamiento completo esperado) es un **input opcional y complementario a la HU**, entregado a Telar
al configurar o descubrir esa HU. Cuando está disponible:

1. `skills/01-...md` guarda su referencia en `spec.md` (`prototipo_ref`).
2. `skills/02-...md` lo usa junto con `spec.md` para generar TCs que cubren el comportamiento completo
   descrito — no solo lo que el texto de los criterios alcanza a especificar.
3. `skills/05-...md` lo usa (vía `plan.md`) para descomponer la HU en paquetes de trabajo que cubran
   **ambos lados** (back y front) sin dejar huecos, verificando primero contra el diagnóstico
   (`skills/03-...md`) qué de eso ya existe, para no duplicar trabajo.

Esto resuelve la ambigüedad original del diagnóstico: ya no hace falta distinguir "el TC falla porque
no existe nada" de "falla porque falta la otra mitad de la misma HU" — la descomposición, informada por
el prototipo, genera todos los paquetes necesarios en ambas capas por construcción; el diagnóstico solo
necesita señalar qué TC está pendiente, no diagnosticar la causa.

Cuando **no** hay prototipo, el flujo sigue exactamente igual que antes (ADR-0004): `spec.md` es la
única fuente para TCs y descomposición.

## Consecuencias

- `spec.md` gana un campo opcional: `prototipo_ref`.
- `skills/02-...md` y `skills/05-...md` actualizan sus entradas para considerar el prototipo cuando
  existe.
- Reduce significativamente el riesgo de "TC fallido sin poder atribuir causa" que quedaba abierto en
  `skills/03-...md` — la responsabilidad de cubrir ambos lados pasa a la descomposición, no al
  diagnóstico.
- Pendiente: formato(s) concreto(s) de prototipo que el sistema sabe interpretar (imagen, Figma,
  OpenAPI, texto estructurado) — detalle de implementación, no bloquea el diseño.
- Pendiente: qué hace el sistema si el prototipo y el texto de `spec.md` se contradicen entre sí.
