import sys; sys.path.insert(0,'.')
from ciclo_ui import *
def impl(l):
    l.ir("/proyectos/"+PID); l.pg.get_by_role("tab", name=re.compile("Implementación")).click(); time.sleep(2)
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID); l.captura("36-fase3-completa-ruta-del-proyecto")
    impl(l); l.pg.get_by_role("button", name="Generar release.py").scroll_into_view_if_needed(); l.captura("37-fase4-configuracion-de-despliegue")
    l.pg.get_by_role("button", name="Generar release.py").click(); time.sleep(6); l.captura("37b-fase4-release-py-generado")
    l.pg.keyboard.press("Escape"); time.sleep(1)
    impl(l); b=l.pg.get_by_role("button", name=re.compile("Publicar en el repositorio")); b.scroll_into_view_if_needed(); b.click(); time.sleep(8)
    esperar_actividad(l, maximo=600, cada=20, prefijo="38b-fase4-publicar-progreso")
    impl(l); l.pg.get_by_role("button", name="Ejecutar release").scroll_into_view_if_needed(); l.captura("38c-fase4-pr-de-despliegue-publicado")
    t=l.pg.inner_text("body"); print(re.findall(r"https://github.com/\S+/pull/\d+", t))
finally: l.cerrar()
