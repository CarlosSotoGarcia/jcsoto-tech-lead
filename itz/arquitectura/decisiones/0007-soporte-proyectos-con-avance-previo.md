# ADR-0007: Soporte para proyectos con avance previo (brownfield), no solo proyectos nuevos

## Estado

Aceptada. Extiende el flujo de [ADR-0004](0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md)
sin reemplazarlo.

## Contexto

ADR-0004 describe el flujo HU → TCs → arquitectura → subtareas → código, asumiendo implícitamente que
cada HU arranca sin código relacionado ya escrito. En la práctica, el skill debe poder aplicarse sobre
soluciones que ya tienen avance: código existente que cubre total o parcialmente los criterios de
aceptación de una HU (una implementación previa, manual o de una corrida anterior del propio skill).
Sin esto, el sistema regeneraría desde cero trabajo que ya existe, o diseñaría arquitectura ignorando
los patrones ya presentes en el repositorio.

## Decisión

Se agrega un paso de **evaluación de avance existente** entre la generación de TCs (paso 2 de ADR-0004)
y el diseño de arquitectura (paso 3): el skill ejecuta los TCs recién generados contra el estado actual
del código/ambiente de desarrollo configurado (ADR-0005), **antes** de diseñar o descomponer nada.

- Los TCs que ya pasan indican criterios de aceptación ya cubiertos por el código existente — no
  generan subtarea.
- Los TCs que fallan (incluidos los que fallan porque la funcionalidad ni siquiera existe todavía, caso
  greenfield) sí generan subtarea.
- El diseño de arquitectura (paso 3) se hace **a partir de lo que ya existe**: extiende o se ajusta a
  los patrones presentes en el código, no propone una arquitectura nueva ignorándolos.

Este mecanismo reutiliza el mismo skill de ejecución de TCs que ya hacía smoke testing al final del
flujo (ADR-0006) — se invoca dos veces con el mismo propósito (evaluar qué TCs pasan), en dos momentos
distintos: diagnóstico inicial y validación final.

## Consecuencias

- El caso greenfield queda cubierto como caso particular: si no existe nada, todos los TCs fallan en el
  diagnóstico inicial y todos generan subtarea — el flujo de ADR-0004 no cambia para ese caso.
- El caso brownfield evita trabajo redundante: solo se generan subtareas para lo que realmente falta o
  está incompleto.
- El diseño de arquitectura y la indexación de código (ADR-0002) dejan de ser un paso "en el vacío":
  necesitan poder leer y respetar convenciones/patrones ya existentes, no solo estructura y historial.
- Pendiente de definir: qué hacer con TCs que no se pueden evaluar tan temprano porque dependen de un
  cambio de contrato que otra subtarea de la misma HU todavía no ha hecho (dependencias entre TCs/
  subtareas) — no todo se puede diagnosticar de forma aislada en el primer paso.
