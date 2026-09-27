"""Ajusta las variables de entorno del despliegue a las que exige el backend generado (env.schema.ts)."""
import sys; sys.path.insert(0,'.')
from ciclo_ui import *
VARS = "NODE_ENV=production\nFRONTEND_URL={URL_FRONTEND}\nMAIL_ADAPTER=console"
l=Loom()
try:
    l.login(); l.ir("/proyectos/"+PID); l.pg.get_by_role("tab", name=re.compile("Implementación")).click(); time.sleep(2)
    ta=l.pg.locator("#variables_entorno"); ta.scroll_into_view_if_needed(); l.captura("40-fase4-variables-antes")
    ta.fill(VARS); l.pg.locator("#secretos_generados").fill("JWT_ACCESS_SECRET")
    l.captura("40b-fase4-variables-ajustadas-al-codigo-generado")
    l.pg.get_by_role("button", name="Guardar cambios").click(); time.sleep(4)
finally: l.cerrar()
