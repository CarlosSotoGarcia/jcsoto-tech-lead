import sys, json; sys.path.insert(0,'.')
from loom_ui import *
D = json.load(open("decisiones-supuestos.json", encoding="utf-8"))
l=Loom()
try:
    l.login(); l.ir("/decisiones-pendientes")
    tarjetas = l.pg.locator("p-card, .card, section, div").filter(has_text="PILOTO E3c").filter(has=l.pg.locator("textarea"))
    t=l.pg.inner_text("main"); print([m for m in re.findall(r"(HU-00\d) · [^\n]+\n(PILOTO [^\n]+)", t)])
    l.captura("15-decisiones-pendientes-supuestos")
    for i, hu in enumerate(("HU-001","HU-002","HU-003")):
        l.ir("/decisiones-pendientes")
        ta = l.pg.locator(f"textarea[id='dec-{PID}/{hu}']")
        ta.fill(D[i]); time.sleep(0.5)
        ta.scroll_into_view_if_needed()
        if i == 0: l.captura("15b-decision-escrita-hu-001")
        ta.locator("xpath=ancestor::section[1]").get_by_role("button", name=re.compile("Confirmar decisión")).click(); time.sleep(3)
    l.ir("/decisiones-pendientes"); l.captura("16-decisiones-confirmadas")
    print("quedan E3c:", l.pg.inner_text("main").count("PILOTO E3c"))
finally: l.cerrar()
