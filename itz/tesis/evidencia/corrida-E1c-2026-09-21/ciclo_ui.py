"""Ciclo de cada paquete operado solo desde la interfaz de Loom: generar código -> UNA revisión -> aceptar (fusionar) el PR."""
import json, sys, urllib.request, urllib.parse
sys.path.insert(0, '.')
from loom_ui import *

def api(path, tok=None, form=None):
    h = {"Authorization": "Bearer " + tok} if tok else {}
    d = urllib.parse.urlencode(form).encode() if form else None
    return json.loads(urllib.request.urlopen(urllib.request.Request("http://localhost:8000" + path, data=d, headers=h), timeout=60).read())

TOK = api("/auth/login", form={"username": "admin", "password": "admin123"})["access_token"]
def paquetes(): return api(f"/proyectos/{PID}/paquetes", TOK)
def de_estado(e): return [p for p in paquetes() if p["estado"] == e]

def tab_desarrollo(l):
    l.ir("/proyectos/" + PID); l.pg.get_by_role("tab", name=re.compile("Desarrollo")).click(); time.sleep(2)

def fila(l, p):
    return l.pg.locator("li, div").filter(has_text=re.compile(rf"PT-{p['id'][3:]} ")).filter(has_text=p["titulo"][:25]).last

def uno(l, k, log):
    pendientes = de_estado("pendiente")
    ya_revisado = de_estado("aprobado") or de_estado("con_observaciones")
    if not de_estado("en_revision") and not ya_revisado:
        if not pendientes: return False
        l.ir("/proyectos/" + PID)
        ok = cta(l, "Siguiente paquete", prefijo=f"{k:02d}a-generar-codigo", esperar=2700, cada=60)
        log.write(f"{k} generar ok={ok}\n"); log.flush()
    er = de_estado("en_revision") or ya_revisado
    if not er:
        log.write(f"{k} sin paquete en revision tras generar: {[ (p['grupo'],p['id'],p['estado']) for p in paquetes() if p['estado'] not in ('pendiente','fusionado')]}\n"); log.flush(); return False
    p = er[0]; ref = f"{p['grupo']}-{p['id']}"
    for c in l.pg.context.pages: pass
    # renombrar capturas del paso con la referencia
    for f in CAPS.glob(f"{k:02d}a-generar-codigo-*.png"): f.rename(CAPS / f.name.replace("generar-codigo", f"{ref}-generar-codigo"))
    # UNA revisión
    tab_desarrollo(l)
    if p["estado"] == "en_revision":
        l.pg.get_by_role("button", name="Revisar PRs").last.click(); time.sleep(8)
        l.pg.evaluate("window.scrollTo(0,0)"); l.captura(f"{k:02d}b-{ref}-revision-en-ejecucion")
        esperar_actividad(l, maximo=1800, cada=45, prefijo=f"{k:02d}b-{ref}-revision-progreso")
        time.sleep(3)
    q = next(x for x in paquetes() if x["grupo"] == p["grupo"] and x["id"] == p["id"])
    log.write(f"{k} {ref} tras revisión: {q['estado']} obs={len(q.get('observaciones') or [])}\n"); log.flush()
    tab_desarrollo(l); f = fila(l, p); f.scroll_into_view_if_needed(); l.captura(f"{k:02d}c-{ref}-resultado-de-la-revision")
    if q.get("observaciones") and f.locator("button:has(.pi-list)").count():
        f.locator("button:has(.pi-list)").click(); time.sleep(2); l.captura(f"{k:02d}d-{ref}-observaciones"); l.pg.keyboard.press("Escape"); time.sleep(1)
    # aceptar el PR: Loom exige CI en verde (ADR-0076); se espera a que GitHub termine los checks antes de pulsar
    import subprocess
    t0 = time.time()
    while time.time() - t0 < 1500 and p.get("pr"):
        r = subprocess.run(["gh", "pr", "checks", p["pr"], "--json", "bucket"], capture_output=True, text=True)
        if r.returncode in (0, 1, 8) and r.stdout.strip():
            b = {x["bucket"] for x in json.loads(r.stdout)}
            if "pending" not in b: break
        time.sleep(20)
    log.write(f"{k} {ref} checks CI: {sorted(b) if 'b' in dir() else '?'}" + chr(10)); log.flush()
    f.locator("button:has(.pi-check-circle)").click(); time.sleep(2); l.captura(f"{k:02d}e-{ref}-confirmar-fusion")
    l.pg.get_by_role("button", name="Fusionar PR").last.click(); time.sleep(5); l.captura(f"{k:02d}f-{ref}-fusionando")
    t0 = time.time()
    while time.time() - t0 < 1500:
        q = next(x for x in paquetes() if x["grupo"] == p["grupo"] and x["id"] == p["id"])
        if q["estado"] == "fusionado": break
        time.sleep(20)
    log.write(f"{k} {ref} fusión: {q['estado']}\n"); log.flush()
    tab_desarrollo(l); fila(l, p).scroll_into_view_if_needed(); l.captura(f"{k:02d}g-{ref}-fusionado")
    return q["estado"] == "fusionado"

if __name__ == "__main__":
    k0 = int(sys.argv[1]); tope = int(sys.argv[2])
    l = Loom(); log = open("logs/ciclo_ui.log", "a", encoding="utf-8")
    try:
        l.login()
        for k in range(k0, k0 + tope):
            if not uno(l, k, log): break
    finally:
        l.cerrar()
