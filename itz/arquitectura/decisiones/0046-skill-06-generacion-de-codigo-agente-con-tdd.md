# ADR-0046: Skill 06 — generación de código por un agente con herramientas acotadas y TDD

## Estado

Aceptada. Implementa `skills/06-generacion-de-codigo.md` para los paquetes de trabajo de
[ADR-0045](0045-skill-05-descomposicion-desde-arquitectura-fundacional.md), con la cuenta de
desarrollo y las copias locales de [ADR-0043](0043-copias-locales-cuenta-de-desarrollo-por-proyecto-y-publicacion-por-pr.md).

## Contexto

La skill 06 debe convertir un paquete de trabajo en un Pull Request con código real. Quedaban abiertos
cómo genera el código un LLM sin herramientas de un IDE, qué hace si el código no compila, y en qué
orden se ejecutan los paquetes (ADR-0029). Además se pidió que el desarrollo siga TDD, pensando en
las pruebas unitarias desde el principio.

## Decisión

1. **Un paquete a la vez, en orden.** `POST /proyectos/{id}/hus/generar-codigo?grupo=&pt=` (sin
   parámetros: el siguiente elegible). Es elegible un paquete `pendiente` con la arquitectura
   aprobada, la cuenta de desarrollo configurada y todas sus dependencias `fusionado`: las de paquete
   (`depende_de`, también entre grupos como `BASE/PT-02`) y las de HU (todos los paquetes de las HUs de
   las que depende). Primero el esqueleto `BASE`, luego las HUs. Si hay paquetes en revisión que
   bloquean a los pendientes, el mensaje lo dice y remite a «Sincronizar PRs».
2. **Agente con herramientas acotadas.** Un bucle de tool-use de Claude (`listar_directorio`,
   `leer_archivo`, `escribir_archivo`, `terminar`) sobre un *worktree* de la rama del paquete, creado
   desde la rama base actualizada (`TrabajoEnRama`). El agente no ejecuta comandos ni tiene red: solo
   archivos, confinados al worktree (rutas absolutas, `..` y `.git` rechazados), con límites de 40
   turnos, 60 archivos, 200 KB por archivo y 1.5 MB por paquete. Recibe el paquete, la arquitectura del
   repositorio, la spec y los TCs de la HU, los paquetes de los que depende y el árbol existente.
3. **TDD.** El prompt exige escribir primero la prueba unitaria de cada pieza de lógica (derivada de los
   criterios de aceptación y los TCs), y después la implementación mínima; y diseñar para ser
   probable (dependencias inyectadas, lógica separada de controladores y acceso a datos, pruebas sin
   red ni base de datos real). Se hace cumplir con una compuerta: en paquetes de capa `backend` o
   `frontend`, `terminar` se rechaza (hasta 2 veces) si no se escribió ningún archivo de prueba. Los
   paquetes de infra no la exigen; el esqueleto debe dejar configurado el tooling de pruebas con una
   prueba de humo. Los TCs de la HU son de UI (E2E) y no se implementan aquí: las pruebas unitarias los
   complementan.
4. **Sin ejecución local en v1.** No se compila ni se corren las pruebas antes de abrir el PR: la CI que
   crea `BASE/PT-01` (y la revisión, skill 07) dan la retroalimentación. Es una limitación asumida: el
   PR declara que el código no se ejecutó. Resuelve así el pendiente de la ficha ("abrir igual").
5. **Commit y PR.** Un commit con la identidad de la cuenta de desarrollo, `push --force-with-lease` de
   la rama `hu/{id_fuente}/{PT}` (o `base/{PT}`) y PR contra la rama base. La descripción lleva el
   paquete, sus entregables, los TCs, los supuestos heredados de la HU (ADR-0011), las notas del agente,
   el resumen, las pruebas unitarias escritas y los archivos resultantes.
6. **Estado.** El paquete pasa a `en_revision` con su `pr` (base de datos y `paquetes/PT-0N.md` del
   repositorio de control, un commit por cambio). `POST /proyectos/{id}/paquetes/sincronizar` consulta
   a GitHub: PR fusionado → `fusionado` (libera a los dependientes); cerrado sin fusionar → vuelve a
   `pendiente` para regenerarlo.
7. **Interfaz.** En la pestaña Desarrollo: botón por paquete (con candado y motivo si no es elegible),
   «Siguiente paquete» y «Sincronizar PRs», con el mismo progreso en vivo (una línea por archivo).
   «Ejecutar todas las fases» no genera código: cada PR es una decisión humana.

## Consecuencias

- Cada paquete cuesta una corrida larga del agente (minutos) y su PR debe revisarse y fusionarse antes
  de seguir con los dependientes: el flujo es deliberadamente secuencial (ADR-0029).
- Sin ejecutar el código, pueden llegar PRs que no compilan; la compuerta de pruebas asegura que
  existan, no que pasen. Ejecutar pruebas en un sandbox local queda como mejora.
- El agente ve solo el árbol y lo que lea; en repositorios grandes puede no encontrar convenciones
  relevantes. El límite de 60 archivos obliga a paquetes pequeños (coherente con ADR-0045).

## Pendiente

- Skill 07 (revisión) y rondas de corrección (`ronda` 2+, `rondas_revision`).
- Ejecutar build y pruebas localmente antes del PR.
- Reintentos y bloqueo al fallar repetidamente la generación de un paquete.
- Identificar los PRs generados por Loom con una etiqueta (hoy: autoría de la cuenta y pie del PR).
