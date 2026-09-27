import sys; sys.path.insert(0,'.')
from ciclo_ui import *
URL = "https://taller-web-118746543308.us-central1.run.app"
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID); l.pg.get_by_role("tab", name=re.compile("Implementación")).click(); time.sleep(2)
    c=l.pg.get_by_label(re.compile("URL del ambiente de desarrollo")); c.fill(URL); c.scroll_into_view_if_needed()
    l.captura("41-fase4-url-del-ambiente-de-desarrollo")
    l.pg.get_by_role("button", name="Guardar cambios").click(); time.sleep(4)
    l.ir("/proyectos/"+PID); l.captura("41b-ruta-tras-el-release")
finally: l.cerrar()
