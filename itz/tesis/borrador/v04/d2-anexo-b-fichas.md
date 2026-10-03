@@ tesis_anexos+
CAPITULO: B
### Anexo B. Fichas de las *skills*

Cada ficha es el documento de diseño de una *skill* tal como está en el repositorio de arquitectura: su propósito, cuándo se invoca, sus entradas y salidas, lo que hace, los registros de decisión relacionados, sus criterios de éxito y los pendientes de diseño que quedaron abiertos. Los documentos de diseño llaman *Telar* al orquestador con sus *skills*; en esta tesis se usa Loom para el conjunto. Las fichas describen el diseño; lo que de cada función se implementó y se ejercitó está en la tabla 4.5.

### B.1 Orquestador
No es una skill de fase como las demás (01-09): es el despachador que decide, para cada HU o paquete de trabajo, cuál de esas 9 skills invocar a continuación — ninguna skill de fase llama a otra directamente, siempre pasan por aquí (ver notas del diagrama 02).
*Propósito*
Mantener el estado de cada HU/paquete de trabajo de un Proyecto y decidir, en cada momento, qué skill de fase ejecutar — ya sea siguiendo el flujo secuencial completo (comportamiento por defecto, ADR-0004) o despachando una sola fase bajo demanda (modo selectivo, ADR-0014). El orquestador no hace el trabajo especializado él mismo (eso lo hacen las 9 skills) — solo lee estado, decide, despacha, y aplica los gates que no son responsabilidad de ninguna skill de fase (revisión manual, merge).
*De dónde lee el estado*
El orquestador no mantiene una base de datos propia — el estado ya vive en el front-matter de los archivos SDD (`spec.md`, `test-cases.md`, `plan.md`, `tasks.md`, `paquetes/*.md`, `evidencia/*.md`, ADR-0008) dentro del repositorio de control del Proyecto (ADR-0012). Para decidir el siguiente paso de una HU o paquete de trabajo, el orquestador simplemente lee el campo `fase`/`estado` correspondiente.
*Tabla de transición (modo secuencial, por defecto)*
TABLA:
| Fase/estado actual | Skill que despacha | Fase/estado resultante |
| (HU no descubierta) | `01` descubrimiento y especificación | `especificada` |
| `especificada` | `02` generación de TCs | `tcs_generados` |
| `tcs_generados` | `03` diagnóstico de avance existente | `diagnosticada` |
| `diagnosticada`, con TCs `pendiente` | `04` diseño de arquitectura | `planificada` |
| `diagnosticada`, todos los TCs `cubierto` | — | HU completa directo |
| `planificada` | `05` descomposición en paquetes de trabajo | `descompuesta` (crea N paquetes de trabajo `pendiente`, `ronda: 1`) |
| paquete de trabajo `pendiente` (sin `depende_de` sin resolver) | `06` generación de código | paquete de trabajo `en_revision` |
| paquete de trabajo `en_revision` | `07` revisión de código | con observaciones → vuelve a `06`; sin observaciones → gate de merge (ver abajo) |
| PR aprobado por `07` | *(el propio orquestador, ADR-0015)* | si `requiere_revision_manual`: espera aprobación humana; si no: merge directo → paquete de trabajo `fusionado` |
| paquete de trabajo `fusionado` | *(el propio orquestador, gate `RONDA`, ADR-0023)* | si quedan paquetes de trabajo de la misma `ronda` sin fusionar: espera (no se dispara `08`); si todos fusionados: pasa al gate `DEPLOY` |
| todos los paquetes de trabajo de la ronda `fusionado` | *(el propio orquestador, gate `DEPLOY`, ADR-0025)* | si el ambiente dev todavía no refleja el cambio: espera; si ya lo refleja: dispara `08` |
| ambiente dev actualizado | `08` smoke testing (todos los TCs de la HU) | todos pasan → HU y sus paquetes de trabajo quedan `completo`; alguno falla → `09` |
| TC fallido en smoke testing | `09` generación de fixes | crea paquete(s) de trabajo `tipo: fix` en `pendiente`, nueva `ronda` → vuelve a `06` |
| HU `completa` | — | fin |

Camino reducido para Actividades (ADR-0026): si `skills/01-...md` clasifica el elemento como `clasificacion: actividad` (sin criterios de aceptación verificables), el orquestador salta `02` y `03` directo a `04` (diseño/plan) → `05` (descomposición en paquetes de trabajo) → `06`/`07` (código y revisión) → merge. Como no hay TCs asociados, tras el merge no se pasa por `RONDA`/`DEPLOY`/`08` — la Actividad se marca completa directo al fusionarse, sin smoke testing.
*Responsabilidades que no son de ninguna skill de fase*
- El gate de revisión manual (ADR-0015): tras la aprobación de `07`, el orquestador consulta `requiere_revision_manual` en la configuración del Proyecto. Si es `true`, deja el paquete de trabajo esperando la aprobación de alguno de los `usuarios_autorizados_a_aprobar` antes de continuar.
- El merge en sí: ninguna de las 9 skills lo ejecuta explícitamente — es el orquestador quien lo realiza (con la cuenta de desarrollo, ADR-0013), una vez que `07` aprobó y, si aplica, la revisión manual quedó satisfecha.
- El gate `RONDA` (ADR-0023): tras cada merge, el orquestador compara cuántos paquetes de trabajo tiene la ronda en curso (`tasks.md`) contra cuántos ya están `fusionado`. Solo cuando coinciden pasa al gate `DEPLOY` — ni la descomposición original ni una tanda de fixes disparan smoke testing por un paquete de trabajo suelto.
- El gate `DEPLOY` (ADR-0025): antes de despachar `08`, el orquestador verifica que el ambiente de desarrollo ya sirve el código recién fusionado — fusionar no es lo mismo que desplegar. El mecanismo concreto de verificación es detalle de implementación (ADR-0025).
*Modo selectivo (Proyecto en modo `avanzado`, ADR-0014)*
En vez de determinar automáticamente la siguiente fase según la tabla de transición, el orquestador puede recibir una invocación explícita: "ejecutar la skill X sobre estas HUs/paquetes de trabajo" (p. ej. "solo `07` sobre todos los paquetes de trabajo en `en_revision`", o "solo `08` sobre los ya fusionados"). En este modo:
- No se sigue la secuencia completa — se ejecuta únicamente lo pedido, actualizando el estado igual que en modo secuencial.
- Requiere que la HU/paquete de trabajo objetivo ya tenga los archivos SDD que la skill pedida necesita como entrada (p. ej. no se puede pedir "solo revisión de código" sobre algo que nunca tuvo `plan.md`) — si no existen porque el trabajo se hizo fuera de Telar antes de adoptarlo, hace falta reconstruirlos primero (pendiente, ver ADR-0014).
- Cada fase exige solo *su propia* configuración de Proyecto, no toda — las 9 skills se agrupan en 4 fases de desarrollo (Requerimientos, Diseño, Desarrollo, Implementación) con su config mínima documentada en ADR-0034. Si se pide despachar una fase sin su config lista, el orquestador falla señalando específicamente qué le falta a esa fase, no un checklist del Proyecto completo.
*Modo fundacional (Proyecto en modo `nuevo`, ADR-0014)*
Antes de procesar la primera HU de un repositorio objetivo vacío, el orquestador despacha `04` en su modo fundacional (una sola vez por repositorio, no por HU) para establecer la arquitectura base.
*ADRs relacionados*
Prácticamente todos — el orquestador es el punto donde convergen: ADR-0004, ADR-0005, ADR-0008, ADR-0009, ADR-0012, ADR-0013, ADR-0014, ADR-0015, ADR-0020, ADR-0022, ADR-0023, ADR-0024, ADR-0025, ADR-0026, ADR-0028, ADR-0029, ADR-0030.
*Criterios de éxito*
Toda HU/paquete de trabajo de un Proyecto activo tiene, en todo momento, una fase/estado consistente con los archivos SDD que existen para ella; el orquestador nunca despacha una skill cuya entrada no está disponible; el merge solo ocurre cuando corresponde según `07` y, si aplica, la aprobación manual.
*Pendientes propios del orquestador*
- Mecanismo de reconstrucción de `spec.md`/`plan.md`/`tasks.md` para HUs/paquetes de trabajo que ya existían antes de adoptar Telar (modo `avanzado`, ADR-0014) — bloquea que el modo selectivo funcione sobre trabajo preexistente.
- Qué framework de agentes implementa al orquestador y a las skills (Claude Code Skills u otra alternativa) — pendiente general desde el inicio de `00-vision-general.md`.
- Orden/paralelismo de paquetes de trabajo con `depende_de` (resuelto) — resuelto en ADR-0029: secuencial estricto, nunca en paralelo.
- Si el orquestador procesa una HU a la vez o puede paralelizar (resuelto) — resuelto en ADR-0030: puede procesar varias HUs del mismo Proyecto en paralelo, salvo que una declare `depende_de` sobre otra a nivel HU.
- Cómo se declara `depende_de` entre HUs cuando la fuente no lo modela explícitamente (Jira sí tiene "issue links"; Markdown probablemente necesite declararlo a mano). *(ADR-0030)*

