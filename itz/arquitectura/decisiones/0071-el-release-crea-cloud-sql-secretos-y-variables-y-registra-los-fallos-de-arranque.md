# ADR-0071: El release crea Cloud SQL, secretos y variables, y los fallos de arranque quedan registrados

## Estado

Aceptada. Amplía el release generado ([ADR-0054](0054-release-py-en-lugar-de-release-sh.md) y [ADR-0055](0055-ejecutar-el-release-desde-la-plataforma.md)) y complementa la compuerta de compilación ([ADR-0070](0070-compuerta-de-compilacion-antes-de-abrir-o-corregir-un-pr.md)).

## Contexto

El primer release del piloto E1c construyó la imagen, pero el servicio de Cloud Run no arrancó: la aplicación necesita una base de datos y variables que el `release.py` no proveía. Al proveerlas aparecieron, uno tras otro, defectos del **código generado** que ni la revisión ni la compuerta de compilación pueden ver porque solo aparecen al arrancar de verdad:

| # | Defecto (piloto E1c, Claude por CLI) | Cómo apareció | Dónde se corrigió |
|---|---|---|---|
| 1 | La migración V2 metía los placeholders de Flyway dentro de literales `$adm$…$adm$`, donde Flyway no los sustituye: fallaba con cualquier valor. | Cloud Run: «ADMIN_PASSWORD_HASH no es un hash BCrypt válido» | PR #14 del repositorio del piloto |
| 2 | `SecurityConfig` pedía un `CorsConfigurationSource` y Spring MVC registra otro (`mvcHandlerMappingIntrospector`). | Cloud Run: «expected single matching bean but found 2» | PR #15 |
| 3 | `docker-entrypoint.sh` del frontend validaba con `tr -d '[:graph:]'`, que busybox/alpine no soporta: rechazaba toda URL. | Cloud Run: «API_BASE_URL inválida» | PR #16 |
| 4 | Sin `package-lock.json` en el frontend, `npm ci` (Firebase Hosting) falla. | Release | Se despliega el frontend en Cloud Run con su Dockerfile |
| 5 | La prueba `MigracionFlywayPostgresTest` habría detectado el defecto 1, pero necesita Docker y no se ejecutó. | Análisis posterior | Pendiente (ejecutar pruebas de integración) |

## Decisión

1. **El release provee lo que la aplicación necesita para arrancar.** El proyecto declara la base de datos (`cloud_sql_postgres`), variables de entorno sin secretos, nombres de secretos generados y si el servicio es público. El script crea la instancia de Cloud SQL, la base y el usuario si no existen (IP pública con TLS obligatorio y contraseña aleatoria en Secret Manager: nivel de pruebas), una cuenta de ejecución dedicada, y despliega con `--set-secrets` y `--env-vars-file` (un archivo, porque `gcloud.cmd` en Windows deforma el separador `^`). Se espera a que la instancia esté lista.
2. **Las URL se conocen antes de desplegar.** `{URL_BACKEND}` y `{URL_FRONTEND}` en las variables se resuelven con la URL determinista de Cloud Run (`https://<servicio>-<número de proyecto>.<región>.run.app`), lo que permite configurar el CORS del backend sin desplegar dos veces. El frontend en Cloud Run recibe `API_BASE_URL` con la URL del backend y es público.
3. **Los fallos de arranque se registran como hallazgos.** Cada defecto que aparece al desplegar se anota con el escenario, el síntoma, la causa y el arreglo (tabla del contexto) y se refleja en el plan de la tesis, como evidencia de que el código que pasa revisión y compilación puede fallar al ejecutarse.

## Consecuencias

- El release cuesta dinero mientras exista la instancia de Cloud SQL, y la IP pública con `0.0.0.0/0` no es apta para producción.
- Los defectos 1 a 3 los corrigió una persona con PR en el repositorio del piloto; Loom todavía no los detecta antes del release.

## Pendiente

- **Compuerta de arranque** (siguiente decisión): antes del release, levantar en Docker la imagen de producción junto con un PostgreSQL desechable y comprobar el endpoint de salud; el error de arranque volvería al agente igual que el de compilación. Habría detectado los defectos 1 a 3.
- Ejecutar las pruebas de integración con Testcontainers dentro de la compuerta.
- Que el paquete «Dockerfiles de producción y CI» genere el `package-lock.json` o use `npm install` cuando no exista.
