# ADR-0003: El código es el eje principal del análisis; HUs y prototipos quedan como contexto secundario

## Estado

Reemplazada por [ADR-0004](0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md).

## Contexto

El diseño original trataba las historias de usuario (HUs) y los prototipos como "fuente de verdad"
formal de la intención de negocio, con un esquema de ingesta dedicado como pilar central del sistema,
al mismo nivel que el análisis de código. Se decidió reorientar el skill para que sea más orientado al
código.

## Decisión

El skill analiza primero y principalmente el código: el diff, la estructura del repositorio, las
convenciones y las pruebas existentes. Las historias de usuario y los prototipos se incorporan como
**contexto adicional opcional** cuando están disponibles, para enriquecer la revisión y la generación
de pruebas — pero el sistema no depende de que existan, ni de que sigan un formato formalmente
modelado de "HU evaluable".

## Consecuencias

- Se simplifica el diseño: ya no se requiere un esquema de ingesta de intención como componente
  central obligatorio (ver ADR-0002 sobre alcance de infraestructura, en la misma línea de reducir
  alcance).
- Reduce el riesgo de "variabilidad de calidad de HUs/prototipos entre sistemas" señalado en la
  propuesta original, porque deja de ser una dependencia dura del sistema.
- Cambia el eje de la contribución: ya no es tanto "qué tan bien se correlaciona código con una fuente
  de intención externa formalizada", sino "qué tan buena revisión y qué tan buenas pruebas puede
  producir el análisis de código por sí solo, mejoradas cuando hay contexto de negocio disponible".
- Falta definir (pendiente de un ADR futuro): cómo se mide la mejora que aporta el contexto de
  HU/prototipo cuando está presente, frente al análisis de solo-código, para no perder esa parte de la
  contribución original.
