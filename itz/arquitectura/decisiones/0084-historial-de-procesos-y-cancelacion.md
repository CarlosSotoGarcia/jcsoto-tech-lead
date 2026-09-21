# ADR-0084: Historial de procesos y cancelación

## Estado

Aceptada. Completa la actividad visible ([ADR-0080](0080-actividad-en-curso-visible-desde-cualquier-sesion.md)) y los procesos concurrentes ([ADR-0083](0083-procesos-concurrentes-con-reglas-de-exclusion.md)).

## Contexto

Los procesos vivían solo en la memoria del backend: al reiniciarlo se perdía qué se había ejecutado, sobre qué HU, cuándo empezó y cuándo terminó. Tampoco había forma de detener un proceso que ya no interesaba (por ejemplo, un avance de HU que consume tiempo y costo).

## Decisión

1. **Historial en Mongo.** Cada proceso se guarda en la colección `procesos` con su skill, las HUs sobre las que trabajó, el estado, cuándo se pidió, cuándo empezó a correr, cuándo terminó, el motivo y su registro de eventos (hasta 400). Se guarda al crear, al empezar, cada 20 eventos y al terminar, con un índice único por Proyecto y proceso. La memoria sigue siendo el estado vivo que necesitan las reglas de exclusión; Mongo es el registro permanente.
2. **Estados:** `en_cola`, `corriendo`, `terminada`, `error`, `rechazada`, `cancelada` e `interrumpida` (lo que estaba corriendo cuando se reinició el backend; se marca al arrancar).
3. **Consulta.** `GET /hus/procesos` (todo el Proyecto o `?hu=`) y `GET /hus/procesos/{id}` con el registro completo. El panel de actividad tiene un botón de historial que lista los procesos con inicio, fin y duración y abre el registro guardado de cualquiera; el detalle de cada HU tiene la pestaña «Procesos» con lo que se ejecutó sobre ella.
4. **Cancelación.** `POST /hus/actividad/{id}/cancelar` cancela un proceso en cola o corriendo: cancela la tarea que hace el trabajo y termina los procesos externos que lanzó (el agente por CLI, el contenedor de compilación, la suite de smoke, el release local) con `taskkill /T`. El panel muestra «Cancelar proceso» con confirmación. Lo que ya se hizo (commits, PR, archivos) se conserva; solo se corta lo que faltaba. **Cerrar o recargar la pantalla que lanzó un proceso NO lo cancela:** el proceso corre en su propia tarea en el servidor y la conexión solo lo va mostrando. Solo se detiene cancelándolo de forma explícita. (Una primera versión sí lo cancelaba al cerrar la conexión y una recarga de página mató un avance de HU y un smoke en curso; se corrigió.)
5. **El release que Loom lanza al completar una HU** también queda en el historial y se puede cancelar mientras espera turno o corre en la máquina; una corrida ya lanzada en GitHub Actions sigue allá aunque se cancele.

## Consecuencias

- Verificado con un proceso simulado con un proceso externo de 120 s: al cancelar, el proceso externo se detuvo, el flujo terminó en 0.1 s con el aviso y el proceso quedó `cancelada` en memoria y en Mongo. El historial y la pestaña de la HU se comprobaron con procesos reales que fallaron al instante. No se ha cancelado todavía un avance de HU real.
- Cancelar un contenedor de Docker mata el proceso local (`docker run`); el contenedor termina por su cuenta y se borra solo.
- Un proceso ya lanzado por la API sobrevive al reinicio del backend solo hasta que este se reinicia; luego queda `interrumpida`.

## Pendiente

- Reanudar un proceso interrumpido en lugar de solo marcarlo.
- Enlazar cada proceso del historial con las métricas de costo.
