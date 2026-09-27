# Corrida E3c — ITZ Agenda Taller con Claude por CLI — 2026-09-26/27

Evidencia de la corrida completa (fases 1 a 4) del Proyecto «PILOTO E3c ITZ Agenda Taller (Claude cuenta normal CLI)» (id Loom `b17137fd304348d7a48532ba5db89270`), segundo proyecto de la tesis (P2, Jira `IAT`), operada desde la interfaz de Loom con Playwright. La bitácora cronológica, con cada hallazgo y cada intervención, está en [logs/bitacora.log](logs/bitacora.log). **No se ha incorporado todavía al documento de tesis.**

## Configuración

- Repositorio privado `CarlosSotoGarcia/loom-piloto-e3c-claude-cli`, iniciado solo con README.
- Stack elegido distinto al de P1 para probar la generalización: Node (NestJS, Prisma, Jest) y React (MUI, React Router, TanStack Query, Vitest), monorepo, JWT.
- GCP: proyecto `itz-inventario`, Cloud Run `taller-api`/`taller-web`, base `taller` en la instancia `inventarios-db`.
- HUs: IAT-2 (autorregistro de cliente), IAT-3 (inicio y cierre de sesión), IAT-4 (recuperación de contraseña) → HU-001 a HU-003.
- Modelo: **claude-opus-5-5 con claude-haiku-4-5** vía el CLI de Claude Code. Loom no fija el modelo del CLI y tomó el predeterminado, cambiado a Opus el 2026-09-26; E1c usó claude-sonnet-5. No son comparables en costo ni en modelo.
- Mismas reglas que E1c: una sola revisión por paquete y aceptar el PR; una corrección solo si el CI queda en rojo.

## Resultados

| Etapa | Resultado | Tiempo |
|---|---|---|
| Fase 1: especificar 3 HUs | 3 HUs, todas con supuestos | 1.9 min |
| Fase 2: casos de prueba | 101 casos (35, 39, 27); en E1c fueron 44 | 4.7 min |
| Fase 2: arquitectura | 7 entidades, 8 decisiones, 10 preguntas; aprobada | 1.5 min |
| Fase 3: descomposición | 17 paquetes (BASE 5, 4 por HU) al primer intento | 3.0 min |
| Fase 3: ciclo de paquetes | 17/17 fusionados; 19 revisiones (7 aprobado, 12 con observaciones), 69 observaciones (12 mayores, 57 menores); 4 correcciones (2 por CI en rojo) | generación 185 min en los 16 procesos que terminaron |
| Fase 4: release | Correcto al tercer intento, tras corregir Loom (ADR-0086 y ADR-0087) y las variables de entorno | 21 min en los 6 procesos terminados |
| Fase 4: pruebas de humo | 68 aprobados, 9 fallidos, 24 bloqueados de 101 (resultado final de cada HU) | 75 min en las 5 corridas guardadas |
| Uso del modelo | 532 llamadas; costo nocional 120.99 USD que informa el CLI | — |

Las pruebas de humo de la HU-001 se corrieron tres veces: las dos primeras dejaron 33 de 35 casos bloqueados por el emparejamiento de roles, y la tercera, ya con ADR-0088 y cuentas por rol, dio 28 aprobados, 4 fallidos y 3 bloqueados.

## Hallazgos de generalización (Loom)

1. El release suponía `backend/` y `frontend/` en la raíz; este monorepo usa `apps/` con Dockerfiles que se construyen desde la raíz → **ADR-0086**.
2. El backend Node/Prisma necesita `DATABASE_URL`; el frontend Vite fija la URL de la API al compilar → **ADR-0087**.
3. Los casos de prueba usan roles en texto libre (32 distintos) y Loom emparejaba cuentas por nombre exacto → **ADR-0088**.
4. La compuerta de compilación quedó omitida en 21 de 25 ejecuciones: busca `package.json` en la raíz del monorepo y no revisa `apps/` → pendiente de corregir antes de E3/E4.
5. Las variables de entorno del Proyecto se escriben a mano y Loom no las contrasta con las que exige el código generado (`JWT_ACCESS_SECRET`, `FRONTEND_URL`).
6. La corrección desde el botón de la UI no recibe el log del CI; un paquete «Aprobado» con el CI en rojo no tiene cómo corregirse desde la UI.
7. El CLI de Claude alcanzó su límite de sesión cuatro veces; los procesos cortados quedan «corriendo» en el historial.
8. El modelo del CLI no está fijado en Loom (`LOOM_CLAUDE_CLI_MODEL`).

## Intervenciones fuera de la interfaz de Loom

- «Avanzar HU» llamado por la API (HU-001/PT-04 y HU-002/PT-02) para corregir con el log del CI; en HU-002/PT-02 implicó una segunda revisión y se canceló a propósito al fusionarse.
- Fusión del PR de despliegue (#18) con `POST /despliegue/fusionar`.
- Cuentas de prueba sembradas con el seed de la propia aplicación (`npm run db:seed` contra Cloud SQL) y dos cambios de estado por SQL (inactiva y pendiente de verificación).
- Corrección de Loom durante la corrida (ADR-0086, 0087 y 0088) y reinicios del backend de Loom.

## Contenido

| Ruta | Qué es | ¿En git? |
|---|---|---|
| `capturas/` | 602 capturas; inventario en [CAPTURAS.md](CAPTURAS.md) | No (solo en disco local) |
| `datos/` | Exportación de Mongo del Proyecto (secretos enmascarados) | Sí |
| `artefactos/` | Repositorio de control de Loom (specs, casos, arquitectura, paquetes, despliegue) | Sí |
| `logs/` | Bitácora, salidas de los guiones, eventos de «avanzar HU» | Sí (salvo `descartadas/`) |
| `decisiones-supuestos.json` | Decisiones registradas sobre los supuestos de las 3 HUs (política del piloto) | Sí |
| `loom_ui.py`, `ciclo_ui.py`, `pasoN_*.py` | Guiones de Playwright usados, en orden | Sí |

La estimación de costos de E3 y E4 que usa estos datos está en [../costos/](../costos/).
