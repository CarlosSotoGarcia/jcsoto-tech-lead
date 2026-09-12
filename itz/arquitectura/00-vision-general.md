# Visión general de la solución

> Punto de entrada rápido al diseño. El detalle completo del planteamiento y la justificación original
> está en la propuesta aprobada por los asesores:
> [`../documentación/propuesta-tesis-idea-elegida.pdf`](../documentación/propuesta-tesis-idea-elegida.pdf).
> El objetivo, los objetivos específicos y el alcance de **esta página son los vigentes** y ya
> incorporan los ajustes de diseño posteriores a la aprobación (ver Estado).

## Estado

**Aprobada por los asesores**, con el diseño refinado en varios ADRs desde entonces:

- [ADR-0002](decisiones/0002-alcance-de-infraestructura-diseno-no-despliegue.md) — la infraestructura
  de indexación se documenta a nivel de diseño, no se despliega ni se opera como servicio persistente.
- ~~ADR-0003~~ — código como eje y HUs como contexto secundario. **Reemplazado por ADR-0004.**
- [ADR-0004](decisiones/0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md) — la HU es
  la entrada primaria: el skill genera código a partir de ella, abre PRs, se autorrevisa y valida con
  smoke tests. Este es el diseño vigente.
- [ADR-0005](decisiones/0005-solucion-configurable-repositorios-y-ambiente-dev.md) — la solución es
  configurable por N repositorios (backend/frontend) y una URL de ambiente de desarrollo.
- [ADR-0006](decisiones/0006-smoke-tests-con-playwright-y-bitacora-de-hus.md) — smoke tests con
  Playwright (Python); bitácora de HUs preferentemente en GitHub (parte propuesta, no cerrada).

## Problema

Los enfoques actuales de asistencia por IA en el ciclo de desarrollo suelen automatizar una sola etapa
aislada (solo revisión, o solo generación de pruebas) y operan sobre código ya escrito, sin partir de la
intención de negocio ni cerrar el ciclo hasta la validación funcional real. Falta un flujo que, a partir
de una historia de usuario, cubra de punta a punta: generación de casos de prueba, diseño, desarrollo,
revisión de código, integración y validación funcional contra un ambiente real — de forma agnóstica al
sistema sobre el que se aplique.

## Objetivo general

Diseñar e implementar un sistema de skills de IA que, a partir de una historia de usuario, orqueste todo
el ciclo de desarrollo de una funcionalidad — generación de casos de prueba, diseño de arquitectura,
descomposición en subtareas, generación de código, revisión de código, integración y validación
funcional mediante smoke tests — de forma generalizable a distintos repositorios y sistemas.

## Objetivos específicos

1. Diseñar el mecanismo de análisis de una HU y sus criterios de aceptación para generar casos de
   prueba (TCs) derivados de ellos. *(ADR-0004)*
2. Diseñar el mecanismo de diseño de arquitectura y descomposición de una HU en subtareas a partir de
   los TCs generados. *(ADR-0004)*
3. Implementar el skill de generación de código por subtarea y de apertura de Pull Requests. *(ADR-0004)*
4. Implementar el skill de revisión de código y el ciclo de aplicación de observaciones hasta que un PR
   queda sin pendientes. *(ADR-0004)*
5. Implementar el skill de smoke testing: generación de scripts Playwright (Python) a partir de los TCs
   y ejecución contra el ambiente de desarrollo configurado, con evidencia como salida. *(ADR-0005,
   ADR-0006)*
6. Diseñar el mecanismo de fallo → subtarea de fix, que reintroduce el ciclo de generación y revisión
   de código hasta que los TCs correspondientes pasan. *(ADR-0004)*
7. Diseñar (sin necesidad de desplegar ni operar como servicio persistente) el mecanismo de indexación
   multi-repositorio que da contexto de código a los skills anteriores. *(ADR-0002)*
8. Validar el sistema completo ejecutándolo sobre al menos 2-3 soluciones (conjuntos de repositorios)
   de dominios distintos, cada una con su propia configuración de repos y ambiente de desarrollo.
   *(ADR-0002, ADR-0005)*
