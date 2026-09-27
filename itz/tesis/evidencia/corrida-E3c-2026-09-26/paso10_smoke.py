import sys; sys.path.insert(0,'.')
from ciclo_ui import *
hu = sys.argv[1]; k = sys.argv[2]
l=Loom()
try:
    l.login(); tab_desarrollo(l)
    b = l.pg.get_by_role("button", name="Probar HU")
    idx = int(hu[-1]) - 1
    b.nth(idx).scroll_into_view_if_needed(); b.nth(idx).click(); time.sleep(4)
    l.captura(f"{k}a-{hu}-smoke-dialogo"); 
    d = l.pg.locator("p-dialog")
    if d.count() and d.first.is_visible():
        print([x for x in d.first.get_by_role("button").all_inner_texts() if x])
        d.first.get_by_role("button", name=re.compile("Probar|Iniciar|Ejecutar|Aceptar")).last.click(); time.sleep(8)
    l.pg.evaluate("window.scrollTo(0,0)"); l.captura(f"{k}b-{hu}-smoke-en-ejecucion")
    print(esperar_actividad(l, maximo=2700, cada=60, prefijo=f"{k}c-{hu}-smoke-progreso"))
    l.ir("/proyectos/"+PID); l.captura(f"{k}d-{hu}-smoke-terminado")
    l.ir(f"/proyectos/{PID}/hus/{hu}"); l.pg.get_by_role("tab", name=re.compile("Smoke testing")).click(); time.sleep(3)
    l.captura(f"{k}e-{hu}-resultado-del-smoke-testing")
    l.pg.screenshot(path=str(CAPS/f"{k}f-{hu}-resultado-del-smoke-testing-completo.png"), full_page=True)
finally: l.cerrar()
