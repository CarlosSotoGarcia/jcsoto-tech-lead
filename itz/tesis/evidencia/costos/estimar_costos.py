"""Estimación del costo de los escenarios E3 (Claude por API) y E4 (Gemini por API) de ITZ Agenda Taller, con los datos
medidos por Loom en las corridas E1c, E2 y E3c y con los precios configurados en Loom (LOOM_PRECIOS_MODELOS).

Uso: <python del backend de Loom> estimar_costos.py   (escribe datos-costos.json y estimacion-E3-E4.md en esta carpeta)
Lee MongoDB local (colección `metricas`); no llama a ninguna API."""
import collections, datetime, json, pathlib, sys
from pymongo import MongoClient

sys.stdout.reconfigure(encoding="utf-8")
AQUI = pathlib.Path(__file__).parent
db = MongoClient("mongodb://localhost:27017")["loom"]
PRECIOS = {  # USD por millón de tokens, tomados de LOOM_PRECIOS_MODELOS (backend/.env) el 2026-09-27
    "claude-sonnet-5": {"in": 2.0, "out": 10.0, "cache_in": 0.2},
    "gemini-3.6-flash": {"in": 0.75, "out": 3.75},
    "gemini-pro-latest": {"in": 2.0, "out": 12.0},
}
CODIGO = {"generar-codigo", "corregir-codigo", "avanzar-hu"}  # skills que escriben código (Gemini usa el modelo «pro»)
ESCENARIOS = {
    "E1c": ("9c764535fb44470a8dc92fc74c8b835e", AQUI.parent / "corrida-E1c-2026-09-21" / "datos" / "metricas.json"),
    "E2": ("bfc805e3495e4326afce54d676ce7bd2", None),
    "E3c": ("b17137fd304348d7a48532ba5db89270", None),
}


def metricas(pid, respaldo):
    docs = list(db.metricas.find({"proyecto_id": pid, "tipo": "llamada"}))
    if not docs and respaldo and respaldo.exists():  # E1c: su Mongo se puede limpiar; queda la exportación
        docs = [d for d in json.load(open(respaldo, encoding="utf-8")) if d.get("tipo") == "llamada"]
    return docs


def resumen(docs):
    por_skill = collections.defaultdict(collections.Counter)
    modelos = collections.Counter()
    for d in docs:
        c = por_skill[d["skill"]]
        c.update({"llamadas": 1, "in": d.get("tokens_in") or 0, "out": d.get("tokens_out") or 0, "cache": d.get("tokens_cache") or 0})
        c["usd"] += d.get("costo_usd") or 0
        modelos[d.get("modelo")] += 1
    tot = collections.Counter()
    for c in por_skill.values():
        tot.update(c)
    return {"por_skill": {k: dict(v) for k, v in por_skill.items()}, "total": dict(tot), "modelos": dict(modelos)}


def precio(modelo, t_in, t_out, t_cache=0):
    p = PRECIOS[modelo]
    return (t_in * p["in"] + t_out * p["out"] + t_cache * p.get("cache_in", p["in"])) / 1e6


datos = {}
for nombre, (pid, respaldo) in ESCENARIOS.items():
    r = resumen(metricas(pid, respaldo))
    r["paquetes"] = db.paquetes.count_documents({"proyecto_id": pid}) or None
    r["fusionados"] = db.paquetes.count_documents({"proyecto_id": pid, "estado": "fusionado"}) or None
    datos[nombre] = r
if not datos["E1c"]["total"]:
    datos["E1c"]["paquetes"] = datos["E1c"]["fusionados"] = 12
e3c, e1c, e2 = datos["E3c"], datos["E1c"], datos["E2"]
paq = e3c["paquetes"] or 17

# --- E3 (Claude API, claude-sonnet-5)
t = e3c["total"]
e3_tokens_e3c = precio("claude-sonnet-5", t["in"], t["out"], t["cache"])  # mismo volumen de tokens que E3c, a precio de Sonnet 5
e3_escala_e1c = e1c["total"]["usd"] / e1c["fusionados"] * paq  # costo de E1c (Sonnet 5 por CLI) por paquete, escalado a E3c

# --- E4 (Gemini API: flash para análisis y revisión, pro para código)
cod = collections.Counter(); ana = collections.Counter()
for skill, c in e3c["por_skill"].items():
    (cod if skill in CODIGO else ana).update({"in": c["in"], "out": c["out"]})
e4_tokens_e3c = precio("gemini-pro-latest", cod["in"], cod["out"]) + precio("gemini-3.6-flash", ana["in"], ana["out"])
e4_escala_e2 = e2["total"]["usd"] / (e2["fusionados"] or 1) * paq

resultado = {
    "fecha": datetime.date.today().isoformat(),
    "precios_usd_por_millon": PRECIOS,
    "E3c_costo_nocional_cli_usd": round(e3c["total"]["usd"], 2),
    "E3_claude_api": {"a_volumen_de_tokens_de_E3c": round(e3_tokens_e3c, 2), "escalando_E1c_por_paquete": round(e3_escala_e1c, 2)},
    "E4_gemini_api": {"a_volumen_de_tokens_de_E3c_sin_cache": round(e4_tokens_e3c, 2), "escalando_E2_por_paquete": round(e4_escala_e2, 2)},
    "datos": datos,
}
json.dump(resultado, open(AQUI / "datos-costos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: v for k, v in resultado.items() if k != "datos"}, ensure_ascii=False, indent=1))
for n, r in datos.items():
    print(n, "llamadas", r["total"].get("llamadas"), "in", r["total"].get("in"), "out", r["total"].get("out"),
          "cache", r["total"].get("cache"), "usd", round(r["total"].get("usd", 0), 2), "paquetes", r["paquetes"], "fusionados", r["fusionados"], r["modelos"])
