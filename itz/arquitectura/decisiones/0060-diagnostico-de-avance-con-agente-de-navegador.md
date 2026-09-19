# ADR-0060: Diagnóstico de avance existente con el agente de navegador

## Estado

Aceptada. Implementa la skill 03 (`skills/03-diagnostico-de-avance-existente.md`) reutilizando el motor de ejecución de TCs de
[ADR-0059](0059-smoke-testing-por-hu-con-script-generado-desde-el-codigo.md). Aplica a los modos de arranque distintos de «nuevo» ([ADR-0007](0007-modos-de-arranque-de-proyecto.md)).

## Decisión

1. **Se corre antes de diseñar.** `POST /proyectos/{id}/hus/diagnostico?hu=`: ejecuta los TCs de cada HU contra el ambiente de desarrollo ya desplegado. Sin `hu`, las HUs que
   todavía no tienen diagnóstico; con `hu`, repite ese diagnóstico.
2. **Solo agente, sin código.** Es el agente de navegador de la skill 08 (la IA del Proyecto ve la página con el árbol de accesibilidad y actúa con Playwright) con las cuentas de
   prueba por rol. No genera script: no hay código nuevo que probar, solo un aplicativo que ya existe.
3. **Cobertura por TC:** `cubierto` (el TC pasó), `pendiente` (falló: el aplicativo no lo cumple) o `sin_evaluar` (sin cuenta de prueba para su rol). Se guarda en el TC
   (`cobertura`, `cobertura_detalle`) y se refleja en `test-cases.md` con la línea «Cobertura» y `fase: diagnosticada`.
4. **`sin_evaluar` cuenta como por cubrir.** Sin prueba de que exista, se construye; es la opción segura frente a omitir trabajo.
5. **La skill 05 solo descompone lo pendiente.** `tcs_por_cubrir(hu)` deja fuera lo `cubierto`: la descomposición recibe únicamente esos TCs. Una HU con todos sus TCs cubiertos queda en
   fase `cubierta` y no genera paquetes.
6. **Evidencia.** Cada corrida se guarda en Mongo (`smoke`, con `tipo: "diagnostico"`, sin mezclarse con las del smoke testing) y en el repositorio de control:
   `HU-00N/evidencia/diagnostico-0K.md` y una captura por TC. `GET /smoke?tipo=diagnostico` las lista.
7. **Interfaz.** Tarjeta «Diagnóstico de avance» en Diseño (solo si el modo no es «nuevo») con el resultado por HU y sus TCs pendientes, botón «Repetir» por HU, y paso
   recomendado «Diagnosticar el avance existente» antes de la arquitectura.

## Consecuencias

- Un TC mal interpretado por el agente puede dar un falso «pendiente»: se construye de más, pero nunca se omite algo que faltaba.
- Un falso «cubierto» sí omitiría trabajo; el agente solo declara «pasa» tras verificar el resultado esperado en la página (regla de la skill 08).
- Requiere ambiente accesible y cuentas de prueba; sin ellos todo queda `sin_evaluar` y el comportamiento es el de un proyecto nuevo.
- Probado contra una aplicación de demostración local (4 TCs): 2 cubiertos, 1 pendiente (función inexistente), 1 sin evaluar (rol sin cuenta); no se ha corrido contra un proyecto real.

## Pendiente

- Un TC `cubierto` que luego regresa debería detectarlo el smoke testing (ADR-0020); no se enlazan todavía.
- Correrlo en ITZ Inventarios e IAT para la tesis y medir aciertos contra una revisión manual.
