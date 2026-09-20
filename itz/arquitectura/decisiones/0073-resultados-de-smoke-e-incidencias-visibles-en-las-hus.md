# ADR-0073: Resultados del smoke testing e incidencias visibles en las HUs

## Estado

Aceptada. Complementa el smoke testing ([ADR-0059](0059-smoke-testing-por-hu-con-script-generado-desde-el-codigo.md)) y la generación de fixes ([ADR-0061](0061-generacion-de-fixes-desde-smoke-testing.md)).

## Contexto

Las corridas de smoke testing ya se guardaban en Mongo y como evidencia en Markdown, pero solo se veían en la pantalla del proyecto y el informe mostraba el resultado como texto («pasa», «bloqueado»), sin totales. En la primera corrida real del piloto (HU-001: 13 casos pasan, 0 fallan, 6 bloqueados) hizo falta contar a mano.

## Decisión

1. **El informe `smoke-NN.md` usa iconos** (✅ Pasa, ❌ Falla, ⛔ Bloqueado), trae una tabla de resumen con casos y porcentaje por resultado, y el encabezado guarda `porcentaje_pasan`, `porcentaje_fallan` y `porcentaje_bloqueados`.
2. **«Ver HUs» muestra el último resultado de cada HU** (pasan, fallan y bloqueados, con casos y porcentaje) y cuántos fixes tiene abiertos.
3. **El detalle de la HU tiene dos pestañas nuevas:** «Smoke testing» (todas las corridas, la más reciente abierta, con el resultado y el motivo de cada caso) e «Incidencias» (los paquetes de fix de la HU con su estado y PR).
4. **Las incidencias son los paquetes de fix de la propia HU** (ronda nueva, ADR-0061); no se crean tickets en Jira. La integración con Jira de Loom es de solo lectura.

## Consecuencias

- Las corridas anteriores conservan su informe con el formato viejo; el nuevo aplica desde la siguiente corrida.
- Un caso bloqueado no genera fix (solo los que fallan), de modo que no aparece en Incidencias.

## Pendiente

- Decidir si cada fix debe crear además una incidencia en Jira ligada a la HU de origen (requiere permisos de escritura y decidir el tipo de ticket).