9. Medir, por HU procesada: tasa de TCs generados que efectivamente cubren los criterios de aceptación,
   número de rondas de revisión de código hasta aprobación, tasa de éxito de smoke tests por iteración,
   y grado de generalización del sistema entre las soluciones validadas.

## Alcance vigente

**Dentro de alcance:**
- Lectura de una HU con criterios de aceptación y generación de TCs a partir de ellos.
- Diseño de arquitectura y descomposición en subtareas para esa HU.
- Generación de código por subtarea y apertura de PRs.
- Revisión de código automatizada, con ciclo de aplicación de observaciones hasta PR limpio.
- Smoke testing con Playwright (Python) contra un ambiente de desarrollo ya desplegado (externo al
  proyecto), a partir de los TCs generados, con evidencia como salida.
- Generación de subtareas de fix ante TCs fallidos, reentrando al ciclo de código/revisión.
- Documentación del proceso (HUs, subtareas, observaciones, evidencia), preferentemente en GitHub.
- Configuración explícita por solución objetivo: N repositorios (backend/frontend) + URL de ambiente
  de desarrollo.
- Diseño (no despliegue) de un mecanismo de indexación multi-repositorio como soporte de contexto.
- Validación en 2-3 soluciones de dominios distintos (candidatos: proyectos propios ya públicos en
  GitHub; opcionalmente uno de un empleador, sujeto a autorización).

**Fuera de alcance:**
- Reemplazar por completo la revisión humana — el sistema asiste; una persona sigue pudiendo intervenir
  en cualquier fase.
- Optimizar para un lenguaje, framework o stack único; el objetivo es generalizar el enfoque.
- Desplegar y operar infraestructura de indexación multi-repositorio como servicio persistente/productivo
  del propio proyecto de tesis *(ADR-0002)*.
- Desplegar o administrar el ambiente de desarrollo usado para smoke testing — se asume ya existente y
  configurado por quien use el sistema *(ADR-0005)*.

## En discusión ahora (sin confirmar, no todavía un ADR)

Sesión en curso sobre cómo documentar HUs/hallazgos y persistir el estado de fase. Sin JSON — la
dirección acordada hasta ahora es Markdown con front-matter YAML (legible para humanos, parseable por
el orquestador, y con `git log` como auditoría gratis de cada transición de fase), más adoptar
**Spec-Driven Development (SDD)** como metodología para que la generación de código ("vibecoding") se
haga siempre contra una especificación concreta, no un prompt suelto. Mapeo propuesto:

| Artefacto SDD | Fase de ADR-0004 | Contenido |
|---|---|---|
| `spec.md` | Lectura de HU + criterios | HU, escenarios, criterios de aceptación |
| `test-cases.md` | Generación de TCs | TCs derivados de los criterios |
| `plan.md` | Diseño de arquitectura | Plan técnico para esta HU |
| `tasks.md` | Descomposición en subtareas | Lista de subtareas planeadas |
| `subtareas/ST-0N.md` | Desarrollo por subtarea | Seguimiento de ejecución: PR, estado, rondas de revisión |
| `evidencia/*.md` | Smoke testing | Resultado de cada corrida |

**Preguntas abiertas antes de cerrar esto como ADR:**
1. ¿Se confirman estos nombres de archivo y este mapeo SDD, o se ajustan?
2. Esta carpeta por HU — ¿vive dentro de cada repositorio objetivo, o en un repositorio/carpeta de
   control aparte que agrupa todas las HUs de una solución? Relevante porque una HU puede tocar back y
   front a la vez (ADR-0005) y no debería quedar ambiguo o duplicado entre repos.

## Qué falta decidir

Esta sección se vacía a medida que las decisiones se documentan como ADRs en
[`decisiones/`](decisiones/). Pendientes tras ADR-0004/0005/0006, más allá de lo que está en discusión
arriba:

- Qué framework de agentes implementa el skill orquestador y los skills por fase (Claude Code Skills u
  otra alternativa).
- Cómo se representa e indexa el código de un repositorio (AST, embeddings, grep estructurado, etc.).
- Cómo se decide en qué repositorio(s) de la configuración debe generar código una subtarea dada.
- Esquema/formato exacto de la configuración de repos + ambiente dev (ADR-0005).
- Qué subconjunto de TCs se vuelve a correr tras un fix: solo los que fallaron o todos los de la
  subtarea.
