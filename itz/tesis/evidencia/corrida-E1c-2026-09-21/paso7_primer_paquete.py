import sys; sys.path.insert(0,'.')
from loom_ui import *
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID)
    ok = cta(l, "Siguiente paquete", prefijo="17-BASE-PT-01-generar-codigo", esperar=2400, cada=60)
    print("terminó:", ok)
    l.pg.get_by_role("tab", name=re.compile("Desarrollo")).click(); time.sleep(2)
    l.pg.get_by_text("Entorno de desarrollo dockerizado").first.scroll_into_view_if_needed(); l.captura("17b-BASE-PT-01-paquete-en-revision")
    print([b for b in l.pg.get_by_role("button").all_inner_texts() if b][7:22])
finally: l.cerrar()
