import sys; sys.path.insert(0,'.')
from ciclo_ui import *
l=Loom()
try:
    l.login(); tab_desarrollo(l)
    grupo = l.pg.locator("div").filter(has_text=re.compile(r"HU-003 · Cerrar sesión")).last
    grupo.get_by_role("button", name="Avanzar con esta HU").click(); time.sleep(2)
    d = l.pg.locator("p-dialog")
    d.locator(".ronda-opcion", has_text="1").click()
    d.locator("input[type=checkbox]").check(); time.sleep(1)
    l.captura("34-HU-003-avanzar-dialogo-una-ronda-de-correccion")
    d.get_by_role("button", name="Iniciar avance").last.click(); time.sleep(8)
    l.pg.evaluate("window.scrollTo(0,0)"); l.captura("34b-HU-003-avanzar-en-ejecucion")
    print(esperar_actividad(l, maximo=3000, cada=60, prefijo="34c-HU-003-avanzar-progreso"))
    l.ir("/proyectos/"+PID); l.captura("34d-HU-003-avanzar-terminado")
finally: l.cerrar()
