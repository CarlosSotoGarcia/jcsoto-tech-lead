import sys, subprocess; sys.path.insert(0,'.')
from ciclo_ui import *
p = next(x for x in paquetes() if x["grupo"]=="HU-003" and x["id"]=="PT-02")
l=Loom()
try:
    l.login(); tab_desarrollo(l); f=fila(l,p); f.scroll_into_view_if_needed()
    l.captura("34-HU-003-PT-02-con-observaciones-y-ci-rojo")
    f.locator("button:has(.pi-wrench)").click(); time.sleep(3)
    l.captura("34b-HU-003-PT-02-corrigiendo-por-ci-rojo-y-observaciones")
    tit = l.pg.get_by_role("button", name=re.compile("Corregir|Aplicar|Iniciar|Confirmar"))
    print([t for t in l.pg.get_by_role("button").all_inner_texts() if t][-6:])
finally: l.cerrar()
