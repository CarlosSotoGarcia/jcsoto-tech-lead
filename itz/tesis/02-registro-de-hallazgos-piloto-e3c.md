# Registro de hallazgos — piloto E3c (ITZ Agenda Taller, Claude por CLI), 2026-09-26/27

Segundo proyecto de la tesis (P2, Jira `IAT`), con un stack distinto al de P1 (Node con NestJS y Prisma, React con Vite) para probar la generalización. Mismo procedimiento que la corrida E1c del 2026-09-21: tres HUs, una sola revisión por paquete, aceptar el PR y una corrección solo con el CI en rojo. Evidencia completa (bitácora con hora, datos, artefactos, guiones) en `evidencia/corrida-E3c-2026-09-26/`.

Convenciones: igual que el registro del E1c. «Loom» = lo hizo la plataforma; «Manual» = una persona o el asistente fuera de la interfaz de Loom.

## A. Defectos u omisiones del código generado

| # | Defecto | Lo detectó | Lo resolvió |
|---|---|---|---|
| A1 | Prueba de Vitest de `VerificarCorreoPage` en rojo (HU-001/PT-04, paquete «Aprobado») | CI | Loom (corrección con el log del CI, vía «avanzar HU» por la API) |
| A2 | Prueba de Jest de `auth.service` en rojo (HU-002/PT-02): refrescar sin cookie no respondía 401 | CI | Loom (la corrección del botón no bastó; la de «avanzar HU» con el log del CI sí) |
| A3 | El monorepo no trae `package-lock.json` (builds no reproducibles) | Manual, al sembrar cuentas | Sin resolver (mismo tipo que A8 del E1c) |
| A4 | La app lee variables con otros nombres que la configuración del Proyecto (`JWT_ACCESS_SECRET`, `FRONTEND_URL`) y siembra usuarios con su propio seed, que el contenedor no ejecuta | Despliegue | Manual: variables ajustadas desde la UI; seed de la app ejecutado a mano |
| A5 | Omisiones funcionales que solo mostró el smoke: recepción sin sección «Clientes», sin módulo de auditoría para el admin, `/login` no redirige con sesión iniciada, personal interno puede abrir `/mis-vehiculos`, sin documentación de la API publicada | Smoke testing | Sin resolver (9 casos fallidos) |

## B. Proceso y supuestos de Loom que no generalizaron

| # | Hallazgo | Estado |
|---|---|---|
| B1 | El release suponía `backend/` y `frontend/` en la raíz; el monorepo usa `apps/` y sus Dockerfile se construyen desde la raíz | Resuelto: ADR-0086 |
| B2 | El release no daba `DATABASE_URL` (Prisma) y el frontend Vite fija la URL de la API al compilar; Loom solo la pasaba en tiempo de ejecución | Resuelto: ADR-0087 |
| B3 | Los casos de prueba usan 32 roles distintos en texto libre y Loom emparejaba cuentas por nombre exacto: 33 de 35 casos bloqueados en HU-001 | Resuelto: ADR-0088 (actor principal) + cuentas por rol; pendiente restringir los roles en la skill 02 |
| B4 | La compuerta de compilación no se ejecutó en ninguna de sus 21 ejecuciones (todas «omitida»): busca `package.json` en la raíz del monorepo y no revisa `apps/` | **Abierto**: corregir antes de E3/E4 |
| B5 | El proveedor WIF compartido solo aceptaba el repositorio del primer Proyecto | Resuelto: ADR-0085 |
| B6 | La configuración de variables de entorno se escribe a mano y no se contrasta con la que exige el código generado | Abierto (trabajo futuro en ADR-0087) |
| B7 | La corrección desde el botón de la UI no recibe el log del CI; un paquete «Aprobado» con CI en rojo no tiene cómo corregirse desde la UI | Abierto |
| B8 | La cuenta `cliente_bloqueable` queda bloqueada por los primeros casos y arrastra a los siguientes; casos que piden esperar 25–30 min o llamar a la API no los monta el agente de navegador | Abierto (mismo tipo que B7 del E1c) |

## C. Errores de la plataforma o del entorno durante la corrida

- El CLI de Claude alcanzó su límite de sesión cuatro veces (generación de HU-001/PT-01, HU-002/PT-02 y HU-003/PT-01; smoke de HU-002 y HU-003). En dos casos el CLI volvió a responder antes de la hora que anunciaba el mensaje.
- Los procesos cortados por el límite de sesión quedan «corriendo» en el historial de Mongo aunque ya no existen en memoria.
- Los cuatro releases automáticos fallidos (al completarse BASE, HU-001, HU-002 y HU-003) quedaron como «terminada» en el historial; el fallo solo aparece en `release_resultado` del Proyecto.
- El backend de Loom no recargó un cambio de código pese a `--reload`: la segunda corrida de smoke repitió el resultado de la primera; se reinició a mano.
- Una caída de la sesión de trabajo del asistente tumbó el backend y el frontend de Loom a mitad de una corrección (quedó «interrumpida» y se repitió).
- **Validez:** el CLI usó `claude-opus-5-5` (con `claude-haiku-4-5`), no `claude-sonnet-5` como en E1c. Loom no fija `LOOM_CLAUDE_CLI_MODEL` y tomó el modelo predeterminado de Claude Code, cambiado a Opus el 2026-09-26. Costo y calidad no son comparables con E1c.
- La plataforma cambió durante la corrida (ADR-0086, 0087, 0088): E3c no corrió sobre una versión congelada.

## D. Intervenciones fuera de la interfaz de Loom (para medir la autonomía)

| Intervención | Por qué |
|---|---|
| Decisión escrita sobre los supuestos de cada HU (política del piloto) | Regla de supuestos sin confirmar (hecha desde la UI) |
| «Avanzar HU» llamado por la API en HU-001/PT-04 y HU-002/PT-02 | La UI no ofrece corregir con el log del CI en esos estados |
| Cancelación manual de «avanzar HU» al fusionar HU-002/PT-02 | Para no aplicar rondas extra a PT-03 y PT-04 |
| Fusión del PR de despliegue (#18) por `POST /despliegue/fusionar` | La UI no tiene el botón |
| Ajuste de variables de entorno del despliegue (desde la UI) | A4 |
| Seed de la app contra Cloud SQL y dos cambios de estado por SQL | Cuentas de prueba por rol (A4, B3) |
| Corrección de Loom durante la corrida (ADR-0086, 0087, 0088) y reinicios del backend | B1, B2, B3 |
| Relanzar procesos cortados por el límite de sesión | C |

Ninguna intervención editó el código generado de la aplicación.
