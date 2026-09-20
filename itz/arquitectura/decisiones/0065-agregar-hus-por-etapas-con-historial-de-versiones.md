# ADR-0065: Agregar HUs por etapas, sin perder avance, con historial de versiones

## Estado

Aceptada. Ajusta las skills 01, 04 y 05 ([ADR-0040](0040-deteccion-de-cambios-en-la-fuente-y-regeneracion-selectiva.md), [ADR-0044](0044-skill-04-arquitectura-fundacional-documento-y-aprobacion.md), [ADR-0045](0045-skill-05-descomposicion-desde-arquitectura-fundacional.md)).

## Contexto

Se puede leer un subconjunto de HUs, generar sus casos de prueba y, después, leer otras. Al revisar ese escenario aparecieron cuatro huecos: no se veía por HU qué tenía (especificación, casos de prueba, paquetes); la arquitectura ya aprobada no sabía de HUs posteriores; «Volver a descomponer» reemplazaba siempre el esqueleto, aunque tuviera PRs; y la especificación y los casos de prueba solo guardaban su versión actual (el historial vivía en el git local del repositorio de control, que se pierde si se reinicia el proyecto).

## Decisión

1. **Estado por HU visible.** «Ver HUs» muestra por HU si tiene especificación, cuántos casos de prueba y cuántos paquetes fusionados. La lista de Jira muestra también las HUs ya leídas («Ya leídas») con su estado, además de las nuevas o modificadas.
2. **La arquitectura registra qué HUs consideró** (`arquitectura_hus`). Si se leen HUs después de generarla, la interfaz avisa y recomienda regenerarla y aprobarla otra vez. Los proyectos anteriores a este registro no muestran el aviso.
3. **El esqueleto con avance no se reemplaza.** Al volver a descomponer, si algún paquete de `BASE` ya no está `pendiente` se conserva tal cual (como ya ocurría con las HUs en curso); solo se recalcula el orden de las HUs.
4. **Historial en Mongo** (colección `hu_versiones`). Cada vez que cambia el contenido de `spec.md` o `test-cases.md` de una HU se guarda una versión nueva (tipo, número, motivo, fecha, fase y contenido; en los casos de prueba, también los casos estructurados). No se sobrescribe ni se borra ninguna. La identidad es el elemento de la fuente (`fuente_ref`, p. ej. ITZINV-12) y no el id interno HU-00N, así la numeración sigue aunque el proyecto se reinicie. Guardar sin cambios no crea versión. Las HUs anteriores al versionamiento reciben su contenido actual como versión 1 al consultarlas. `GET /hus/{id}/versiones` y la pestaña «Historial» del detalle de HU lo muestran.

## Consecuencias

- Un reinicio del proyecto borra las HUs pero no su historial de versiones.
- No hay restauración automática de una versión ni comparación entre versiones (solo lectura).
- El historial guarda el texto completo de cada versión: crece con cada regeneración.
- El motivo de la versión es una etiqueta simple (generada, regenerada, generados, regenerados, diagnóstico de avance).
- Probado: la protección del esqueleto con un proyecto desechable, y el versionamiento con guardados repetidos, cambios y un reinicio; el aviso de arquitectura se verificó en pantalla simulando una HU posterior.

## Pendiente

- Versionar también los paquetes de trabajo y la arquitectura.
- Comparar dos versiones y restaurar una.
