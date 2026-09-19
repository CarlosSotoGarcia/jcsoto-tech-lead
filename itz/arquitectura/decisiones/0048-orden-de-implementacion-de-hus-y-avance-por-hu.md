# ADR-0048: Orden de implementación de las HUs y avance por HU en Desarrollo

## Estado

Aceptada. Completa [ADR-0030](0030-paralelismo-entre-hus-con-dependencias.md) y
[ADR-0045](0045-skill-05-descomposicion-desde-arquitectura-fundacional.md), y cambia cómo la skill 06
([ADR-0046](0046-skill-06-generacion-de-codigo-agente-con-tdd.md)) elige el siguiente paquete.

## Contexto

La skill 05 calculaba un orden de las HUs y sus dependencias, pero el orden solo servía para procesarlas
en esa corrida: no se guardaba. La skill 06 elegía el siguiente paquete por id de HU (HU-001, HU-002...),
ignorando la prioridad de negocio y el orden real. Además, en Desarrollo no había forma de decidir con qué
HU avanzar.

## Decisión

1. **La fase de Requerimientos lee todas las HUs y registra su prioridad de negocio.** Jira se consulta
   con `ORDER BY Rank ASC` (el orden del sprint; si el proyecto no lo admite, por fecha de creación) y la
   posición se guarda en la HU como `orden_fuente`. Al volver a leer, el orden de la fuente se refresca sin
   usar IA aunque el contenido no haya cambiado. Mientras no exista otro, `orden` = `orden_fuente`.
2. **La skill 05 fija el orden de implementación (`orden`, 1 = primero)**: la prioridad de negocio manda,
   salvo que una dependencia real obligue a adelantar otra HU (orden topológico con desempate por prioridad).
   Sin prioridad de fuente (p. ej. Markdown) se usa el orden propuesto por el análisis. El prompt recibe la
   prioridad de cada HU y se le pide respetarla. Se guarda también para las HUs cuyos paquetes se conservan.
3. **La skill 06 elige por ese orden**: primero el esqueleto (`BASE`) y luego las HUs por `orden`;
   «Siguiente paquete» toma el primero elegible. Las dependencias siguen mandando (ADR-0029): un paquete
   con dependencias sin fusionar no se ofrece.
4. **Avance por HU.** `POST .../hus/generar-codigo?grupo=HU-00N` (sin `pt`) genera el siguiente paquete
   elegible de esa HU, para avanzar con la que se prefiera sin esperar su turno. Si está bloqueada, el
   error dice qué falta fusionar. No se salta ninguna dependencia.
5. **Interfaz.** La lista de paquetes se ordena por `orden` y muestra el número de cada HU; cada HU
   elegible tiene «Avanzar con esta HU». La lista de HUs muestra la columna Orden.

## Consecuencias

- Reordenar en Jira y volver a correr Requerimientos actualiza `orden_fuente`; `orden` solo se recalcula al
  volver a descomponer (skill 05).
- Al elegir una HU fuera de turno se puede trabajar en paralelo en HUs independientes, pero los paquetes
  dependientes siguen en secuencia estricta.
- Volver a especificar una HU ya no borra sus `depende_de` (antes se reiniciaban).

## Pendiente

- Reordenar o fijar el orden a mano desde la plataforma.
- Elegir un conjunto de HUs «en alcance» para el siguiente ciclo.
- Probar `ORDER BY Rank` contra un Jira real (hay respaldo por fecha si falla).
