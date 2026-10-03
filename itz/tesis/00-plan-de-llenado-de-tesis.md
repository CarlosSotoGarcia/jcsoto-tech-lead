# Plan de llenado de la tesis (documento de trabajo)

> Inventario de **todo lo que hace falta** para llenar [`GUIA PARA ESTRUCTURA DE TESIS.docx`](GUIA%20PARA%20ESTRUCTURA%20DE%20TESIS.docx)
> con una tesis enfocada en lo que hace **Loom** (el sistema que convierte HUs en código verificado y revisado).
> Modelo de redacción y profundidad: [`../referencias/`](../referencias/) (tesis de Javier García: metodología en 3 fases y
> resultados en 3 secciones, 243 páginas). Este archivo no es la tesis: es el mapa de qué escribir, con qué evidencia y
> qué falta.
>
> Estado: **borrador 3 — 2026-09-21** (segunda etapa del piloto E1c, § 2.5; cómo se llena cada sección y flujo de redacción, § 12 y § 13). Se actualiza conforme se resuelven las decisiones abiertas (sección 10).

---

## 1. Qué es la tesis (base a redactar)

| Elemento | Contenido de partida | Fuente en el repositorio |
|---|---|---|
| Título tentativo | *Sistema de skills de IA que orquesta el ciclo de desarrollo de una funcionalidad a partir de historias de usuario: de la especificación al Pull Request revisado* (por afinar) | `itz/documentación/propuesta-tesis-idea-elegida.pdf` |
| Problema | Las herramientas de IA automatizan una sola etapa (solo revisión o solo pruebas), asumen proyecto nuevo y operan sobre el diff sin partir de la intención de negocio | `itz/arquitectura/00-vision-general.md` § Problema |
| Objetivo general | Diseñar e implementar un sistema de skills de IA que, desde una HU, orqueste el ciclo de desarrollo (TCs, arquitectura, paquetes, código, revisión, validación) de forma generalizable | ídem § Objetivo general |
| Objetivos específicos | 11 objetivos vigentes (ver § 8 para el estado de cada uno) | ídem § Objetivos específicos |
| Contribución | Un marco reproducible + herramienta funcional que muestra que dar a un LLM la HU, sus TCs y la arquitectura aprobada como contexto explícito mejora la relevancia de la revisión y la cobertura de criterios, frente a solo ver el diff | `ideas-proyecto-titulacion.md` idea #3 |
| Generalización | La herramienta es agnóstica del sistema y del proveedor de IA; se valida en más de un proyecto y con más de un proveedor (Claude, Gemini) | ADR-0009, ADR-0047 |

**Decisión de redacción:** hablar de **Loom** como la implementación del sistema (en la documentación de arquitectura también
se le llamó *Telar*; unificar el nombre en la tesis y aclararlo una sola vez en el capítulo 4).

### Hipótesis y variables (propuesta para el cap. 1.6 y 1.7)

- **H1.** Un pipeline que alimenta al LLM con la HU, los casos de prueba derivados de sus criterios y la arquitectura aprobada produce
  paquetes de código cuya revisión automática detecta observaciones **relevantes** (no ruido) en una proporción mayor que una revisión
  que solo ve el diff.  *(requiere línea base "solo diff": ver § 5, experimento C)*
- **H2.** El sistema es **generalizable**: con la misma configuración base logra el ciclo completo en proyectos de dominios distintos.
- **H3 (comparativa).** El proveedor de IA (Claude vs. Gemini) afecta la calidad y el costo del resultado; la arquitectura del sistema permite
  intercambiarlo sin modificar las skills.
- Variable independiente: contexto entregado al LLM (solo diff / HU + TCs + arquitectura); proveedor de IA; proyecto.
- Variables dependientes: cobertura de criterios de aceptación por los TCs; relevancia de las observaciones; rondas de revisión hasta aprobar; tiempo,
  tokens y costo por paquete; tasa de reintentos por salida mal formada.

---

## 2. Diseño de la validación (lo que se va a ejecutar)

### 2.1 Proyectos y proveedores: matriz 2 × 2

| | Claude | Gemini |
|---|---|---|
| **P1 — ITZ Control Inventarios** (Jira, 28 HUs, 63 paquetes) | E1 | E2 |
| **P2 — IAT** (Jira `jncsoga.atlassian.net`, tablero 2) | E3 | E4 |

Cada escenario `E#` = **una corrida completa de las fases 1 a 3** sobre el mismo backlog, cambiando **solo** el proveedor
(`proveedor_llm` del Proyecto). Todo lo demás se mantiene igual: mismas HUs, mismos repositorios de partida, mismos prompts, misma cuenta de desarrollo.

**Datos que hacen falta de P2 (IAT):** cuántas HUs hay en el sprint activo, dominio, stack deseado, si es greenfield o ya tiene código, repositorio
de GitHub destino y su rama base, y credenciales de Jira (correo + API token, por proyecto). No se guardan credenciales en este documento.

### 2.2 Reglas para que la comparación sea válida

1. **Mismas entradas:** mismo sprint congelado (capturar la lista de HUs y su texto antes de correr; guardar el JSON de Jira como evidencia).
2. **Un repositorio destino por escenario** (o rama base idéntica reiniciada): los PRs de Claude y de Gemini no deben mezclarse.
3. **Repeticiones:** los LLM no son deterministas; mínimo **3 corridas** por escenario para las fases baratas (1, 2, 5) y 1 corrida completa de la fase 3
   más una muestra de paquetes repetidos (p. ej. 5 paquetes × 3 veces) para medir varianza.
4. **Evaluación ciega:** quien califique relevancia de observaciones y suficiencia de TCs no debe saber qué proveedor los generó (asignar etiquetas A/B).
5. **Registrar fallos** además de éxitos: JSON mal formado, truncamientos, reintentos, terminaciones sin pruebas, archivos obligatorios ausentes.
6. **Usar la API en los experimentos:** el proveedor «Claude (cuenta normal)» (ADR-0053) es solo para desarrollo; no da tokens, tiempo ni costo
   comparables. Los escenarios E1–E4 se corren con Claude (API) y Gemini.
7. **Congelar versión:** anotar el commit de Loom y los modelos exactos usados (`claude-sonnet-5`; Gemini `gemini-3.6-flash` para análisis y
   `gemini-pro-latest` para código; cambian con el tiempo).

### 2.3 Experimentos

| # | Pregunta | Qué se compara | Métrica principal |
|---|---|---|---|
| A | ¿Los TCs generados cubren los criterios de aceptación? | TCs de cada HU vs. sus criterios (`criterio_ref` en cada TC) | % de criterios con ≥1 TC; TCs sin criterio (ruido) |
| B | ¿Claude o Gemini hacen mejor cada skill? | E1 vs. E2 y E3 vs. E4 en skills 01, 02, 04, 05, 06, 07 | calidad (rúbrica), reintentos, tiempo, tokens, costo |
| C | ¿La revisión con contexto supera a la revisión solo con el diff? | Mismos PRs revisados con (i) contexto completo y (ii) solo el diff | % de observaciones relevantes; observaciones bloqueantes válidas |
| D | ¿Generaliza? | P1 vs. P2 (dominios y stacks distintos) | ciclo completo alcanzado sin reconfiguración profunda |
| E | ¿El código generado funciona? | Paquetes con CI o con `docker compose up` / pruebas ejecutadas por una persona | % de paquetes que compilan y pasan sus pruebas a la primera |

---

### 2.4 Estado del piloto (2026-09-19)

Piloto acotado (tope 20 USD) sobre P1 con 3 HUs: **E2 (Gemini) ejecutado**, fases 1 a 3 y 5 de 10 paquetes, 4.76 USD estimados; **E1 (Claude API) bloqueado** por saldo insuficiente en la API de Anthropic; **E1c (Claude por CLI) ejecutado** como alternativa exploratoria (6 de 13 paquetes, costo nocional 10.02 USD, no comparable con la API); E3/E4 pendientes (IAT sin configurar). Resultados en el capítulo 5 de `Loom - Tesis.docx` y evidencia en `evidencia/piloto-E2-2026-09-19/`. Hallazgos: 100 % de trazabilidad criterio-caso pero todos los casos son de interfaz; el frontend generado pasa sus 19 pruebas y el backend no compila (dependencia sin versión) sin que la revisión lo detecte; posible subconteo de tokens de entrada en las skills de análisis.

