# ADR-0047: Proveedor de IA por Proyecto (Claude o Gemini) para análisis y generación de código

## Estado

Aceptada. Amplía [ADR-0046](0046-skill-06-generacion-de-codigo-agente-con-tdd.md): la IA deja de ser
solo Claude.

## Contexto

Las skills de análisis (01, 02, 04, 05) y el agente de código (06) llamaban directamente a Claude con
una key global del servidor. Se pidió poder elegir la IA al dar de alta un Proyecto y usar Gemini.

## Decisión

1. **El proveedor es un atributo del Proyecto** (`proveedor_llm`: `claude` | `gemini`, por defecto
   `claude`), elegido en el alta (paso «Inteligencia artificial») y editable después.
2. **Una sola configuración por corrida.** Cada ejecución fija el proveedor del Proyecto al iniciar
   (`fijar_llm`, contexto asíncrono); las skills no reciben parámetros nuevos.
3. **Keys.** Claude: `LOOM_ANTHROPIC_API_KEY` (servidor). Gemini: `gemini_api_key` del Proyecto, con
   `LOOM_GEMINI_API_KEY` del servidor como respaldo. La key del Proyecto se guarda tal cual (mismo
   pendiente del gestor de secretos, ADR-0033), nunca se devuelve por la API y vacía al editar conserva
   la guardada.
4. **Modelos.** Análisis: `LOOM_GEMINI_MODEL` (por defecto `gemini-2.5-flash`). Código:
   `LOOM_GEMINI_MODEL_CODIGO` (por defecto `gemini-2.5-pro`).
5. **Adaptación.** El análisis usa function calling forzado (REST) con el esquema del tool convertido al
   subconjunto OpenAPI de Gemini; el agente de código usa el mismo bucle de herramientas con un
   adaptador por proveedor, reenviando el contenido del modelo tal cual (firmas de razonamiento). Se
   conservan las salvaguardas: reintento por truncamiento, reparación de arreglos como texto, sandbox
   de archivos y la compuerta TDD.

## Consecuencias

- Gemini no tiene la misma calidad ni formato garantizado que Claude en salida estructurada y en
  agentes largos: no está evaluado en vivo con este flujo; conviene una corrida de prueba antes de
  usarlo en un Proyecto real.
- Un Proyecto usa un solo proveedor para todas las skills; mezclar (p. ej. análisis con Gemini y código
  con Claude) no está soportado.
- Otros proveedores requieren un adaptador más, no cambios en las skills.

## Pendiente

- Evaluar Gemini de punta a punta (specs, TCs, arquitectura, paquetes, código) y ajustar prompts.
- Elegir proveedor por skill si hace falta.
