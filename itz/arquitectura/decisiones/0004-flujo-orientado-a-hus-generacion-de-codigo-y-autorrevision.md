# ADR-0004: El flujo se orienta a partir de HUs — el skill genera código, abre PRs y se autorrevisa

## Estado

Aceptada. Reemplaza a [ADR-0003](0003-codigo-como-eje-principal-hus-prototipos-como-contexto-secundario.md).

## Contexto

ADR-0003 planteaba un skill que analiza principalmente código ya existente (diff de un PR escrito por
una persona) y usa la historia de usuario (HU) solo como contexto opcional. Al detallar el flujo real
que se espera del sistema, queda claro que la HU no es contexto secundario: es la entrada primaria y el
disparador de todo el pipeline. El sistema no solo revisa código — lo genera, lo somete a su propio
ciclo de revisión, lo prueba y lo corrige. Esto contradice directamente a ADR-0003, que queda
reemplazado por este ADR.

## Decisión

El flujo end-to-end, por historia de usuario, es:

1. **Lectura de la HU** y sus criterios de aceptación.
2. **Generación de casos de prueba (TCs)** a partir de los criterios de aceptación.
3. **Diseño de arquitectura** de la solución para esa HU, a partir de los TCs.
4. **Descomposición en subtareas** de la HU.
5. Por cada subtarea: **generación de código** y apertura de **Pull Request**.
6. **Revisión de código** de cada PR.
7. El sistema **lee las observaciones de la revisión, aplica los cambios y sube una nueva versión** —
   este ciclo (6→7) se repite hasta que no hay más observaciones.
8. Una vez que el PR está limpio y fusionado a `develop`, se ejecutan los **smoke tests** (ver
   ADR-0005) contra el ambiente de desarrollo desplegado, generando evidencia.
9. Si hay TCs fallidos, se genera una **subtarea de fix**, que reentra al flujo desde el paso 5 (nuevo
   código → nuevo PR → nueva revisión) y vuelve a ejecutar los TCs correspondientes al terminar.
10. Todo el proceso queda documentado: HUs, subtareas, observaciones de revisión y evidencia de
    pruebas (ver ADR-0006 sobre dónde vive esa documentación).

El sistema se organiza como **un skill orquestador** que sabe en qué fase del flujo está una HU/subtarea
dada, y **un skill especializado por fase** (análisis de HU + generación de TCs, diseño de arquitectura,
descomposición en subtareas, generación de código, revisión de código, smoke testing, generación de
fixes) que el orquestador invoca según corresponda. Ver el diagrama de flujo y el de skills en
[`../diagramas/`](../diagramas/).

## Consecuencias

- El alcance del skill crece de forma sustancial frente a ADR-0003: ya no es un asistente de revisión
  de código ajeno, sino un orquestador de un ciclo completo de desarrollo asistido — genera, revisa,
  prueba y corrige.
- Se necesita capacidad operativa real: crear ramas y commits, abrir y actualizar PRs, leer comentarios
  de revisión, y hacer merge. Esto **no contradice ADR-0002**: la ejecución sigue siendo puntual y bajo
  demanda por HU (no un servicio persistente propio del proyecto), y el ambiente de desarrollo contra
  el que se valida es externo — ya desplegado por quien use el sistema, no infraestructura que la tesis
  deba operar.
- Se necesita un mecanismo explícito de descomposición de HU → subtareas y de fallo de TC → subtarea de
  fix, con criterio claro de cuándo una HU se considera completa (todas sus subtareas con PR fusionado
  y smoke tests en verde).
- Pendiente de ADR: cómo se representa y persiste el estado de una HU a través de las fases (qué
  subtareas existen, en qué fase está cada una, historial de observaciones e iteraciones) — es la base
  para que el skill orquestador sepa "en qué fase va" y pueda reaccionar en consecuencia.
- La evaluación de la tesis (objetivos 4 y 5 en `00-vision-general.md`) debe actualizarse: ya no se
  mide solo precisión de revisión sobre PRs ajenos, sino la calidad de todo el ciclo — TCs generados,
  código producido, tasa de correcciones necesarias por ronda de revisión, y tasa de éxito de smoke
  tests por iteración.
