import sys; sys.path.insert(0,'.')
from loom_ui import *
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID)
    l.pg.get_by_role("tab", name=re.compile("Desarrollo")).click(); time.sleep(2)
    fila = l.pg.locator("li, div").filter(has_text=re.compile(r"PT-01 Entorno de desarrollo")).last
    fila.locator("button:has(.pi-list)").click(); time.sleep(2)
    l.captura("19-BASE-PT-01-observaciones-de-la-revision")
    l.pg.keyboard.press("Escape"); time.sleep(1)
    fila.locator("button:has(.pi-check-circle)").click(); time.sleep(2)
    l.captura("20-BASE-PT-01-confirmar-aceptar-pr")
    print(l.pg.inner_text("body")[-600:])
finally: l.cerrar()
