# ADR-0012: Plataforma de visualización de avance y reportes

## Estado

Aceptada

## Contexto

Se requiere una plataforma donde, además de dar de alta Proyectos (ADR-0009), se pueda **visualizar el
avance de cada HU** a través de las fases del pipeline (una especie de log/timeline de progreso) y
**generar reportes** agregados — las métricas que ya pedía el objetivo específico 11 de
`00-vision-general.md` (tasa de TCs, rondas de revisión, éxito de smoke tests, generalización, etc.).

Esto expuso un pendiente que venía arrastrándose desde ADR-0008/0009 sin resolverse del todo: **dónde
vive físicamente** la carpeta de documentación por HU (`spec.md`, `test-cases.md`, `plan.md`,
`tasks.md`, `subtareas/`, `evidencia/`). Sin una respuesta única, la plataforma no tiene un lugar
consistente de dónde leer el estado de todas las HUs de un Proyecto, sobre todo cuando ese Proyecto
tiene N repositorios (ADR-0005).

## Decisión

1. La plataforma es de **solo lectura respecto al pipeline**: no dispara fases ni sustituye al
   orquestador — únicamente refleja el estado que las skills ya escribieron. Esto no aplica a la
   **configuración** del Proyecto: dar de alta un Proyecto, y administrar cosas como la lista de
   usuarios autorizados a aprobar (ADR-0015), sí son acciones de escritura de la plataforma — la
   restricción de solo lectura es sobre el estado de HUs/subtareas en curso, no sobre la configuración.
   La plataforma expone:
   - Un **log/timeline por HU**: las transiciones de fase, leídas del front-matter de los archivos SDD
     (ADR-0008) y de su historial en `git log` sobre esos archivos (ya establecido en ADR-0008 como
     auditoría "gratis").
   - **Reportes agregados** por Proyecto (y, más adelante, entre Proyectos): las métricas del objetivo
     11 de `00-vision-general.md`.
2. La carpeta de documentación por HU vive en **un repositorio de control por Proyecto**, no dispersa
   dentro de cada repo backend/frontend configurado (ADR-0005). La plataforma tiene así un solo lugar
   por Proyecto de dónde leer, sin importar cuántos repos objetivo tenga ese Proyecto ni si una HU toca
   uno o varios a la vez.

## Consecuencias

- La configuración de Proyecto (ADR-0009) gana un campo más: el repositorio de control donde vive la
  documentación de sus HUs. Pendiente de detallar: ¿se declara explícito al dar de alta el Proyecto, o
  la plataforma crea uno por default?
- La plataforma probablemente necesita algún mecanismo de sincronización/lectura sobre ese repo de
  control para reflejar cambios en (casi) tiempo real — sin comprometer tecnología todavía; seguimos en
  documentación, no en implementación.
- Los reportes se arman agregando esos mismos archivos — no se asume una base de datos separada por
  ahora; sería una optimización a evaluar más adelante, no parte del diseño actual.
- No cambia nada de las skills ya documentadas (01, 02): siguen escribiendo los mismos archivos con el
  mismo contrato de ADR-0008, solo se fija dónde viven físicamente.
- Las skills que generan código y PRs (pendientes de documentar) leen/escriben en dos lugares
  distintos: el repo de control (documentación SDD) y el/los repo(s) objetivo (código real, ADR-0005) —
  vale la pena tenerlo presente al detallarlas para no asumir que todo vive en un solo repositorio.
