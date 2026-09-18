# ADR-0042: Skill de release — generación de release.sh y su disparador para GCP

## Estado

Aceptada. Implementa lo que [ADR-0041](0041-configuracion-de-despliegue-gcp-para-release-sh.md)
dejó como pendiente ("la skill que genera release.sh") y agrega una skill a la Fase 4
(Implementación) de [ADR-0034](0034-fases-de-desarrollo-y-configuracion-minima-por-fase.md).

## Contexto

ADR-0041 capturó qué datos hacen falta para desplegar en GCP, pero nada los convertía en los
archivos que realmente hacen el despliegue. Además, en esta etapa Loom todavía no tiene un
mecanismo real de credenciales para la cuenta de desarrollo (ADR-0032/ADR-0033: es solo una nota
de texto), así que **no puede clonar los repositorios del código ni escribir en ellos**.

## Decisión

1. **Skill 10 — Generación de release** (`skills/10-generacion-de-release.md`), dentro de la
   Fase 4. Es **determinista**: plantillas rellenadas con la configuración guardada del Proyecto,
   sin LLM. Genera:
   - `release.sh` (monorepo, o `release-backend.sh` / `release-frontend.sh` en multirepo),
   - el disparador: un workflow de GitHub Actions (`.github/workflows/release*.yml`) o un
     `cloudbuild*.yaml`, según `ci_plataforma`,
   - `LEEME.md` con los pasos de una sola vez ya rellenados con los valores del Proyecto: APIs,
     repositorio de Artifact Registry, roles de la service account, Workload Identity Federation
     (o la llave como secreto) y, con Cloud Build, el comando del trigger.
2. **Sin credenciales, por construcción**: el workflow autentica (`google-github-actions/auth`,
   con WIF o con el secreto referenciado por nombre) y el script solo construye y despliega.
3. **Dónde queda**: en el repositorio de control, carpeta `despliegue/`, en un solo commit
   ("Genera artefactos de despliegue en GCP..."), visible en la bitácora (ADR-0037). La plataforma
   los muestra con botón de copiar. **Publicarlos en el repositorio del código queda pendiente**
   hasta que exista el mecanismo real de credenciales de la cuenta de desarrollo (ADR-0013).
4. **Disparo**: botón "Generar release.sh" en la pestaña Implementación
   (`POST /proyectos/{id}/despliegue/generar`, `GET .../despliegue` para leer lo ya generado). Usa
   la configuración **guardada**; si faltan datos, responde con la lista de lo que falta. Al
   terminar registra la última ejecución de la Fase 4.
5. **Alcance actual**: backend en Cloud Run; frontend en Firebase Hosting o en Cloud Run. App
   Engine, GKE y Cloud Storage + CDN se rechazan explícitamente.
6. **Ajuste a la guía de ADR-0041**: `gcloud builds submit` también necesita
   `roles/storage.objectAdmin` y `roles/serviceusage.serviceUsageConsumer` en la service account;
   se agregaron a la guía de la plataforma y al LEEME generado.

## Consecuencias

- La skill no toca el repositorio del código: es la persona quien copia los archivos (o, más
  adelante, la skill de código los publicará vía PR con la cuenta de desarrollo).
- El script asume un `Dockerfile` en el directorio de cada servicio de Cloud Run y, con Firebase,
  un `firebase.json`; el LEEME lo dice. Generar esos archivos es trabajo de la skill de código (06).
- Las advertencias (frontend sin configurar, monorepo/multirepo sin elegir, sin repositorio de
  GitHub para armar los comandos de WIF) se devuelven junto con los archivos.
- La lista de campos faltantes existe dos veces (backend al generar, formulario en vivo): deben
  mantenerse alineadas.

## Pendiente

- Publicar los archivos en el repositorio del código (PR con la cuenta de desarrollo).
- Verificar el despliegue tras el release (ADR-0025) y el smoke testing contra el ambiente.
- Variables de entorno y secretos de la aplicación, base de datos gestionada, dominios.
- Otros destinos (App Engine, GKE, Cloud Storage + CDN) y otras nubes.
