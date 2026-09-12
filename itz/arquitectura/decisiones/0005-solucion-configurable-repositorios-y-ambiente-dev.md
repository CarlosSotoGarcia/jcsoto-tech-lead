# ADR-0005: La solución es configurable por repositorios (N backends/frontends) y ambiente de desarrollo

## Estado

Aceptada

## Contexto

El sistema debe poder operar sobre soluciones reales compuestas por múltiples repositorios — típicamente
varios backends y varios frontends que conforman una misma solución — y validar sus cambios contra un
ambiente de desarrollo ya desplegado. Esto no puede quedar fijo en el diseño: cada solución sobre la que
corra el skill tiene su propia topología de repositorios y su propia URL de ambiente.

## Decisión

La solución recibe como configuración de entrada, por proyecto/solución objetivo:

- La lista de repositorios que la componen, cada uno tipado (backend/frontend) y con su ubicación
  (URL del repositorio, rama base).
- La URL del ambiente de desarrollo desplegado, usada por el skill de smoke testing (ADR-0004,
  ADR-0006) para ejecutar los TCs contra el sistema real.

Esta configuración es un insumo explícito por corrida — el sistema no asume una topología fija de "un
backend y un frontend", sino N repositorios de cada tipo.

## Consecuencias

- El diseño de indexación de código (ADR-0002) y el de generación de subtareas/PRs (ADR-0004) deben
  operar sobre una colección de repositorios, no sobre uno solo — una subtarea puede tocar uno o varios
  repos a la vez (p. ej. un cambio de contrato que afecta backend y frontend).
- Falta definir (pendiente de ADR): el esquema/formato exacto de este archivo o estructura de
  configuración (repos + ambiente dev), y cómo el skill decide en qué repositorio(s) debe generar
  código para una subtarea dada.
- Refuerza el carácter agnóstico al sistema de la propuesta original: la validación en 2-3 sistemas
  distintos (objetivo específico 4) se hace simplemente apuntando la misma solución a configuraciones
  distintas.
