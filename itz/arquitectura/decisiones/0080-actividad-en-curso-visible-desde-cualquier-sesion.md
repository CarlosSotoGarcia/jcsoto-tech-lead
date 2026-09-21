# ADR-0080: Actividad en curso visible desde cualquier sesión

## Estado

Aceptada. Da respuesta al pendiente del [ADR-0074](0074-avanzar-con-una-hu-de-punta-a-punta.md) (estado consultable de un proceso largo).

## Contexto

El panel «Actividad» seguía solo la conexión que abrió su propia pestaña. Un proceso lanzado por otra pestaña, otra persona o un script (como los avances de HU en el piloto) corría en el servidor pero el panel decía «Sin actividad todavía». Además, lanzar una segunda corrida desde la pantalla mezclaba el registro de las dos.

## Decisión

1. **El servidor registra la corrida más reciente de cada Proyecto** (skill, estado `corriendo`/`terminada`/`error`, inicio, fin y los últimos 400 eventos) y la expone en `GET /hus/actividad`.
2. **El panel consulta ese registro cada 4 segundos** cuando no tiene una corrida propia y, si algo corre, lo muestra («En el servidor · …») con su progreso y su registro.
3. **Un solo proceso a la vez desde la pantalla:** mientras haya una corrida propia o ajena en curso, el panel ignora una nueva y los botones de ejecución se deshabilitan.

## Consecuencias

- El registro vive en memoria del backend: se pierde al reiniciarlo y no distingue varias corridas simultáneas del mismo Proyecto (se muestra la última).
- No cancela ni reanuda procesos; solo los hace visibles.

## Pendiente

- Persistir el registro en Mongo y mostrar el historial de corridas.
- Poder cancelar una corrida desde el panel.
