import sys; sys.path.insert(0,'.')
from loom_ui import *
D = [
 "Autorización por rol (administrador y usuario final). El registro de usuarios es de otra HU. Fuera de alcance: recordarme, MFA y SSO; recuperación y cierre de sesión son las HU-002 y HU-003. Bloqueo tras 5 intentos fallidos por 15 minutos; sesión de 30 minutos; contraseña de mínimo 8 caracteres con letra y número. Cuenta desactivada o bloqueada: mismo mensaje genérico que credenciales inválidas. Solo web; tras entrar se redirige a la pantalla de inicio.",
 "Enlace con token de un solo uso, vigencia de 30 minutos. Se aplica la política de contraseñas del sistema (mínimo 8 caracteres con letra y número). Solo cuentas con contraseña local. El usuario se identifica por correo electrónico. Sin verificación adicional para ningún rol. Se asume infraestructura de correo transaccional disponible; mensaje en español. Tras restablecer no hay inicio de sesión automático: se redirige al inicio de sesión.",
 "Inactividad de 30 minutos, fija (no configurable). Sin aviso previo. «Al salir» significa solo el botón de cerrar sesión, no cerrar la pestaña. Solo web. Al expirar se descarta el trabajo no guardado. Aplica igual a todos los roles.",
]
l=Loom()
try:
    l.login(); l.ir("/decisiones-pendientes")
    tas = l.pg.locator("textarea")
    for i,t in enumerate(D): tas.nth(i).fill(t)
    l.captura("15b-decisiones-escritas-hu-001")
    for i in range(3):
        l.pg.get_by_role("button", name=re.compile("Confirmar decisión")).first.click(); time.sleep(3)
    l.ir("/decisiones-pendientes"); l.captura("16-decisiones-confirmadas")
    print(l.pg.inner_text("main")[:600])
finally: l.cerrar()
