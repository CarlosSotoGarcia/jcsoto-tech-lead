# ADR-0055: Ejecutar el release desde la plataforma y detectar cambios de infraestructura

## Estado

Aceptada. Completa [ADR-0042](0042-skill-10-generacion-de-release.md), [ADR-0043](0043-copias-locales-cuenta-de-desarrollo-por-proyecto-y-publicacion-por-pr.md)
y [ADR-0054](0054-release-py-en-lugar-de-release-sh.md): hasta ahora el `release.py` solo lo ejecutaba la CI (trigger de Cloud Build o GitHub Actions).

## Contexto

Los artefactos de despliegue se generan en el repositorio de control (`despliegue/`) y se publican por PR en el repositorio del código. Faltaba
poder ejecutar el release desde Loom y enterarse de cuándo un cambio de código afecta la infraestructura y conviene regenerar y volver a ejecutar.

## Decisión

1. **Botón «Ejecutar release» (pestaña Implementación).** `POST /proyectos/{id}/hus/ejecutar-release?confirmar=true` (con el mismo progreso en vivo
   del panel de actividad) descarga la rama base más reciente de cada repositorio en un worktree, escribe encima el `release.py` generado con la
   configuración guardada y lo ejecuta con el intérprete de Python del backend. Sin `confirmar=true` se rechaza; la pantalla pide confirmación
   explícita porque **despliega de verdad** en GCP y puede generar costos.
2. **Credenciales.** Loom no guarda llaves de GCP: la ejecución usa la sesión de `gcloud` de la máquina (se verifica que `gcloud` exista y tenga
   cuenta activa). Al proceso se le quitan del entorno las variables `LOOM_*`, `ANTHROPIC_*` y `GEMINI_*`. Los repositorios se ejecutan en orden (backend
   primero); si un script falla, se detiene y se muestra su salida. Se guarda la fecha y un resumen (cuenta y URL de los servicios) del último release.
3. **Detección de cambios de infraestructura.** Al fusionar un PR (desde Loom, ADR-0051, o al sincronizar), se consultan los archivos que cambió;
   si tocó `Dockerfile*`, `docker-compose*`, `cloudbuild*`, `firebase.json`, `.firebaserc`, `release*.py`, `nginx*.conf`, `.env.example`, `app.yaml` o
   workflows de GitHub, el Proyecto queda con el despliegue «desactualizado» y la lista de motivos (`paquete: archivo`). La pantalla muestra un aviso
   con esos motivos y pide regenerar `release.py`, volver a publicarlo y ejecutarlo. Regenerar limpia el aviso. Es una ayuda: si GitHub no responde
   no se bloquea la fusión.
4. **El script sigue saliendo de la configuración del Proyecto** (plantilla determinista): regenerar no cambia nada si la configuración no cambió;
   el aviso invita a revisarla (nombres de servicio, directorios, rama).

## Consecuencias

- Solo sirve donde el backend corre en una máquina con `gcloud` autenticado (desarrollo local); en un servidor compartido el release lo debe hacer la CI.
- La ejecución es real: es la única acción de la plataforma que puede generar costos en la nube; por eso exige confirmación.
- Se probó con un repositorio local y un `gcloud` falso (rama base, escritura del script, salida en vivo, URL, resumen guardado) y la interfaz en el navegador
  hasta el error controlado de un proyecto sin repositorios; no se ha ejecutado contra GCP real.

## Pendiente

- Paso opcional de IA que lea el repositorio y **proponga ajustes** a `release.py` (servicios nuevos, otros directorios), siempre por PR.
- Disparar el workflow de GitHub Actions (o el trigger de Cloud Build) en lugar de ejecutar local.
- Detectar también servicios y puertos nuevos comparando con la arquitectura.
