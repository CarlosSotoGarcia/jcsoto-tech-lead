# ADR-0001: Usar Architecture Decision Records para registrar decisiones de arquitectura

## Estado

Aceptada

## Contexto

El proyecto de tesis requiere que el diseño de la solución quede documentado de forma que un asesor o
sinodal pueda entender, en cualquier momento del desarrollo, qué se decidió y por qué — no solo qué se
construyó al final. Sin un registro explícito de decisiones, el razonamiento detrás de cada elección de
diseño (framework de agentes, forma de indexar código, formato de HU aceptado, etc.) se pierde o queda
disperso entre commits, conversaciones y memoria.

## Decisión

Se documentan las decisiones de arquitectura relevantes como ADRs individuales en
`itz/arquitectura/decisiones/`, numeradas secuencialmente y con este formato fijo:

- **Título**: la decisión en una frase.
- **Estado**: Propuesta / Aceptada / Reemplazada por ADR-000N.
- **Contexto**: qué problema u opción forzó la decisión.
- **Decisión**: qué se decidió, en términos concretos.
- **Consecuencias**: qué implica — ventajas, costos, trade-offs aceptados.

Una decisión tomada no se edita retroactivamente para cambiar su contenido: si una decisión posterior
la reemplaza, se crea un ADR nuevo y el anterior se marca como reemplazado, conservando el historial
de por qué cambió el rumbo.

## Consecuencias

- Cada decisión de diseño no trivial (framework de agentes, esquema de indexación, formato de HU
  aceptado, mecanismo de correlación código↔intención, instrumentación de métricas, etc.) debe
  aterrizar en un ADR antes de darse por definitiva.
- El coste es disciplina: escribir el ADR en el momento de decidir, no después.
- A cambio, la tesis tiene evidencia directa y fechada del proceso de diseño, útil tanto para la
  redacción del documento final como para defender decisiones ante el comité.
