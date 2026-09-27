"""Agrega desde la UI las cuentas de prueba para los roles que usan los casos de prueba del E3c (credenciales en el scratchpad)."""
import sys, json; sys.path.insert(0,'.')
from ciclo_ui import *
S = r"C:\Users\jncso\AppData\Local\Temp\claude\c--jsoto-jcsoto-tech-lead\2fb87c39-b3bb-467a-b8b2-b1b1a850b42c\scratchpad\piloto"
roles = json.load(open(S + r"\cuentas_roles_e3c.json", encoding="utf-8"))
base = {c["rol"]: c for c in json.load(open(S + r"\cuentas_prueba_e3c.json", encoding="utf-8"))}
filas = [("recepcion", roles["recepcion"]), ("personal_interno", roles["recepcion"]), ("usuario_final", roles["usuario_final"]),
         ("cliente_bloqueable", roles["cliente_bloqueable"]), ("cuenta_pendiente_verificacion", roles["cuenta_pendiente_verificacion"]),
         ("cuenta_inactiva", base["usuario_inactivo"])]
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID); l.pg.get_by_role("tab", name=re.compile("Implementación")).click(); time.sleep(2)
    for rol, c in filas:
        l.pg.get_by_role("button", name="Agregar cuenta").click(); time.sleep(0.5)
        l.pg.locator("input[formcontrolname=rol]").last.fill(rol)
        l.pg.locator("input[formcontrolname=usuario]").last.fill(c["usuario"])
        l.pg.locator("input[placeholder^='Contraseña']").last.fill(c["contrasena"])
    l.pg.get_by_role("button", name="Agregar cuenta").scroll_into_view_if_needed(); l.captura("42g-cuentas-de-prueba-por-rol")
    l.pg.get_by_role("button", name="Guardar cambios").click(); time.sleep(4)
finally: l.cerrar()
