# Experimento C — revisión con contexto frente a solo el diff (H1)

Diseño y decisiones: [ADR-0089](../../../arquitectura/decisiones/0089-experimento-c-revision-con-contexto-frente-a-solo-el-diff.md).
Corrida `c1`, del 2026-09-27 19:22 al 2026-09-28 09:37 (hora de Zacatecas), con tres interrupciones (ver *Bitácora*).

## Qué se hizo

Las 29 primeras revisiones de los pilotos (E1c Inventarios, 12 paquetes; E3c Agenda Taller, 17) se repitieron en dos condiciones con
el mismo modelo y el mismo diff:

| | Contexto | Solo diff |
|---|---|---|
| Prompt de sistema | `REVISION_SYSTEM` de la skill 07, sin cambios | `REVISION_SYSTEM_SOLO_DIFF` (misma estructura, fuentes, severidades y reglas) |
| Mensaje | paquete + arquitectura + spec y casos de prueba de la HU + título y descripción del PR + diff | solo el diff |
| Entrada media | 121,611 caracteres | 76,529 caracteres |
| Modelo | `claude-sonnet-5` por el CLI de Claude Code (el CLI usa además Haiku 4.5 para tareas auxiliares) | igual |

- **Diff:** el del primer commit de cada PR respecto a su padre, reconstruido desde GitHub; coincide con el diff guardado de las 29
  revisiones (primeros 60,000 caracteres). Tres diffs de E3c pasan de 140,000 caracteres y se recortan igual en las dos condiciones.
- **Paquete:** el del repositorio de control de Loom en el commit anterior a su primera revisión (ver *Descarte*).
  `verificar_contexto.py` comprueba que la spec, los casos de prueba y la arquitectura no cambiaron después de las primeras revisiones.
- **Observaciones:** solo las del modelo; no se agregan las que Loom inyecta (compuerta de compilación, supuestos).

## Resultados antes de calificar

| | Contexto | Solo diff |
|---|---|---|
| Observaciones | 85 | 92 |
| Bloqueantes / mayores / menores | 7 / 21 / 57 | 2 / 21 / 69 |
| Por fuente: criterio de aceptación | 13 | 0 |
| arquitectura | 19 | 15 |
| buenas prácticas | 39 | 50 |
| pruebas | 9 | 7 |
| seguridad | 5 | 20 |
| PRs sin observaciones | 0 | 0 |
| Duración total del modelo | 92.4 min | 100.0 min |
| Costo nocional (suscripción) | 14.81 USD | 11.39 USD |

Estos conteos **no contestan H1**: H1 habla de observaciones *relevantes*, y eso solo lo dice la evaluación ciega. Fuera del
experimento se gastaron 13.84 USD nocionales más (29 llamadas descartadas y 2 de prueba); hubo 2 llamadas fallidas por el límite de
sesión del CLI, que se repitieron. Datos en `datos/resumen-c1.json`.

## Descarte de la primera pasada de «contexto»

La primera pasada de la condición «contexto» tomó el `md` del paquete desde Mongo. Ese `md` se regenera después de cada revisión con
las observaciones de la última revisión del piloto y el estado final (`fusionado`), así que el revisor recibió, como parte del
paquete, observaciones ya hechas. Se detectó al armar la hoja de evaluación, se descartó completa (29 revisiones, 123 observaciones)
y se repitió con el paquete reconstruido desde el repositorio de control. Los resultados descartados siguen en Mongo
(`experimento_c`, corrida `c1-descartada`) y sus llamadas en `metricas` (`experimento-c-contexto-descartada`); no forman parte del
análisis. La condición «solo diff» no se afectó: solo recibe el diff.

## Resultado con la evaluación automática (2026-09-29)

Por decisión del autor ([ADR-0091](../../../arquitectura/decisiones/0091-experimento-c-se-reporta-la-evaluacion-automatica.md)), la
tesis reporta la calificación automática de `claude-opus-5-5` (ver *Segunda opinión automática*). Antes de abrirla se comprobó que
las tres huellas SHA-256 publicadas coincidían. Resultado (`python analizar.py c1 opinion` → `datos/resultados-c1-opinion.json`):

| | Contexto (85) | Solo diff (92) |
|---|---|---|
| Relevante y correcta | 24 (28.2 %) | 21 (22.8 %) |
| Relevante pero mal sustentada | 4 | 7 |
| Relevantes en sentido amplio | 28 (32.9 %) | 28 (30.4 %) |
| Ruido | 45 | 53 |
| Falsa | 12 | 11 |
| Bloqueantes válidas / total | 4 / 7 | 1 / 2 |
| Mayores válidas / total | 12 / 21 | 13 / 21 |

Prueba pareada sobre los 29 PRs, relevancia amplia: 7 a favor de contexto, 7 de solo diff, 15 empates; Wilcoxon p = 1.0, r = 0.
Relevancia estricta: 8, 6 y 15; p = 0.47, r = 0.2. De 18 pares de observaciones equivalentes entre condiciones, 9 tienen las dos
relevantes: 47 hallazgos relevantes distintos, 28 por condición. **No hay evidencia a favor de H1 con este calificador; H1 no se
declara rechazada**, porque el instrumento que la decide es la calificación por una persona.

## Evaluación ciega por una persona (pendiente, trabajo futuro)

La califica una persona, no el asistente que generó las observaciones. Desde el 2026-09-29 la clave, los datos crudos y la
opinión automática están versionados y el resultado automático es público: quien califique no debe consultarlos antes. Instrucciones en
[`evaluacion-ciega/guia-del-evaluador.md`](evaluacion-ciega/guia-del-evaluador.md).