### 2.5 Segunda etapa del piloto E1c (2026-09-20 y 2026-09-21)

Decisión del 2026-09-20: **primero se hace funcionar de punta a punta el proyecto experimento** (E1c, ITZ Inventarios con Claude por CLI), registrando cada error y cada
intervención manual para que Loom los evite solo; **después se repite el ejercicio desde cero** para documentar el proceso completo y limpio. Lo que sigue es lo que
ya ocurrió en esta etapa (todo con fuente en el repositorio o en la conversación de trabajo; los números son de la corrida indicada, no un promedio).

| Qué | Resultado | Fuente |
|---|---|---|
| Generación de código por Loom | HU-001, HU-002 y HU-003 completas (paquetes generados, revisados, corregidos y fusionados); HU-004 y HU-005 sin generar | Mongo `paquetes`; PR del piloto |
| Ciclo de HU-001 (2 paquetes, 1 ronda de corrección) | 14.82 USD nocional (Claude por CLI, no comparable con la API); cada paquete terminó con observaciones abiertas, una de ellas bloqueante | Métricas de la corrida |
| Despliegue en GCP (Cloud Run + Cloud SQL) | Ambiente funcionando (backend y frontend); el `release.py` que genera Loom crea la base, los secretos y las variables (ADR-0071) | Cloud Run; `health` en `UP` |
| Smoke testing de HU-001 | 19 casos: 13 pasan, 0 fallan, 6 bloqueados (límite de intentos del login por el orden de los casos y falta de datos de prueba); 332 s | `HU-001/evidencia/smoke-01.md` |
| Defectos del código generado que solo aparecieron al desplegar o en el CI | 10 (A1 a A10): migración, CORS, entrypoint del frontend, Dockerfile, pruebas, lock, autenticación de GCP, checksum de Flyway | `01-registro-de-hallazgos-piloto-e1c.md` |
| Intervenciones manuales sobre el código del piloto | 6 PR directos (#14, #15, #16, #23, #24, #28), `flyway repair` en Cloud SQL, usuarios de prueba insertados en Cloud SQL, decisión de negocio (90 min de inactividad) registrada por la API | Mismo registro (§ D) |
| Mejoras a la plataforma nacidas de estos hallazgos | ADR-0071 a ADR-0084: release con Cloud SQL, release automático, avance de HU de punta a punta, no fusionar con el CI en rojo, corregir con el log del CI, lint y pruebas antes de subir, despliegue con GitHub Actions + Workload Identity, procesos concurrentes, historial y cancelación | `arquitectura/decisiones/` |

**Lectura para el capítulo 5 (sin adelantar conclusiones):** el código generado pasó la revisión de Loom y la compilación, pero falló al ejecutarse o en el CI de forma repetida
(A1 a A5); la revisión de código no detecta lo que solo se ve al arrancar. Esto sostiene el argumento de las compuertas de ejecución (compilación, lint, pruebas y arranque real) y
debe reportarse como resultado, incluida la parte que todavía no está resuelta (la compuerta de arranque, ADR-0071, no está implementada).

**Advertencia de validez:** esta etapa mezcla trabajo de la plataforma con corridas del piloto. Los números de arriba sirven para orientar y para el registro de hallazgos, **no** como
resultados del experimento; los resultados válidos saldrán de la repetición desde cero con la plataforma congelada (§ 9, paso 3).

### 2.6 Corridas desde cero: E1c (2026-09-21) y E3c (2026-09-26/27)

Las dos corridas se hicieron desde un Proyecto limpio, operando Loom desde su interfaz con Playwright, con tres HUs, una sola revisión por paquete y una corrección solo con el CI en rojo. Ambas usaron el **CLI de Claude con suscripción**, no la API: son pilotos completos, no los escenarios E1–E4 de la matriz (regla 6 de § 2.2).

| | E1c — P1 Inventarios | E3c — P2 Agenda Taller |
|---|---|---|
| Stack generado | Java/Spring Boot + Angular, monorepo en la raíz | Node/NestJS + Prisma + React/Vite, monorepo con `apps/` |
| Modelo | claude-sonnet-5 | **claude-opus-5-5** + claude-haiku-4-5 (Loom no fija el modelo del CLI) |
| Casos de prueba | 44 | 101 |
| Paquetes fusionados | 12/12 | 17/17 |
| Observaciones de revisión | 66 (2 bloqueantes, 24 mayores, 40 menores) | 69 en 19 revisiones (12 mayores, 57 menores) |
| Correcciones | 1 (CI en rojo) | 4 registros (2 paquetes con CI en rojo) |
| Compuerta de compilación | ejecutada en 10 de 12 paquetes | **omitida en las 21 ejecuciones** (no detecta `apps/`) |
| Release | correcto al 2.º intento (BD con migraciones previas) | correcto al 3.er intento, tras ADR-0086 y 0087 |
| Smoke | 36 pasan, 2 fallan, 6 bloqueados de 44 | 68 pasan, 9 fallan, 24 bloqueados de 101 (HU-001 en su 3.ª corrida, tras ADR-0088) |
| Llamadas / costo nocional | 128 / 16.67 USD | 532 / 120.99 USD |
| Hallazgos | `01-registro-de-hallazgos-piloto-e1c.md`, Anexo C de la tesis | `02-registro-de-hallazgos-piloto-e3c.md` |

**Lectura:** E3c es la primera evidencia de generalización (PI3/H2): el mismo flujo completó el ciclo en un segundo dominio y un segundo stack, pero **no solo con cambios de configuración**: hizo falta cambiar Loom en tres puntos (ADR-0086, 0087, 0088) y ajustar la configuración a lo que el código generado pedía. Es un resultado parcial y honesto de H2: la arquitectura de *skills* se mantuvo, pero el release y el smoke tenían supuestos atados al stack del primer proyecto.

**Validez:** modelos distintos (Sonnet 5 vs. Opus 5.5), plataforma no congelada (cambió durante E3c) y una sola repetición por proyecto. E1–E4 con la API siguen sin correr: Anthropic sin saldo y Gemini con la facturación bloqueada (2026-09-27); estimación de costo en `evidencia/costos/estimacion-E3-E4.md` (≈ 100 USD recomendados para E1 y E3 con la API de Claude).

## 3. Métricas y datos: qué existe y qué falta

### 3.1 Ya se registra hoy

| Dato | Dónde queda |
|---|---|
| HUs con criterios explícitos/inferidos, supuestos, posición en la fuente (`orden_fuente`) y orden final (`orden`) | Mongo `hus`; `HU-00N/spec.md` |
| TCs por HU con `criterio_ref` (deriva de qué criterio) | Mongo `hus.casos_prueba`; `test-cases.md` |
| Paquetes: capa, repo, entregables, TCs asociados, dependencias, estado, PR, `rondas_revision`, observaciones (fuente, severidad, archivo, línea) | Mongo `paquetes`; `paquetes/PT-0N.md` |
| Rondas de revisión y de corrección de cada PR: observaciones (severidad, fuente, ubicación), respuesta de la corrección, commit, valoración humana | Mongo `revisiones`; CSV en «Exportar revisiones» (ADR-0068) |
| Historial cronológico de cada artefacto | `git log` del repositorio de control (`loom_target/<id>/`) |
| PRs con descripción, diff, comentarios de revisión y commits | GitHub del proyecto |
| Pruebas escritas por paquete (archivos de prueba) | Descripción del PR y árbol de la rama |
| Corridas de smoke testing por HU: resultado de cada caso, motivo, capturas, script y % de aprobados (informe con iconos y porcentajes, ADR-0073) | Mongo `smoke`; `HU-00N/evidencia/smoke-NN.md` |
| **Procesos ejecutados** (skill, HU, cuándo empezó y terminó, estado, registro de eventos; ADR-0084) | Mongo `procesos`; pestaña «Procesos» de cada HU |
| Versiones de la especificación y de los casos de prueba de cada HU (ADR-0065) | Mongo `hu_versiones` |
| Decisiones de una persona sobre los supuestos de una HU y cuándo se tomaron (ADR-0077) | Mongo `hus` (`decisiones`) |
| Resultado del compilado, lint y pruebas previos al push (`compilacion` del paquete, ADR-0070 y 0079) | Mongo `paquetes` |
| Estado del CI de cada PR y extracto del log cuando falla (ADR-0076 y 0078) | Lectura de la API de GitHub al avanzar; no se guarda aparte |
| Resultado de cada release (local o en GitHub Actions) | Campo `release_resultado` del proyecto; ejecuciones en GitHub Actions |
| Hallazgos e intervenciones manuales de la segunda etapa | `01-registro-de-hallazgos-piloto-e1c.md` |

### 3.2 **Falta registrar** (bloquea el capítulo 5 si no se hace antes de correr los escenarios)

| Dato | Por qué importa | Propuesta |
|---|---|---|
| Proveedor y modelo usados en cada ejecución de skill | Comparación Claude vs. Gemini | Colección `metricas` |
| Duración de cada skill y de cada paquete | Tiempo por HU y por paquete | ídem |
| Tokens de entrada/salida y costo estimado | Costo por HU | ídem (ambos proveedores devuelven el uso) |
| Reintentos y tipo de falla (truncado, JSON como texto, sin tool call) | Robustez por proveedor | ídem |
| Rechazos de las compuertas (falta de pruebas, README/compose ausentes) | Efecto de las reglas TDD | ídem |
| Etiqueta ciega A/B de cada artefacto y calificación humana | Evaluación ciega | hoja de cálculo o colección aparte |
| Resultado de CI del PR y de `docker compose up` | Experimento E | manual o lectura de la API de GitHub |
| Versión de Loom (commit) por corrida | Reproducibilidad | campo en `metricas` |

> **Hecho (ADR-0057):** el sistema ya registra proveedor, modelo, tokens, duración, reintentos, rechazos de compuertas y costo en la colección
> `metricas` (resumen en la tarjeta «Uso de IA» y CSV con «Exportar CSV»). Falta cargar `LOOM_PRECIOS_MODELOS` con los precios vigentes, registrar la
> calificación humana y la versión de Loom por corrida.
>
> ~~Acción técnica previa: instrumentar `_llm.py` y `agente_codigo.py` para escribir un registro por llamada (`skill`, `proveedor`, `modelo`,
> `duración`, `tokens_in`, `tokens_out`, `reintentos`, `resultado`) y un endpoint/exportación a CSV. Es un ADR nuevo.~~

> **Estado al 2026-09-21:** el «Resultado de CI del PR» ya se **lee** para decidir si se fusiona (ADR-0076), pero **no se guarda** por paquete: falta persistirlo para el experimento E.
> También falta guardar el costo por HU completa (hoy hay costo por corrida y por skill), la versión de Loom por corrida y la calificación humana. El número de intervenciones manuales
> se lleva a mano en el registro de hallazgos; conviene definir un criterio único de qué cuenta como intervención antes de repetir el ejercicio.

### 3.3 Rúbricas de evaluación humana (por definir y anexar)

- **Suficiencia de TCs (por HU):** 0–2 por criterio (no cubierto / parcial / cubierto); TCs redundantes o inventados se cuentan aparte.
- **Relevancia de una observación de revisión:** relevante y correcta / relevante pero mal sustentada / ruido / falsa.
- **Calidad de un paquete de código:** cumple entregables (0–2), sigue la arquitectura (0–2), pruebas con sentido (0–2), compila/corre (0–2).
- **Calidad de la arquitectura y del plan (skills 04–05):** coherencia con las HUs, dependencias correctas, tamaño razonable de paquetes.

---

## 4. Escenarios y casos de uso (la parte que "llena" los capítulos 4 y 5)

### 4.1 Plantilla de caso de uso (una ficha por CU, va como tabla en el cap. 4 y detalle en anexos)

`Id · Nombre · Actor · Precondiciones · Disparador · Flujo principal (pasos) · Flujos alternos/errores · Postcondiciones · Artefactos que produce · Skill/ADR relacionado · Evidencia (captura o archivo)`

### 4.2 Catálogo propuesto de casos de uso

| Id | Caso de uso | Actor | Skill / ADR | Estado en Loom |
|---|---|---|---|---|
| CU-01 | Dar de alta un proyecto (fuente de HUs, IA) | Administrador | ADR-0009, 0014, 0047 | Implementado |
| CU-02 | Descubrir y especificar HUs desde Jira | Administrador | Skill 01, ADR-0040, 0048 | Implementado (Jira); Markdown pendiente |
| CU-03 | Generar casos de prueba por HU | Administrador | Skill 02 | Implementado |
| CU-04 | Proponer stack y generar la arquitectura; aprobarla | Administrador / arquitecto | Skill 04, ADR-0039, 0044 | Implementado |
| CU-05 | Descomponer en paquetes con esqueleto Docker/README y orden | Administrador | Skill 05, ADR-0045, 0048, 0050 | Implementado |
| CU-06 | Generar el código de un paquete y abrir el PR (TDD) | Administrador | Skill 06, ADR-0046 | Implementado |
| CU-07 | Revisar el PR y publicar observaciones | Administrador | Skill 07, ADR-0049 | Implementado |
| CU-08 | Corregir observaciones en la misma rama | Administrador | Skill 07, ADR-0049 | Implementado (sin probar en vivo) |
| CU-09 | Fusionar y sincronizar para liberar dependientes | Administrador / revisor | ADR-0029, 0046 | Implementado |
| CU-10 | Generar y publicar el release a GCP | Administrador | Skill 10, ADR-0041, 0042 | Implementado |
| CU-11 | Cambiar de proveedor de IA por proyecto | Administrador | ADR-0047 | Implementado |
| CU-12 | Diagnosticar avance previo (brownfield) | Administrador | Skill 03, ADR-0007 | **No implementado** |
| CU-13 | Smoke testing con Playwright y fixes | Administrador | Skills 08 y 09 | Implementado (ADR-0059, ADR-0061); falta correrlo en proyectos reales |

### 4.3 Escenarios de validación (los `E1`–`E4` de § 2.1)

Cada escenario se documenta con la misma estructura, para poder tabular resultados:

1. Contexto (proyecto, sprint congelado, proveedor, modelo, fecha, commit de Loom).
2. Entrada: HUs leídas (n.º de HUs y actividades, con supuestos).
3. Salidas por fase: TCs, arquitectura, paquetes (n.º, capas), orden.
4. Ejecución de la fase 3: paquetes generados, PRs, revisiones, observaciones, correcciones.
5. Métricas (tabla de § 3) y hallazgos cualitativos (fallas, casos interesantes).

---

## 5. Mapa capítulo por capítulo (guía → contenido → evidencia → estado)

Formato exigido: carta, Arial 12 con sangría de primera línea, títulos Arial 16 negrita centrados (Capítulo I…), subtítulos Arial 14 negrita,
márgenes 2.5 sup/inf/der y 3.0 izq, interlineado 1.5, numeración abajo a la derecha, capítulos en sección nueva, rótulos de figura (abajo) y de tabla
(arriba) con número de capítulo, **80–150 cuartillas**. Empastado vino con letras doradas.

| Sección de la guía | Qué debe contener (para Loom) | Evidencia / fuente | Estado | Falta |
|---|---|---|---|---|
| Portada y hoja de autorización | Datos del tesista, director, título final, fecha | Guía | Pendiente | Título final, nombre del director |
| Agradecimientos | Texto libre | — | Pendiente | Lo redacta el autor |
| Índices (figuras, gráficas, tablas) | Se generan al final | — | Pendiente | Usar estilos de título/rótulo desde el inicio |
| Resumen / Abstract | Objetivo, método, resultados clave, conclusiones; sin abreviaturas ni referencias | Se escribe al final | Pendiente | Resultados de los escenarios |
| Introducción | Área (ingeniería de software asistida por IA), razones, resumen de capítulos; ≤ 3 cuartillas | Vision-general | Pendiente | — |
| **1.1 Descripción del problema** | Problema delimitado, en forma de pregunta, con literatura | § 1 | Base lista | Citas |
| 1.2 Preguntas de investigación | Sobre contexto explícito, generalización y proveedor | § 1–2 | Por redactar | — |
| 1.3 Objetivos | General + 11 específicos | Vision-general | Base lista | Revisar los que no se cumplen (§ 8) |
| 1.4 Justificación | Beneficiarios, utilidad, costo de no hacerlo | Propuesta aprobada | Base lista | Datos de contexto (encuestas/estudios citados) |
| 1.5 Alcances y limitaciones | Dentro/fuera de alcance | Vision-general § Alcance | Base lista | Actualizar con lo implementado y lo no implementado |
| 1.6–1.7 Hipótesis y variables | H1–H3 y variables | § 1 | Propuesta | Validar con el director |
| **2 Marco teórico** | LLM y agentes con herramientas (function calling); ingeniería de software dirigida por especificaciones (SDD); historias de usuario y criterios de aceptación; pruebas (TDD, E2E); revisión de código; CI/CD y contenedores; ADRs | Vision-general, ADRs | Por escribir | Bibliografía |
| **3.1 Trabajos relacionados** | Máx. media cuartilla por trabajo (ver § 6) | — | Por investigar | Búsqueda bibliográfica |
| 3.2 Análisis comparativo | Tabla comparativa de herramientas/trabajos vs. Loom | § 6 | Por hacer | Criterios y datos verificados |
| **4.1 Metodología de solución** | Enfoque, población/muestra (proyectos y HUs), instrumentos (métricas y rúbricas), validez y confiabilidad | § 2–3 | Por escribir | Instrumentación, rúbricas |
| **4.2 Metodología implementada** | Fases de Loom (Requerimientos, Diseño, Desarrollo, Implementación), arquitectura, skills, modelo de datos, SDD, TDD, revisión, proveedor de IA; y las compuertas de ejecución (compilación, lint y pruebas, CI en verde), el avance de HU de punta a punta, el release por GitHub Actions y los procesos concurrentes | ADRs 0001–0084, `skills/`, código | Material listo, falta redactar | Diagramas y figuras (§ 7); actualizar con los ADR 0071–0084 |
| **5.1 Pruebas** | Cómo se probó: corridas, repeticiones, evaluación ciega | § 2 | Por ejecutar | Correr E1–E4 |
| **5.2 Resultados** | Tablas y gráficas por escenario y por skill; comparación Claude vs. Gemini; casos ilustrativos; **defectos que la revisión no detecta y que aparecen al ejecutar** (registro de hallazgos), autonomía (intervenciones manuales) | § 2.5, § 3–4; registro de hallazgos | Parcial (E1c, segunda etapa) | Repetir desde cero con la plataforma congelada; datos de E1/E3/E4 |
| 6.1 Conclusiones | Respuesta a preguntas e hipótesis | — | Pendiente | Resultados |
| 6.2 Recomendaciones | Para quien adopte el enfoque | — | Pendiente | — |
| 6.3 Trabajos futuros | Diagnóstico brownfield, más proveedores/fuentes, **adaptadores de proveedor de código (GitLab) y de despliegue**, compuerta de arranque contra una base real, pruebas de integración con Testcontainers en la compuerta, protección de rama en GitHub, Terraform como IaC, persistencia y reanudación de procesos, subtareas en Jira y creación de incidencias en Jira, gestor de secretos | Pendientes de los ADRs 0071–0084 | Base lista | — |
| Referencias | Estilo por definir (ver decisiones) | — | Pendiente | Elegir formato |
| Anexos A–… | A: ADRs; B: fichas de skills; C: prompts de cada skill; D: ejemplo completo de una HU (spec, TCs, paquetes, PR, revisión); E: rúbricas; F: capturas de la plataforma; G: datos crudos de los escenarios; H: manual de instalación (README) | Repo | Parcial | Curar y numerar |

---

## 6. Estado del arte (búsqueda a realizar)

> Todo lo siguiente son **candidatos a investigar y verificar**: no se afirma nada de ellos hasta leer sus fuentes.

**Criterios para la tabla comparativa (cap. 3.2):** entrada (¿parte de la HU o solo del código?), cobertura del ciclo (TCs, arquitectura, código,
revisión, validación), contexto usado en la revisión, generaliza a otros repos, soporta varios proveedores de IA, evidencia/trazabilidad, ejecución de
pruebas, modo brownfield, licencia/costo.

| Categoría | Candidatos a revisar |
|---|---|
| Asistentes/agentes de código | GitHub Copilot (agente y code review), Claude Code, Cursor, Devin, Sweep, Aider, OpenHands |
| Revisión de código con IA | CodeRabbit, Qodo (Codium) PR-Agent, revisión automática de GitHub y GitLab |
| Desarrollo dirigido por especificaciones | GitHub Spec Kit, Kiro (AWS), OpenSpec |
| Agentes multi-rol de investigación | MetaGPT, ChatDev, AutoGen, SWE-agent, AutoCodeRover |
| Benchmarks y evaluación | SWE-bench, HumanEval/MBPP (para contrastar qué miden y qué no) |
| Generación de pruebas con LLM | Estudios sobre generación de pruebas desde requisitos/criterios de aceptación |
| Revisión de código y calidad | Literatura sobre revisión automática de código y su relevancia percibida |

Búsqueda sugerida: IEEE Xplore, ACM DL, arXiv, Google Scholar; cadenas como "LLM agents software development lifecycle", "user story to test cases LLM",
"automated code review LLM", "spec-driven development". Objetivo: **≥ 15 trabajos relacionados**, media cuartilla cada uno.

---

## 7. Inventario de figuras, tablas y gráficas

Numeración por capítulo (Figura 4.1, Tabla 5.2…). Fuente: diagramas existentes en `itz/arquitectura/diagramas/` (Mermaid) y capturas de la plataforma.

| Id | Título | Capítulo | Origen |
|---|---|---|---|
| F 2.1 | Ciclo de vida del desarrollo con IA (contexto) | 2 | Nuevo |
| F 4.1 | Flujo del pipeline HU → PR revisado | 4 | `diagramas/01-…` |
| F 4.2 | Skills del orquestador por fase | 4 | `diagramas/02-…` |
| F 4.3 | Arquitectura de Loom (backend, frontend, Mongo, repo de control, GitHub, proveedores de IA) | 4 | Nuevo |
| F 4.4 | Modelo de datos (Proyecto, HU, TC, Paquete, Observación) | 4 | Nuevo |
| F 4.5 | Ciclo del paquete: pendiente → PR → revisión → corrección → fusionado | 4 | Nuevo |
| F 4.6–4.9 | Pantallas: alta guiada, ruta del proyecto, paquetes, panel de actividad, revisión | 4/5 | Capturas |
| T 3.1 | Comparativa de herramientas y trabajos relacionados | 3 | § 6 |
| T 4.1 | Fases, skills, entradas y salidas | 4 | `skills/` |
| T 4.2 | Catálogo de casos de uso | 4 | § 4.2 |
| T 4.3 | Métricas y cómo se miden | 4 | § 3 |
| T 5.1 | Descripción de los escenarios E1–E4 | 5 | § 4.3 |
| T 5.2 | Resultados de TCs y cobertura de criterios | 5 | Datos |
| T 5.3 | Resultados de arquitectura/paquetes | 5 | Datos |
| T 5.4 | Resultados de generación y revisión de código por proveedor | 5 | Datos |
| T 5.5 | Tiempo, tokens y costo por skill y proveedor | 5 | Datos (instrumentación) |
| G 5.1–5.n | Barras/cajas de las métricas por proveedor y proyecto | 5 | Datos |

Símbolos y abreviaturas (la guía pide relación con ≥ 10 elementos): HU, TC, PR, ADR, SDD, TDD, LLM, CI/CD, MCP, PAT, E2E, GCP, SSE, RBAC.

---

## 8. Cumplimiento de los objetivos específicos (honestidad necesaria)

| Obj. | Tema | Estado hoy | Acción |
|---|---|---|---|
| 1 | Modelo de Proyecto y fuente pluggable | Fuentes de HUs implementadas (Jira y Markdown, ADR-0058); GitHub como fuente no. **El proveedor de código es solo GitHub** (PR, checks, fusión, despliegue): con GitLab hace falta un adaptador (ADR-0081) | Decidir si se implementa GitHub como fuente o se acota; declarar el alcance por proveedor |
| 2 | Análisis de HU y generación de TCs | Implementado (skills 01–02) | Medir (experimento A) |
| 3 | Diagnóstico de avance existente | Implementado (skill 03, ADR-0060) | Correr en ITZ Inventarios / IAT y medir aciertos contra revisión manual |
| 4 | Arquitectura y descomposición | Implementado (skills 04–05) | Medir |
| 5 | Generación de código y PRs | Implementado (skill 06) con compuerta de compilación, lint y pruebas antes de subir (ADR-0070 y 0079) | Medir; el código generado falló al ejecutarse (registro de hallazgos) |
| 6 | Revisión de código y ciclo de observaciones | Implementado (skill 07); **rondas automáticas implementadas** dentro de «Avanzar con esta HU» (ADR-0074): corregir hasta N rondas, esperar el CI y fusionar solo con los checks en verde (ADR-0076) | Medir rondas y observaciones que quedan abiertas |
| 7 | Ejecución de TCs con Playwright | Implementado (skill 08, ADR-0059) y **ejecutado sobre HU-001** (13 de 19 pasan, 6 bloqueados); el diagnóstico (skill 03) no se ha corrido | Correr en HU-002 y HU-003; resolver los bloqueados |
| 8 | Fallo → fix | Implementado (skill 09, ADR-0061); **no se ha ejercitado**: el smoke de HU-001 no dejó fallas de la aplicación, solo casos bloqueados | Correr el ciclo completo con fallas reales y medir rondas hasta que el TC pasa |
| 9 | Indexación multi-repo (solo diseño) | Documentado a nivel de diseño (ADR-0002, 0018) | Redactar |
| 10 | Validar en 2–3 proyectos, greenfield y con avance previo, variando fuente | Jira en 2 proyectos; ambos greenfield probablemente | Ver decisiones 1 y 2 |
| 11 | Medir por HU | Parcial: hay métricas por corrida y skill, historial de procesos con inicio y fin (ADR-0084) y resultados de smoke; falta costo por HU completa y resultado de CI por paquete | § 3.2 |

**Aportes no previstos en los objetivos originales** (a describir en el capítulo 4.2 y a reportar como alcance ampliado): despliegue a GCP con base de datos y secretos, release automático por
GitHub Actions con identidad federada, compuertas de ejecución previas al push, corrección con el log del CI, decisiones de negocio sobre los supuestos, procesos concurrentes con reglas de
exclusión, historial y cancelación de procesos. Ninguno estaba en los 11 objetivos: si no se documentan como limitación de tiempo, pueden leerse como desviación.

Si se decide **acotar** (recomendado por tiempo), se documenta con un ADR nuevo que reemplace/ajuste el alcance de `00-vision-general.md` (los ADRs no se
editan) y la tesis reporta esos puntos como limitaciones y trabajo futuro en lugar de resultados.

---

## 9. Orden de trabajo sugerido

1. **Cerrar decisiones abiertas** (sección 10).
2. **Instrumentar métricas** (§ 3.2) — antes de correr los escenarios, para no repetirlos.
3. **Congelar y capturar** los backlogs de P1 y P2; preparar un repositorio destino por escenario. **Repetir el ejercicio desde cero** con la plataforma congelada cuando el proyecto
   experimento funcione de punta a punta (decisión del 2026-09-20): esa repetición es la que aporta los resultados válidos; la segunda etapa actual es de depuración.
4. **Correr E1–E4** (fases 1–3) y, en paralelo, redactar lo que no depende de datos:
   caps. 1 y 2, 4.2 (metodología implementada) y anexos A–C.
5. **Búsqueda bibliográfica** y cap. 3 (estado del arte y tabla comparativa).
6. **Evaluación humana** ciega con las rúbricas y experimento C (solo diff vs. contexto).
7. **Capítulo 5** con datos, tablas y gráficas; luego conclusiones.
8. **Resumen/Abstract, introducción, índices**, revisión de formato (Arial, márgenes, rótulos) y entrega (2 impresas + 5 digitales).

Recomendación de redacción: escribir en el formato final desde el inicio (plantilla `.docx` con estilos de la guía) y usar los anexos para todo lo que
pase de las 150 cuartillas.

---

## 10. Decisiones abiertas (necesito tu respuesta)

1. **Alcance de objetivos 3, 7 y 8** (diagnóstico, smoke testing, fixes): ¿se implementan o se pasan a trabajo futuro y se acotan los objetivos?
2. **Proyectos:** ¿P2 (IAT) es greenfield o ya tiene código? ¿Hay un tercer proyecto con avance previo y fuente distinta (Markdown/GitHub) para cubrir el objetivo 10?
3. **Experimento C** (revisión solo con diff vs. con contexto): ¿se incluye? Es lo que sostiene H1; implica una variante de la skill 07 que solo reciba el diff.
4. **Quién evalúa** relevancia de observaciones y suficiencia de TCs (tú, tu director u otra persona) y cuántas muestras es viable calificar.
5. **Estilo de citas y referencias:** el flujo de redacción asume **IEEE** (numérico, por orden de aparición; lo fija la skill `redaccion-academica`). Confirmarlo con el director y con las dos tesis de referencia.
6. **Título definitivo y director**, y si la tesis se presenta como Loom o Telar.
7. **Fecha objetivo** de entrega, para dimensionar cuántas repeticiones y cuántos paquetes se pueden evaluar.
8. **Costos:** presupuesto de API para las corridas y repeticiones (E1–E4 con 63 paquetes cada una es una cantidad relevante de tokens).
9. **Alcance por proveedor de código:** ¿se declara que el piloto valida solo GitHub (recomendado) o se construye el adaptador de GitLab? (ADR-0081).
10. **Qué cuenta como intervención manual** en la medición de autonomía (un PR de arreglo, una decisión de negocio, un reinicio, un `repair`): definirlo antes de repetir el ejercicio.
11. **Protección de la rama base en GitHub:** exige GitHub Pro (o repositorio público); hasta entonces solo Loom impide fusionar en rojo, no un clic directo en GitHub.
12. **Costos de nube** del ambiente de pruebas (Cloud SQL por hora, Cloud Run): ¿se apaga entre sesiones y se reporta el costo aparte del de IA?
13. **Declaración del uso de IA en la redacción:** el borrador de la tesis se apoya en asistentes de IA. ¿El programa exige declararlo y en qué forma (nota metodológica, agradecimientos, anexo)? Confirmarlo con el director **antes** de redactar, porque cambia cómo se documenta el proceso.
14. **Voz y persona gramatical** (impersonal, primera persona del plural o del singular): tomar una muestra de 2 a 3 párrafos de la tesis de referencia y fijarla. Es la base para la pasada de humanización (§ 13).

## 11. Riesgos

| Riesgo | Efecto | Mitigación |
|---|---|---|
| Modelos de IA cambian o se retiran (ya ocurrió con Gemini 2.5) | Resultados no reproducibles | Registrar modelo y fecha; congelar la corrida; guardar todos los artefactos |
| No determinismo | Diferencias por azar | Repeticiones y reporte de varianza |
| Falta de instrumentación | Sin datos de tiempo/costo | Hacerlo antes de correr |
| Código sin ejecutar | Resultados de "calidad" sobrestimados | Experimento E con CI/ejecución manual |
| Sesgo del evaluador | Comparación poco creíble | Evaluación ciega y rúbrica escrita |
| Los proyectos son propios/de prueba | Validez externa limitada | Declararlo en limitaciones; añadir un proyecto de otro dominio |
| Alcance mayor al tiempo disponible | Tesis incompleta | Acotar objetivos con un ADR (§ 8); la segunda etapa ya amplió la plataforma más allá de los 11 objetivos |
| Las intervenciones manuales del tesista contaminan la medición de autonomía | Se sobrestima lo que Loom resuelve solo | Registrar cada intervención (hallazgos § D) y repetir el ejercicio desde cero sin ellas |
| Defectos que la revisión no ve y que aparecen al ejecutar (migraciones, arranque, CI) | «Código revisado» no significa «código que funciona» | Compuertas de ejecución (ADR-0070, 0079) y, pendiente, la de arranque (ADR-0071); reportarlo como resultado |
| Dependencia de servicios externos y de cuenta (GitHub, GCP, la sesión del CLI de Claude) | Corridas que fallan por el entorno y no por la plataforma | Registrar la causa de cada fallo (entorno vs. plataforma vs. código generado) |
| Evolución rápida de la plataforma durante el piloto | La plataforma no es la misma entre corridas | Congelar la versión (commit) antes de repetir; registrar la versión por corrida (§ 3.2) |

---

## 12. Cómo se llena cada sección que no es de resultados

Revisión del `Loom - Tesis.docx` (copia de trabajo, 2026-09-21; **ver § 14 para el estado de v01 y v02**): de sus 33 controles de contenido, **solo 5.1 y 5.2 tienen texto redactado**; el índice se genera solo y los anexos son marcadores («Pendiente de integrar»); los otros 29 siguen con la guía original de la plantilla.
El capítulo 5 ya redactado corresponde a la **primera** etapa del piloto (E2 y E1c) y se reescribirá con los resultados de la repetición desde cero (por eso se deja fuera de este
apartado). Presupuesto total: **80–150 cuartillas**; con el reparto de abajo se llega a unas **105** sin anexos.

**Regla común a todas las secciones:** cada afirmación sobre Loom cita un artefacto del repositorio (ADR, especificación de skill, código, evidencia); cada afirmación sobre el mundo exterior
cita una fuente `[N]` verificada o queda marcada `[CITA PENDIENTE]`; cada cifra sale de la tabla de trazabilidad (§ 13, paso 5). Nada se rellena con autores, años o cifras plausibles.

| Sección | Cuartillas | Qué lleva | Fuente en el repositorio | Cómo se redacta | Depende de resultados | Qué no se puede afirmar |
|---|---|---|---|---|---|---|
| Resumen y *Abstract* | 1 y 0.5 | Objetivo, método, resultados clave, conclusiones; sin abreviaturas ni citas | Se escribe con 5 y 6 terminados | Último paso; el *Abstract* se traduce y se revisa por separado | **Sí** | Cualquier resultado que no esté en el capítulo 5 |
| Introducción | 3 | Área, razones y resumen de capítulos | `00-vision-general.md`, propuesta aprobada | Después de los capítulos 1 a 4; empieza por el objeto de estudio, sin historia de la computación | Parcial | Promesas que la plataforma no cumple (§ 8) |
| 1.1 Descripción del problema | 2 | Problema delimitado, en forma de pregunta, con literatura | § 1 de este plan; registro de hallazgos (el código revisado que no arranca) | Del problema general al caso concreto: HU a código verificado; un párrafo con evidencia propia | No | Estadísticas de la industria sin fuente |
| 1.2 Preguntas de investigación | 1 | Contexto explícito, generalización, proveedor | § 1–2 | Una pregunta por párrafo, numeradas | No | Preguntas que los experimentos no pueden contestar |
| 1.3 Objetivos | 1.5 | General y específicos | `00-vision-general.md` y § 8 | Se ajustan a lo implementado; el recorte se documenta con un ADR nuevo, no editando los anteriores | No | Objetivos «logrados» sin medición |
| 1.4 Justificación | 2 | Beneficiarios, utilidad, costo de no hacerlo | Propuesta aprobada | Argumento con datos externos citados | No | Cifras de productividad o costo sin fuente (hoy no hay ninguna verificada) |
| 1.5 Alcances y limitaciones | 2 | Dentro y fuera de alcance | Visión general, § 8, ADR-0081 | Lista corta y honesta: proveedor de código solo GitHub, un usuario, ejecución local, seguridad de pruebas, proyectos propios | No | Generalidad que el piloto no probó |
| 1.6–1.7 Hipótesis y variables | 2 | H1–H3, variables independientes y dependientes | § 1 | Solo hipótesis medibles con los datos que se van a tener (§ 3) | Sí (cierre) | Hipótesis sin instrumento |
| **2 Marco teórico** | 18–22 | LLM y agentes con herramientas, ingeniería dirigida por especificaciones, historias de usuario y criterios, pruebas (TDD, E2E), revisión de código, CI/CD y contenedores, ADR | Ninguna: es literatura | Cada concepto: definición formal `[N]`, y una oración que lo vincula con Loom. Se arma primero la lista de referencias verificadas y después el texto | No | Definiciones de memoria: se citan o se marcan |
| **3.1 Trabajos relacionados** | 8–10 | Media cuartilla por trabajo | Búsqueda documentada (§ 6) | Ficha por trabajo con problema, método, resultado y limitación; solo se afirma lo que dice la fuente primaria | No | Capacidades de herramientas comerciales tomadas de mercadeo |
| 3.2 Análisis comparativo | 3–4 | Tabla de criterios contra Loom | § 6 | Criterios fijados antes de llenar la tabla; cada celda con su fuente y su fecha de consulta | No | Ventajas de Loom no medidas |
| **4.1 Metodología de solución** | 8 | Diseño de la investigación, muestra, instrumentos, validez y confiabilidad, ética de datos | § 2–3, decisiones 1–14 | Describir el diseño **real**: etapa de depuración y repetición con la plataforma congelada; datos de terceros generalizados (`CLAUDE.md`) | No | Aleatorización o repeticiones que no se harán |
| **4.2 Metodología implementada** | 18–22 | Arquitectura, fases y skills, modelo de datos, compuertas, revisión, despliegue, concurrencia y procesos | ADR 0001–0084, `skills/00–10`, `diagramas/`, `pantallas-plataforma-telar.md`, código | Una subsección por skill con su especificación; las decisiones se citan por número de ADR (lista completa en el anexo A); figuras de los diagramas Mermaid | Parcial (versión congelada) | Funciones que no se han ejercitado (diagnóstico, fixes, compuerta de arranque) |
| 6.1 Conclusiones | 3 | Respuesta a preguntas e hipótesis | Capítulo 5 | Una conclusión por pregunta, con la cifra que la sostiene | **Sí** | Nada fuera de lo medido |
| 6.2 Recomendaciones | 1.5 | Para quien adopte el enfoque | Registro de hallazgos | Derivadas de los defectos y de lo que la plataforma ya corrige | Parcial | Recomendaciones sin evidencia propia |
| 6.3 Trabajos futuros | 1.5 | Lo pendiente y lo acotado | Pendientes de los ADR 0071–0084, § 8 | Lista priorizada con motivo | No | — |
| Referencias | — | Lista IEEE por orden de aparición | Se arma mientras se redacta | Un archivo de trabajo con cada referencia y su estado (verificada / pendiente) | No | Referencias con datos inventados |

**Anexos** (fuera del conteo): A) índice de ADR (se genera de `decisiones/`, sin redactar a mano); B) fichas de skills (de `skills/`); C) prompts de cada skill (se extraen del código, no se transcriben);
D) **ejemplo completo de una HU** (HU-001: especificación, casos de prueba, paquetes, PR, rondas de revisión, informe de smoke; ya existe la evidencia); E) rúbricas; F) capturas
(tomarlas al final, con la interfaz ya rediseñada); G) datos crudos; H) manual de instalación.

