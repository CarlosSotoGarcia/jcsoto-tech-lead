import sys, json, time
from common import *
clave = sys.argv[1]; lista = [x.split("/") for x in sys.argv[2].split(",")]; tope = float(sys.argv[3])
pid = json.load(open("ids.json"))[clave]; tok = login()
def costo():
    m = json.loads(call("GET", f"/proyectos/{pid}/metricas", tok=tok)[1]); return sum((x["costo_usd"] or 0) for x in m["llamadas"])
def paquete(g, p):
    return next(q for q in json.loads(call("GET", f"/proyectos/{pid}/paquetes", tok=tok)[1]) if q["grupo"] == g and q["id"] == p)
def paso(endpoint, g, p):
    t = time.time(); c0 = costo()
    s, r = call("POST", f"/proyectos/{pid}/hus/{endpoint}?grupo={g}&pt={p}", tok=tok)
    ev = sse(r, f"logs/{clave}_{endpoint}_{g}_{p}_{int(t)}.json", mostrar=("error",))
    fin = [e for e in ev if e["tipo"] == "completado"]
    return {"endpoint": endpoint, "seg": round(time.time() - t, 1), "costo_usd": round(costo() - c0, 4), "http": s, "ok": bool(fin), "mensaje": (fin[0]["mensaje"] if fin else [e.get("mensaje") for e in ev if e["tipo"] == "error"])}
resumen = []
for g, p in lista:
    if costo() > tope: print("TOPE DE COSTO alcanzado", round(costo(), 3)); break
    r = {"paquete": f"{g}/{p}", "pasos": []}
    q = paquete(g, p)
    if q["estado"] == "pendiente": r["pasos"].append(paso("generar-codigo", g, p)); q = paquete(g, p)
    if q["estado"] == "en_revision": r["pasos"].append(paso("revisar-codigo", g, p)); q = paquete(g, p)
    r["tras_revision"] = {"estado": q["estado"], "observaciones": [{"sev": o["severidad"], "fuente": o["fuente"]} for o in q["observaciones"]]}
    if q["estado"] == "con_observaciones":
        r["pasos"].append(paso("corregir-codigo", g, p)); q = paquete(g, p)
        if q["estado"] == "en_revision": r["pasos"].append(paso("revisar-codigo", g, p)); q = paquete(g, p)
        r["tras_correccion"] = {"estado": q["estado"], "observaciones": [{"sev": o["severidad"], "fuente": o["fuente"]} for o in q["observaciones"]]}
    r["estado_final_antes_de_fusionar"] = q["estado"]; r["pr"] = q["pr"]; r["rondas_revision"] = q["rondas_revision"]
    if q["estado"] in ("aprobado", "con_observaciones", "en_revision") and q["pr"]:
        s, f = call("POST", f"/proyectos/{pid}/paquetes/fusionar?grupo={g}&pt={p}", tok=tok); r["fusion"] = s if s == 200 else f[:200].decode("utf-8", "ignore")
    resumen.append(r); print(json.dumps(r, ensure_ascii=False)); sys.stdout.flush()
    json.dump(resumen, open(f"logs/{clave}_ciclo_resumen.json", "w"), ensure_ascii=False, indent=1)
print("costo total", round(costo(), 3))
