"""HU-001/PT-04 quedó «Aprobado» con el CI en rojo: la UI no ofrece corregir en ese estado. Se usa la acción avanzar-hu de Loom
(corrige con el log del CI, ADR-0078) llamada por su API, con 1 ronda, y se capturan las pantallas mientras corre."""
import sys, threading, json, urllib.request; sys.path.insert(0,'.')
from ciclo_ui import *
g = sys.argv[1]; k = sys.argv[2]; parar = sys.argv[3] if len(sys.argv) > 3 else None  # p. ej. "PT-02": cancelar al fusionarse ese paquete
eventos = []
def llamar():
    req = urllib.request.Request(f"http://localhost:8000/proyectos/{PID}/hus/avanzar-hu?grupo={g}&rondas=1", data=b"", method="POST", headers={"Authorization": "Bearer " + TOK})
    for linea in urllib.request.urlopen(req, timeout=7200):
        linea = linea.decode("utf-8", "ignore").strip()
        if linea.startswith("data:"):
            e = json.loads(linea[5:]); eventos.append(e)
            if parar and e.get("tipo") == "item_listo" and f"{g}/{parar}: PR fusionado" in (e.get("mensaje") or ""):
                cancelar(); return
def cancelar():
    import subprocess
    py = r"C:\jsoto\jcsoto-tech-lead\loomackend\.venv\Scripts\python.exe"
    corrida = subprocess.run([py, "-c", f"from pymongo import MongoClient; x=MongoClient('mongodb://localhost:27017')['loom'].procesos.find_one({{'proyecto_id':'{PID}','skill':'avanzar-hu','estado':'corriendo'}}); print(x['corrida'] if x else '')"], capture_output=True, text=True).stdout.strip()
    if corrida:
        urllib.request.urlopen(urllib.request.Request(f"http://localhost:8000/proyectos/{PID}/hus/actividad/{corrida}/cancelar", data=b"", method="POST", headers={"Authorization": "Bearer " + TOK}), timeout=60)
        eventos.append({"tipo": "nota", "mensaje": f"cancelado a propósito tras fusionar {g}/{parar}"})
hilo = threading.Thread(target=llamar, daemon=True); hilo.start()
l=Loom()
try:
    l.login(); tab_desarrollo(l)
    p = next(x for x in paquetes() if x["grupo"]==g and x["estado"]!="fusionado")
    fila(l,p).scroll_into_view_if_needed(); l.captura(f"{k}h-{g}-{p['id']}-con-ci-en-rojo")
    time.sleep(8); l.ir("/proyectos/"+PID); l.captura(f"{k}i-{g}-avanzar-hu-en-ejecucion")
    n = 0
    while hilo.is_alive():
        time.sleep(60); n += 1; l.ir("/proyectos/"+PID); l.captura(f"{k}j-{g}-avanzar-hu-progreso-{n}")
    l.ir("/proyectos/"+PID); l.captura(f"{k}k-{g}-avanzar-hu-terminado")
    tab_desarrollo(l); fila(l,p).scroll_into_view_if_needed(); l.captura(f"{k}l-{g}-{p['id']}-resultado")
finally:
    l.cerrar()
    json.dump(eventos, open(f"logs/avanzar_{g}.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    for e in eventos[-6:]: print(e.get("tipo"), (e.get("mensaje") or "")[:250])