**Orden recomendado para las secciones sin datos:** 4.2 (hay material completo), 1.5 y 1.3 (se ajustan con § 8), 4.1, 1.1–1.2 y 1.6–1.7, 2 y 3 (necesitan la bibliografía), anexos A–D; y al final introducción, resumen, conclusiones.

## 13. Flujo de redacción y estilo

Las skills disponibles y para qué sirve cada una en esta tesis:

| Skill | Sirve para | Límite |
|---|---|---|
| `redaccion-academica` (del repositorio) | Estilo técnico-académico en español: variar la longitud de las oraciones, quitar muletillas, anclar cada generalidad en un término exacto y dejar la cita lista en IEEE (`[N]`) | No inventa citas ni datos; deja `[CITA PENDIENTE]` |
| `humanizer` | Quitar los rasgos de texto generado por IA (contraste «no es X sino Y», cierres de una línea, tríadas forzadas, guiones por todas partes, inflación de importancia, negritas decorativas) sin cambiar lo que dice | Sus listas de palabras están en inglés: los patrones estructurales valen en español, las palabras hay que traducirlas (lista abajo). Con una muestra de escritura, la muestra manda sobre sus reglas |
| `writing-guidelines` (Vercel) | Guía de estilo para documentación de producto en inglés, consultada por internet | **No aplica a la tesis** (idioma y género distintos); solo serviría para el `README` del repositorio |