### B.2 Skill — Descubrimiento y especificación de HU
Alias en diagramas: `S0` en diagrama 02.
*Propósito*
Leer una historia de usuario desde la fuente configurada del Proyecto (Jira, Markdown o GitHub — ADR-0009, ADR-0010) e interpretarla como lo haría un analista de requerimientos senior — no solo extraer texto — para producir su especificación normalizada: `spec.md`, en el formato interno del sistema (SDD, ADR-0008). Es el punto de entrada único del pipeline: sin importar si la HU vino de un issue de Jira o de un archivo Markdown, todo lo que pasa después (generación de TCs, diagnóstico, arquitectura, código) trabaja siempre sobre el mismo `spec.md`, nunca contra la fuente original directamente.
*Rol: analista de requerimientos (LLM)*
Esta skill corre sobre un LLM con buena capacidad de análisis, con el mismo criterio que aplicaría un analista de negocio/requerimientos experimentado al recibir una HU antes de pasarla a desarrollo:
- Interpreta la intención real detrás de la HU, no solo el texto literal — qué problema de negocio resuelve, no nada más qué dice la redacción.
- Detecta criterios de aceptación implícitos que la HU no menciona explícitamente pero que un analista experimentado asumiría como parte del alcance (manejo de errores, casos límite, validaciones, permisos) — y los hace explícitos.
- Estructura los criterios de aceptación en un formato consistente y verificable (Given/When/Then o equivalente), incluso si la fuente los trae en prosa libre o desordenados.
- Distingue inferencia razonable de ambigüedad real. Cuando el vacío es inferible con confianza (un detalle que casi cualquier analista completaría igual), lo completa. Cuando el vacío cambia el alcance o admite más de una interpretación válida, no inventa silenciosamente — lo deja marcado como supuesto o pregunta abierta (ver Salidas).
- Clasifica el elemento como HU o Actividad (ADR-0026): si tiene o se le pueden inferir criterios de aceptación verificables, es una HU y sigue el pipeline completo; si es trabajo de arquitectura o preparación sin comportamiento de usuario verificable (por lo regular así son los elementos que la fuente tipa como "Tarea"), es una Actividad y sigue un pipeline reducido — sin TCs ni smoke testing (ver Salidas y Qué hace).
Esto es explícitamente distinto de un parser: la misma HU puede llegar incompleta o ambigua desde la fuente, y esta skill hace el trabajo de análisis, no solo de transcripción.
*Cuándo se invoca*
- Al dar de alta un Proyecto, para el recorrido inicial completo del backlog configurado.
- Ante una HU nueva o modificada en la fuente (re-descubrimiento incremental).
*Pendiente: si el recorrido es "una corrida completa bajo demanda" o si hay un modo continuo/polling — ver Pendientes.*
*Entradas*
- Configuración del Proyecto (ADR-0009, ADR-0010): tipo de fuente (`jira` | `markdown` | `github`) y sus parámetros de conexión (proyecto de Jira; ubicación/repositorio de los archivos Markdown; o repositorio de GitHub del que se leen Issues).
- Un elemento del backlog (ADR-0009, ADR-0026) identificado durante el recorrido de la fuente — antes de saber si es una HU o una Actividad (eso lo determina esta misma skill, ver abajo).
*Salidas*
Un archivo `spec.md` por HU, con este contrato:
Front-matter:
CODIGO:
id: HU-001                # identificador interno, asignado por esta skill (o AC-001 si es Actividad)
clasificacion: hu          # hu | actividad — ADR-0026
fuente_tipo: jira          # jira | markdown | github
fuente_ref: PROY-123       # ID del issue de Jira, o ruta del archivo Markdown original — trazabilidad
fase: especificada
estado: pendiente
fecha_descubrimiento: 2026-09-13
tiene_supuestos: true       # true si el análisis tuvo que asumir o marcar algo como ambiguo
prototipo_ref: null          # referencia al prototipo entregado junto con la HU, si existe (ADR-0027)
depende_de: []               # IDs de otras HUs de las que esta depende, si aplica (ADR-0030)
FIN-CODIGO
Cuerpo (Markdown libre, legible):
- Título de la HU.
- Descripción / narrativa (el "como usuario quiero... para...", tal como la interpretó el análisis, no necesariamente copiada literal de la fuente).
- Criterios de aceptación explícitos de la fuente — los que ya venían dados, estructurados en formato verificable.
- Criterios de aceptación inferidos — los que el análisis agregó por juicio de analista, marcados como tales (no se mezclan sin distinción con los explícitos).
- Supuestos y vacíos identificados — ambigüedades reales que no se resolvieron por inferencia, cada una con una nota de qué se necesitaría para cerrarla.
- Notas de la fuente original que no encajen en lo anterior (p. ej. comentarios relevantes de Jira).
*Qué hace (alto nivel)*
- Lee la configuración del Proyecto y determina qué adaptador de lectura usar (Jira, Markdown o GitHub).
- Recorre el backlog de la fuente (vía el contrato de ADR-0019) para identificar elementos procesables.
- Por cada elemento encontrado, analiza su contenido — no solo lo normaliza — aplicando el rol de analista de requerimientos descrito arriba: interpreta intención, estructura criterios explícitos, infiere los implícitos razonables, marca como supuesto lo genuinamente ambiguo, y clasifica el elemento como `hu` o `actividad` según si termina teniendo criterios de aceptación verificables.
- Escribe `spec.md` separando claramente lo explícito de lo inferido y de lo pendiente de aclarar.
- Deja la fase en `especificada` para que el orquestador continúe: si `clasificacion: hu`, con la generación de TCs; si `clasificacion: actividad`, saltando directo a diseño/plan (sin TCs ni smoke testing, ADR-0026) — una HU con `tiene_supuestos: true` puede necesitar una regla especial de qué hacer con esos supuestos antes de avanzar (ver Pendientes).
*Paso adicional en Proyectos nuevos*
Cuando `modo_arranque` es `nuevo`, al terminar de especificar todas las HUs la skill hace un último análisis como arquitecto sobre lo leído y guarda una propuesta de stack (tecnología y herramientas de backend y frontend, autenticación, estructura de repositorios, microservicios) con su justificación, que la pantalla de Diseño precarga (ADR-0039). No genera archivos SDD; es estado del Proyecto, y su falla no invalida el descubrimiento.
*Orden de las HUs*
El orden de las HUs (ADR-0048): lee todas las HUs y guarda la posición de cada una en la fuente (Jira Rank) como prioridad de negocio (`orden_fuente`).
*Fuente Markdown*
Se implementó junto a Jira: los archivos `.md` se suben desde la plataforma a una carpeta del servidor, uno por HU o actividad, y se analizan en orden natural de nombre (ADR-0058). La fuente GitHub sigue pendiente.
*ADRs relacionados*
- ADR-0039 — propuesta de stack al terminar el descubrimiento en Proyectos nuevos.
- ADR-0008 — formato y ubicación de `spec.md`.
- ADR-0009 — fuente pluggable y recorrido de la jerarquía del backlog.
- ADR-0010 — GitHub Issues como tercera fuente soportada.
- ADR-0011 — qué pasa con una HU marcada `tiene_supuestos: true`.
- ADR-0026 — distinción HU vs. Actividad, y vocabulario general.
- ADR-0027 — `prototipo_ref`, cuando se entrega un prototipo junto con la HU.
- ADR-0030 — `depende_de` a nivel HU.
*Criterios de éxito*
Existe un `spec.md` válido — con todos los campos de front-matter listados arriba, al menos un criterio de aceptación explícito o inferido, y cualquier ambigüedad real registrada como supuesto en vez de resuelta en silencio — por cada HU procesable encontrada en la fuente configurada.
*Pendientes propios de esta skill*
- Qué hace el orquestador con una HU marcada `tiene_supuestos: true` (resuelto) — resuelto en ADR-0011: el pipeline avanza sin bloquear, y el supuesto se resuelve visiblemente en la revisión de código (S5).
- Cómo se detectan HUs ya procesadas antes vs. nuevas/modificadas (resuelto) — resuelto en ADR-0040: huella del título+descripción de la fuente; revisión sin LLM y regeneración solo de lo nuevo/modificado o de HUs puntuales. Sigue abierto el descubrimiento automático (polling/webhook).
- Formato mínimo esperado de un archivo Markdown de HU cuando la fuente es `markdown` — sigue abierto; fuente `markdown` todavía no está implementada (ADR-0033).
- Mapeo exacto de campos de Jira... al `spec.md` interno (resuelto) — resuelto en ADR-0033: resumen y descripción (aplanada desde Atlassian Document Format) se pasan al LLM, que hace el análisis completo — no hay mapeo campo-a-campo de criterios de aceptación, se infieren del texto.
- Mapeo exacto de un Issue de GitHub (título, cuerpo, labels, sub-issues) al `spec.md` interno, y qué convención de labels/milestones se asume cuando el repositorio no usa sub-issues nativos (ADR-0010).
- Modo de ejecución: ¿corrida bajo demanda sobre todo el backlog, o descubrimiento continuo/incremental (polling, webhook de Jira, etc.)?
- Qué tan "agresiva" debe ser la inferencia de criterios implícitos antes de que se considere que el análisis se está excediendo de su alcance (inventando requisitos, no infiriéndolos).

