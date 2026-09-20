# Piloto E2 (Gemini) y E1c (Claude por CLI) — ITZ Control Inventarios — 2026-09-19

Evidencia del piloto acotado que respalda el capítulo 5 de `Loom - Tesis.docx`. Tope de gasto de API: 20 USD (gastados: 4.76 USD estimados).

| Escenario | Estado |
|---|---|
| E1 (P1 + Claude API) | **No ejecutado**: la API de Anthropic respondió 400 «credit balance is too low» (`logs/E1.descubrir.txt`). |
| E1c (P1 + Claude cuenta normal, CLI) | Ejecutado como alternativa exploratoria: fases 1 a 3, 6 de 13 paquetes (BASE/PT-01 a PT-04 y HU-001). Costo nocional 10.02 USD informado por el CLI; no comparable con la API. |
| E2 (P1 + Gemini) | Ejecutado: fases 1 a 3, 5 de 10 paquetes (esqueleto BASE/PT-01 a PT-03 y HU-001 completa). |
| E3, E4 (P2 IAT) | No ejecutados: el proyecto IAT no está configurado. |

Configuración: Loom commit `4f8a12a`; HUs ITZINV-12, 13 y 14; repositorio destino privado `loom-piloto-e2-gemini`; modelos `gemini-3.6-flash` (análisis y revisión) y `gemini-pro-latest` (código).

## Contenido

- `logs/` — eventos SSE completos de cada skill (`E2_<skill>...json`), resumen del ciclo por paquete (`E2_ciclo_resumen.json`, codificado en cp1252) y salida de las pruebas del código generado (`E2.mvn.txt`, `E2.jest.txt`).
- `artefactos/E2/` y `artefactos/E1c/` — los Markdown que produjo Loom en cada escenario: `spec.md` y `test-cases.md` de cada HU, `tasks.md`, y el documento de arquitectura.
- `datos_E2.json` y `datos_E1c.json` — HUs, paquetes y métricas del escenario tal como las devolvió la API. `arbol_E2.txt` — archivos del repositorio generado.
- `capturas/` — pantallas de Loom y gráficas usadas en el capítulo.
- `scripts/` — `fase.py` (una fase por la API) y `ciclo.py` (generar, revisar, corregir una vez y fusionar cada paquete). Usan las variables `LOOM_USER` y `LOOM_PASSWORD`, y un `ids.json` `{"E2": "<id del Proyecto>"}`.

## Cómo repetir E1 (cuando haya saldo en la API de Anthropic)

1. Crear un repositorio privado destino y un Proyecto copiando la configuración del proyecto ITZ Control Inventarios, con `proveedor_llm=claude`.
2. `fase.py E1 descubrir "claves=ITZINV-12&claves=ITZINV-13&claves=ITZINV-14"`, luego `generar-tcs`, `arquitectura`, aprobar la arquitectura, `descomponer`.
3. `ciclo.py E1 "BASE/PT-01,BASE/PT-02,BASE/PT-03,HU-001/PT-01,HU-001/PT-02" 8`.
4. Ejecutar las pruebas del repositorio resultante en contenedores (Maven y Jest) y exportar las métricas.

## Hallazgos que cambiaron Loom

En E1c la descomposición aceptó respuestas vacías del modelo (HUs con 0 paquetes) y las reportó como éxito; se corrigió con reintentos y error explícito (ADR-0062). Los logs `E1c_descomponer_intento*.json` conservan esos intentos.

## Limitaciones conocidas

Una corrida, un proveedor, un proyecto; sin evaluación ciega; los PRs se fusionaron aunque conservaran observaciones para poder avanzar; el conteo de tokens de entrada de las skills de análisis parece bajo y debe verificarse.
