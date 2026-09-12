# Documentación de arquitectura — proyecto de tesis

Carpeta para documentar el diseño de la solución del proyecto de tesis aprobado por los asesores:
**Skill + infraestructura para automatizar revisión de código y pruebas a partir de historias de
usuario y prototipos** (ver la propuesta completa en
[`../documentación/propuesta-tesis-idea-elegida.pdf`](../documentación/propuesta-tesis-idea-elegida.pdf)).

Esta carpeta es la fuente viva del diseño: la propuesta en `documentación/` describe el *qué* y el
*por qué* a nivel de anteproyecto; aquí se documenta el *cómo*, y se espera que evolucione conforme
avanza la implementación.

## Estructura

- [`00-vision-general.md`](00-vision-general.md) — problema, objetivo y alcance vigentes, como punto de
  entrada rápido sin tener que releer la propuesta completa.
- [`decisiones/`](decisiones/) — Architecture Decision Records (ADRs). Una decisión de arquitectura por
  archivo, numeradas secuencialmente (`0001-...md`, `0002-...md`). Formato: Título, Estado, Contexto,
  Decisión, Consecuencias. Una decisión ya tomada no se reescribe: si cambia, se abre un ADR nuevo que
  la supera y se marca la anterior como "Reemplazada por ADR-000N".
- [`diagramas/`](diagramas/) — diagramas de arquitectura en Mermaid dentro de Markdown, para que se
  puedan versionar y editar como texto en vez de mantener imágenes estáticas.

## Convenciones

- Igual que el resto del repositorio, todo en español.
- Nada de nombres de un empleador específico ni de sus métricas — el tema de tesis se generalizó a
  propósito para no depender de autorización de datos de terceros (ver
  [`../../CLAUDE.md`](../../CLAUDE.md)); mantener esa misma disciplina aquí.
- Cada ADR y cada diagrama debe poder entenderse sin haber leído el anterior — son documentos de
  referencia, no una narrativa lineal.
