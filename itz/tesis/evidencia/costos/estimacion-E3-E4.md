# Estimación de costo — escenarios E3 (Claude API) y E4 (Gemini API) de ITZ Agenda Taller

Fecha: 2026-09-27. Fuente: colección `metricas` de Loom (llamadas al modelo con tokens y costo) de las corridas E1c, E2 y E3c, y precios de `LOOM_PRECIOS_MODELOS`. Se reproduce con `estimar_costos.py`; los datos quedan en `datos-costos.json`.

## Datos medidos

| Corrida | Proyecto / proveedor | Modelo | Paquetes fusionados | Llamadas | Tokens entrada | Tokens salida | Tokens de caché | Costo (USD) |
|---|---|---|---|---|---|---|---|---|
| E1c (2026-09-21) | Inventarios, Claude por CLI | claude-sonnet-5 | 12 | 128 | 2.15 M | 0.52 M | 14.6 M | 16.67 (nocional) |
| E2 (2026-09-19, parcial) | Inventarios, Gemini API | gemini-3.6-flash + gemini-pro-latest | 5 de 10 | 113 | 1.18 M | 0.06 M | 0.57 M | 4.77 |
| E3c (2026-09-26/27) | Agenda Taller, Claude por CLI | claude-opus-5-5 + claude-haiku-4-5 | 17 | 532 | 7.03 M | 2.03 M | 113.2 M | 120.99 (nocional) |

Valores de E3c actualizados al cierre de la corrida (2026-09-27 15:00), con sus pruebas de humo completas (tres corridas en la HU-001).

Precios usados (USD por millón de tokens, configurados en Loom): claude-sonnet-5 2.00 entrada / 10.00 salida / 0.20 caché; gemini-3.6-flash 0.75 / 3.75; gemini-pro-latest 2.00 / 12.00. Conviene verificarlos contra las páginas de precios vigentes de cada proveedor antes de citarlos.

## Estimación

| Escenario | Método | Estimación (USD) |
|---|---|---|
| E3 (Claude API, claude-sonnet-5) | Mismo volumen de tokens que E3c, a precio de Sonnet 5 | 57.1 |
| | Costo por paquete de E1c (Sonnet 5) × 17 paquetes | 23.6 |
| **E3, rango** | | **24 – 57** |
| E4 (Gemini API) | Mismo volumen de tokens de entrada y salida que E3c (sin caché), pro para código y flash para análisis | 31.9 |
| | Costo por paquete fusionado de E2 × 17 paquetes | 16.2 |
| **E4, rango** | | **16 – 32** |

Presupuesto sugerido con un 20 % de margen para correcciones, reintentos y pruebas de humo: **E3 ≈ 70 USD de saldo en la API de Anthropic** (el E1 original no pudo correr por «credit balance too low»), **E4 ≈ 40 USD**.

## Supuestos y límites

- **El perfil de tokens cambia con el proveedor.** Con el CLI, Claude Code agrega su propio contexto y reutiliza caché en cada paso del agente (decenas de millones de tokens de caché en E3c); con la API, Loom ejecuta su propio ciclo de herramientas y el volumen de caché no es el mismo. Por eso el método «mismo volumen de tokens» es una cota superior para E3 y el de «escalar E1c» una cota inferior.
- **Gemini usó muchos menos tokens de salida en E2** (0.06 M para 5 paquetes) pero más llamadas de corrección (35 de 113). La cota inferior de E4 asume que se mantiene esa proporción; la superior, que Gemini escriba tanto código como Claude en E3c.
- **E3c no es comparable directamente con E1c:** corrió con Opus 5.5 porque Loom no fija el modelo del CLI (hallazgo en la bitácora de E3c). Para E3 y E4 hay que fijar y registrar los modelos exactos antes de correr.
- **No incluye Google Cloud.** El release usa Cloud Build, Cloud Run (escala a cero), Artifact Registry y la instancia de Cloud SQL `inventarios-db`, que ya existe y se comparte; su costo mensual es fijo y no depende del proveedor de IA.
- El costo que reporta el CLI con una suscripción es nocional: no se cobra por llamada.

## Estado de las APIs al 2026-09-27 (10:30)

Llamada mínima de prueba desde Loom antes de correr E3 y E4:

- **Claude API:** 400 «Your credit balance is too low to access the Anthropic API». Hay que cargar saldo (≈ 70 USD sugeridos) antes de correr E3.
- **Gemini API:** 403 «Lightning dunning decision is deny» para el proyecto de Google 748395755364: la facturación del proyecto está bloqueada por cobro pendiente. Hay que regularizar la cuenta de facturación antes de correr E4.
