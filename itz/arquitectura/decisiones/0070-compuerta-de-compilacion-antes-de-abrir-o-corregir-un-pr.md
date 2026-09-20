# ADR-0070: Compuerta de compilación antes de abrir o corregir un PR

## Estado

Aceptada. Amplía las compuertas de la skill 06 ([ADR-0046](0046-skill-06-generacion-de-codigo-agente-con-tdd.md)) y la corrección de la skill 07 ([ADR-0049](0049-skill-07-revision-de-codigo-y-correcciones.md)).

## Contexto

Ni el agente que escribe el código ni la revisión compilan nada: el agente solo escribe archivos y la revisión lee el diff. En el piloto de la tesis llegó a `main` código que no compilaba en dos proyectos: una dependencia de Maven sin versión (escenario con Gemini) y una prueba con genéricos inválidos (escenario con Claude por CLI), esta última detectada hasta que falló el build de la imagen en el release, con los PR ya fusionados.

## Decisión

1. **Se compila antes de subir.** Después de que el agente escribe (y también tras una corrección de la revisión) y antes del commit, Loom compila la capa del paquete dentro de un contenedor de Docker: Maven (`test-compile`, con la versión de Java del `pom.xml`), Gradle, .NET, Python (`compileall`), Angular (`ng build` y las pruebas con `tsc`) o TypeScript (`tsc --noEmit`). Los paquetes de infraestructura no se compilan.
2. **Sin ensuciar la rama.** La carpeta de trabajo se monta de solo lectura y se copia dentro del contenedor; `target/`, `node_modules/` y demás quedan dentro y no llegan al commit. Los volúmenes de caché de dependencias se conservan entre corridas. Al contenedor no se le pasan las variables con secretos.
3. **Si falla, se le devuelve el error al agente** (hasta 2 correcciones) con el comando y la salida del compilador, y se vuelve a compilar.
4. **Si no se logra, no se esconde.** El PR se abre igual, con una advertencia en su descripción con la salida, el paquete guarda el resultado (`compilacion`) y la siguiente revisión agrega una observación **bloqueante** «el código no compila». La corrección vuelve a pasar por la compuerta.
5. **Se omite con aviso** si Docker no está disponible, si no se reconoce cómo compilar la capa o si se desactiva con `LOOM_COMPILAR_ANTES_DEL_PR=0`.
6. **Métrica.** Cada intento queda en las métricas como compuerta `compilacion` (ok, falla u omitida, con el intento y los segundos), para medir cuántos paquetes compilan a la primera y cuántos se arreglan con la compuerta.

## Consecuencias

- Requiere Docker en la máquina del backend; la primera compilación descarga las dependencias (unos 50 s en la prueba con Maven; unos 16 a 19 s con la caché).
- Compila, no ejecuta las pruebas: un código que compila puede seguir fallando en pruebas.
- Sube el tiempo y el costo por paquete cuando el agente tiene que corregir.
- Probado con el código real del escenario con el CLI: sobre el estado roto detectó el error de compilación y, con un agente simulado que lo arregla, terminó compilando tras una corrección; con un agente que no corrige, abrió el camino a la advertencia. No se ha corrido todavía con un agente real ni con una capa de frontend.

## Pendiente

- Ejecutar también las pruebas unitarias en el contenedor (las de integración que necesitan Docker quedan fuera).
- Reportar en el capítulo 5 cuántos paquetes compilan a la primera y cuántas correcciones necesita la compuerta.
