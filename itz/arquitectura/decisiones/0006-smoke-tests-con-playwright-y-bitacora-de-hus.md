# ADR-0006: Smoke tests con Playwright (Python) y bitácora de HUs preferentemente en GitHub

## Estado

Aceptada la parte de Playwright. **Propuesta** (no cerrada) la parte de dónde vive la bitácora de HUs —
ver discusión abajo.

## Contexto

Una vez que una subtarea llega a `develop`, hay que validar contra el ambiente de desarrollo real (ADR-
0005) que los criterios de aceptación de la HU se cumplen, no solo que el código pasó revisión. Además,
todo el proceso (HUs, subtareas, observaciones de revisión, resultados de pruebas) necesita quedar
documentado de forma que se pueda ir armando la bitácora de lo que se corrigió conforme avanza el
pipeline, no solo al final.

## Decisión

**Smoke testing.** Los TCs derivados de los criterios de aceptación (ADR-0004, paso 2) se ejecutan como
smoke tests usando **Playwright para Python**: el skill de smoke testing genera los scripts de prueba a
partir de los TCs, los corre contra la URL del ambiente de desarrollo (ADR-0005), y produce evidencia
(capturas, resultado por TC) como salida.

**Documentación / bitácora.** Se prioriza documentar las HUs y el avance directamente en GitHub (issues
y/o PRs) en vez de solo archivos Markdown sueltos, cuando el repositorio de destino lo permite — esto
construye la bitácora de lo que se va corrigiendo como subproducto natural del propio flujo (comentarios
de revisión, commits, estado del PR), en vez de mantenerla por separado. Markdown queda como respaldo
para lo que no tiene un lugar natural en GitHub (p. ej. el diseño de arquitectura de una HU, si no se
quiere versionar como issue).

## Consecuencias

- Añade una dependencia técnica concreta: Playwright (Python) como motor de smoke testing — impacta el
  diseño del skill de esa fase y el formato en que se le deben entregar los TCs para poder generarle
  scripts ejecutables.
- La evidencia generada por los smoke tests (capturas, logs, resultado por TC) es un entregable en sí
  mismo, útil tanto para decidir si una subtarea pasa como para la evaluación de la tesis.
- La parte de "bitácora en GitHub" queda como **propuesta, no definitiva**: falta decidir el mapeo
  exacto HU → issue, subtarea → PR/checklist, y observación de revisión → comentario, antes de darla
  por Aceptada. Revisar y, si se confirma, promover esta sección a un ADR propio o actualizar el estado
  de este.