### B.3 Skill — Generación de casos de prueba (TCs)
Alias en diagramas: `S1` en diagrama 02.
*Propósito*
A partir de `spec.md` (ya analizado por la skill de descubrimiento, `skills/01-...md`), generar los casos de prueba (TCs) que verifican cada criterio de aceptación — explícito o inferido — de la HU. Los TCs son el contrato que usan dos skills más adelante (diagnóstico de avance, ADR-0007, y smoke testing, ADR-0006) para saber si algo "ya funciona" o "todavía falta".
*Cuándo se invoca*
Cuando una HU llega a la fase `especificada` (salida de `skills/01-...md`) y no tiene supuestos sin resolver que bloqueen continuar (ver el pendiente de la skill 01 sobre `tiene_supuestos: true`).
*Entradas*
- `spec.md` de la HU: criterios de aceptación explícitos e inferidos, y cualquier supuesto ya aceptado.
- Prototipo, si existe (`prototipo_ref` en `spec.md`, ADR-0027): mockup, contrato de API o wireframe entregado como input a Telar junto con la HU. Cuando está presente, se usa junto con `spec.md` para generar TCs que cubran el comportamiento completo descrito, no solo lo que el texto de los criterios alcanza a especificar.
*Salidas*
`test-cases.md`, con este contrato:
Front-matter:
CODIGO:
hu_id: HU-001
fase: tcs_generados
total_tcs: 5
fecha_generacion: 2026-09-13
FIN-CODIGO
Cuerpo (un TC por criterio de aceptación, como mínimo):
- ID del TC (p. ej. `TC-001`), y el criterio de aceptación del que se deriva (referencia directa al criterio en `spec.md`, explícito o inferido).
- Escenario en formato Given/When/Then (consistente con cómo `skills/01-...md` ya estructuró los criterios).
- Tipo de verificación esperada: por ahora, proyectos tipo web (ADR-0009) — el TC se piensa para ejecutarse como interacción de UI vía Playwright (ADR-0006), no como prueba unitaria de código.
- Rol requerido (`rol_requerido`): qué rol de la aplicación necesita la cuenta de prueba con la que se ejecuta este TC (p. ej. `admin`, `usuario_final`, `invitado`) — ver ADR-0016. Se infiere del criterio de aceptación en `spec.md` (quién realiza la acción descrita).
- Resultado esperado explícito (qué se debe observar si el TC pasa).
*Qué hace (alto nivel)*
- Lee `spec.md` y recorre cada criterio de aceptación (explícito e inferido).
- Por cada criterio, deriva uno o más TCs — un criterio compuesto puede generar varios TCs si cubre más de un caso (camino feliz, casos límite, manejo de error), coherente con el nivel de detalle que la skill 01 ya dejó en el criterio.
- Estructura cada TC en Given/When/Then con un resultado esperado verificable, pensado para que la skill de ejecución de TCs (diagnóstico/smoke testing) lo pueda convertir en un script de Playwright.
- Escribe `test-cases.md` y deja la fase en `tcs_generados`.
*ADRs relacionados*
- ADR-0004 — TCs como segundo paso del flujo.
- ADR-0006 — los TCs se ejecutan con Playwright (Python).
- ADR-0007 — los mismos TCs alimentan el diagnóstico de avance existente, no solo el smoke testing final.
- ADR-0008 — formato de `test-cases.md`.
- ADR-0011 — un criterio con supuesto no resuelto igual genera TC; el supuesto se resuelve en revisión de código.
- ADR-0016 — cada TC declara el rol con el que debe ejecutarse.
- ADR-0027 — el prototipo, cuando existe, informa la generación de TCs completos.
*Criterios de éxito*
Cada criterio de aceptación de `spec.md` (explícito o inferido, no los supuestos sin resolver) tiene al menos un TC en `test-cases.md`, en formato Given/When/Then con resultado esperado explícito.
*Pendientes propios de esta skill*
- Cuántos TCs por criterio son razonables — ¿solo camino feliz, o también casos límite/error por defecto? Afecta directamente qué tan caro es correr el diagnóstico de avance (ADR-0007) y el smoke testing (ADR-0006).
- Cómo se referencia un TC de vuelta a su criterio de aceptación en `spec.md` de forma estable (¿un ID de criterio explícito desde la skill 01?) — necesario para que el diagnóstico pueda decir "este criterio ya está cubierto" con precisión.
- Qué pasa con un criterio marcado como supuesto no resuelto (resuelto) — resuelto en ADR-0011: se genera TC igual, usando la interpretación de la skill 01; el supuesto se resuelve visiblemente en la revisión de código (S5), no aquí.
- Esta skill asume proyectos tipo web (Playwright/UI). Si algún día se soporta tipo API (ADR-0009, fuera de alcance de esta tesis), un TC necesitaría otra forma de expresar la verificación esperada.
- Qué hacer cuando el criterio de aceptación no deja claro qué rol requiere el TC — ¿rol por default, o se marca para confirmación humana? (ADR-0016)

### B.4 Skill — Diagnóstico de avance existente
Alias en diagramas: `S1B` en diagrama 02.
*Propósito*
Ejecutar los TCs de `test-cases.md` contra el estado actual del ambiente de desarrollo, antes de diseñar o descomponer nada, para distinguir qué criterios de aceptación ya están cubiertos (proyecto con avance previo, ADR-0007) de los que realmente faltan. Cubre greenfield como caso particular: si no existe nada, todos los TCs fallan y todos quedan pendientes — el mecanismo es el mismo en ambos casos.
Esta skill es el mismo motor de ejecución de TCs que usa `smoke testing` (S6, ADR-0006) más adelante en el flujo — se documenta aquí en detalle y `S6` solo referencia esta ficha, para no duplicar el diseño del mecanismo (ver Notas).
*Cuándo se invoca*
Cuando una HU llega a la fase `tcs_generados` (salida de `skills/02-...md`).
*Entradas*
- `test-cases.md` de la HU: TCs en formato Given/When/Then.
- Configuración del Proyecto (ADR-0005): URL del ambiente de desarrollo contra el que se corren los TCs (los repos de código no se tocan en esta fase — ver Notas sobre acceso).
*Salidas*
- `evidencia/diagnostico-01.md` (numerado por corrida), con front-matter:
CODIGO:
hu_id: HU-001
tipo: diagnostico
fecha: 2026-09-14
tcs_totales: 5
tcs_pasan: [TC-002, TC-004]
tcs_fallan: [TC-001, TC-003, TC-005]
FIN-CODIGO
Cuerpo: por cada TC, resultado (pasa/falla), evidencia (captura o descripción de lo observado), y si falló, por qué (funcionalidad inexistente vs. comportamiento distinto al esperado).
- Actualiza `test-cases.md`: cada TC queda marcado con su estado más reciente (`cubierto` / `pendiente`), que es lo que lee la skill de diseño de arquitectura (siguiente en el flujo) para saber qué falta.
- Deja la fase de la HU en `diagnosticada`.
*Qué hace (alto nivel)*
- Lee `test-cases.md` y la URL del ambiente de desarrollo configurado (ADR-0005).
- Por cada TC, genera un script de Playwright (Python, ADR-0006) a partir de su Given/When/Then y lo ejecuta contra ese ambiente, como lo haría un usuario real.
- Registra el resultado (pasa/falla) y la evidencia correspondiente.
- Escribe `evidencia/diagnostico-01.md` y actualiza el estado de cobertura en `test-cases.md`.
- Deja la fase en `diagnosticada` para que el orquestador continúe con diseño de arquitectura.
*Estado de implementación*
Implementada — ADR-0060: el agente de navegador de la skill 08 prueba los TCs contra el ambiente existente, marca cada uno `cubierto`, `pendiente` o `sin_evaluar`, y la skill 05 solo descompone lo que falta.
*ADRs relacionados*
- ADR-0060 — implementación.
- ADR-0006 — Playwright como motor de ejecución de TCs.
- ADR-0007 — decisión de origen de esta skill.
- ADR-0008 — formato de `evidencia/`.
- ADR-0016 — selección de cuenta de prueba por rol declarado en cada TC.
*Criterios de éxito*
Cada TC de `test-cases.md` tiene un resultado registrado (pasa/falla) con evidencia — incluyendo los que fallan porque la funcionalidad todavía no existe (greenfield).
*Notas sobre acceso (relevante para no confundir con la skill de generación de código)*
Esta skill no necesita acceso de escritura a los repositorios (no genera commits, no abre PRs) — solo necesita poder interactuar con el ambiente de desarrollo ya desplegado (la URL configurada en ADR-0005) como lo haría un usuario real, con el rol que cada TC declare (`rol_requerido`, ADR-0016) — no una sola cuenta genérica: la configuración del Proyecto aporta un conjunto de cuentas de prueba, una por rol relevante de la aplicación, y esta skill selecciona la que corresponda a cada TC. Esto es, de cualquier forma, distinto de la cuenta de desarrollo con acceso a los repos que sí va a necesitar la skill de generación de código (`skills/06-...md`) para hacer commit, push y abrir PRs (ADR-0013) — son credenciales con alcances distintos y no deberían mezclarse.
*Pendientes propios de esta skill*
- Qué hacer con TCs que no se pueden evaluar de forma aislada porque dependen de un paquete de trabajo que todavía no existe (resuelto) — resuelto en ADR-0027: esta skill no necesita distinguir la causa del fallo. Simplemente marca el TC como `pendiente`; es la descomposición (`skills/05-...md`), informada por el prototipo cuando existe, la que genera todos los paquetes necesarios en ambas capas para cubrirlo por completo.
- Umbral entre "TC falla" (la funcionalidad no cumple el criterio) y "TC no se pudo ejecutar" (error técnico al correr el script, ambiente caído, etc.) — ¿cuentan igual para efectos de generar un paquete de trabajo?
- Qué credencial de prueba usa esta skill (resuelto) — resuelto en ADR-0016: un conjunto de cuentas por rol, seleccionada según el `rol_requerido` de cada TC.

