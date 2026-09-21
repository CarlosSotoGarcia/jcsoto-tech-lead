import sys; sys.path.insert(0,'.')
from loom_ui import *
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID)
    print("terminó:", cta(l, "Generar arquitectura", prefijo="08-fase2-arquitectura", esperar=1500))
    print([b for b in l.pg.get_by_role("button").all_inner_texts()][7:9])
finally: l.cerrar()
