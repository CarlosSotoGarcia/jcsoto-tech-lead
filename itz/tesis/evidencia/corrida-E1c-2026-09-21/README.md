# Corrida E1c — ITZ Control Inventarios con Claude por CLI — 2026-09-21

Evidencia de la corrida completa (fases 1 a 4) del Proyecto «PILOTO E1c ITZ Inventarios (Claude cuenta normal CLI)» (id Loom `9c764535fb44470a8dc92fc74c8b835e`), operada desde la interfaz de Loom con Playwright. Respalda el capítulo 5 y el Anexo C de `Loom - Tesis v01.docx` (borradores `borrador/v01/f-capitulo-5-resultados.md` y `e-anexo-c-corrida-e1c.md`).

## Punto de partida

- Repositorio `CarlosSotoGarcia/loom-piloto-e1c-claude-cli`: `main` reiniciado al commit inicial (solo README) con force-push.
- Mongo: borrados todos los documentos del Proyecto en `hus`, `hu_versiones`, `paquetes`, `revisiones`, `smoke`, `metricas`, `procesos`; el documento del Proyecto conservó la configuración y se reinició su estado.
- Borradas las carpetas `loom/loom_target/<id>` y `loom/loom_repos/<id>`.
- Loom en el commit vigente del 2026-09-21; modelo `claude-sonnet-5` vía el CLI de Claude Code.

## Contenido

| Ruta | Qué es | ¿En git? |
|---|---|---|
| `capturas/` | 281 capturas de la interfaz, nombradas por paso (`NN[letra]-<qué>.png`). Inventario y mapeo a figuras del Anexo C en [CAPTURAS.md](CAPTURAS.md) | **No** (`.gitignore`); solo en disco local |
| `datos/` | Exportación de Mongo del Proyecto al terminar la corrida: `hus`, `hu_versiones`, `paquetes`, `revisiones` (con observaciones), `smoke` (resultado por caso), `metricas` (llamadas, compuertas, reintentos), `procesos` (duración y estado de cada ejecución) y `proyecto.json` (configuración, secretos enmascarados) | Sí |
| `artefactos/` | Copia del repositorio de control de Loom: `spec.md`, `test-cases.md`, `tasks.md`, paquetes y evidencia por HU; documento de arquitectura; archivos de despliegue generados | Sí |
| `logs/` | Registro del ciclo de paquetes (`ciclo_ui.log`), salidas de los guiones, y `descartadas/` (capturas de intentos fallidos, fuera de git) | Sí (salvo `descartadas/`) |
| `loom_ui.py` | Ayudante de Playwright: login, navegación, captura con nombre y espera del panel «Actividad» | Sí |
| `ciclo_ui.py` | Ciclo por paquete desde la UI: «Siguiente paquete» → «Revisar PRs» (una sola revisión) → espera los checks de GitHub → «Aceptar el PR» | Sí |
| `pasoN_*.py` | Un guion por paso (tabla siguiente) | Sí |

## Pasos ejecutados

| Paso | Guion | Acción en Loom | Resultado | Capturas |
|---|---|---|---|---|
| 1 | `paso1_fase1.py` | Ver HUs de Jira, seleccionar ITZINV-12/13/14, procesar | 3 HUs especificadas (1 min 24 s), todas con supuestos | 01–05 |
| 2 | `paso2_tcs.py` | Generar TCs | 44 casos (14/14/16) | 06–07 |
| 3 | `paso3_arquitectura.py` | Generar arquitectura | 5 entidades, 7 decisiones, 7 preguntas | 08 |
| 4 | `paso4_aprobar_arquitectura.py` | Ver documento y aprobar | Arquitectura aprobada | 09–12 |
| 5 | `paso5_descomponer.py` | Descomponer | **Falló**: sin paquetes para HU-003 tras 3 reintentos | 13-…-intento1 |
| 5b | `paso5b_redescomponer.py` | Volver a descomponer | 12 paquetes en 4 grupos | 13-…-intento2, 14 |
| 6 | `paso6_decisiones.py` | Decisiones pendientes: una decisión por HU (redactadas como política del piloto) | Supuestos confirmados | 15–16 |
| 7–9 | `paso7_primer_paquete.py`, `paso8_revisar_y_aceptar.py`, `paso9_aceptar.py` | BASE/PT-01: generar, revisar, aceptar | Fusionado (PR #32) | 17–22 |
| 23–33 | `ciclo_ui.py 23 11` (+ relanzamientos) | Resto de paquetes | 11 fusionados; ver `logs/ciclo_ui.log` | 23a–33f |
| 34–35 | `paso11_corregir_hu003.py`, `paso12_tras_correccion.py`, `paso13_aceptar_hu003.py` | HU-003/PT-02: compuerta y CI en rojo → 1 corrección → aceptar | Fusionado (PR #43) | 34–35c |
| 36 | — | Ruta con la Fase 3 completa | 12/12 fusionados | 36 |
| 37–38 | `paso14_release_generar.py`, `paso15_publicar.py` | Completar SA y proveedor WIF, generar `release.py`, publicar PR de despliegue | PR #44 | 37–38c |
| — | API (`logs/despliegue_fusionar_pr44.txt`) | Fusionar el PR de despliegue | La UI no tiene botón para esto | — |
| 39 | `paso16_release.py` | Ejecutar release | 1.er intento falló (Flyway checksum con BD previa); BD `inventarios` recreada; 2.º intento OK (8.5 min) | 39–39c |
| 40–41 | `paso17_url_ambiente.py` | Registrar URL del ambiente | `https://inventarios-web-118746543308.us-central1.run.app` | 40–41 |
| — | SQL (fuera de Loom) | Sembrar 3 cuentas de prueba (admin, usuario final, inactivo) en Cloud SQL | El código generado no tiene alta de usuarios | — |
| 42–44 | `paso18_smoke.py HU-00N NN` | Smoke testing por HU | 36 pasan, 2 fallan, 6 bloqueados | 42a–44f |
| — | `paso19_detalle_hu.py` | Detalle de HU: especificación, casos, paquetes, resultado de smoke | — | 06b, 07b, 14b, 42e–44f |

`paso10_avanzar_hu003.py` fue un intento de usar «Avanzar con esta HU» que no aplicaba (el botón no aparece con un paquete ya con observaciones); no produjo capturas útiles.

## Intervenciones fuera de Loom

1. Fusión del PR de despliegue (#44) con `POST /proyectos/{id}/despliegue/fusionar` (misma regla de CI en verde).
2. Recreación de la base de datos `inventarios` en Cloud SQL (`gcloud sql databases delete/create`), autorizada por el usuario.
3. Siembra de las cuentas de prueba con `gcloud sql import sql` (archivo temporal borrado del bucket; permiso temporal al bucket retirado).

## Cómo reproducir

Con Loom levantado (`make dev` en `loom/`) y el Proyecto limpio como en «Punto de partida», correr los guiones en el orden de la tabla desde esta carpeta (`python -X utf8 pasoN_*.py`). Los guiones usan el usuario semilla `admin` de Loom y el id del Proyecto fijo en `loom_ui.py`.