**Pasos por sección (en este orden):**

1. **Ficha de sección:** objetivo, extensión (§ 12), fuentes del repositorio, cifras permitidas con su origen y lo que no se puede afirmar. Es lo que evita redactar de memoria.
2. **Borrador desde las fuentes:** viñetas a prosa, en la copia de trabajo `Loom - Tesis.docx` (control de cambios activo, nunca en la guía original). Cada dato lleva su fuente entre corchetes hasta el paso 5.
3. **Pasada `redaccion-academica`:** ritmo del párrafo, muletillas, anclaje técnico, citas `[N]`. Devuelve dos listas: citas pendientes y generalidades sin evidencia (se resuelven con el autor, no se rellenan).
4. **Pasada `humanizer`:** con la muestra de voz de la tesis de referencia (decisión 14); texto técnico, así que **neutro y sin opiniones agregadas**; en modo archivo solo cambia prosa (no toca datos, rutas, código ni nombres de ADR).
5. **Verificación de cifras y citas:** cada número se contrasta con su fuente en una tabla de trazabilidad (`trazabilidad-de-cifras.md`, por crear: cifra, valor, archivo o colección, fecha de la corrida). Cada `[N]` se resuelve o se deja como pendiente visible.
6. **Formato:** estilos de título y rótulo de la guía (Arial 12, márgenes, interlineado, rótulos de figuras y tablas con número de capítulo) para que los índices se generen solos.
7. **Revisión del director** por capítulo, no al final.

