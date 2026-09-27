# ADR-0086: El release ubica los servicios en monorepos con workspaces

## Estado

Aceptada. Ajusta el generador de release ([ADR-0042](0042-skill-de-release-generacion-de-release-sh.md)) y el despliegue en Cloud Run ([ADR-0071](0071-el-release-crea-cloud-sql-secretos-y-variables-y-registra-los-fallos-de-arranque.md)).

## Contexto

`release.py` construía cada servicio con `gcloud builds submit <carpeta> --tag <imagen>`, con la carpeta fija en `backend/` y `frontend/` en la raíz del repositorio. En el piloto E3c (ITZ Agenda Taller, stack Node con NestJS y React), la arquitectura que generó Loom organizó el monorepo con workspaces de npm: `apps/backend` y `apps/frontend`, con un solo `package-lock.json` en la raíz. Sus Dockerfile de producción se construyen desde la raíz (`docker build -f apps/backend/Dockerfile .`) porque copian los manifiestos de todos los workspaces. El release automático falló dos veces (al completar HU-001 y HU-002): no encontraba `backend/` y, aunque lo hubiera encontrado, construir con la carpeta del servicio como contexto no habría funcionado. En el piloto E1c (Java con Angular) no apareció porque ese monorepo usa `backend/` y `frontend/` en la raíz, con contexto propio.

El release no puede suponer una sola forma de monorepo: la decide la arquitectura generada para cada stack.

## Decisión

1. **Ubicar el Dockerfile.** Para cada servicio, `release.py` busca su `Dockerfile` en la carpeta configurada (`backend`/`frontend`, o `BACKEND_DIR`/`FRONTEND_DIR`) y, si no está ahí, en `apps/<carpeta>`, `packages/<carpeta>` y `services/<carpeta>`, en ese orden.
2. **Elegir el contexto de build.** Si el Dockerfile menciona rutas de su propia carpeta (por ejemplo `COPY apps/backend/package.json`), fue escrito para construirse desde la raíz del repositorio: el contexto es la raíz y el Dockerfile se pasa con `-f`. Si no, el contexto es la carpeta del servicio, como antes.
3. **Construir con `-f` sin configuración en el repositorio.** Cuando el Dockerfile no es `<contexto>/Dockerfile`, el release escribe un `cloudbuild.yaml` temporal con un solo paso (`docker build -f <Dockerfile> -t <imagen> .`) y lo usa con `gcloud builds submit --config`. El caso de siempre sigue usando `--tag`.

## Consecuencias

- Probado sin desplegar sobre un clon del repositorio del E3c: ubica `apps/backend/Dockerfile` y `apps/frontend/Dockerfile` con contexto en la raíz; con la forma del E1c (`backend/Dockerfile` que copia `.`) conserva el contexto `backend`.
- La regla del contexto es una heurística sobre el texto del Dockerfile. Un Dockerfile de subcarpeta que no mencione su propia ruta pero necesite la raíz seguiría fallando; se puede forzar la carpeta con `BACKEND_DIR`/`FRONTEND_DIR`.
- La plantilla se carga al arrancar el backend de Loom: el cambio aplica después de reiniciarlo.
