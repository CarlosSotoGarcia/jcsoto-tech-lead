# ADR-0081: Despliegue automático con GitHub Actions y Workload Identity Federation

## Estado

Aceptada. Sustituye como camino recomendado al trigger de Cloud Build del [ADR-0054](0054-release-py-en-lugar-de-release-sh.md) y cambia el disparo del release automático del [ADR-0072](0072-release-automatico-al-aceptar-un-pr.md).

## Contexto

Loom lanzaba el release desde su propio proceso al fusionar el último PR de una HU. Se pidió que el despliegue lo dispare un cambio en el repositorio, declarado por el propio `release.py`. Se probó el trigger de Cloud Build: crearlo falló con `FAILED_PRECONDITION: Repository mapping does not exist`, porque conectar GitHub con Cloud Build exige instalar y autorizar una app de GitHub con la cuenta de la persona, un paso interactivo sin API. Terraform no evita esa conexión (`google_cloudbuild_trigger` la necesita igual), así que no se adopta por ahora.

## Decisión

1. **El despliegue automático lo hace GitHub Actions**, que ya está conectado al repositorio: Loom genera `.github/workflows/release.yml`, que ejecuta `release.py` en cada push a la rama base.
2. **La autenticación es Workload Identity Federation, sin llaves.** `release.py` crea, de forma idempotente, la cuenta de servicio desplegadora, el pool y el proveedor OIDC (que solo aceptan a este repositorio: `assertion.repository == 'dueño/repo'`) y el permiso `workloadIdentityUser` para ese repositorio.
3. **Los datos de la federación llegan al workflow como variables del repositorio** (`GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_SERVICE_ACCOUNT`), que `release.py` guarda con `gh variable set`. Si `gh` no está autenticado, el script imprime las dos variables para crearlas a mano.
4. **El CI (`ci.yml`) solo verifica**: no lleva un job de despliegue propio. Coexistir con `release.yml` duplicaba el despliegue con otros nombres de servicio.
5. **Alcance por proveedor:** hoy Loom es GitHub-only en la revisión, la fusión, los checks y el despliegue. Con GitLab el equivalente es GitLab CI con OIDC, o una conexión de Cloud Build por tokens (que sí es automatizable); requeriría un adaptador de proveedor de código y otro de estrategia de despliegue. Queda como trabajo futuro, no como promesa del piloto.

## Consecuencias

- Cero pasos manuales de conexión: lo único que se necesita es `gh` autenticado en la máquina que ejecuta el primer release.
- La cuenta desplegadora tiene roles amplios (Run, Cloud SQL, Secret Manager, Artifact Registry, Storage, cuentas de servicio): es de pruebas, no de producción.
- El primer release lo sigue ejecutando Loom; a partir de ahí, cada push a `main` despliega desde GitHub Actions.
- Se creó y luego se eliminó una cuenta `loom-release-trigger` del intento con Cloud Build.

## Pendiente

- Que el paquete de CI que genera el agente no incluya un job de despliegue (hoy se quitó a mano en el piloto, PR #28).
- Adaptadores de proveedor de código y de despliegue para admitir GitLab.
