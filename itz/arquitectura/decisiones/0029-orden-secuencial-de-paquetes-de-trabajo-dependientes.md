# ADR-0029: Paquetes de trabajo dependientes entre repos se generan en orden secuencial, no en paralelo

## Estado

Aceptada. Cierra el pendiente de `skills/06-generacion-de-codigo.md` sobre coordinación entre paquetes
de trabajo relacionados que tocan repos distintos.

## Contexto

Cuando una HU requiere cambios coordinados en más de un repositorio (p. ej. backend y frontend, unidos
por `depende_de`, `skills/05-...md`), quedaba sin decidir si ambos se generan en paralelo (abriendo los
dos PRs a la vez sobre ramas que se integran después) o en secuencia estricta.

## Decisión

Se generan en **secuencia estricta**, no en paralelo. Si el frontend depende del backend, el paquete de
trabajo de frontend **no empieza** (no se invoca `skills/06-...md` para él) hasta que el paquete de
backend del que depende está fusionado. Cada paquete, al completarse su código, pasa por su propio
ciclo de calidad completo (`skills/06-...md` → `skills/07-...md` → merge, ADR-0028) de forma
independiente — no se generan varias capas de una HU a la vez.

Los smoke tests siguen siendo a nivel HU (ADR-0020/0023): esta secuencia solo afecta el orden de
generación y revisión de código, no cuándo se valida el comportamiento completo.

## Consecuencias

- Telar necesita acceso a todo lo "alcanzable" para una HU (todos los repos involucrados, ya
  configurados por Proyecto, ADR-0005) para poder recorrer la secuencia completa sin intervención
  externa entre pasos.
- Es más simple de razonar y más seguro (el paquete dependiente siempre trabaja contra código ya
  fusionado, nunca contra una rama en progreso) a cambio de ser más lento que generar en paralelo.
- El orquestador (`skills/00-...md`) despacha `06` para un paquete solo cuando todos los paquetes en su
  `depende_de` están `fusionado` — ya es consistente con cómo `depende_de` se documentó desde
  `skills/05-...md`, esto solo confirma que la espera es secuencial y no solo a nivel de merge final.
