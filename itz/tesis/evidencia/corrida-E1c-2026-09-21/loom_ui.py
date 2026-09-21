"""Ayudante de Playwright para operar Loom desde su interfaz y guardar capturas numeradas de cada paso."""
import json, re, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FRONT = "http://localhost:4200"
PID = "9c764535fb44470a8dc92fc74c8b835e"
CAPS = Path(__file__).parent / "capturas"


class Loom:
    def __init__(self, headless=True):
        self.p = sync_playwright().start()
        self.b = self.p.chromium.launch(headless=headless)
        self.ctx = self.b.new_context(viewport={"width": 1440, "height": 900}, locale="es-MX")
        self.pg = self.ctx.new_page()
        self.n = len(list(CAPS.glob("*.png")))

    def login(self, user="admin", pw="admin123"):
        self.pg.goto(FRONT + "/login")
        self.pg.get_by_label(re.compile("usuario", re.I)).fill(user)
        self.pg.locator("input[type=password]").fill(pw)
        self.pg.get_by_role("button", name=re.compile("entrar|iniciar|ingresar", re.I)).click()
        self.pg.wait_for_url(re.compile("proyectos"))

    def ir(self, ruta):
        self.pg.goto(FRONT + ruta); self.pg.wait_for_load_state("networkidle"); time.sleep(1)

    def captura(self, nombre, completa=False):
        f = CAPS / f"{nombre}.png"
        self.pg.screenshot(path=str(f), full_page=completa)
        print("captura", f.name); return f.name

    def cerrar(self):
        self.b.close(); self.p.stop()


def esperar_actividad(l, maximo=1500, cada=45, prefijo="progreso", capturar=True):
    """Espera a que el panel Actividad diga «Nada en curso»; captura el panel cada `cada` segundos."""
    t0 = time.time(); k = 0
    while time.time() - t0 < maximo:
        txt = l.pg.inner_text("body")
        if "Nada en curso" in txt: return True
        k += 1
        if capturar and k % max(1, 60 // cada) == 0: l.captura(f"{prefijo}-{k}")
        time.sleep(cada)
    return False


def cta(l, texto, esperar=900, cada=30, prefijo="progreso", tras=None):
    """Pulsa el botón principal de la ruta (texto exacto), captura el arranque, espera el fin y devuelve True si terminó."""
    l.pg.evaluate("window.scrollTo(0,0)")
    l.pg.locator("button").filter(has_text=texto).filter(has_not_text=re.compile(r"Lista para correr|Bloqueada|Completa|Por configurar")).first.click()
    time.sleep(8)
    l.pg.evaluate("window.scrollTo(0,0)"); l.captura(f"{prefijo}-en-ejecucion")
    ok = esperar_actividad(l, maximo=esperar, cada=cada, prefijo=prefijo + "-progreso")
    time.sleep(3); l.ir("/proyectos/" + PID); l.captura(f"{prefijo}-terminado")
    return ok
