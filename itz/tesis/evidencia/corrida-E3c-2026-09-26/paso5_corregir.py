"""Una corrección desde la UI (botón de corregir del paquete) cuando el CI queda en rojo; luego espera CI y acepta el PR.
Uso: python paso5_corregir.py HU-001 PT-04 25"""
import sys, subprocess; sys.path.insert(0,'.')
from ciclo_ui import *
g, pt, k = sys.argv[1], sys.argv[2], sys.argv[3]
ref = f"{g}-{pt}"
p = next(x for x in paquetes() if x["grupo"]==g and x["id"]==pt)
l=Loom()
try:
    l.login(); tab_desarrollo(l); f=fila(l,p); f.scroll_into_view_if_needed()
    l.captura(f"{k}h-{ref}-con-ci-en-rojo")
    f.locator("button:has(.pi-wrench)").click(); time.sleep(5)
    l.pg.evaluate("window.scrollTo(0,0)"); l.captura(f"{k}i-{ref}-correccion-en-ejecucion")
    esperar_actividad(l, maximo=2400, cada=60, prefijo=f"{k}j-{ref}-correccion-progreso")
    p = next(x for x in paquetes() if x["grupo"]==g and x["id"]==pt); print("tras corrección:", p["estado"])
    tab_desarrollo(l); f=fila(l,p); f.scroll_into_view_if_needed(); l.captura(f"{k}k-{ref}-tras-la-correccion")
finally: l.cerrar()
t0=time.time(); b={"pending"}
while time.time()-t0<1500:
    r=subprocess.run(["gh","pr","checks",p["pr"],"--json","bucket"],capture_output=True,text=True)
    b={x["bucket"] for x in json.loads(r.stdout)} if r.stdout.strip() else {"pending"}
    if "pending" not in b: break
    time.sleep(20)
print("CI tras corrección:", sorted(b))
if "fail" in b: sys.exit("CI sigue en rojo")
l=Loom()
try:
    l.login(); tab_desarrollo(l); f=fila(l,p); f.scroll_into_view_if_needed()
    f.locator("button:has(.pi-check-circle)").click(); time.sleep(2); l.captura(f"{k}l-{ref}-confirmar-fusion")
    l.pg.get_by_role("button", name="Fusionar PR").last.click(); time.sleep(6)
    t0=time.time()
    while time.time()-t0<600:
        q=next(x for x in paquetes() if x["grupo"]==g and x["id"]==pt)
        if q["estado"]=="fusionado": break
        time.sleep(15)
    print("final:", q["estado"]); tab_desarrollo(l); fila(l,p).scroll_into_view_if_needed(); l.captura(f"{k}m-{ref}-fusionado")
finally: l.cerrar()
