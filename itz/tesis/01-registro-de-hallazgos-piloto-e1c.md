# Registro de hallazgos — piloto E1c (Claude por CLI), segunda etapa

Objetivo de esta etapa (decidido 2026-09-20): hacer que el proyecto experimento funcione de punta a punta, registrando cada error y cada intervención manual para que Loom los evite solo. Después se repite el ejercicio desde cero para documentarlo limpio. Este archivo es el registro vivo; cada fila indica **quién lo detectó**, **quién lo resolvió** y **qué debe hacer Loom para no depender de una persona**.

Convenciones: «Loom» = lo hizo la plataforma por sí sola; «Manual» = lo hizo una persona (o yo, fuera de Loom); «CI»/«Despliegue» = lo destapó el CI de GitHub o el arranque en Cloud Run.

## A. Defectos del código generado (aplicación del piloto)

| # | Defecto | Lo detectó | Lo resolvió | Qué falta en Loom |
|---|---|---|---|---|
| A1 | Migración V2: los placeholders de Flyway no se sustituyen dentro de `$adm$${x}$adm$` (el backend no arrancaba) | Despliegue (Cloud Run) | Manual, PR #14 | Compuerta de arranque: levantar la imagen con un PostgreSQL desechable antes del release ([ADR-0071](../arquitectura/decisiones/0071-el-release-crea-cloud-sql-secretos-y-variables-y-registra-los-fallos-de-arranque.md)) |
| A2 | Mi arreglo A1 rompía con comillas en los datos del admin (regresión; `MigracionFlywayPostgresTest` en rojo) | CI | Manual, PR #23 | Ejecutar las pruebas de integración con Testcontainers en la compuerta; no fusionar en rojo ([ADR-0076](../arquitectura/decisiones/0076-no-fusionar-ni-avanzar-con-la-integracion-continua-en-rojo.md)) |
| A3 | `SecurityConfig` recibía dos beans `CorsConfigurationSource` (el backend no arrancaba) | Despliegue | Manual, PR #15 | Compuerta de arranque |
| A4 | `docker-entrypoint.sh` del frontend validaba con `tr -d '[:graph:]'` (no existe en alpine): rechazaba toda URL | Despliegue | Manual, PR #16 | Compuerta de arranque con el contenedor del frontend |
| A5 | Dockerfile del frontend: `npm ci` rechazaba el lock generado por `npm install` en el CI | CI | Manual, PR #24 | Probar la construcción de la imagen en la compuerta |
| A6 | Pruebas Jest de `logout` esperaban `sessionStorage` vacío (HU-003/PT-02) | CI | Loom (corrección con el log del CI) | — resuelto por [ADR-0078](../arquitectura/decisiones/0078-corregir-con-el-log-de-la-integracion-continua.md) |
| A7 | HU-003/PT-03: lint `prefer-const` y una prueba de `inactivity.service.spec.ts` en rojo | CI | En curso (Loom) | El agente corrige a ciegas: no ejecuta lint ni Jest. Ejecutarlos en un contenedor antes del push |
| A8 | `package-lock.json` ausente: `npm ci` fallaba en Firebase Hosting | Release | Manual (cambio a Cloud Run) | El paquete de Dockerfiles de producción debe generar y validar el lock |
| A9 | Deploy de CI falla en «Autenticación en GCP (Workload Identity Federation)» | CI | Abierto | Coherencia entre el tipo de autenticación configurado y el workflow generado |

## B. Proceso: lo que Loom hacía mal o no hacía

| # | Hallazgo | Estado |
|---|---|---|
| B1 | Se fusionaron PR con el CI en rojo (#14 a #22) y se construyó encima | Resuelto: ADR-0076 (no fusionar ni avanzar en rojo). Falta proteger la rama en GitHub (requiere Pro) |
| B2 | Un supuesto sin confirmar bloquea la revisión y ninguna corrección lo resuelve; no había dónde decidirlo | Resuelto: ADR-0077 (pantalla «Decisiones pendientes»). HU-001 y HU-002 se fusionaron con esa observación abierta |
| B3 | El release no proveía base de datos, secretos ni variables | Resuelto: ADR-0071 |
| B4 | Sin forma de completar una HU sin repetir cuatro acciones por paquete | Resuelto: ADR-0074 |
| B5 | El release no se lanzaba al terminar una HU | Resuelto en código (ADR-0072); pendiente verificar de punta a punta |
| B6 | El agente marca como corregido lo que no pudo ejecutar; la verificación real llega hasta el CI | Abierto (ver A7) |
| B7 | El smoke testing dejó 6 de 19 casos bloqueados: límite de intentos del login por el orden de los casos y falta de datos de prueba | Abierto: ordenar casos que provocan bloqueos y sembrar usuarios |

## C. Errores de la propia plataforma corregidos en esta etapa

`avanzar-hu` sin opciones (422), contador «7 de 3», extractor del log del CI que devolvía el checkout de Git, `formGroupName` anidado que dejaba la pantalla a medias, y una regresión de la migración V2 introducida por el propio arreglo. Todos se detectaron probando, no por revisión de código.

## D. Intervenciones manuales (para medir la autonomía)

PR #14, #15, #16, #23 y #24 en el repositorio del piloto (fusionados con `gh`); usuarios de prueba insertados en Cloud SQL; decisión de 90 minutos registrada por la API. Todo lo demás sobre el código del piloto lo hizo Loom, disparado por su API.

## E. Pendiente de esta etapa

Terminar HU-003 (PT-03), verificar que el release se lance al completar la HU, correr el smoke de HU-002 y HU-003 y repetir las pruebas bloqueadas de HU-001, y decidir si Loom ejecuta lint y pruebas en contenedor antes del push.
