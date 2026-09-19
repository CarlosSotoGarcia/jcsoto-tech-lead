# ADR-0053: Proveedor «Claude (cuenta normal)» para desarrollo, sin API de pago

## Estado

Aceptada. Amplía [ADR-0047](0047-proveedor-de-ia-por-proyecto-claude-o-gemini.md) con un tercer proveedor.

## Contexto

Durante el desarrollo de Loom cada corrida con la API de Claude cuesta por token, y las pruebas repetidas (descomponer 28 HUs, generar
paquetes) se acumulan. La persona ya usa Claude con su cuenta normal (suscripción) en el CLI de Claude Code de su máquina.

## Decisión

1. **Nuevo valor de `proveedor_llm`: `claude_cli`** («Claude (cuenta normal)»). Se elige en el alta y en la configuración del Proyecto, junto a
   Claude (API) y Gemini. Sigue siendo una decisión por Proyecto y no exige `LOOM_ANTHROPIC_API_KEY`.
2. **Análisis.** Las skills de análisis (01, 02, 04, 05, 07) llaman al CLI en modo no interactivo (`claude -p --json-schema`, sin herramientas, con
   un directorio neutro para no cargar ajustes de ningún proyecto) y leen el resultado estructurado.
3. **Agente de código (skills 06 y 07).** El CLI hace su propio ciclo de herramientas dentro del worktree del paquete, con permisos acotados por
   ruta: solo leer/escribir/editar dentro del repositorio (`./**`), sin shell, red ni subagentes. La compuerta de pruebas y la de archivos
   obligatorios (README y compose, ADR-0050) se comprueban después mirando `git status` del worktree, pidiendo al agente que los complete
   (hasta 2 veces). No hay «notas para el revisor» del agente: el resumen final del CLI ocupa su lugar.
4. **Sin cobro por API.** Al lanzar el CLI se quitan `ANTHROPIC_API_KEY` y `ANTHROPIC_AUTH_TOKEN` del entorno para que use la sesión iniciada y no
   facture por API. El proveedor solo se puede elegir si el CLI está instalado (`GET /catalogo/llm` informa `claude_cli`).
5. **Configuración.** `LOOM_CLAUDE_CLI_PATH` (ejecutable; en Windows se usa el binario nativo, no el shim `.cmd`) y `LOOM_CLAUDE_CLI_MODEL`.

## Consecuencias

- **Solo desarrollo local:** exige sesión iniciada en `claude` en la máquina que corre el backend; no sirve en un servidor compartido.
- Consume el cupo de la suscripción y cada llamada arranca un proceso (más lento que la API).
- **No usarlo para los experimentos de la tesis:** no da tokens, tiempo ni costo comparables ni reproducibles. Esos experimentos (Claude vs.
  Gemini) deben correrse con la API (ver `itz/tesis/00-plan-de-llenado-de-tesis.md`).
- Un hallazgo de diseño: en el modo `acceptEdits` el CLI escribió fuera del directorio de trabajo; por eso se usan reglas de permiso por ruta en
  lugar de ese modo. Verificado con un intento de escribir `../archivo`: quedó denegado.

## Pendiente

- Registrar tokens/tiempo cuando el CLI los informe (`usage` en su salida JSON) para la instrumentación de métricas.
- Reintentar con espera cuando el CLI devuelva un límite de uso.