**Rasgos de IA a vigilar en español** (adaptación de la lista del `humanizer`): «es importante destacar/señalar», «cabe mencionar», «en el panorama actual», «en un mundo cada vez más…», «juega un papel fundamental/clave/crucial»,
«no solo… sino también» y «no es X, es Y», «un abanico de», «sin lugar a dudas», «robusto», «holístico», «sinergia», «revolucionar», cierres de párrafo que repiten la idea («En definitiva…», «En resumen…»),
tríadas de adjetivos o sustantivos por costumbre, guion largo como conector universal (en este repositorio abunda; en la tesis se usa con medida), negritas y encabezados decorativos, y párrafos que anuncian lo que van a decir.

**Dos cuidados propios de esta tesis**

- **Coherencia entre lo que se afirma y lo que se implementó:** los ADR y el plan usan «implementado» con cautela; en la tesis, una función solo se describe como resultado si se ejercitó (§ 8). Lo demás va como diseño o trabajo futuro.
- **Trazabilidad del proceso de redacción:** como la tesis trata de asistentes de IA, conviene guardar qué partes se redactaron con apoyo de IA y qué revisó el autor (decisión 13).

## 14. Revisión del estado de la tesis (2026-09-27)

Revisión de `Loom - Tesis v01.docx` contra la guía (`GUIA PARA ESTRUCTURA DE TESIS.docx`), este plan y los dos registros de hallazgos. La guía pide los mismos 33 controles que tiene la copia de trabajo (portada, oficio, agradecimientos, símbolos, resumen, *abstract*, introducción, capítulos 1 a 6, referencias y anexos): **la estructura está completa**; lo que falta es contenido y actualización.

