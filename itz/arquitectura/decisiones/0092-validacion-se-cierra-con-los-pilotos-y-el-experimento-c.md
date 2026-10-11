# ADR-0092: La validación de la tesis se cierra con los dos pilotos y el experimento C

## Estado

Aceptada (2026-10-08). Reduce el alcance de la validación prevista en el plan de llenado de la tesis (matriz de cuatro escenarios con API, E1 a E4) y en la regla de comparación «uso de la API de cada proveedor en los experimentos».

## Contexto

El diseño de la evaluación preveía cuatro escenarios: dos proyectos por dos proveedores de IA (Claude y Gemini), corridos con la API de cada uno para obtener tokens, tiempos y costos comparables. Ninguno se ejecutó. Al momento de las corridas, la API de Anthropic no tenía saldo y la de Gemini tenía la facturación bloqueada. En su lugar se hicieron dos pilotos completos con el CLI de Claude Code (E1c y E3c) y un experimento de control sobre la revisión (C, ADR-0089 a ADR-0091).

En la revisión 1 de la tesis v04, la directora de tesis decidió con el autor cerrar la validación con lo que ya existe.

## Decisión

1. **La validación de la tesis son los pilotos E1c y E3c y el experimento C.** No se ejecutan los escenarios E1 a E4 para esta tesis.
2. **La comparación entre proveedores (PI4) queda como trabajo futuro.** La tesis la declara sin respuesta, explica por qué y deja descrito el diseño de la matriz para quien la retome.
3. **La regla «uso de la API en los experimentos» se conserva como diseño, no como condición cumplida.** Los pilotos y el experimento C usaron el CLI con suscripción, y la tesis lo declara en cada lugar donde reporta tiempo o costo (costo nocional).

## Consecuencias

- El capítulo 4 describe la matriz como diseño y su reducción de alcance; el capítulo 5 reporta solo E1c, E3c y C; el capítulo 6 deja la matriz y PI4 en trabajos futuros.
- La generalización (PI3) se apoya en dos proyectos con un solo proveedor. La validez externa queda limitada a lo que esos dos proyectos muestran.
- Si después hay saldo en las APIs, la matriz puede correrse con la plataforma congelada y el modelo fijado (recomendación de la tesis) sin cambiar este diseño.
