# ADR-0059: Smoke testing a nivel de HU con un script de Playwright generado desde el código

## Estado

Aceptada. Implementa la skill 08 (`skills/08-smoke-testing.md`), con el mecanismo de ejecución de TCs que la ficha comparte con la skill 03.
Resuelve los pendientes de [ADR-0016](0016-cuentas-de-prueba-por-rol-para-ejecucion-de-tcs.md) sobre TCs sin cuenta y la representación de las corridas de
[ADR-0020](0020-smoke-testing-corre-todos-los-tcs-como-regresion.md).

## Decisión

1. **Se ejecuta a nivel de HU** y no por paquete: una HU se prueba cuando todos sus paquetes están fusionados (ADR-0023); `forzar=true` prueba lo que ya hay.
   `POST /proyectos/{id}/hus/smoke-testing?hu=&forzar=&regresion=`; sin `hu`, todas las HUs terminadas, en su orden.
2. **La IA lee el código y escribe un script de Playwright (Python) por HU.** Se toman fragmentos del código real del repositorio de frontend en su rama base
   (primero los archivos que tocaron los PRs de la HU; luego rutas, acceso y plantillas; hasta ~50 KB) y los casos de prueba de la HU. La IA devuelve una función
   `tc_NNN(page, base_url, usuario, contrasena)` por TC, basada en rutas, etiquetas e ids reales. Si no hay repositorio de frontend, se escribe solo con los TCs.
3. **Los scripts se validan antes de ejecutarse** (análisis estático): una sola función por TC con esa firma, sin imports, sin `eval/exec/open/getattr`, sin acceso a
   `os/sys/subprocess...` ni a atributos `__x__`. Un script inválido no se ejecuta: ese TC pasa a la verificación del agente.
4. **Ejecución aislada.** La suite corre en un proceso aparte (`python -I`), sin las variables `LOOM_*`, `ANTHROPIC_*` ni `GEMINI_*`, con un contexto de navegador limpio por TC,
   la cuenta de prueba del rol del TC y una captura de pantalla por TC. Las contraseñas llegan por stdin, nunca por la línea de comandos ni a la IA, y se enmascaran
   en cualquier mensaje.
5. **Un agente de navegador verifica los fallos.** Si el script de un TC falla, un agente (la IA del Proyecto, viendo la página real con el árbol de accesibilidad de
   Playwright y actuando con Playwright) intenta ejecutar el TC. Si pasa, el script estaba mal: el resultado es «pasa» y el script se reemplaza por el que resultó de los
   pasos del agente; si falla, es un fallo real del aplicativo y queda con el motivo observado. Un TC nunca puede terminar en «pasa» sin haber verificado su resultado.
6. **TCs sin cuenta: bloqueados.** Si el TC pide un rol sin cuenta de prueba configurada, no se ejecuta y queda «bloqueado» con ese motivo (pendiente de ADR-0016).
   La configuración del Proyecto tiene una lista de cuentas de prueba por rol (usuario y contraseña; la contraseña no se devuelve por la API, y vacía al editar conserva la guardada).
7. **Evidencia y regresión (ADR-0020).** Cada corrida se guarda en Mongo (`smoke`) y en el repositorio de control: `HU-00N/evidencia/smoke-0K.md` (informe con front-matter:
   TCs que pasan, fallan, están bloqueados y **regresiones**, es decir, los que pasaban en la corrida anterior), `smoke-0K/HU-00N_smoke.py` (el script de la HU, ejecutable a mano) y
   una captura por TC. `regresion=true` repite la corrida **solo con el script guardado, sin IA**: rápido, sin costo y determinista. Si todos los TCs pasan, la HU queda `completa`.
8. **Interfaz.** Botón «Probar HU» en cada HU con todos sus paquetes fusionados, etiqueta con el último resultado (`pasan/total`), diálogo con cada TC (origen: script o agente),
   captura, regresiones y botones «Repetir regresión (sin IA)» y «Volver a generar el script»; sección «Cuentas de prueba por rol» en Implementación (con los roles que piden los TCs
   para agregarlos de un clic) y paso recomendado «Probar las HUs terminadas».

## Consecuencias

- Es ejecución de código generado por IA en la máquina del backend: la validación y el proceso aislado reducen el riesgo, pero no es un sandbox; solo para desarrollo local.
- Chromium (Playwright) debe estar instalado en la máquina del backend.
- Un TC de UI escrito con poca información del código puede fallar por selectores; por eso el agente adjudica antes de dar un fallo por bueno.
- No se verifica todavía que el ambiente ya sirva el código recién fusionado (ADR-0025): solo que responda.
- Probado contra una aplicación de demostración local (login, existencias): scripts generados con «Claude (cuenta normal)» a partir de un repositorio local, un TC que pasa, uno sobre una función
  inexistente (falla confirmada por el agente), uno bloqueado por falta de cuenta, regresión detectada al romper la app y validador contra 9 scripts maliciosos; no se ha corrido contra el ambiente de un
  proyecto real.

## Pendiente

- Skill 09 (fixes): convertir un TC fallido en un paquete de fix.
- Diagnóstico de avance (skill 03) reutilizando este mismo motor antes de diseñar.
- Verificar el despliegue del ambiente (ADR-0025) y leer también el código del backend/API para TCs con datos.
- Configurar `TEST_*` en la CI del repositorio para ejecutar el script de la HU allí.
