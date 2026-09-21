import sys; sys.path.insert(0,'.')
from loom_ui import *
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID)
    l.captura("01-proyecto-limpio-ruta-del-proyecto")
    l.pg.get_by_role("button", name="Ver las HUs de Jira").click(); time.sleep(6)
    for k in ("ITZINV-12","ITZINV-13","ITZINV-14"):
        l.pg.locator("li, tr, div").filter(has_text=re.compile(k+" —")).last.locator("input[type=checkbox], .p-checkbox").first.click()
    l.pg.get_by_text("Procesar las seleccionadas").scroll_into_view_if_needed()
    l.captura("02-fase1-seleccion-de-3-hus")
    l.pg.get_by_role("button", name=re.compile("Procesar las seleccionadas")).click(); time.sleep(8)
    l.pg.evaluate("window.scrollTo(0,0)"); l.captura("03-fase1-en-ejecucion-panel-actividad")
    ok = esperar_actividad(l, maximo=900, cada=30, prefijo="03b-fase1-progreso")
    time.sleep(3); l.ir("/proyectos/"+PID); l.captura("04-fase1-terminada-ruta")
    l.pg.get_by_role("button", name="Historial").click(); time.sleep(2); l.captura("05-fase1-historial-de-procesos")
    print("terminó:", ok)
finally: l.cerrar()
