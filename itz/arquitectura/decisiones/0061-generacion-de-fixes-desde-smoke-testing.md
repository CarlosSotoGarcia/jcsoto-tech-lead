# ADR-0061: Generación de fixes a partir de los fallos del smoke testing

## Estado

Aceptada. Implementa la skill 09 (`skills/09-generacion-de-fixes.md`). Resuelve los pendientes de la ficha sobre agrupación, atribución, regresiones y límite de rondas.

## Decisión

1. **Disparo.** `POST /proyectos/{id}/hus/generar-fixes?hu=`. Una HU es candidata si su último smoke testing tiene TCs en `falla` (los `bloqueado` no son un defecto del código), todos sus paquetes están
   fusionados y no hay fixes posteriores a esa corrida. Sin `hu`, todas las candidatas.
2. **Diagnóstico con IA.** Recibe la spec, la arquitectura, los TCs fallidos (esperado, observado y pasos del agente de la skill 08) y los paquetes ya fusionados con los archivos que tocó el PR de cada uno
   (mejor esfuerzo). Devuelve los fixes: capa, causa probable, entregables (siempre con una prueba que falle sin el fix), TCs cubiertos y `paquete_origen`.
3. **Agrupación:** un paquete por causa raíz probable; cada TC fallido queda en **exactamente un** fix (los duplicados se quitan; un TC sin asignar se agrega al último fix con un aviso).
4. **Atribución:** `paquete_origen` es mejor esfuerzo; si el id que devuelve la IA no existe en la HU, queda vacío. Nunca se inventa.
5. **Regresiones:** los TCs que pasaban en la corrida anterior se marcan `REGRESIÓN` en el análisis para que el fix no deshaga lo nuevo. No cambian la prioridad: el orden de trabajo sigue siendo el de los paquetes.
6. **Un fix es un paquete normal** (`tipo: fix`, `ronda` +1, `paquete_origen`, `evidencia_origen`, sin dependencias porque todo lo anterior ya está fusionado). Se escribe en Mongo y en `paquetes/PT-0N.md` y
   `tasks.md` del repositorio de control, y sigue el ciclo de las skills 06 y 07 sin trato especial. La HU pasa a fase `en_correccion`.
7. **Límite de rondas:** `MAX_RONDAS_FIX = 3`. Si tras tres rondas de fix la HU sigue fallando, la skill se niega y pide que una persona revise (evita ciclos indefinidos).
8. **Volver a probar.** Cada corrida de smoke guarda su `ronda`. Con todos los fixes fusionados, la interfaz recomienda volver a probar la HU (corrida completa, ADR-0020/0023).
9. **Interfaz:** paso recomendado «Corregir los fallos del smoke testing» y luego «Volver a probar las HUs corregidas»; botón «Generar fixes» en el diálogo del smoke testing; etiqueta `fix` y ronda en la lista de paquetes.
10. Vuelve a descomponer la HU (skill 05) reemplaza sus paquetes, fixes incluidos: los fixes son trabajo posterior a la descomposición y no se preservan si se rehace.

## Consecuencias

- Un diagnóstico equivocado produce un fix que no arregla el TC: se detecta en la siguiente corrida y consume una ronda del límite.
- El diagnóstico usa el resultado observado por el agente de navegador, no logs del servidor: fallos cuya causa está solo en el backend pueden atribuirse a la capa equivocada.
- Probado con una HU de demostración (1 TC pasa, 1 falla por botón inexistente, 1 regresión de filtro): 2 fixes de ronda 2 en el paquete de origen correcto, con prueba en los entregables; el ciclo completo
  (código, revisión, fusión y nueva corrida) no se ha corrido contra un proyecto real.

## Pendiente

- Métrica de retrabajo (fixes frente a paquetes originales) para el objetivo 11.
- Adjuntar al diagnóstico logs del backend y el diff del PR, no solo los nombres de archivo.
