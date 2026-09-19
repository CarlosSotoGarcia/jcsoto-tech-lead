import sys, json, time
from common import *
clave, endpoint = sys.argv[1], sys.argv[2]
params = sys.argv[3] if len(sys.argv) > 3 else ""
ids = json.load(open("ids.json")); pid = ids[clave]; tok = login()
t = time.time()
s, r = call("POST", f"/proyectos/{pid}/hus/{endpoint}{('?' + params) if params else ''}", tok=tok)
seg = round(time.time() - t, 1)
tag = endpoint + ("_" + params.replace("=", "-").replace("&", "_") if params else "")
ev = sse(r, f"logs/{clave}_{tag}.json")
print(f"{clave} {endpoint} {params} -> http {s}, {seg}s, eventos {len(ev)}, error: {[e.get('mensaje') for e in ev if e['tipo']=='error']}")
s, m = call("GET", f"/proyectos/{pid}/metricas", tok=tok); m = json.loads(m)
print(f"{clave} costo acumulado:", round(sum((x['costo_usd'] or 0) for x in m['llamadas']), 4), "USD; llamadas:", sum(x['llamadas'] for x in m['llamadas']))