### 14.1 Qué ya está (v01)

| Sección | Palabras (≈ cuartillas) | Meta (§ 12) | Estado |
|---|---|---|---|
| Símbolos y abreviaturas | 114 | — | Listo |
| Introducción | 540 (≈ 2) | 3 | Borrador completo |
| 1.1 a 1.7 | 1,686 (≈ 6) | ≈ 11.5 | Borrador completo; 1.5 no menciona el segundo stack |
| 2 Marco teórico | 1,292 (≈ 4.6) | 18–22 | **Muy corto** |
| 3.1 Trabajos relacionados | 631 (≈ 2.3) | 8–10 | **Corto**; falta el protocolo de búsqueda |
| 3.2 Análisis comparativo | 280 (≈ 1) | 3–4 | Corto; celdas «por verificar» |
| 4.1 Metodología de solución | 705 (≈ 2.5) | 8 | Corto; describe la matriz E1–E4 pero no las corridas reales (E1c, E3c) |
| 4.2 Metodología implementada | 2,047 (≈ 7.3) + 4 figuras | 18–22 | Corto; sin ADR-0085 a 0088 |
| 5.1 y 5.2 Resultados | 2,179 (≈ 7.8) + 2 gráficas | — | Solo E1c |
| 6.1 a 6.3 | 1,731 (≈ 6.2) | 6 | Escritos sobre E1c |
| Referencias | 31 en IEEE | — | 3 por completar (volumen/páginas) |
| Anexos | A (ADR), B (skills), C (recorrido E1c, 33 figuras) | — | D a H pendientes |

