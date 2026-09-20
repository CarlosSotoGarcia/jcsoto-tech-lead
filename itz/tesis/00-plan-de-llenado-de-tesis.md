# Plan de llenado de la tesis (documento de trabajo)

> Inventario de **todo lo que hace falta** para llenar [`GUIA PARA ESTRUCTURA DE TESIS.docx`](GUIA%20PARA%20ESTRUCTURA%20DE%20TESIS.docx)
> con una tesis enfocada en lo que hace **Loom** (el sistema que convierte HUs en código verificado y revisado).
> Modelo de redacción y profundidad: [`../referencias/`](../referencias/) (tesis de Javier García: metodología en 3 fases y
> resultados en 3 secciones, 243 páginas). Este archivo no es la tesis: es el mapa de qué escribir, con qué evidencia y
> qué falta.
>
> Estado: **borrador 1 — 2026-09-19**. Se actualiza conforme se resuelven las decisiones abiertas (sección 10).

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
| **4.2 Metodología implementada** | Fases de Loom (Requerimientos, Diseño, Desarrollo, Implementación), arquitectura, skills, modelo de datos, SDD, TDD, revisión, proveedor de IA | ADRs 0001–0050, `skills/`, código | Material listo, falta redactar | Diagramas y figuras (§ 7) |
| **5.1 Pruebas** | Cómo se probó: corridas, repeticiones, evaluación ciega | § 2 | Por ejecutar | Correr E1–E4 |
| **5.2 Resultados** | Tablas y gráficas por escenario y por skill; comparación Claude vs. Gemini; casos ilustrativos | § 3–4 | Por ejecutar | Datos |
| 6.1 Conclusiones | Respuesta a preguntas e hipótesis | — | Pendiente | Resultados |
| 6.2 Recomendaciones | Para quien adopte el enfoque | — | Pendiente | — |
| 6.3 Trabajos futuros | Diagnóstico brownfield, smoke testing y fixes, más proveedores/fuentes, confirmación de supuestos, CI como evidencia, subtareas en Jira, gestor de secretos | Pendientes de los ADRs | Base lista | — |
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
| 1 | Modelo de Proyecto y fuente pluggable | Implementado (Jira y Markdown, ADR-0058); GitHub no | Decidir si se implementa GitHub o se acota el alcance |
| 2 | Análisis de HU y generación de TCs | Implementado (skills 01–02) | Medir (experimento A) |
| 3 | Diagnóstico de avance existente | Implementado (skill 03, ADR-0060) | Correr en ITZ Inventarios / IAT y medir aciertos contra revisión manual |
| 4 | Arquitectura y descomposición | Implementado (skills 04–05) | Medir |
| 5 | Generación de código y PRs | Implementado (skill 06) | Medir |
| 6 | Revisión de código y ciclo de observaciones | Implementado (skill 07); rondas automáticas no | Medir; decidir si hay rondas automáticas |
| 7 | Ejecución de TCs con Playwright | Implementado (skill 08, ADR-0059); falta el diagnóstico (skill 03) que reutiliza el motor | Correr en los proyectos reales y medir |
| 8 | Fallo → fix | Implementado (skill 09, ADR-0061) | Correr el ciclo completo en los proyectos reales y medir rondas hasta que el TC pasa |
| 9 | Indexación multi-repo (solo diseño) | Documentado a nivel de diseño (ADR-0002, 0018) | Redactar |
| 10 | Validar en 2–3 proyectos, greenfield y con avance previo, variando fuente | Jira en 2 proyectos; ambos greenfield probablemente | Ver decisiones 1 y 2 |
| 11 | Medir por HU | Parcial (falta instrumentación) | § 3.2 |

Si se decide **acotar** (recomendado por tiempo), se documenta con un ADR nuevo que reemplace/ajuste el alcance de `00-vision-general.md` (los ADRs no se
editan) y la tesis reporta esos puntos como limitaciones y trabajo futuro en lugar de resultados.

---

## 9. Orden de trabajo sugerido

1. **Cerrar decisiones abiertas** (sección 10).
2. **Instrumentar métricas** (§ 3.2) — antes de correr los escenarios, para no repetirlos.
3. **Congelar y capturar** los backlogs de P1 y P2; preparar un repositorio destino por escenario.
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
5. **Estilo de citas y referencias** que exige el programa (APA, IEEE…) — revisar las dos tesis de referencia y confirmar con el director.
6. **Título definitivo y director**, y si la tesis se presenta como Loom o Telar.
7. **Fecha objetivo** de entrega, para dimensionar cuántas repeticiones y cuántos paquetes se pueden evaluar.
8. **Costos:** presupuesto de API para las corridas y repeticiones (E1–E4 con 63 paquetes cada una es una cantidad relevante de tokens).

## 11. Riesgos

| Riesgo | Efecto | Mitigación |
|---|---|---|
| Modelos de IA cambian o se retiran (ya ocurrió con Gemini 2.5) | Resultados no reproducibles | Registrar modelo y fecha; congelar la corrida; guardar todos los artefactos |
| No determinismo | Diferencias por azar | Repeticiones y reporte de varianza |
| Falta de instrumentación | Sin datos de tiempo/costo | Hacerlo antes de correr |
| Código sin ejecutar | Resultados de "calidad" sobrestimados | Experimento E con CI/ejecución manual |
| Sesgo del evaluador | Comparación poco creíble | Evaluación ciega y rúbrica escrita |
| Los proyectos son propios/de prueba | Validez externa limitada | Declararlo en limitaciones; añadir un proyecto de otro dominio |
| Alcance mayor al tiempo disponible | Tesis incompleta | Acotar objetivos con un ADR (§ 8) |
