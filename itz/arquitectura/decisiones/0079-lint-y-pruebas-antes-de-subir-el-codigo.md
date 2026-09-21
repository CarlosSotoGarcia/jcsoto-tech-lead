# ADR-0079: Lint y pruebas antes de subir el código

## Estado

Aceptada. Amplía la compuerta de compilación ([ADR-0070](0070-compuerta-de-compilacion-antes-de-abrir-o-corregir-un-pr.md)).

## Contexto

El agente que escribe o corrige código no ejecuta nada. Con la compuerta del ADR-0070 solo se compilaba, así que un error de lint o una prueba en rojo se descubría hasta que corría el CI de GitHub (de 2 a 4 minutos por intento). En HU-003 los paquetes PT-02 y PT-03 gastaron varias esperas de CI en errores que un contenedor local habría mostrado antes de subir.

## Decisión

1. **La compuerta corre también el lint y las pruebas unitarias**, dentro del mismo contenedor y antes del commit y el push, tanto al generar como al corregir. En proyectos npm lee los scripts del `package.json` (`lint`, `test:ci` o `test` con Jest) y los ejecuta como el CI; en Maven corre `mvn test`.
2. **Las pruebas que usan Testcontainers se excluyen** de la compuerta local (necesitan hablar con Docker desde dentro del contenedor) y quedan cubiertas por el CI.
3. **Si algo falla, el error vuelve al agente** (hasta 2 veces, como antes) con la instrucción de corregir sin debilitar ni borrar pruebas.

## Consecuencias

- Verificado sobre el commit real de PT-03 (`41154f2`): la compuerta reprodujo en 173 s una prueba de `inactivity.service.spec.ts` en rojo, la misma clase de falla que detuvo al CI.
- Cada intento tarda más (instalación, lint, pruebas y build) y en la primera corrida hay que descargar dependencias.
- El resultado se sigue guardando en `compilacion` del paquete, aunque ahora cubre más que compilar.

## Pendiente

- Ejecutar también las pruebas de integración con Testcontainers (requiere Docker dentro del contenedor o un contenedor auxiliar).
