import sys; sys.path.insert(0,'.')
from loom_ui import *
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID)
    print("terminó:", cta(l, "Descomponer", prefijo="13-fase3-descomposicion-en-paquetes", esperar=1500))
    print([b for b in l.pg.get_by_role("button").all_inner_texts() if b][7:12])
    l.ir(f"/proyectos/{PID}/hus"); l.captura("14-lista-de-hus-con-paquetes")
finally: l.cerrar()