Total ≈ 15,900 palabras con anexos (≈ 56 cuartillas); **sin anexos ≈ 45 cuartillas**, contra el mínimo de 80 de la guía.

### 14.2 Qué falta

1. **Datos del autor**: título definitivo, nombre, director, fecha (portada y oficio); agradecimientos.
2. **Resumen y *Abstract***: se escriben al final.
3. **Volumen**: capítulo 2 (+14 cuartillas), 3.1 (+6), 4.1 (+5), 4.2 (+10). Sin esto no se llega a 80.
4. **Resultados de la matriz E1–E4 con API**: bloqueados por saldo (Anthropic) y facturación (Gemini).
5. **Experimento C** (revisión solo con el *diff*) y **evaluación ciega** de observaciones: sin ellos H1 no se puede contestar. **Avance 2026-09-28:** el experimento C ya se corrió (ADR-0089, 29 PRs, 85 frente a 92 observaciones); falta la calificación ciega por una persona.
6. **Trazabilidad de cifras** (`trazabilidad-de-cifras.md`, § 13 paso 5): no existe.
7. **Anexos D–H**: ejemplo completo de una HU, rúbricas, capturas finales, datos crudos, manual de instalación.
8. **Pasadas de estilo** (`redaccion-academica`, `humanizer`): no se han hecho; decisión 14 (voz) sin fijar.

### 14.3 Observaciones

- **E3c cambia el capítulo 5 y el 6**: aporta la primera evidencia de PI3/H2 (dos dominios, dos stacks) y cuatro hallazgos de generalización. v01 no lo incluye → se crea **v02**.
- **Los pilotos no son la matriz**: E1c y E3c usan el CLI y modelos distintos entre sí; la tesis debe presentarlos como pilotos completos y dejar E1–E4 como diseño cuya ejecución está pendiente (o reformular el diseño si el tiempo no alcanza, con un ADR).
- **La plataforma no está congelada**: cada corrida la cambió (E1c: ADR-0071–0084; E3c: 0085–0088). Es un resultado en sí (ciencia del diseño: el artefacto evoluciona con la evaluación), pero hay que decirlo en 4.1.5.
- **Hallazgo transversal** de los dos pilotos: lo que la revisión de código no ve aparece al ejecutar (E1c: A1–A10; E3c: CI en rojo y 9 fallos de smoke). Sostiene PI5 con dos proyectos.
- **Seguridad del repositorio**: `jcsoto-tech-lead` es público y el hash de la contraseña de prueba del admin quedó en el historial (commit `246065e`); ya está enmascarado en el archivo. **Resuelto el 2026-09-27:** la contraseña de prueba se cambió en las dos aplicaciones desplegadas (inventarios y taller) y en la configuración de Loom; el hash del historial ya no sirve.
- **Decisiones abiertas** (§ 10): resueltas o con avance — 2 (P2 es greenfield), 5 (IEEE en uso), 8 (costo estimado), 10 (lista de intervenciones en los registros). Siguen abiertas: 1, 3, 4, 6, 7, 9, 11, 12, 13 y 14.

### 14.4 Siguiente paso sugerido

1. v02 con E3c en los capítulos 1.5, 4.1, 4.2, 5 y 6 y un anexo D breve (hecho el 2026-09-27; ver § 14.5).
2. Corregir la compuerta de compilación para monorepos (B4 del registro E3c) y fijar el modelo del CLI antes de cualquier corrida nueva.
3. Cerrar con el director las decisiones 3, 4, 6, 7 y 13; con eso se decide si E1–E4 se corren con la API (≈ 100 USD) o si la validación queda en los dos pilotos.
4. Ampliar capítulo 2 y 3.1 (no dependen de resultados) y crear la trazabilidad de cifras.

