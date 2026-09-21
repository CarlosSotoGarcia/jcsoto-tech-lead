import sys, subprocess; sys.path.insert(0,'.')
from ciclo_ui import *
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID)
    print(esperar_actividad(l, maximo=1800, cada=45, prefijo="34c-HU-003-PT-02-correccion-progreso"))
    p = next(x for x in paquetes() if x["grupo"]=="HU-003" and x["id"]=="PT-02"); print(p["estado"], p["pr"])
    l.ir("/proyectos/"+PID); l.captura("34d-HU-003-PT-02-correccion-terminada")
    tab_desarrollo(l); f=fila(l,p); f.scroll_into_view_if_needed(); l.captura("34e-HU-003-PT-02-tras-la-correccion")
finally: l.cerrar()
