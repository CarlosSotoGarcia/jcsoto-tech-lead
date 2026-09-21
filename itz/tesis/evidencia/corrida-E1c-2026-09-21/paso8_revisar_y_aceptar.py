import sys; sys.path.insert(0,'.')
from loom_ui import *
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID)
    l.pg.get_by_role("tab", name=re.compile("Desarrollo")).click(); time.sleep(2)
    l.pg.get_by_role("button", name="Revisar PRs").last.click(); time.sleep(8)
    l.pg.evaluate("window.scrollTo(0,0)"); l.captura("18-BASE-PT-01-revision-en-ejecucion")
    print(esperar_actividad(l, maximo=1500, cada=45, prefijo="18-BASE-PT-01-revision-progreso"))
    l.ir("/proyectos/"+PID); l.pg.get_by_role("tab", name=re.compile("Desarrollo")).click(); time.sleep(2)
    fila = l.pg.locator("div").filter(has_text=re.compile("PT-01 Entorno de desarrollo")).last
    fila.scroll_into_view_if_needed(); l.captura("18b-BASE-PT-01-resultado-de-la-revision")
    print(fila.inner_html()[:1500])
finally: l.cerrar()