### 14.5 Cómo se generó `Loom - Tesis v02.docx`

```
cp "Loom - Tesis.docx" "Loom - Tesis v02.docx"
python herramientas/llenar_tesis.py "Loom - Tesis v02.docx" borrador/v02
python herramientas/limpiar_obsoleto.py "Loom - Tesis v02.docx"
```

Cambios respecto a v01 (borradores en `borrador/v02/`):

- **1.5:** la validación se hace sobre dos proyectos de dominios y pilas distintos; el modo con avance previo sigue sin probarse.
- **4.1.2 y 4.1.5:** P2 descrito (agenda de taller, Node + React) y los pilotos E1c/E3c separados de la matriz E1–E4; riesgo de que la plataforma evolucione entre corridas.
- **4.2.8 y 4.2.9:** ADR-0085 a 0088 (proveedor WIF compartido, servicios en `apps/`, `DATABASE_URL` y URL de la API al compilar, rol por actor principal).
- **5.1:** reescrito para las dos corridas (tabla de escenarios con E3/E4 configurados y bloqueados; modelos distintos; plataforma no congelada).
- **5.2.9 a 5.2.14:** corrida E3c, supuestos de Loom que no generalizaron, comparación E1c–E3c (tabla 5.12 y figura 5.3) y lo que no se puede concluir.
- **6.1 a 6.3:** PI1, PI3 (respuesta parcial), PI5 y H2 (evidencia parcial, en contra en su forma estricta), objetivo 10 cumplido en parte, dos recomendaciones y los pendientes del segundo piloto.
- **Anexo D:** 11 pantallas del E3c, sin secretos visibles.

**Limpieza (`limpiar_obsoleto.py`):** la copia de trabajo `Loom - Tesis.docx` tenía, **fuera de los controles de contenido**, el capítulo 5 y los anexos del primer piloto (E2, 2026-09-19) y la referencia de ejemplo de la plantilla («Mapachez itz»). v01 los arrastra (su capítulo 5 muestra el nuevo y el viejo, uno tras otro); en v02 se quitaron 92 párrafos, 20 tablas y 11 imágenes. La copia de trabajo no se modificó.

**Pendiente de formato:** entre secciones siguen los párrafos de instrucciones de la plantilla institucional («En ésta sección se le informa al lector…», reglas de formato, «Es la traducción del Resumen…»). Se conservaron porque vienen de la guía oficial; hay que quitarlos antes de entregar (o al pasar a una copia limpia) y confirmarlo con el director.

### 14.6 `Loom - Tesis v03.docx` (2026-09-28)

Generada igual que v02, desde `borrador/v03/`. Cambios respecto a v02:

- **4.1.7 (nuevo):** diseño del experimento de control de la revisión (ADR-0089): mismos 29 PRs, mismo modelo, contexto reconstruido desde el repositorio de control, calificación ciega con clave fuera del repositorio.
- **5.1.1 y Tabla 5.1:** fila del experimento C; H1 pasa a «calificación pendiente».
- **5.2.14 (nuevo):** Tabla 5.13 con los conteos por condición (85 frente a 92 observaciones), el descarte de la primera ejecución «contexto» (paquete de Mongo con las observaciones del piloto) y los límites del experimento. El antiguo 5.2.14 pasa a 5.2.15.
- **6.1.1, 6.1.2, 6.2 y 6.3:** PI2 y H1 con la comparación de control hecha y la calificación pendiente; recomendación nueva sobre reconstruir entradas desde el historial; séptima línea de trabajo futuro (repeticiones y segunda persona evaluadora).
- **Anexo E:** rúbrica de relevancia de una observación (Tabla E.1).
- **Herramienta:** los subtítulos aplican cursiva.

≈ 18,150 palabras (≈ 65 cuartillas con anexos), 73 leyendas. **Los pendientes concretos de la tesis se llevan desde ahora en [03-pendientes-de-la-tesis.md](03-pendientes-de-la-tesis.md).**

### 14.7 `Loom - Tesis v04.docx` (2026-09-28)

```
cp "Loom - Tesis.docx" "Loom - Tesis v04.docx"
python herramientas/llenar_tesis.py "Loom - Tesis v04.docx" borrador/v04
python herramientas/limpiar_obsoleto.py "Loom - Tesis v04.docx"
python herramientas/marcar_instrucciones.py "Loom - Tesis v04.docx"
```

- **Capítulo 2:** reescrito con estilo humano y ampliado de 1,296 a ≈ 3,100 palabras, con 15 referencias nuevas verificadas (46 citadas en total).
- **4.1.7:** la cita pendiente de las pruebas pareadas se resolvió (Wilcoxon; Arcuri y Briand).
- **Resaltado en amarillo** (paso nuevo): 107 párrafos que parecen instrucción y no texto de la tesis, para quitarlos o sustituirlos antes de entregar.

≈ 20,400 palabras (≈ 73 cuartillas con anexos). Pendientes en [03-pendientes-de-la-tesis.md](03-pendientes-de-la-tesis.md).

**Decisión del autor (2026-09-28):** v04 es la versión de trabajo; los cambios siguientes se hacen sobre `borrador/v04/` y se regenera `Loom - Tesis v04.docx` con los mismos tres comandos, sin crear v05.
- **2026-09-28, sobre v04:** 4.2 ampliada a ≈ 4,500 palabras (descripción de cada *skill*, agente de código, credenciales, cambios en los requisitos, interfaz y Tabla 4.3 de estado de implementación). Total ≈ 22,500 palabras (≈ 80 cuartillas con anexos y referencias, ≈ 65 sin ellos).
- **2026-09-28, sobre v04:** 3.1 reescrita con protocolo de búsqueda y 12 trabajos nuevos verificados (revisión de código con LLM en la industria, SGCR, generación de pruebas desde código y desde historias de usuario, Agentless, OpenHands); tabla 3.1 actualizada. Total ≈ 24,100 palabras (≈ 86 cuartillas con anexos y referencias, ≈ 69 sin ellos); 58 referencias citadas.
- **2026-09-29, sobre v04:** 4.1 reorganizada y ampliada (muestra, relación preguntas-hipótesis-instrumentos, análisis de los datos con tamaño del efecto); total ≈ 24,800 palabras (≈ 89 cuartillas con anexos y referencias, ≈ 72 sin ellos); 59 referencias.
- **2026-09-29, sobre v04:** PI1 calculada (cobertura nominal 110 de 110 criterios; 70 % de los criterios son inferidos) en la nueva 5.2.15, con evidencia en `evidencia/cobertura-pi1/`. Total ≈ 25,300 palabras.
- **2026-09-29, sobre v04:** experimento C evaluado de forma automática por decisión del autor (ADR-0090 y ADR-0091): sin evidencia a favor de H1 (32.9 % frente a 30.4 % de observaciones relevantes; 47 hallazgos relevantes distintos, 9 compartidos). H1 queda sin apoyo y sin declararse rechazada; la calificación por una persona pasa a trabajo futuro. Total ≈ 26,500 palabras.
- **2026-09-29, sobre v04:** resumen y *abstract* escritos; introducción y capítulo 1 ajustados a los resultados. Total ≈ 27,600 palabras (≈ 99 cuartillas con anexos y referencias, ≈ 81 sin ellos): el mínimo de 80 se alcanza.
- **2026-09-30, sobre v04:** pasada de estilo y de exactitud a la introducción y a los capítulos 1, 5 y 6 (el capítulo 6 cita ya las dos corridas y el experimento de control).
- **2026-09-30, sobre v04:** referencias cotejadas (ninguna queda en `revisar`) y trazabilidad de cifras (`trazabilidad-de-cifras.md`, 86 cifras recalculadas desde la evidencia, todas coinciden).
- **2026-10-03, sobre v04:** anexos A a I completos (B, F y G generados con `herramientas/anexos_generados.py`), cita pendiente de 1.4 resuelta, datos de la infraestructura de GCP en 5.2.13 y 1.5. Todo lo que no depende del autor o del director está hecho. Para la revisión con el director: `04-pendientes-para-revision-con-el-director.md` y su versión `Pendientes para revisión con el director.docx`.