### B.5 Skill — Diseño de arquitectura
Alias en diagramas: `S2` en diagrama 02.
*Propósito*
A partir de los TCs marcados como `pendiente` por el diagnóstico de avance (`skills/03-...md`), diseñar cómo se va a construir lo que falta — respetando y extendiendo la arquitectura y convenciones que ya existen en el/los repositorio(s) objetivo, no proponiendo una solución nueva ignorando lo que hay (ADR-0007). Es el "plan" de Spec-Driven Development (ADR-0008): el puente entre "qué falta" (TCs pendientes) y "en qué paquetes de trabajo se va a partir el trabajo" (siguiente skill).
Esta skill opera en dos modos, según el modo de arranque del Proyecto (ADR-0014):
- Modo extensión (Proyecto `avanzado` o con código ya existente): el comportamiento descrito abajo — analiza lo que ya existe y extiende sus patrones.
- Modo fundacional (Proyecto `nuevo`, ADR-0014): no hay nada que analizar ni extender. La skill define la arquitectura inicial del repositorio objetivo — elección de stack/framework (si no viene ya fijada por el tipo de Proyecto, ADR-0009), estructura de carpetas, capas y convenciones de partida. Ese resultado es lo que las HUs siguientes van a encontrar como "lo ya existente" y podrán extender en modo normal. Se ejecuta una sola vez por repositorio objetivo, no por cada HU.
- Proyecto en modo `con_arquitectura` (ADR-0014): esta skill no se invoca — se asume una arquitectura ya definida por humanos, aportada al sistema por otro medio (pendiente de definir en ADR-0014).
*Cuándo se invoca*
En modo extensión: cuando una HU llega a la fase `diagnosticada` (salida de `skills/03-...md`) y tiene al menos un TC marcado `pendiente`. Si todos los TCs ya están `cubierto`, la HU se da por completa sin pasar por esta skill (todo lo pedido ya existe).
En modo fundacional: una vez, al dar de alta un repositorio objetivo de un Proyecto en modo `nuevo` (ADR-0014), antes de procesar su primera HU.
*Entradas*
- `test-cases.md`: qué TCs quedaron `pendiente` tras el diagnóstico (los `cubierto` no generan trabajo).
- `spec.md`: criterios de aceptación asociados a cada TC pendiente, y cualquier supuesto marcado (`tiene_supuestos`, ADR-0011) que afecte el diseño.
- Código actual del/los repositorio(s) objetivo (ADR-0005): estructura, convenciones, patrones ya presentes — vía el mecanismo de indexación de código (ADR-0002, todavía sin detallar como skill propia).
*Salidas*
*(Lo siguiente describe el modo extensión, ligado a una HU. El modo fundacional produce un artefacto de arquitectura base a nivel de repositorio, no de HU — formato pendiente de definir junto con ADR-0014.)*
`plan.md`, con front-matter:
CODIGO:
hu_id: HU-001
fase: planificada
tcs_cubiertos_por_plan: [TC-001, TC-003, TC-005]   # los que test-cases.md marcó pendiente
repos_involucrados: [backend-principal, frontend-admin]
fecha_plan: 2026-09-14
FIN-CODIGO
Cuerpo:
- Resumen del enfoque: qué se va a construir y por qué esa aproximación, en términos de la arquitectura ya existente (qué capa/módulo/patrón se extiende, no se reinventa).
- Repositorios afectados: de los N configurados (ADR-0005), cuáles necesita tocar esta HU y por qué — insumo directo para que la skill de generación de código sepa dónde generar cada cosa.
- Decisiones de diseño puntuales relevantes a esta HU (no arquitectura del sistema completo, solo lo que esta HU necesita: p. ej. "se agrega un nuevo endpoint siguiendo el patrón REST ya usado en `X`", "el nuevo componente de UI reutiliza el layout de `Y`").
- Supuestos heredados de `spec.md`, si los hay, con nota de cómo el diseño los interpretó (para que lleguen visibles hasta la revisión de código, ADR-0011).
*Qué hace (alto nivel)*
- Lee los TCs `pendiente` de `test-cases.md` y sus criterios asociados en `spec.md`.
- Analiza el código actual de los repos involucrados (vía el mecanismo de indexación, ADR-0002) para identificar patrones y convenciones existentes relevantes a lo que falta construir.
- Propone un enfoque que extiende esos patrones — no una arquitectura nueva en el vacío.
- Identifica qué repositorio(s) de los configurados necesita tocar esta HU.
- Escribe `plan.md` y deja la fase en `planificada`.
*Estado de implementación*
Implementada la variante fundacional (Proyecto `nuevo`) — ADR-0044. El modo extensión sigue pendiente y depende del diagnóstico (skill 03).
*API y Swagger*
La arquitectura de un repositorio con backend incluye la sección «API y Swagger/OpenAPI» (ADR-0052).
*ADRs relacionados*
- ADR-0044 — formato del documento, aprobación y ejecución en la Fase 2.
- ADR-0002 — el mecanismo de indexación de código del que depende esta skill (diseño, no infraestructura desplegada).
- ADR-0004 — el diseño de arquitectura como fase del flujo.
- ADR-0007 — el diseño debe extender lo existente, no ignorarlo.
- ADR-0008 — `plan.md` como artefacto SDD.
- ADR-0011 — los supuestos de `spec.md` deben quedar visibles en `plan.md`.
- ADR-0014 — modo fundacional vs. modo extensión, según el modo de arranque del Proyecto.
- ADR-0022 — qué hacer cuando el enfoque de diseño necesita un repo fuera de la configuración del Proyecto, o un tipo de sistema fuera del alcance de Telar.
*Criterios de éxito*
`plan.md` cubre todos los TCs marcados `pendiente` (ninguno queda sin un enfoque de diseño asociado), identifica explícitamente qué repositorios toca, y no contradice patrones ya presentes en el código sin justificarlo.
*Pendientes propios de esta skill*
- Cómo se implementa el mecanismo de indexación de código (resuelto) — resuelto en ADR-0018: análisis bajo demanda con grep/glob, sin índice persistente.
- Qué pasa si el enfoque de diseño requiere un repositorio fuera de configuración (resuelto) — resuelto en ADR-0022: se marca en `plan.md` como pendiente de definir (recuperable, amplía config) o como fuera de alcance (si es un tipo de sistema no soportado) — la plataforma lo escala al humano en ambos casos.
- Nivel de detalle esperado en "decisiones de diseño puntuales": ¿alcanza con guiar a la skill de generación de código, o debe ser suficientemente detallado para que un humano lo revise como si fuera un mini-RFC?
- Si esta skill también debería registrar sus propias decisiones como ADRs del Proyecto (paralelo a cómo se documenta la arquitectura de este mismo sistema, ADR-0001) o si `plan.md` basta.
- Formato exacto del artefacto de arquitectura fundacional (modo fundacional, ADR-0014) (resuelto) — resuelto en ADR-0044: un Markdown por repositorio en `arquitectura/<repositorio>.md`, con aprobación humana antes de descomponer. Implementado solo el modo fundacional.
- Cómo se decide el stack/framework en modo fundacional cuando el tipo de Proyecto (ADR-0009, solo "web" por ahora) no basta para elegirlo por sí solo (resuelto) — resuelto en ADR-0038: la persona puede declarar tecnología de backend/frontend, número de microservicios y tipo de autenticación al configurar el Proyecto; cuando vienen llenos, esta skill los usa como restricción en vez de decidir desde cero.

