import sys; sys.path.insert(0,'.')
from loom_ui import *
l=Loom()
try:
    l.login()
    for hu in ("HU-001","HU-002","HU-003"):
        l.ir(f"/proyectos/{PID}/hus/{hu}")
        if hu=="HU-001":
            l.captura("06b-HU-001-especificacion")
            l.pg.get_by_role("tab", name=re.compile("Casos de prueba")).click(); time.sleep(2); l.captura("07b-HU-001-casos-de-prueba")
            l.pg.get_by_role("tab", name=re.compile("Paquetes de trabajo")).click(); time.sleep(2); l.captura("14b-HU-001-paquetes-de-trabajo")
        l.pg.get_by_role("tab", name=re.compile("Smoke testing")).click(); time.sleep(3)
        n={"HU-001":"42","HU-002":"43","HU-003":"44"}[hu]
        l.captura(f"{n}e-{hu}-resultado-del-smoke-testing")
        l.pg.screenshot(path=str(CAPS/f"{n}f-{hu}-resultado-del-smoke-testing-completo.png"), full_page=True)
finally: l.cerrar()
