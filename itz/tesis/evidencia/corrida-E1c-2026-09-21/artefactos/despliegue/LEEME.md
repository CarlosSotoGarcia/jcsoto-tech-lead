# Despliegue en GCP — PILOTO E1c ITZ Inventarios (Claude cuenta normal CLI)

Generado por Loom (ADR-0042). Estos son los pasos que se hacen **una sola vez** en GCP; después cada cambio se libera solo.

## Archivos generados

- `release.py`
- `.github/workflows/release.yml`

- Todo va en la raíz del repositorio; los workflows en `.github/workflows/`.

## 1. Prerrequisitos en el repositorio

- Un `Dockerfile` en el directorio de cada servicio que va a Cloud Run.

## 2. APIs y repositorio de imágenes

```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
  cloudbuild.googleapis.com iam.googleapis.com iamcredentials.googleapis.com sts.googleapis.com \
  --project itz-inventario
gcloud artifacts repositories create inventarios --repository-format=docker \
  --location=us-central1 --project itz-inventario
```

## 3. Roles de la service account desplegadora

```bash
for ROL in roles/run.admin roles/artifactregistry.writer roles/cloudbuild.builds.editor roles/storage.objectAdmin roles/serviceusage.serviceUsageConsumer roles/iam.serviceAccountUser; do
  gcloud projects add-iam-policy-binding itz-inventario \
    --member="serviceAccount:loom-release-deployer@itz-inventario.iam.gserviceaccount.com" --role="$ROL"
done
```

## 4. Workload Identity Federation (sin llaves)

```bash
gcloud iam workload-identity-pools create loom-github --project=itz-inventario --location=global
gcloud iam workload-identity-pools providers create-oidc github \
  --project=itz-inventario --location=global --workload-identity-pool=loom-github \
  --issuer-uri=https://token.actions.githubusercontent.com \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository=='CarlosSotoGarcia/loom-piloto-e1c-claude-cli'"
gcloud iam service-accounts add-iam-policy-binding loom-release-deployer@itz-inventario.iam.gserviceaccount.com --project=itz-inventario \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/118746543308/locations/global/workloadIdentityPools/loom-github/attribute.repository/CarlosSotoGarcia/loom-piloto-e1c-claude-cli"
```

## Primer despliegue manual

Con `gcloud` autenticado (y Python 3):

```bash
python release.py
```
