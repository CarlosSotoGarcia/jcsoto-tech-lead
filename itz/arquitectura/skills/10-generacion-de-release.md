# Skill — Generación de release

**Alias:** skill 10, Fase 4 (Implementación) — ADR-0034, ADR-0042.

## Propósito

Convertir la configuración de despliegue en GCP de un Proyecto (ADR-0041) en los archivos que hacen
el despliegue: un `release.py`, el disparador que lo ejecuta cuando cambia el repositorio y un
LEEME con los pasos de una sola vez. Es determinista: plantillas, sin LLM.

## Cuándo se invoca

Bajo demanda desde la plataforma (botón "Generar release.py" en la pestaña Implementación), una vez
que la configuración de despliegue está completa y guardada. No lo despacha el orquestador todavía.

## Entradas

- `despliegue_gcp` del Proyecto (proyecto, región, servicios, Artifact Registry, disparador, CI,
  autenticación, service account, proveedor WIF o nombre del secreto).
- `estructura_repositorios` (monorepo o multirepo) y la lista de repositorios (para derivar el
  dueño/repositorio de GitHub de los comandos de Workload Identity).

## Salidas

En el repositorio de control, carpeta `despliegue/` (un commit):

- Monorepo: `release.py`. Multirepo: `release-backend.py` y, si hay frontend, `release-frontend.py`.
- Si `ci_plataforma` es GitHub Actions: `.github/workflows/release*.yml` (disparo por push a rama, por
  tag `v*` o solo manual; siempre `workflow_dispatch`). Si es Cloud Build: `cloudbuild*.yaml`.
- `LEEME.md` con los pasos de una sola vez rellenados con los valores del Proyecto.

Ningún archivo contiene credenciales: el workflow se autentica antes de ejecutar el script.

## Qué hace (alto nivel)

1. Valida que la configuración esté completa; si no, devuelve la lista de lo que falta.
2. Elige la forma de los artefactos según monorepo/multirepo, hosting del frontend y CI.
3. Rellena las plantillas, escribe todo en `despliegue/` y hace un solo commit.
4. Devuelve los archivos y las advertencias, y registra la última ejecución de la Fase 4.

## Artefacto: release.py

El script se genera en Python (`release.py`) y no en Bash — [ADR-0054](../decisiones/0054-release-py-en-lugar-de-release-sh.md).

## ADRs relacionados

- [ADR-0054](../decisiones/0054-release-py-en-lugar-de-release-sh.md) — `release.py` en lugar de `release.py`.

- [ADR-0041](../decisiones/0041-configuracion-de-despliegue-gcp-para-release-sh.md) — la configuración.
- [ADR-0042](../decisiones/0042-skill-de-release-generacion-de-release-sh.md) — esta skill.
- [ADR-0013](../decisiones/0013-cuenta-de-desarrollo-dedicada-para-acceso-a-repositorios.md) y
  [ADR-0032](../decisiones/0032-mecanismo-de-credencial-de-la-cuenta-de-desarrollo.md) — cómo se
  publicaría en el repositorio del código y por qué no hay credenciales en la configuración.
- [ADR-0025](../decisiones/0025-verificacion-de-despliegue-antes-de-smoke-testing.md) — lo que sigue
  tras el release.

## Criterios de éxito

Con la configuración completa, se generan los archivos, `python -m py_compile release.py` valida, los YAML son
válidos y ninguno contiene una llave o token.

## Pendientes propios de esta skill

- ~~Publicar los archivos en el repositorio del código vía PR~~ — resuelto en
  [ADR-0043](../decisiones/0043-copias-locales-cuenta-de-desarrollo-y-publicacion-por-pr.md): botón
  "Publicar en el repositorio (PR)", con la cuenta de desarrollo del Proyecto.
- Destinos distintos de Cloud Run (App Engine, GKE) y otras nubes.
- Que el orquestador la despache como parte del flujo de la Fase 4.
