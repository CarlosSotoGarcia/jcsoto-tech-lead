import sys; sys.path.insert(0,'.')
from ciclo_ui import *
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID); l.pg.get_by_role("tab", name=re.compile("Implementación")).click(); time.sleep(2)
    campo = l.pg.get_by_label(re.compile("URL del ambiente de desarrollo"))
    campo.fill("https://inventarios-web-118746543308.us-central1.run.app")
    campo.scroll_into_view_if_needed(); l.captura("40-fase4-url-del-ambiente-de-desarrollo")
    l.pg.get_by_role("button", name="Guardar cambios").click(); time.sleep(4)
    l.ir("/proyectos/"+PID); l.captura("41-ruta-tras-el-release")
finally: l.cerrar()