- `evaluacion-ciega/hoja-de-evaluacion.xlsx`: 177 observaciones en 29 PRs (`P01`–`P29`, en orden aleatorio), mezcladas dentro de cada
  PR, sin fuente ni severidad. Rúbrica: relevante y correcta / relevante pero mal sustentada / ruido / falsa.
- `evaluacion-ciega/contexto/Pnn.md`: enlace al cambio revisado, paquete (sin observaciones ni estado) y, si aplica, spec y casos de
  prueba de la HU.
- `clave/clave-c1.json`: une cada identificador con su condición. Estuvo fuera de git hasta el 2026-09-29. SHA-256: `7fc38eaac5e2a21d869c9c3d6676b757b6f199f6b12f5096f370aa706911379f`.
- `datos/experimento_c-c1.json`: cada observación con su condición; fuera de git hasta el 2026-09-29.
  SHA-256 (de los bytes del archivo): `acc74cb36778da1ebe90edb670b2a1a4723d1aaf5424ad6434dd1e02e9e26cc1`.

Limitación conocida del cegado: 50 de las 177 observaciones mencionan la HU, sus criterios, los casos de prueba o la arquitectura
(35 de «contexto» y 15 de «solo diff»), lo que puede sugerir su origen. La guía pide calificar solo si lo dicho es cierto y útil.

Para calificar por partes, [`evaluacion-ciega/plan-de-sesiones.md`](evaluacion-ciega/plan-de-sesiones.md) reparte los 29 PRs en seis
sesiones por proyecto y por HU, con los enlaces de cada PR y una bitácora para anotar el tiempo (lo genera `armar_sesiones.py`). El
contexto incluye desde el 2026-09-29 el documento de arquitectura de cada proyecto (`contexto/arquitectura-E1c.md` y `-E3c.md`);
la hoja y la clave no cambiaron.

Cuando la hoja esté completa: `python analizar.py c1` → `datos/resultados-c1.json` (proporción de relevantes por condición, prueba
pareada sobre los 29 PRs, bloqueantes y mayores válidas, observaciones compartidas). Después se versionan la clave y los datos
crudos y se comprueban sus SHA-256.

## Segunda opinión automática

[ADR-0090](../../../arquitectura/decisiones/0090-experimento-c-segunda-opinion-automatica-sellada.md). Un modelo distinto del que
revisó (`claude-opus-5-5`) calificó las mismas 177 observaciones con la misma rúbrica, una llamada nueva por PR, con lo mismo que
recibe la persona y sin la condición, la fuente ni la severidad. Se hizo como análisis secundario y sellado; por ADR-0091 es la
evaluación que reporta la tesis, y **sigue sin decidir H1**.

- `segunda-opinion/opinion-c1.json`: sellado hasta que se decidió usarlo (mismo día). Corrida del 2026-09-29:
  29 llamadas, 177 de 177 observaciones calificadas, 11.7 minutos de modelo y 15.73 USD nocionales.
  SHA-256: `720d6c7b002cd204be7f320a1436ae9a599bec76b7e1d799a1f5e42f23de94f2`.
- `exportar_opinion.py`: lo exporta de Mongo (`experimento_c_opinion`) sin imprimir calificaciones.
- `comparar_opiniones.py`: cuando la hoja esté completa, calcula el acuerdo y el kappa de Cohen (cuatro y dos categorías), la
  matriz de confusión y, como análisis secundario, H1 con la calificación automática → `datos/acuerdo-c1.json`.

## Archivos

| Archivo | Qué es |
|---|---|
| `exportar.py` | exporta de Mongo los resultados y arma el paquete ciego |
| `analizar.py` | cruza la hoja calificada con la clave y calcula los resultados de H1 |
| `verificar_contexto.py` | compara el contexto del experimento con el que vio la primera revisión real |
| `datos/experimento_c-c1.json` | las 58 revisiones con sus observaciones (con fuente y severidad) |
| `datos/resultados-c1-opinion.json` | resultado de H1 con la calificación automática |
| `datos/metricas-c1.json` | llamadas al modelo: duración, costo nocional, modelo informado, errores |
| `datos/resumen-c1.json` | conteos por condición antes de calificar |
| `logs/corrida-c1.log` | bitácora de la corrida con las interrupciones y el descarte |
| `armar_sesiones.py` | arma el plan de calificación por sesiones y copia la arquitectura al contexto |
| `logs/segunda-opinion-c1.log` | bitácora de la segunda opinión automática |

El módulo que corre el experimento está en el repositorio de Loom:
`loom/backend/src/loom_backend/experimentos/revision_contexto.py` (commit `28ca4e2` del repositorio de Loom).

## Bitácora

1. 2026-09-27 19:22 — inicio; prueba previa con un PR (descartada, métricas `-prueba`).
2. 2026-09-27 21:02 — límite de sesión del CLI con 31 de 58 revisiones; Docker (Mongo) apagado. Se reanuda a las 23:43.
3. 2026-09-28 00:20 — *TLS handshake timeout* de la API de GitHub con 42 de 58; se agregan reintentos a `gh api` y se reanuda.
4. 2026-09-28 02:26 — descarte de la primera pasada de «contexto» y repetición con el paquete reconstruido.
5. 2026-09-28 03:07 — límite de sesión del CLI con 13 de 29 «contexto» (se liberaba a las 04:40); se reanuda a las 08:45 y termina a las 09:37.
