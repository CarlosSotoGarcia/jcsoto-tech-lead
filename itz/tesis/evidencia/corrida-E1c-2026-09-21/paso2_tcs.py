import sys; sys.path.insert(0,'.')
from loom_ui import *
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID)
    l.ir(f"/proyectos/{PID}/hus"); l.captura("06-lista-de-hus-especificadas")
    l.ir("/proyectos/"+PID)
    print("terminó:", cta(l, "Generar TCs", prefijo="07-fase2-casos-de-prueba"))
    print(l.pg.get_by_role("button").all_inner_texts()[:12])
finally: l.cerrar()
