# ADR-0033: Primera implementación de la skill 01 (descubrimiento y análisis de HU) — fuente Jira

## Estado

Aceptada. Documenta la primera pieza del pipeline (no solo de la plataforma) que pasa de diseño a
código real, en el repositorio [`loom`](https://github.com/CarlosSotoGarcia/loom). Resuelve dos
pendientes de [skills/01-descubrimiento-y-especificacion-hu.md](../skills/01-descubrimiento-y-especificacion-hu.md).

## Contexto

Hasta ahora "programar" en `loom/` había sido exclusivamente la plataforma (CRUD de Proyecto,
autenticación, UI) — ninguna de las 9 skills del pipeline tenía código. Para validar que el diseño de
la skill 01 (analista de requerimientos vía LLM, clasificación HU/Actividad, ADR-0026) es viable, hacía
falta implementarla contra una fuente real. Se usó el Proyecto de prueba del propio usuario en Jira
(`jncsoga.atlassian.net`, proyecto `ITZINV`) como caso real.

Esta primera implementación obligó a resolver, en la práctica, dos cosas que el diseño había dejado
abiertas:

1. El mapeo exacto de campos de Jira (resumen, descripción en formato ADF) al contrato de `spec.md`.
2. Dónde vive físicamente el resultado del análisis, dado que la escritura real al repositorio de
   control (ADR-0012) — que implica integración de escritura a Git — todavía no está implementada.

## Decisión

- **Fuente Jira**: se lee vía la REST API v3 de Jira Cloud (`GET /rest/api/3/search`), con Basic Auth
  (correo + API token). La descripción, que Jira devuelve en Atlassian Document Format (ADF, JSON
  anidado), se aplana a texto plano antes de pasarla al análisis — se pierde formato rico
  intencionalmente, ya que el análisis reinterpreta el contenido, no lo transcribe.
- **Análisis vía LLM**: se implementó con la API de Anthropic (Claude), usando **tool-use forzado**
  (`tool_choice`) con un schema fijo (`clasificacion`, `titulo`, `descripcion`,
  `criterios_explicitos`, `criterios_inferidos`, `supuestos`, `notas`) para obtener salida
  estructurada confiable, en vez de pedir JSON libre y parsearlo. El system prompt implementa
  literalmente el rol de "analista de requerimientos senior" descrito en skills/01.
- **Persistencia temporal en MongoDB, no en el repositorio de control**: el `spec.md` completo
  (front-matter + cuerpo) se renderiza como texto y se guarda en una colección `hus` de Mongo, además
  de sus campos estructurados — **no** se escribe todavía al repositorio de control real (ADR-0012).
  Es una simplificación deliberada, no un cambio de diseño: el contrato de `spec.md` se respeta al
  pie de la letra, solo cambia dónde vive mientras no exista integración de escritura a Git.
- **Credenciales de Jira por Proyecto, no globales**: cada Proyecto trae su propia cuenta de Jira
  (correo + API token, capturados en su formulario) — refuerza ADR-0009: la fuente de HUs es
  configuración pluggable *por Proyecto*, no un ajuste único del backend. El API token se guarda tal
  cual (sin gestor de secretos real todavía, mismo pendiente que ADR-0032) pero nunca se vuelve a
  exponer por la API una vez guardado: se trata como un campo de contraseña — el formulario lo deja en
  blanco al editar, y dejarlo en blanco conserva el valor ya guardado. La única credencial global del
  backend es `LOOM_ANTHROPIC_API_KEY`, porque el LLM de análisis es una capacidad de Loom mismo, no
  una credencial de un sistema externo del cliente.
- **Sin re-descubrimiento incremental todavía**: cada corrida de "Descubrir HUs" reprocesa todo el
  backlog de Jira; para no duplicar HUs ya existentes, se empareja por `fuente_ref` (la clave del issue)
  y se sobrescribe el análisis — no hay detección de "solo lo nuevo/modificado" (pendiente original de
  skills/01, sigue abierto).

## Consecuencias

- Valida que el diseño de skill 01 es implementable tal cual está documentado: el contrato de
  `spec.md` (front-matter + secciones) no tuvo que cambiar para acomodar la implementación real.
- Deuda técnica explícita y consciente: cuando se implemente la escritura real al repositorio de
  control, hay que migrar de "leer `hus` en Mongo" a "leer archivos del repo" — los consumidores
  (endpoints, UI) ya están escritos contra el contrato de `HU`/`spec.md`, así que el cambio debería ser
  solo en la capa de persistencia, no en el contrato.
- Fuente `markdown` y `github` (ADR-0009, ADR-0010) siguen sin implementar — `markdown` en particular
  necesita la misma integración de lectura a Git que hace falta para escribir el repositorio de
  control, así que probablemente se resuelvan juntas.
- El uso de tool-use forzado para salida estructurada es el patrón a replicar en las skills siguientes
  que también requieran un LLM con salida confiable (02, 04, 05, 07, 09).

## Pendientes que esta implementación deja abiertos

- Integración de escritura real a Git para el repositorio de control (bloquea fuente `markdown` y el
  cierre de la deuda técnica de persistencia mencionada arriba).
- Re-descubrimiento incremental (detectar HUs nuevas/modificadas sin reprocesar todo el backlog).
- Gestor de secretos real (el API token de Jira se guarda tal cual en Mongo, sin cifrar — comparte el
  mismo pendiente que ADR-0032).