### B.6 Skill — Descomposición en paquetes de trabajo
Alias en diagramas: `S3` en diagrama 02.
*Propósito*
A partir de `plan.md` (el enfoque de diseño) y los TCs pendientes, partir el trabajo en paquetes de trabajo lo bastante acotados para que cada uno resulte en un Pull Request propio y revisable. Es la skill que produce los "paquetes de trabajo" que ADR-0004 describe generando código — un término distinto de cualquier elemento del backlog que venga ya de la fuente (ADR-0009/ADR-0026): un paquete de trabajo es siempre interno a Telar, nunca algo leído de Jira/GitHub/Markdown.
*Cuándo se invoca*
Cuando una HU llega a la fase `planificada` (salida de `skills/04-...md`). No aplica a elementos clasificados como Actividad (ADR-0026) — una Actividad no tiene TCs que descomponer en paquetes de trabajo validables por smoke testing; su plan se implementa directo (ver `skills/04-...md`).
*Entradas*
- `plan.md`: enfoque de diseño y repositorios involucrados.
- `test-cases.md`: TCs marcados `pendiente` que el plan debe cubrir.
- Prototipo, si existe (`prototipo_ref` en `spec.md`, ADR-0027): usado para asegurar que la descomposición cubra ambos lados (back y front) sin dejar huecos, contra lo que el diagnóstico (`skills/03-...md`) ya marcó como existente.
*Salidas*
`tasks.md`, con front-matter:
CODIGO:
hu_id: HU-001
fase: descompuesta
total_paquetes: 3
fecha_descomposicion: 2026-09-14
FIN-CODIGO
Cuerpo: lista de paquetes de trabajo planeados, cada uno con su ID, repositorio objetivo, y qué TCs cubre.
Más un archivo `paquetes/PT-0N.md` por cada paquete de trabajo, con front-matter:
CODIGO:
id: PT-01
hu_id: HU-001
repo: backend-principal        # exactamente uno de los repos configurados (ADR-0005)
estado: pendiente               # pendiente | en_revision | fusionado — no "completo" (ADR-0023)
ronda: 1                        # 1 = descomposición original; 2+ = rondas de fix (ADR-0023)
tcs_asociados: [TC-001, TC-003]
pr: null
rondas_revision: 0
depende_de: []                  # IDs de otros paquetes de trabajo que deben completarse antes
id_externo: null                 # ID del paquete/sub-issue creado en la fuente, si aplica (ADR-0024)
FIN-CODIGO
*(`estado: fusionado` es el final de este paquete de trabajo individualmente — ya no `completo`: la HU y sus paquetes de trabajo solo se dan por completos cuando smoke testing pasa a nivel HU, ADR-0023.)*
Creación en la plataforma de origen (ADR-0024): si la fuente de HUs de este Proyecto es Jira o GitHub (plataformas con gestión nativa de subtareas), esta skill además crea el paquete correspondiente ahí, vía MCP, y guarda su referencia en `id_externo`. Si la fuente es Markdown, no hay plataforma externa equivalente — `id_externo` queda `null` y `paquetes/PT-0N.md` en el repo de control es la única representación que existe.
*Qué hace (alto nivel)*
- Lee `plan.md` y los TCs `pendiente` de `test-cases.md`.
- Agrupa esos TCs en unidades de trabajo coherentes y acotadas. Cada paquete de trabajo toca exactamente un repositorio de los configurados (ADR-0005) — si el plan requiere un cambio coordinado en más de uno (p. ej. un contrato de API que afecta backend y frontend), se generan paquetes de trabajo separados, uno por repositorio, relacionados por `depende_de`.
- Determina el orden/dependencias entre paquetes de trabajo cuando uno depende del resultado de otro.
- Escribe `tasks.md` (resumen) y un `paquetes/PT-0N.md` por cada paquete de trabajo, en el repositorio de control (ADR-0012) — esto ocurre siempre, sin importar la fuente de HUs.
- Si la fuente de HUs del Proyecto lo soporta (Jira, GitHub), crea además el paquete correspondiente ahí vía MCP y guarda su referencia en `id_externo` (ADR-0024). Si la fuente es Markdown, se omite este paso.
- Deja la fase de la HU en `descompuesta` — el orquestador puede empezar a despachar paquetes de trabajo individuales a la skill de generación de código.
*Estado de implementación*
Implementada para Proyectos en modo `nuevo` a partir de la arquitectura fundacional aprobada (no de un `plan.md` por HU): planea el esqueleto (grupo `BASE`) y el orden de las HUs, y parte cada HU en paquetes — ADR-0045. El modo extensión, las rondas de fixes y la creación en Jira/GitHub siguen pendientes.
*Orden de las HUs*
El orden de las HUs (ADR-0048): fija el orden de implementación de cada HU (`orden`): prioridad de negocio ajustada por dependencias reales.
*Esqueleto con entorno de desarrollo*
El primer paquete del esqueleto deja el entorno de desarrollo dockerizado y el README (ADR-0050).
*README por servicio*
El esqueleto crea el README de cada servicio (ADR-0056).
*ADRs relacionados*
- ADR-0045 — adaptación al flujo fundacional.
- ADR-0004 — descomposición en paquetes de trabajo como fase del flujo.
- ADR-0005 — cada paquete de trabajo se ancla a exactamente uno de los repos configurados.
- ADR-0008 — formato de `tasks.md` y `paquetes/`.
- ADR-0023 — el estado final de un paquete de trabajo es `fusionado`, no `completo`; el campo `ronda` agrupa qué paquetes deben fusionarse juntos antes de que se dispare smoke testing.
- ADR-0024 — creación adicional del paquete en la plataforma de origen (Jira/GitHub) vía MCP, cuando la fuente lo soporta.
- ADR-0026 — define "paquete de trabajo" como término único, y resuelve la colisión que antes existía con "subtarea".
- ADR-0027 — el prototipo, cuando existe, asegura que la descomposición cubra ambas capas sin huecos.
- ADR-0029 — paquetes con `depende_de` se generan en secuencia estricta, no en paralelo.
*Criterios de éxito*
Todo TC `pendiente` queda cubierto por al menos un paquete de trabajo; cada paquete de trabajo referencia exactamente un repositorio configurado; las dependencias entre paquetes de trabajo quedan explícitas en `depende_de`.
*Pendientes propios de esta skill*
- Qué tan grande puede ser un paquete de trabajo antes de considerarse que debería partirse más — falta un criterio de "tamaño de PR razonable" (hoy: 1 a 4 paquetes por HU, un solo objetivo cada uno).
- Si `depende_de` implica orden estricto o generación en paralelo (resuelto) — resuelto en ADR-0029: orden estricto (p. ej. backend antes que frontend cuando el frontend depende de él).
- Qué hacer si falla la creación del paquete en la plataforma de origen (Jira/GitHub, ADR-0024) — no debería bloquear el control interno; ya resuelto en ADR-0024 que solo se advierte, con opción de reintentar desde la plataforma.

