# ADR-0037: Bitácora y resumen de ejecución por fase en la plataforma

## Estado

Aceptada.

## Contexto

Una vez que la plataforma permite dar play a una fase individual o a todas las configuradas
(ADR-0014, ADR-0034), falta que la persona pueda ver, sin salir de la pantalla del Proyecto, **qué
pasó la última vez que corrió cada fase**: cuándo fue, y un resumen de lo que se recuperó o generó
(cuántas HUs se descubrieron, cuántas ya tienen TCs, etc.), además de una bitácora legible de cada
artefacto que las skills fueron generando (`spec.md`, `test-cases.md`, ...).

ADR-0012 y ADR-0035 ya establecían que el `git log` del repositorio de control es, por
construcción, la auditoría de las transiciones de fase — no hace falta un mecanismo de logging
aparte para eso. Lo único que faltaba era: (1) exponerlo en la plataforma, y (2) una marca rápida
de "última vez que cada fase corrió sin error", que no conviene derivar del log completo cada vez
que se pinta la pantalla.

## Decisión

1. **Bitácora**: nuevo endpoint `GET /proyectos/{id}/bitacora` que lee el `git log` del
   repositorio de control local del Proyecto (`loom_target/<proyecto_id>/`, ADR-0035) y lo devuelve
   como lista de entradas (hash, fecha, mensaje del commit). No se guarda por separado — se lee tal
   cual del repo en cada consulta.
2. **Última ejecución por fase**: el `Proyecto` gana un campo operativo
   `fases_ultima_ejecucion: dict[str, str]` (fase → timestamp ISO), que el backend actualiza él
   mismo cuando el stream de una skill de fase termina sin error — no es parte del formulario de
   configuración, es estado que solo la plataforma escribe.
3. **Resumen por fase**: se calcula en el frontend a partir de la lista de HUs ya cargada (p. ej.
   "N HU(s), M actividad(es) descubiertas" para Fase 1; "N de M HU(s) con TCs generados" para
   Fase 2) — no requiere un endpoint nuevo, reutiliza `GET /proyectos/{id}/hus`.
4. La pantalla de Proyecto (antes un wizard de pasos) pasa a tabs: los datos generales (nombre,
   modo de arranque, estado) quedan fijos arriba, visibles sin importar qué fase se esté viendo, y
   cada tab de fase combina su resumen/última ejecución, su botón de play (si la fase tiene skill
   implementada y está configurada), y su configuración — coherente con que cada fase ya se
   ejecuta de forma independiente (ADR-0014).

## Consecuencias

- No se duplica el git log en otro almacenamiento — se mantiene como única fuente de verdad de qué
  se generó y cuándo, tal como ya establecía ADR-0008.
- `fases_ultima_ejecucion` sí es estado nuevo en Mongo (no derivable limpio del git log sin
  parsear mensajes de commit por fase) — es el único dato operativo que la plataforma persiste
  aparte del propio repositorio de control.
- La pantalla de alta de un Proyecto nuevo (sin HUs, sin bitácora todavía) sigue funcionando igual
  con los tabs — el resumen/bitácora simplemente no tiene nada que mostrar hasta la primera
  ejecución.

## Pendiente

- Si el volumen de commits crece mucho, la bitácora completa por Proyecto puede volverse pesada de
  leer/mostrar — paginación o límite de fecha, cuando haga falta.
