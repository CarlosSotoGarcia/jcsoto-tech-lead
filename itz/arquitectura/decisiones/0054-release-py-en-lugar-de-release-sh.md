# ADR-0054: El release se genera como `release.py` (Python) en lugar de `release.sh`

## Estado

Aceptada. Reemplaza la parte de [ADR-0042](0042-skill-10-generacion-de-release.md) que definía el artefacto como un script de shell
(`release.sh`); el resto de ADR-0041 y ADR-0042 (configuración de despliegue, disparadores, LEEME, publicación por PR) sigue vigente.

## Contexto

El script de release se generaba en Bash. La persona trabaja en Windows y el equipo puede ejecutar el release en su máquina, en GitHub Actions
o en Cloud Build; un script de shell no corre de forma natural en Windows y es más frágil con comillas y variables.

## Decisión

1. **El artefacto es `release.py`** (`release-backend.py` y `release-frontend.py` en multirepo): Python 3 con solo la biblioteca estándar, sin
   dependencias, que ejecuta los mismos pasos (construir la imagen con `gcloud builds submit`, desplegar con `gcloud run deploy`, o publicar el
   frontend en Firebase Hosting). Usa `shutil.which` para resolver `gcloud`, `npm` y `npx` también en Windows, se detiene si un comando falla y
   propaga su código de salida.
2. **Sigue sin credenciales.** La autenticación con GCP la hace quien lo ejecuta antes (workflow de GitHub Actions o Cloud Build); los valores del
   Proyecto se insertan como literales de Python seguros, y el nombre del Proyecto se sanea en el encabezado.
3. **Los disparadores ejecutan Python:** el workflow de GitHub usa `python3 release.py` y Cloud Build usa `entrypoint: python3`. El primer
   despliegue manual es `python release.py`.
4. **El nombre del secreto se valida.** Con autenticación por llave JSON, el nombre del secreto debe ser válido para Secret Manager (letras,
   números, `-` y `_`); un nombre de archivo `.json` se reporta como dato faltante, porque Loom nunca recibe la llave, solo el nombre del secreto
   donde se guardó.

## Consecuencias

- Los repositorios que ya publicaron `release.sh` con la versión anterior deben regenerar y volver a publicar (los nombres cambian).
- La imagen de Cloud Build `cloud-sdk` trae Python, pero no Node: la publicación en Firebase Hosting desde Cloud Build necesitaría un paso
  adicional (limitación que ya existía con el script en Bash).
- Se probó la generación de todas las combinaciones (monorepo/multirepo, Firebase/Cloud Run) y una ejecución simulada con `gcloud` y `npm` falsos;
  no se ha ejecutado contra GCP real.
