import sys; sys.path.insert(0,'.')
from loom_ui import *
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID)
    l.pg.get_by_role("tab", name=re.compile("Desarrollo")).click(); time.sleep(2)
    l.pg.get_by_role("button", name="Volver a descomponer").click(); time.sleep(8)
    l.pg.evaluate("window.scrollTo(0,0)"); l.captura("13-fase3-descomposicion-intento2-en-ejecucion")
    print(esperar_actividad(l, maximo=1500, cada=30, prefijo="13-fase3-descomposicion-intento2-progreso"))
    time.sleep(3); l.ir("/proyectos/"+PID); l.captura("13-fase3-descomposicion-intento2-terminado")
    l.ir(f"/proyectos/{PID}/hus"); l.captura("14-lista-de-hus-con-paquetes")
finally: l.cerrar()
