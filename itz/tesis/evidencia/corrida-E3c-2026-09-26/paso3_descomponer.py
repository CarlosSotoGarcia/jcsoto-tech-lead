import sys; sys.path.insert(0,'.')
from loom_ui import *
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID)
    print("desc:", cta(l, "Descomponer", prefijo="13-fase3-descomposicion", esperar=1800))
    t=l.pg.inner_text("body"); i=t.find("Registro de «Paquetes"); print(t[i:i+1200])
    l.ir(f"/proyectos/{PID}/hus"); l.captura("14-lista-de-hus-con-paquetes")
finally: l.cerrar()