### B.7 Skill — Generación de código
Alias en diagramas: `S4` en diagrama 02.
*Propósito*
Por cada paquete de trabajo (`paquetes/PT-0N.md`), generar el código correspondiente en su repositorio objetivo y abrir un Pull Request — el "vibecoding" del que habla ADR-0008, siempre contra una especificación concreta (`plan.md` + `spec.md` + `test-cases.md`), nunca a partir de un prompt suelto.
*Cuándo se invoca*
Cuando un paquete de trabajo está en estado `pendiente` (salida de `skills/05-...md`), respetando su `depende_de` si tiene dependencias sin resolver. También la reutiliza la skill de generación de fixes (`S7`, pendiente de documentar) cuando un TC falla en smoke testing.
*Entradas*
- `paquetes/PT-0N.md`: repositorio objetivo, TCs asociados, dependencias.
- `plan.md`: enfoque de diseño de la HU.
- `spec.md` / `test-cases.md`: criterios de aceptación y TCs relacionados, incluyendo cualquier supuesto marcado (`tiene_supuestos`, ADR-0011) que este paquete de trabajo deba respetar.
- Configuración del Proyecto: referencia al repositorio objetivo correspondiente (ADR-0005) y la credencial de la cuenta de desarrollo dedicada (ADR-0013) para operar sobre él.
*Salidas*
Esta skill escribe en dos lugares distintos — vale la pena tenerlo presente (ADR-0012):
En el repositorio objetivo (código real, ADR-0005):
- Una rama nueva, nombrada `hu/{id_fuente}/{paquete_id}` — `id_fuente` es el identificador del ticket tal como está dado de alta en la fuente (el issue de GitHub, el ticket de Jira); si la fuente es Markdown, se usa el identificador propio del documento si lo trae, o uno generado por el adaptador si no (ADR-0019, ADR-0021).
- Uno o más commits con el código generado, con autoría de la cuenta de desarrollo (ADR-0013).
- Un Pull Request contra la rama base configurada, cuya descripción incluye: qué paquete de trabajo resuelve, qué TCs cubre, y — si aplica — los supuestos heredados de `spec.md` que el revisor debe confirmar (ADR-0011). Esto es obligatorio cuando el paquete de trabajo desciende de una HU con `tiene_supuestos: true`.
En el repositorio de control (documentación, ADR-0012):
- Actualiza `paquetes/PT-0N.md`: `pr` (URL del PR recién abierto), `estado: en_revision`.
*Qué hace (alto nivel)*
- Verifica que las dependencias del paquete de trabajo (`depende_de`) ya estén resueltas; si no, espera.
- Lee el paquete de trabajo, `plan.md` y el `spec.md`/`test-cases.md` relacionados.
- Genera el código en el repositorio objetivo identificado, siguiendo el enfoque de `plan.md` y respetando las convenciones ya presentes (ADR-0007).
- Crea la rama y hace commit(s) con la cuenta de desarrollo dedicada (ADR-0013).
- Abre el PR, propagando a su descripción los supuestos sin resolver de `spec.md` si los hay (ADR-0011) — esto es lo que le permite a la skill de revisión de código (`S5`, pendiente) saber que no puede aprobar en automático.
- Actualiza `paquetes/PT-0N.md` en el repositorio de control con la URL del PR y el nuevo estado.
*Estado de implementación*
Implementada — ADR-0046: agente con herramientas acotadas sobre un worktree, desarrollo con TDD (compuerta que exige pruebas unitarias en paquetes de backend/frontend), PR con la cuenta de desarrollo y sincronización del estado de los PRs. Sin ejecución local del código en esta versión.
*Orden de las HUs*
El orden de las HUs (ADR-0048): el siguiente paquete se elige por ese orden, y se puede avanzar con una HU concreta (`grupo` sin `pt`) respetando dependencias.
*Fusión del PR*
La persona acepta el PR desde la plataforma (ADR-0051).
*ADRs relacionados*
- ADR-0046 — implementación y TDD.
- ADR-0004 — generación de código y apertura de PR como fase del flujo.
- ADR-0005 — repositorio objetivo por paquete de trabajo.
- ADR-0007 — respetar el código existente.
- ADR-0008 — SDD como fuente del código generado (spec/plan/tasks), no un prompt suelto.
- ADR-0011 — cómo se propagan los supuestos a la descripción del PR (queda resuelto aquí: van explícitos en la descripción).
- ADR-0012 — esta skill toca repo de control y repo objetivo a la vez.
- ADR-0013 — la identidad con la que se hacen commits, push y PRs.
- ADR-0021 — convención de nombre de rama basada en `id_fuente`.
- ADR-0026 — vocabulario "paquete de trabajo".
- ADR-0028 — el ciclo código→revisión→corrección es el mecanismo de calidad, con o sin revisión manual.
- ADR-0029 — orden secuencial para paquetes dependientes entre repos.
*Criterios de éxito*
Existe un PR abierto en el repositorio objetivo correcto, con autoría de la cuenta de desarrollo, descripción completa (paquete de trabajo, TCs cubiertos, supuestos si aplica), y `paquetes/PT-0N.md` refleja el estado y la URL del PR.
*Pendientes propios de esta skill*
- Qué hace el sistema si el código generado no compila (resuelto) — v1: se abre igual y la CI/la revisión lo detectan (ADR-0046); validar localmente antes del PR queda como mejora.
- Cómo se coordinan paquetes de trabajo relacionados que tocan repos distintos (resuelto) — resuelto en ADR-0029: en secuencia estricta, nunca en paralelo — el dependiente no arranca hasta que la dependencia está fusionada.
- Formato/convención exacta para que un PR "generado por el sistema" sea identificable de forma confiable en los reportes (ADR-0012) — ¿basta la autoría de la cuenta de desarrollo (ADR-0013), o hace falta además un label o un prefijo de rama?
- Qué pasa si la generación de código para un paquete de trabajo falla repetidamente (¿cuántos reintentos antes de marcarlo como bloqueado y escalar a un humano?).

### B.8 Skill — Revisión de código
Alias en diagramas: `S5` en diagrama 02.
*Propósito*
Revisar el PR abierto por la skill de generación de código (`skills/06-...md`) contra tres fuentes de verdad a la vez, no solo "¿se ve bien el código?":
- `spec.md` — ¿el código realmente cumple los criterios de aceptación (explícitos e inferidos) de la HU, y quedó resuelto cualquier supuesto heredado (`tiene_supuestos`, ADR-0011)?
- `plan.md` — ¿el código sigue el enfoque de arquitectura definido para esta HU (ADR-0007: extiende lo existente, no lo contradice sin justificación)?
- Mejores prácticas del lenguaje/framework que ya usa el repositorio objetivo — convenciones idiomáticas específicas (p. ej. PEP 8 y type hints en Python, la guía de estilo de Angular en TypeScript), no reglas genéricas de "buen código" independientes del stack.
Es esta skill la que finalmente implementa la regla de ADR-0011: no se puede aprobar un PR en automático si arrastra un supuesto sin resolver.
*Cuándo se invoca*
- Cuando un paquete de trabajo entra en estado `en_revision` (salida de `skills/06-...md`).
- Cada vez que se sube una nueva versión del PR tras aplicar observaciones — es el ciclo `revisión ↔ aplicar cambios` del diagrama 01, que se repite hasta que no quedan observaciones pendientes.
*Entradas*
- El diff del PR en el repositorio objetivo (ADR-0005).
- `spec.md` de la HU: criterios de aceptación y supuestos (ADR-0011).
- `plan.md` de la HU: enfoque de arquitectura acordado.
- Convenciones/mejores prácticas del lenguaje y framework detectados en el repositorio — vía el mismo mecanismo de indexación de código del que depende `skills/04-...md` (ADR-0002).
*Salidas*
- Comentarios de revisión publicados en el PR (en la plataforma donde vive el repo objetivo — GitHub, GitLab, etc., ADR-0005), agrupados por fuente: incumplimiento de criterio de aceptación, desviación del plan, o convención de lenguaje/framework.
- Si hay un supuesto sin resolver: una observación explícitamente marcada como bloqueante, pidiendo confirmación o corrección — no se mezcla con sugerencias menores.
- Actualiza `paquetes/PT-0N.md` (repo de control, ADR-0012): incrementa `rondas_revision`, y cambia `estado` a `aprobado` (sin observaciones pendientes) o lo deja en `en_revision` (con observaciones).
*Qué hace (alto nivel)*
- Lee el diff del PR junto con `spec.md` y `plan.md` de la HU/paquete de trabajo correspondiente.
- Verifica cumplimiento de cada criterio de aceptación relevante a este paquete de trabajo — no en abstracto, contra lo que el código efectivamente hace.
- Verifica que el código sigue el enfoque de `plan.md`; si se desvía, evalúa si la desviación está justificada o es una observación a corregir.
- Aplica revisión de mejores prácticas específicas del lenguaje/framework detectado, apoyándose en las herramientas de lint/formato que ya tenga configuradas el repositorio si existen.
- Si la HU tiene `tiene_supuestos: true` y el supuesto en cuestión no fue resuelto en esta versión del código, genera la observación bloqueante correspondiente.
- Publica las observaciones en el PR.
- Si no quedan observaciones pendientes (incluidos los supuestos), aprueba el PR; si quedan, deja el PR esperando una nueva versión (vuelve a `skills/06-...md`) y actualiza `paquetes/PT-0N.md`.
- La aprobación de esta skill no siempre implica merge inmediato: si el Proyecto tiene `requiere_revision_manual: true` (ADR-0015), el PR queda esperando la aprobación de alguno de los `usuarios_autorizados_a_aprobar` antes de fusionarse — este paso ya no lo hace esta skill, es un gate del orquestador (ver diagrama 01).
*Estado de implementación*
Implementada — ADR-0049: revisa el diff del PR contra spec, arquitectura y buenas prácticas, publica las observaciones en GitHub, marca el paquete `aprobado` o `con_observaciones` y permite corregirlo sobre la misma rama. Sin CI ni confirmación de supuestos todavía.
*ADRs relacionados*
- ADR-0049 — implementación.
- ADR-0004 — el ciclo de revisión como fase del flujo.
- ADR-0005 — el PR vive en el repositorio objetivo configurado.
- ADR-0007 — el código no debe contradecir sin justificación lo que ya existe.
- ADR-0008 — formato de `paquetes/PT-0N.md`.
- ADR-0011 — esta skill es donde se aplica la regla de no aprobar con supuestos sin resolver.
- ADR-0012 — actualiza el repo de control, no el objetivo.
- ADR-0015 — la aprobación de esta skill puede no ser suficiente para el merge si el Proyecto exige revisión manual.
- ADR-0026 — vocabulario "paquete de trabajo".
- ADR-0028 — esta skill, dentro del ciclo código→revisión→corrección, es el mecanismo de calidad documentado incluso sin revisión manual.
- ADR-0089 — el experimento C repite la revisión de esta skill solo con el diff para medir cuánto aporta el contexto (H1).
- ADR-0090 — segunda opinión automática de las observaciones del experimento C, sellada hasta la calificación humana.
- ADR-0091 — la tesis reporta esa evaluación automática para la corrida c1; la calificación por una persona queda pendiente.
*Criterios de éxito*
Un PR solo se aprueba cuando: cumple los criterios de aceptación de `spec.md` relevantes al paquete de trabajo, sigue (o justifica su desviación de) el enfoque de `plan.md`, no tiene observaciones de convención de lenguaje/framework sin resolver, y no arrastra ningún supuesto sin confirmar.
*Pendientes propios de esta skill*
- Fuente del catálogo de "mejores prácticas por lenguaje": ¿reglas propias del sistema, integración con los linters/formatters ya configurados en el repo (ESLint, Ruff, Flake8, Prettier...), o el criterio del propio LLM sin catálogo explícito?
- Qué cuenta como "resolver" un supuesto en revisión: ¿un comentario del revisor aceptándolo basta, o se exige un cambio de código o una confirmación humana explícita?
- Si esta skill debe operar con una identidad distinta a la cuenta de desarrollo que generó el código (ADR-0013) — separar "quien escribe" de "quien revisa" — o si es aceptable que sea el mismo sistema actuando en dos roles.
- Umbral de severidad: ¿toda observación bloquea el avance, o hay clasificación (bloqueante vs. sugerencia) como en una revisión humana normal?
- Qué pasa si, tras varias rondas, el PR sigue sin poder aprobarse — ¿existe un límite antes de escalar a revisión humana?

