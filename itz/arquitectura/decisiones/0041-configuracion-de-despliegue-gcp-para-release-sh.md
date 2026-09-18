# ADR-0041: Configuración de despliegue en GCP para armar el release.sh

## Estado

Aceptada. Concreta, para GCP, la elección de nube de [ADR-0038](0038-stack-microservicios-y-autenticacion-declarados-en-fase-2.md)
y usa la cuenta de desarrollo de [ADR-0013](0013-cuenta-de-desarrollo-dedicada-para-acceso-a-repositorios.md)
para escribir en el repositorio del código.

## Contexto

Un Proyecto que se despliega en GCP necesita, en el repositorio donde queda el código, un
`release.sh` y un disparador que lo ejecute cuando cambia el repositorio. Para armarlos Loom tiene
que saber qué proyecto de GCP, qué servicios, cómo se autentica el release y quién lo ejecuta. Nada
de eso estaba capturado, y los secretos (llaves, tokens) no deben pasar por Loom.

## Decisión

1. **Dónde se captura**: pestaña Implementación (Fase 4), sección "Despliegue en GCP". El modelo
   `despliegue_gcp` es opcional y anidado en el Proyecto. Por ahora solo GCP (ADR-0038); otras
   nubes serían otro bloque equivalente.
2. **Qué se captura** (solo identificadores y *nombres* de secretos):

| Campo | Para qué lo usa el release.sh |
|---|---|
| `proyecto_id`, `region` | `--project`, `--region` de `gcloud` |
| `servicio_backend` (Cloud Run habilitado; App Engine y GKE previstos), `nombre_servicio_backend` | `gcloud run deploy <servicio>` |
| `hosting_frontend` (Firebase Hosting o Cloud Run), `nombre_servicio_frontend` | despliegue del frontend |
| `artifact_registry` | destino de la imagen: `REGION-docker.pkg.dev/PROYECTO/REPO/SERVICIO:SHA` |
| `disparador` (`push_rama` / `tag` / `manual`), `rama_release` | evento que dispara el workflow |
| `ci_plataforma` (`github_actions` / `cloud_build`) | quién detecta el cambio y ejecuta el script |
| `autenticacion`, `service_account_email`, `wif_provider` / `secret_ref` | cómo se autentica el workflow **antes** del script |

3. **Autenticación**: la recomendada es **Workload Identity Federation** (sin llaves): un pool y un
   provider de GitHub limitado al repositorio del Proyecto, y la service account desplegadora con
   `roles/iam.workloadIdentityUser`. Como alternativa, una **llave JSON de service account**
   guardada como secreto del repositorio; Loom guarda solo el *nombre* del secreto (`secret_ref`),
   nunca la llave. Es el mismo criterio de ADR-0032.
4. **Contrato del release.sh**: no contiene credenciales. El workflow se autentica (con
   `google-github-actions/auth`, permisos `id-token: write` si es WIF) y después llama al script,
   que asume `gcloud` ya autenticado. Esbozo del script para Cloud Run:

```bash
#!/usr/bin/env bash
set -euo pipefail
PROJECT_ID="<proyecto_id>"; REGION="<region>"; SERVICE="<nombre_servicio_backend>"; REPO="<artifact_registry>"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${SERVICE}:$(git rev-parse --short HEAD)"
gcloud builds submit --project "$PROJECT_ID" --tag "$IMAGE" ./backend
gcloud run deploy "$SERVICE" --project "$PROJECT_ID" --region "$REGION" --image "$IMAGE" --quiet
```

5. **Guía en la plataforma**: la sección incluye un paso a paso de lo que hay que preparar en GCP
   (proyecto con facturación, APIs `run`, `artifactregistry`, `cloudbuild`, `iam`,
   `iamcredentials`, `sts`; repositorio de Artifact Registry; service account con
   `run.admin`, `artifactregistry.writer`, `cloudbuild.builds.editor`, `iam.serviceAccountUser` y,
   si aplica, `firebasehosting.admin`) y muestra qué campos faltan para poder armarlo.

## Consecuencias

- Es solo configuración: todavía no existe la skill que genere `release.sh` y el workflow y los
  escriba en el repositorio con la cuenta de desarrollo (ADR-0013). Esta ADR define qué datos
  necesitará esa skill.
- No cambia `fases_configuradas` (ADR-0034/ADR-0036): la configuración de despliegue es opcional y
  no bloquea ninguna fase; la etiqueta "Lista para armar el release.sh" es informativa.
- El ambiente de desarrollo (`ambiente_dev_url`, ADR-0036) sigue siendo aparte: es la URL contra la
  que se hace smoke testing; esto es cómo se llega a ella.

## Pendiente

- La skill que genera `release.sh`, el workflow de GitHub Actions o el trigger de Cloud Build, y los
  escribe en el repositorio.
- Variables de entorno y secretos de la aplicación (cadena de conexión a la base de datos, etc.).
- Base de datos gestionada (Cloud SQL), redes y dominios: no cubiertos.
- App Engine, GKE y Cloud Storage + CDN aparecen en el formulario como "próximamente".
