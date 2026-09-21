import sys, subprocess; sys.path.insert(0,'.')
from ciclo_ui import *
p = next(x for x in paquetes() if x["grupo"]=="HU-003" and x["id"]=="PT-02")
t0=time.time()
while time.time()-t0<1500:
    r=subprocess.run(["gh","pr","checks",p["pr"],"--json","bucket"],capture_output=True,text=True)
    b={x["bucket"] for x in json.loads(r.stdout)} if r.stdout.strip() else {"pending"}
    if "pending" not in b: break
    time.sleep(20)
print("CI:", sorted(b))
l=Loom()
try:
    l.login(); tab_desarrollo(l); f=fila(l,p); f.scroll_into_view_if_needed()
    f.locator("button:has(.pi-check-circle)").click(); time.sleep(2); l.captura("35-HU-003-PT-02-confirmar-fusion")
    l.pg.get_by_role("button", name="Fusionar PR").last.click(); time.sleep(6); l.captura("35b-HU-003-PT-02-fusionando")
    t0=time.time()
    while time.time()-t0<600:
        q=next(x for x in paquetes() if x["grupo"]=="HU-003" and x["id"]=="PT-02")
        if q["estado"]=="fusionado": break
        time.sleep(15)
    print(q["estado"]); tab_desarrollo(l); fila(l,p).scroll_into_view_if_needed(); l.captura("35c-HU-003-PT-02-fusionado")
finally: l.cerrar()