### B.9 Skill — Smoke testing
Alias en diagramas: `S6` en diagrama 02.
*Propósito*
Confirmar, contra el ambiente de desarrollo real, que una HU completa no rompe nada — no basta con que cada PR haya pasado revisión de código (`skills/07-...md`), hace falta validar el comportamiento del código ya integrado. Es el mismo motor de ejecución de TCs que `skills/03-diagnostico-de-avance-existente.md` (Playwright, cuentas de prueba por rol — ADR-0016); esta ficha documenta solo lo que es distinto: cuándo se invoca y qué pasa con el resultado. Para el mecanismo de ejecución en sí, ver `skills/03-...md`.
*Cuándo se invoca*
No por cada paquete de trabajo fusionado — se dispara cuando todos los paquetes de trabajo de la ronda en curso (la descomposición original de `skills/05-...md`, o la tanda de fixes más reciente de `skills/09-...md`) llegan a `estado: fusionado` (ADR-0023). El gate `RONDA` del diagrama 01 es responsabilidad del orquestador (`skills/00-...md`), no de esta skill — esta skill solo se ejecuta una vez que el orquestador determina que ya toca.
Correr smoke testing con paquetes de trabajo de la misma ronda todavía sin fusionar produciría fallos que no son errores reales, solo trabajo incompleto (ADR-0023) — de ahí la espera. Además, el orquestador verifica primero que el ambiente de desarrollo ya sirve el código recién fusionado (ADR-0025) — fusionar no es lo mismo que desplegar; sin esa verificación, esta skill podría correr contra un ambiente todavía desactualizado.
*Entradas*
- Todos los TCs de `test-cases.md` de la HU (ADR-0020): cada corrida es una prueba de regresión completa, no una verificación puntual de un cambio aislado.
- Configuración del Proyecto: URL del ambiente de desarrollo (ADR-0005) y cuentas de prueba por rol (ADR-0016).
*Salidas*
- `evidencia/smoke-0N.md` (numerado por corrida — mismo formato que `evidencia/diagnostico-01.md` de `skills/03-...md`, con `tipo: smoke`). Junto con las corridas anteriores, es el historial de regresión de la HU (ADR-0020), no solo evidencia de una corrida aislada.
- Si todos los TCs pasan: la HU se marca completa (y, con ella, todos sus paquetes de trabajo fusionados pasan de `fusionado` a `completo`).
- Si alguno falla: señala al orquestador para que dispare la skill de generación de fixes (`skills/09-...md`), que arranca una nueva ronda — ver el ciclo `RESULT → FIXSUB → DEV` del diagrama 01.
*Qué hace (alto nivel)*
Idéntico al mecanismo de `skills/03-...md` (generar script Playwright por TC, ejecutar con la cuenta de prueba del rol correspondiente, registrar resultado y evidencia), aplicado sobre todos los TCs de la HU una vez que el orquestador confirma que la ronda en curso está completa (ADR-0023).
*Estado de implementación*
Implementada — ADR-0059: la IA lee el código del frontend y escribe un script de Playwright por HU; se valida y ejecuta en un proceso aparte con cuentas de prueba por rol; un agente de navegador verifica los fallos; las corridas quedan como regresión repetible sin IA. Sin generación de fixes (skill 09) ni verificación del despliegue (ADR-0025) todavía.
*ADRs relacionados*
- ADR-0059 — implementación.
- ADR-0004 — smoke testing como fase posterior al merge.
- ADR-0006 — Playwright como motor de ejecución.
- ADR-0007 — mismo mecanismo que el diagnóstico de avance.
- ADR-0016 — selección de cuenta de prueba por rol.
- ADR-0020 — alcance completo (todos los TCs de la HU) y versionado de cada corrida como regresión.
- ADR-0023 — disparador por ronda completa, no por paquete de trabajo individual.
- ADR-0025 — el orquestador verifica que el ambiente ya refleja el cambio antes de invocar esta skill.
- ADR-0026 — vocabulario "paquete de trabajo".
*Criterios de éxito*
Cada TC de la HU tiene un resultado registrado (pasa/falla) con evidencia en la corrida más reciente, y el resultado agregado decide correctamente si la HU queda completa o se dispara una nueva ronda de fix.
*Pendientes propios de esta skill*
Comparte los pendientes de `skills/03-...md` (umbral falla vs. error técnico, TC sin rol configurado). Específico de esta skill:
- Si un TC falla en smoke testing pero había pasado en una corrida anterior (regresión introducida por el propio cambio) — ¿se trata igual que cualquier TC fallido, o amerita una señal distinta (algo se rompió, no que algo nunca se hizo)? Se vuelve más relevante ahora que cada corrida es comparable contra la anterior (ADR-0020).
- Cómo se representa en el front-matter de `evidencia/smoke-0N.md` la comparación contra la corrida anterior (ADR-0020, pendiente).

