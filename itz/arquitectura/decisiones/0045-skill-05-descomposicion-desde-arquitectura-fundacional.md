# ADR-0045: Skill 05 — descomposición en paquetes de trabajo desde la arquitectura fundacional

## Estado

Aceptada. Implementa `skills/05-descomposicion-en-paquetes-de-trabajo.md` para Proyectos en modo
`nuevo` (Fase 3, Desarrollo). Adapta la ficha, pensada para partir de un `plan.md` por HU, al
flujo fundacional de [ADR-0044](0044-skill-04-arquitectura-fundacional-documento-y-aprobacion.md).

## Contexto

La ficha de la skill 05 parte de un `plan.md` por HU (modo extensión). En modo fundacional no hay un
plan por HU: hay una arquitectura por repositorio, aprobada por la persona, y hace falta además
construir primero el esqueleto del aplicativo, que no pertenece a ninguna HU.

## Decisión

1. **Precondición**: arquitectura **aprobada** (ADR-0044) y HUs con casos de prueba. Sin eso la
   skill se detiene y lo dice. Las Actividades no se descomponen (ADR-0026).
2. **Dos pasos de análisis**:
   - **Planeación** (una vez): con la arquitectura y el resumen de las HUs, el análisis define los
     paquetes del **esqueleto** (grupo `BASE`: estructura del proyecto, configuración, migración
     base, seguridad base sin reglas de negocio, shell del frontend, Docker y CI; 3 a 6 paquetes) y
     el **orden y las dependencias entre HUs** (ADR-0030). Las dependencias se depuran: se quitan
     ids desconocidos y autodependencias y, si hay un ciclo, se rompen solo las dependencias de
     quienes lo forman.
   - **Descomposición por HU**: cada HU se parte en 1 a 4 paquetes de una sola capa (backend,
     frontend o infra), con entregables concretos según la estructura de carpetas de la
     arquitectura, los TCs que cubre y sus dependencias internas. El backend va antes que el
     frontend que lo consume (ADR-0029).
3. **Cada paquete toca exactamente un repositorio** (ADR-0005): en monorepo, el único; en multirepo,
   el de su capa (falla con un mensaje claro si falta el de frontend o backend).
4. **Dependencias**: dentro de un paquete, `depende_de` lista los paquetes del esqueleto de su capa
   (`BASE/PT-02`) y los anteriores de la misma HU (`PT-01`); las dependencias **entre HUs** se guardan
   en la propia HU (`depende_de`) en vez de multiplicarlas en cada paquete.
5. **Criterio de éxito**: todo TC de la HU queda cubierto por al menos un paquete. Si el análisis
   deja alguno sin asignar, se agrega al último paquete de backend y la HU se marca "Revisar TCs".
6. **Ramas**: `hu/{id_fuente}/{paquete_id}` (ADR-0021); para el esqueleto, `base/{paquete_id}`.
7. **Salidas**: en el repositorio de control, por grupo, `tasks.md` y `paquetes/PT-0N.md` con el
   front-matter de la ficha (`estado: pendiente`, `ronda: 1`, `pr: null`...); un commit por grupo,
   sin tocar `spec.md` ni `test-cases.md`. En la base de datos, la colección `paquetes`, que es lo que
   lee la plataforma (`GET /proyectos/{id}/paquetes`). La HU pasa a fase `descompuesta`.
8. **Idempotencia y trabajo en curso**: volver a correr la skill regenera los paquetes, salvo los
   de una HU que ya tenga algún paquete fuera de `pendiente`, que se conservan.
9. **Ejecución**: `POST /proyectos/{id}/hus/descomponer`, con el mismo progreso en vivo, y el botón
   "Descomponer en paquetes de trabajo" en la pestaña Desarrollo. Su habilitación depende de sus
   propias precondiciones (arquitectura aprobada), no de que la Fase 3 esté "configurada": no
   necesita todavía la cuenta de desarrollo.

## Consecuencias

- Es el insumo de la skill 06 (generación de código), que tomará los paquetes en orden, creará la
  rama de cada uno y abrirá su PR con la cuenta de desarrollo (ADR-0043).
- Los TCs son de UI (Playwright): un TC "cubierto" por un paquete de backend solo pasa cuando también
  está listo el frontend; por eso el campo `tcs_asociados` indica cobertura, no que ese PR lo haga
  pasar solo.
- Un análisis por HU (~15 s cada uno; unos 8 minutos para 27 HUs).
- Se endureció el manejo de la falla conocida del LLM que devuelve arreglos como texto JSON: antes
  de darla por inválida se intenta decodificarlos.

## Pendiente

- Criterio de tamaño razonable de un paquete (pendiente ya anotado en la ficha).
- Creación del paquete en Jira/GitHub vía MCP (ADR-0024): no implementada; `id_externo` queda `null`.
- Modo extensión (parte de `plan.md` por HU) y rondas de fixes (`ronda` 2+).
- Regenerar solo una HU; cambiar el orden a mano.
