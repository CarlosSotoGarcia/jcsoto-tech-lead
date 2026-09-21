import sys; sys.path.insert(0,'.')
from ciclo_ui import *
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID); l.pg.get_by_role("tab", name=re.compile("Implementación")).click(); time.sleep(2)
    b=l.pg.get_by_role("button", name="Ejecutar release"); b.scroll_into_view_if_needed(); print("habilitado", b.is_enabled())
    b.click(); time.sleep(3); l.captura("39-fase4-ejecutar-release-confirmacion")
    l.pg.locator("p-dialog").get_by_role("button", name="Ejecutar release").click(); time.sleep(10); l.pg.evaluate("window.scrollTo(0,0)"); l.captura("39a-fase4-ejecutar-release-en-curso")
    print(esperar_actividad(l, maximo=2400, cada=60, prefijo="39b-fase4-release-progreso"))
    l.ir("/proyectos/"+PID); l.pg.get_by_role("tab", name=re.compile("Implementación")).click(); time.sleep(2)
    l.pg.get_by_role("button", name="Ejecutar release").scroll_into_view_if_needed(); l.captura("39c-fase4-release-terminado")
    t=l.pg.inner_text("body"); i=t.find("Último release"); print(t[i:i+500])
finally: l.cerrar()