### B.10 Skill — Generación de fixes
Alias en diagramas: `S7` en diagrama 02 y el nodo `FIXSUB` del diagrama 01.
*Propósito*
Cuando smoke testing (`skills/08-...md`) reporta que uno o más TCs de la HU fallaron (tras fusionar toda una ronda de paquetes de trabajo, ADR-0023 — no un paquete de trabajo aislado), generar uno o más paquetes de trabajo de fix que corrijan el comportamiento — sin editar directamente el código ya fusionado en `develop`. Cada fix forma una nueva ronda (ADR-0023): reentra al ciclo normal — genera código (`skills/06-...md`), abre PR, pasa revisión (`skills/07-...md`) — y, a diferencia de la ronda original, en cuanto esa ronda de fixes termina de fusionarse se dispara smoke testing de inmediato (ya no hay más trabajo original pendiente esperando).
Esta skill no introduce un mecanismo nuevo de generación de código ni de revisión — reutiliza `skills/06-...md` y `skills/07-...md` tal cual; lo único propio de esta skill es diagnosticar el fallo y crear el o los paquetes de trabajo de fix correctamente vinculados a su origen.
*Cuándo se invoca*
Cuando `skills/08-...md` (smoke testing) reporta al menos un TC fallido, tras correr sobre todos los TCs de la HU al completarse una ronda (la original o una de fix anterior).
*Entradas*
- `evidencia/smoke-0N.md`: qué TCs fallaron y qué se observó vs. qué se esperaba.
- `tasks.md` y los `paquetes/PT-0N.md` de la ronda recién fusionado (candidatos a haber causado el fallo — ver Notas sobre atribución).
- `spec.md` / `plan.md` de la HU: referencia de qué se pretendía construir.
*Salidas*
Uno o más paquetes de trabajo nuevos, `paquetes/PT-0M.md`, con front-matter:
CODIGO:
id: PT-05
hu_id: HU-001
repo: backend-principal        # el repo donde se corrige el comportamiento
estado: pendiente
ronda: 2                        # nueva ronda de fix (ADR-0023) — incrementa sobre la ronda anterior
tcs_asociados: [TC-003]         # los TCs que fallaron en smoke testing
tipo: fix
paquete_origen: PT-02                   # paquete de trabajo candidato cuyo código causó el fallo, si se pudo atribuir
evidencia_origen: evidencia/smoke-01.md
pr: null
rondas_revision: 0
FIN-CODIGO
Y actualiza `tasks.md`: incrementa `total_paquetes`, agrega el o los nuevos paquetes de trabajo de fix a la lista, todos con el mismo `ronda`.
*Qué hace (alto nivel)*
- Lee `evidencia/smoke-0N.md` para identificar los TCs fallidos y el detalle de cada fallo.
- Diagnostica, contra `spec.md`/`plan.md` y los paquetes de trabajo de la ronda recién fusionado, si el fallo es porque el código no implementa correctamente el criterio, o porque el cambio introdujo una regresión en algo que antes funcionaba (ver Notas) — y, si es posible, a qué paquete de trabajo de esa ronda se puede atribuir.
- Crea un paquete de trabajo `tipo: fix` por cada agrupación razonable de TCs fallidos (ver Pendientes), vinculado a la evidencia que lo disparó (`evidencia_origen`) y, si se pudo atribuir, al paquete de trabajo candidato (`paquete_origen`).
- Actualiza `tasks.md` con la nueva ronda.
- Despacha cada paquete de trabajo de fix a `skills/06-...md` como cualquier otro paquete de trabajo pendiente — mismo mecanismo de generación de código y PR, sin trato especial.
*Estado de implementación*
Implementada — ADR-0061: diagnóstico con IA de los TCs fallidos, un fix por causa raíz (cada TC en exactamente un fix), atribución de mejor esfuerzo, límite de 3 rondas y nueva corrida de smoke testing al fusionar la ronda.
*ADRs relacionados*
- ADR-0061 — implementación.
- ADR-0004 — el ciclo de fix como fase del flujo.
- ADR-0006 / ADR-0007 — origen del TC fallido que dispara esta skill.
- ADR-0008 — formato de `paquetes/PT-0N.md`.
- ADR-0011 — si el fix hereda algún supuesto, se propaga igual que en `skills/06-...md`.
- ADR-0020 — cuando el fix se fusione, `skills/08-...md` vuelve a correr todos los TCs de la HU, no solo el que disparó este fix.
- ADR-0023 — cada fix forma una nueva ronda; a diferencia de la ronda original, al fusionarse dispara smoke testing de inmediato.
- ADR-0026 — vocabulario "paquete de trabajo".
*Criterios de éxito*
Cada TC fallido en smoke testing queda cubierto por exactamente un paquete de trabajo de fix, vinculado a su origen, y ese paquete de trabajo sigue el ciclo normal (código → revisión → smoke) hasta que el TC pasa.
*Notas*
Un TC que falló en smoke testing pero había pasado en una corrida anterior (`skills/03-...md` o un `smoke-0N.md` previo) es una regresión introducida por el propio cambio — distinto de un TC que nunca pasó (trabajo nunca terminado). Esta skill puede necesitar tratar ambos casos distinto (ver Pendientes); por ahora, el front-matter no distingue uno de otro más allá de lo que ya cuenta `evidencia_origen`.
Atribución más difícil desde ADR-0023: como smoke testing ahora corre una sola vez para toda una ronda de paquetes de trabajo (no una por una), un TC fallido ya no apunta obviamente a "el paquete de trabajo que se acaba de fusionar" — pudo haber sido cualquiera de los paquetes de trabajo de esa ronda, o una interacción entre varias. `paquete_origen` queda como *mejor esfuerzo*, no garantizado; cuando no se puede atribuir con confianza, el paquete de trabajo de fix puede quedar sin `paquete_origen` y describir el fallo directamente contra `spec.md`/`plan.md`.
*Pendientes propios de esta skill*
- Cómo se agrupan TCs fallidos relacionados en un solo paquete de trabajo de fix vs. varios — ¿un fix por TC, o uno que cubre varios TCs que probablemente comparten causa raíz?
- Cómo se diagnostica a qué paquete de trabajo de la ronda recién fusionado atribuir un TC fallido cuando no es evidente (ver Notas) — puede requerir analizar el diff de cada paquete de trabajo de la ronda, no solo el resultado del TC.
- Si una regresión (TC que antes pasaba) debería generar un paquete de trabajo de fix con mayor prioridad o señal distinta que un TC que simplemente nunca se implementó — sigue sin decidirse (ver Notas).
- Qué pasa si un fix, a su vez, vuelve a fallar en smoke testing — ¿se generan fixes indefinidamente, o hay un límite de rondas antes de escalar a revisión humana? (mismo tipo de pendiente que quedó abierto en `skills/06-...md` sobre reintentos de generación de código).
- Cómo se refleja un paquete de trabajo de fix en los reportes agregados (ADR-0012): ¿cuenta como trabajo nuevo, o como "retrabajo" del paquete de trabajo original para las métricas del objetivo 11 de `00-vision-general.md`?

### B.11 Skill — Generación de release
Alias: skill 10, Fase 4 (Implementación) — ADR-0034, ADR-0042.
*Propósito*
Convertir la configuración de despliegue en GCP de un Proyecto (ADR-0041) en los archivos que hacen el despliegue: un `release.py`, el disparador que lo ejecuta cuando cambia el repositorio y un LEEME con los pasos de una sola vez. Es determinista: plantillas, sin LLM.
*Cuándo se invoca*
Bajo demanda desde la plataforma (botón "Generar release.py" en la pestaña Implementación), una vez que la configuración de despliegue está completa y guardada. No lo despacha el orquestador todavía.
*Entradas*
- `despliegue_gcp` del Proyecto (proyecto, región, servicios, Artifact Registry, disparador, CI, autenticación, service account, proveedor WIF o nombre del secreto).
- `estructura_repositorios` (monorepo o multirepo) y la lista de repositorios (para derivar el dueño/repositorio de GitHub de los comandos de Workload Identity).
*Salidas*
En el repositorio de control, carpeta `despliegue/` (un commit):
- Monorepo: `release.py`. Multirepo: `release-backend.py` y, si hay frontend, `release-frontend.py`.
- Si `ci_plataforma` es GitHub Actions: `.github/workflows/release*.yml` (disparo por push a rama, por tag `v*` o solo manual; siempre `workflow_dispatch`). Si es Cloud Build: `cloudbuild*.yaml`.
- `LEEME.md` con los pasos de una sola vez rellenados con los valores del Proyecto.
Ningún archivo contiene credenciales: el workflow se autentica antes de ejecutar el script. El pool y el proveedor de Workload Identity son uno por proyecto de GCP y su condición acumula los repositorios de todos los Proyectos que despliegan ahí; `release.py` agrega el del Proyecto si falta, sin quitar los demás (ADR-0085). Cada servicio se construye desde su carpeta o, en monorepos con workspaces (`apps/`, `packages/`, `services/`), desde la raíz con `-f` cuando su Dockerfile lo pide (ADR-0086). El backend recibe `DATABASE_URL` como secreto si su stack no es Java, y el frontend recibe la URL del backend como build-arg si su Dockerfile la fija al compilar (ADR-0087).
*Qué hace (alto nivel)*
- Valida que la configuración esté completa; si no, devuelve la lista de lo que falta.
- Elige la forma de los artefactos según monorepo/multirepo, hosting del frontend y CI.
- Rellena las plantillas, escribe todo en `despliegue/` y hace un solo commit.
- Devuelve los archivos y las advertencias, y registra la última ejecución de la Fase 4.
*Ejecución desde la plataforma*
El release se puede ejecutar desde la pestaña Implementación y los cambios de infraestructura dejan el despliegue «desactualizado» (ADR-0055).
*Artefacto: release.py*
El script se genera en Python (`release.py`) y no en Bash — ADR-0054.
*ADRs relacionados*
- ADR-0054 — `release.py` en lugar de `release.py`.
- ADR-0041 — la configuración.
- ADR-0042 — esta skill.
- ADR-0013 y ADR-0032 — cómo se publicaría en el repositorio del código y por qué no hay credenciales en la configuración.
- ADR-0025 — lo que sigue tras el release.
*Criterios de éxito*
Con la configuración completa, se generan los archivos, `python -m py_compile release.py` valida, los YAML son válidos y ninguno contiene una llave o token.
*Pendientes propios de esta skill*
- Publicar los archivos en el repositorio del código vía PR (resuelto) — resuelto en ADR-0043: botón "Publicar en el repositorio (PR)", con la cuenta de desarrollo del Proyecto.
- Destinos distintos de Cloud Run (App Engine, GKE) y otras nubes.
- Que el orquestador la despache como parte del flujo de la Fase 4.

