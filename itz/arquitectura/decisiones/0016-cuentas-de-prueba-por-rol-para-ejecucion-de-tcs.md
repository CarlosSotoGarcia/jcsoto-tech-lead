# ADR-0016: Cuentas de prueba por rol para la ejecución de TCs

## Estado

Aceptada. Extiende [ADR-0006](0006-smoke-tests-con-playwright-y-bitacora-de-hus.md) y la nota de acceso
de `skills/03-diagnostico-de-avance-existente.md`.

## Contexto

El aplicativo bajo evaluación puede tener múltiples roles (p. ej. administrador, usuario final,
invitado), y un TC puede requerir un rol específico para ejecutarse de forma representativa — un TC
sobre una función administrativa no se puede validar con una cuenta de usuario final, y viceversa. Una
sola "cuenta de prueba genérica" (como se dejó abierto en `skills/03-...md`) no alcanza.

## Decisión

- La configuración de Proyecto incluye un conjunto de **cuentas de prueba, una por rol relevante** de
  la aplicación (no una sola cuenta genérica), para el ambiente de desarrollo configurado (ADR-0005).
- Cada TC, al generarse (`skills/02-generacion-de-tcs.md`), declara explícitamente **qué rol necesita**
  para ejecutarse (campo `rol_requerido` en `test-cases.md`).
- El motor de ejecución de TCs (compartido por diagnóstico de avance y smoke testing —
  `skills/03-...md`) selecciona, para cada TC, la cuenta de prueba correspondiente a su rol declarado
  antes de correrlo contra el ambiente de desarrollo.

## Consecuencias

- `skills/02-generacion-de-tcs.md` gana un campo más por TC: `rol_requerido`.
- `skills/03-diagnostico-de-avance-existente.md` (y, por extensión, la skill de smoke testing) dejan de
  asumir una sola credencial de prueba — leen la credencial correspondiente al rol de cada TC desde la
  configuración del Proyecto.
- La configuración de Proyecto gana un campo más: el mapa rol → credencial de prueba para el ambiente
  de desarrollo.
- Pendiente: qué hace el sistema si un TC no declara rol, o declara uno para el que no hay credencial
  configurada — ¿falla el TC, se asume un rol por default, o se marca como bloqueado para revisión
  humana?
- Pendiente (fuera del alcance de diseño de arquitectura): mecanismo seguro de almacenamiento/rotación
  de estas credenciales de prueba — es una decisión de implementación.
