# Diagrama — skill orquestador y skills por fase

Componentes según [ADR-0004](../decisiones/0004-flujo-orientado-a-hus-generacion-de-codigo-y-autorrevision.md):
un skill orquestador que sabe en qué fase está cada HU/subtarea y despacha al skill especializado de esa
fase. La configuración de repos y ambiente ([ADR-0005](../decisiones/0005-solucion-configurable-repositorios-y-ambiente-dev.md))
alimenta a los skills que tocan código o el ambiente de desarrollo.

```mermaid
flowchart LR
    CFG["Configuración\nrepos (N back / N front) + URL ambiente dev"]
    ORQ["Skill orquestador\n(estado de la HU/subtarea, decide siguiente fase)"]

    S1["Skill: análisis de HU\n+ generación de TCs"]
    S2["Skill: diseño de arquitectura"]
    S3["Skill: descomposición\nen subtareas"]
    S4["Skill: generación de código"]
    S5["Skill: revisión de código"]
    S6["Skill: smoke testing\n(Playwright)"]
    S7["Skill: generación de fixes"]

    BIT["Bitácora\n(HUs, subtareas, observaciones, evidencia)"]

    CFG --> ORQ
    ORQ --> S1 --> ORQ
    ORQ --> S2 --> ORQ
    ORQ --> S3 --> ORQ
    ORQ --> S4 --> ORQ
    ORQ --> S5 --> ORQ
    ORQ --> S6 --> ORQ
    ORQ --> S7 --> ORQ

    CFG -.repos.-> S4
    CFG -.repos.-> S5
    CFG -.URL ambiente.-> S6

    S1 -.registra.-> BIT
    S3 -.registra.-> BIT
    S5 -.registra.-> BIT
    S6 -.registra.-> BIT
```

## Notas

- El orquestador es el único componente con visión del estado global de una HU; los skills de fase no
  se llaman entre sí directamente, siempre a través del orquestador — esto es lo que le permite
  "reaccionar según la fase en la que va".
- `S7` (generación de fixes) reutiliza `S4` (generación de código) y vuelve a pasar por `S5`; se
  dibujan separados porque el disparador es distinto (un TC fallido vs. una subtarea nueva de la HU).
- Pendiente de ADR: qué framework de agentes implementa esto (Claude Code Skills u otra alternativa) —
  sigue abierto desde `00-vision-general.md`.
