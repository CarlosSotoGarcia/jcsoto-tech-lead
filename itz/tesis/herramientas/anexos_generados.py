"""Genera los anexos de la tesis que salen del repositorio, para no transcribirlos a mano.

    python herramientas/anexos_generados.py borrador/v04     (desde itz/tesis; usa el Python del backend de Loom para los prompts)

Escribe en la carpeta del borrador:
- d2-anexo-b-fichas.md: Anexo B, las fichas de las skills (itz/arquitectura/skills/00 a 10) convertidas al formato del borrador;
- k-anexo-g-ejemplo-hu.md: Anexo G, el ejemplo completo de una HU (HU-001 de la corrida E1c) armado con la evidencia exportada;
- j-anexo-f-prompts.md: Anexo F, los prompts de sistema de cada skill tal como están en el código de Loom (se leen importando
  los módulos con el intérprete del backend, así que el texto es exactamente el que recibe el modelo).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SKILLS = RAIZ.parent / "arquitectura" / "skills"
LOOM = RAIZ.parents[1] / "loom" / "backend"


# ---------------------------------------------------------------- Anexo B
def _limpiar_en_linea(t: str) -> str:
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)          # enlaces: solo el texto
    t = t.replace("**", "")                                 # negritas (el generador no las tiene)
    t = re.sub(r"~~(.+?)~~", r"\1 (resuelto)", t)            # tachado: pendiente ya resuelto
    return t.strip()


def ficha_a_borrador(md: str, numero: str) -> list[str]:
    salida: list[str] = []
    parrafo: list[str] = []
    item: list[str] | None = None
    en_codigo = False
    tabla: list[str] = []

    def cerrar():
        nonlocal parrafo, item
        if item is not None:
            salida.append("- " + _limpiar_en_linea(" ".join(item)))
            item = None
        if parrafo:
            salida.append(_limpiar_en_linea(" ".join(parrafo)))
            parrafo = []

    def cerrar_tabla():
        nonlocal tabla
        if tabla:
            filas = [f for f in tabla if not re.match(r"^\|\s*:?-{2,}", f)]
            salida.append("TABLA:")
            salida.extend("| " + " | ".join(_limpiar_en_linea(c) for c in f.strip().strip("|").split("|")) + " |" for f in filas)
            salida.append("")
            tabla = []

    for linea in md.splitlines():
        if linea.startswith("```"):
            cerrar()
            salida.append("FIN-CODIGO" if en_codigo else "CODIGO:")
            en_codigo = not en_codigo
            continue
        if en_codigo:
            salida.append(linea)
            continue
        if linea.strip().startswith("|"):
            cerrar()
            tabla.append(linea)
            continue
        cerrar_tabla()
        if linea.startswith("# ") and numero:
            cerrar()
            titulo = re.sub(r"^#\s*Skill\s*[—-]\s*", "", linea[2:]).strip()
            salida.append(f"### B.{numero} {_limpiar_en_linea(titulo)}")
        elif linea.startswith("# "):
            cerrar()
            salida.append("*" + _limpiar_en_linea(linea[2:]) + "*")
        elif linea.startswith("## ") or linea.startswith("### "):
            cerrar()
            salida.append("*" + _limpiar_en_linea(linea.lstrip("#").strip()) + "*")
        elif re.match(r"^\s*([-*]|\d+\.)\s+", linea) and not linea.startswith("  "):
            cerrar()
            item = [re.sub(r"^\s*([-*]|\d+\.)\s+", "", linea)]
        elif not linea.strip():
            cerrar()
        elif item is not None and linea.startswith(" "):
            item.append(linea.strip())
        else:
            if item is not None:
                cerrar()
            parrafo.append(linea.strip())
    cerrar()
    cerrar_tabla()
    return salida


def anexo_b() -> str:
    partes = ["@@ tesis_anexos+", "CAPITULO: B", "### Anexo B. Fichas de las *skills*", "",
              "Cada ficha es el documento de diseño de una *skill* tal como está en el repositorio de "
              "arquitectura: su propósito, cuándo se invoca, sus entradas y salidas, lo que hace, los registros de decisión relacionados, "
              "sus criterios de éxito y los pendientes de diseño que quedaron abiertos. Los documentos de diseño llaman *Telar* al "
              "orquestador con sus *skills*; en esta tesis se usa Loom para el conjunto. Las fichas describen el diseño; lo que de cada "
              "función se implementó y se ejercitó está en la tabla 4.5.", ""]
    for i, ruta in enumerate(sorted(SKILLS.glob("[0-9][0-9]-*.md")), start=1):
        partes.extend(ficha_a_borrador(ruta.read_text(encoding="utf-8"), str(i)))
        partes.append("")
    return "\n".join(partes) + "\n"


# ---------------------------------------------------------------- Anexo F
PROMPTS = [  # (skill, descripción, módulo, constante)
    ("1", "Lectura y especificación de una HU", "loom_backend.analisis.hu", "SYSTEM_PROMPT"),
    ("1", "Propuesta de stack del arquitecto (Proyectos nuevos)", "loom_backend.analisis.propuesta_stack", "SYSTEM_PROMPT"),
    ("2", "Generación de casos de prueba", "loom_backend.analisis.tcs", "SYSTEM_PROMPT"),
    ("4", "Diseño de la arquitectura fundacional", "loom_backend.analisis.arquitectura", "SYSTEM_PROMPT"),
    ("5", "Planeación del esqueleto y del orden de las HUs", "loom_backend.analisis.descomposicion", "PLAN_SYSTEM"),
    ("5", "Descomposición de una HU en paquetes", "loom_backend.analisis.descomposicion", "HU_SYSTEM"),
    ("6", "Agente de generación de código", "loom_backend.analisis.agente_codigo", "SYSTEM"),
    ("7", "Revisión de un Pull Request (con contexto)", "loom_backend.analisis.revision_codigo", "REVISION_SYSTEM"),
    ("7", "Respuestas a las observaciones al corregir", "loom_backend.analisis.revision_codigo", "RESPUESTAS_SYSTEM"),
    ("7", "Segunda opinión sobre las observaciones", "loom_backend.analisis.evaluacion_observaciones", "SYSTEM"),
    ("3 y 8", "Agente de navegador que ejecuta un caso de prueba (diagnóstico y pruebas de humo)", "loom_backend.analisis.smoke_testing", "SMOKE_SYSTEM"),
    ("8", "Generación del guion de pruebas de humo con Playwright", "loom_backend.analisis.smoke_testing", "SUITE_SYSTEM"),
    ("9", "Diagnóstico de fallos y paquetes de corrección", "loom_backend.analisis.generacion_fixes", "SYSTEM"),
    ("9 (cambios)", "Paquetes de cambio cuando cambian los casos de prueba", "loom_backend.analisis.generacion_cambios", "SYSTEM"),
    ("Experimento C", "Revisión con solo el diff (condición de control)", "loom_backend.experimentos.revision_contexto", "REVISION_SYSTEM_SOLO_DIFF"),
    ("Experimento C", "Calificación automática de las observaciones", "loom_backend.experimentos.segunda_opinion_c", "OPINION_SYSTEM"),
]


def leer_prompts() -> list[str]:
    codigo = ("import importlib, json\n"
              f"especificacion = {json.dumps([(m, c) for _, _, m, c in PROMPTS])}\n"
              "print(json.dumps([getattr(importlib.import_module(m), c) for m, c in especificacion]))\n")
    python = LOOM / ".venv" / "Scripts" / "python.exe"
    r = subprocess.run([str(python), "-c", codigo], cwd=LOOM, capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(r.stdout)


def anexo_f() -> str:
    commit = subprocess.run(["git", "log", "-1", "--format=%h"], cwd=LOOM, capture_output=True, text=True).stdout.strip()
    partes = ["@@ tesis_anexos+", "CAPITULO: F", "### Anexo F. *Prompts* de cada *skill*", "",
              f"Son los *prompts* de sistema que Loom envía al modelo, extraídos del código de la "
              f"plataforma (repositorio de Loom, commit `{commit}`) para no transcribirlos a mano. El mensaje de cada llamada se arma "
              "aparte con los datos de la tarea (la HU, los casos de prueba, la arquitectura, el *diff*) y no se reproduce aquí. La *skill* "
              "10 no usa un modelo: el *script* de despliegue lo produce un generador determinista a partir de una plantilla. Los dos "
              "últimos *prompts* son los del experimento de control (apartado 4.1.7).", ""]
    for n, ((skill, descripcion, modulo, constante), texto) in enumerate(zip(PROMPTS, leer_prompts()), start=1):
        partes += [f"### F.{n} *Skill* {skill}: {descripcion}" if skill[0].isdigit() else f"### F.{n} {skill}: {descripcion}",
                   f"Fuente: `{modulo.replace('.', '/')}.py`, constante `{constante}`.", "", "CODIGO:"]
        partes += texto.rstrip("\n").split("\n")
        partes += ["FIN-CODIGO", ""]
    return "\n".join(partes) + "\n"


# ---------------------------------------------------------------- Anexo G
E1C = RAIZ / "evidencia" / "corrida-E1c-2026-09-21" / "datos"


def _celda(t) -> str:
    return _limpiar_en_linea(str(t or "")).replace("|", "/").replace("\n", " ")


def anexo_g() -> str:
    cargar = lambda n: json.loads((E1C / n).read_text(encoding="utf-8"))
    hu = next(h for h in cargar("hus.json") if h["id"] == "HU-001")
    paquetes = sorted((p for p in cargar("paquetes.json") if p["grupo"] == "HU-001"), key=lambda p: p["id"])
    revisiones = {r["pt"]: r for r in cargar("revisiones.json") if r.get("grupo") == "HU-001" and r["tipo"] == "revision" and str(r.get("ronda")) == "1"}
    smoke = next(s for s in cargar("smoke.json") if s["hu_id"] == "HU-001")
    spec = hu["spec_md"]
    frente, _, cuerpo = spec.partition("\n---\n") if spec.startswith("---") else ("", "", spec)
    partes = ["@@ tesis_anexos+", "CAPITULO: G", "### Anexo G. Ejemplo completo de una HU", "",
              f"Recorre la HU-001 de la corrida E1c, «{hu['titulo']}» ({hu['fuente_ref']} en Jira), "
              "por todos los artefactos que Loom generó para ella: la especificación, los casos de prueba, los paquetes de trabajo con sus "
              "Pull Requests, la primera revisión de cada paquete y el resultado de las pruebas de humo. Los textos son los que produjo Loom; "
              "solo se cambió el formato. Fuente: `evidencia/corrida-E1c-2026-09-21/datos/`.", "",
              "### G.1 Especificación (spec.md)", "", "Encabezado del archivo:", "CODIGO:", *frente.strip("-\n").split("\n"), "FIN-CODIGO", ""]
    partes += ficha_a_borrador(cuerpo, "")
    partes += ["", "### G.2 Casos de prueba (test-cases.md)", "",
               f"La *skill* 2 generó {len(hu['casos_prueba'])} casos; cada uno guarda el criterio del que deriva (apartado 5.2.15).", "",
               "TABLA: Casos de prueba de la HU-001 de E1c", "| Caso | Escenario | Rol | Resultado esperado |"]
    partes += [f"| {c['id']} | {_celda(c['escenario'])} | {_celda(c['rol_requerido'])} | {_celda(c['resultado_esperado'])} |" for c in hu["casos_prueba"]]
    partes += ["", "### G.3 Paquetes de trabajo", ""]
    for p in paquetes:
        partes += [f"*{p['id']}, {p['titulo']}* (capa {p['capa']}). Pull Request: {p['pr']}. Casos que cubre: {', '.join(p.get('tcs_asociados') or [])}. Depende de: {', '.join(p.get('depende_de') or []) or 'ninguno'}.",
                   "Entregables:"]
        partes += [f"- {_limpiar_en_linea(e)}" for e in p.get("entregables") or []]
        partes.append("")
    partes += ["### G.4 Primera revisión de cada paquete", ""]
    for p in paquetes:
        r = revisiones.get(p["id"])
        if not r:
            continue
        partes += [f"*{p['id']}*: veredicto «{r.get('veredicto', '').replace('_', ' ')}», {len(r['observaciones'])} observaciones. Resumen del revisor: {_limpiar_en_linea(r.get('resumen'))}"]
        for o in r["observaciones"]:
            lugar = (o.get("archivo") or "") + (f":{o['linea']}" if o.get("linea") else "")
            partes.append(f"- {o['severidad']}, {o['fuente'].replace('_', ' ')}{', `' + lugar + '`' if lugar else ''}: {_limpiar_en_linea(o['descripcion'])}")
        partes.append("")
    partes += ["### G.5 Pruebas de humo", "",
               f"La corrida de pruebas de humo de la HU-001 ejecutó {len(smoke['resultados'])} casos contra la aplicación desplegada: {smoke['pasan']} aprobados, "
               f"{smoke['fallan']} fallidos y {smoke['bloqueados']} bloqueados.", "",
               "TABLA: Resultado de las pruebas de humo de la HU-001 de E1c", "| Caso | Rol | Resultado | Motivo |"]
    nombre = {"pasa": "Aprobado", "falla": "Fallido", "bloqueado": "Bloqueado"}
    partes += [f"| {r['tc_id']} | {_celda(r.get('rol'))} | {nombre.get(r['resultado'], r['resultado'])} | {_celda(r.get('motivo')) or '—'} |" for r in smoke["resultados"]]
    return "\n".join(partes) + "\n"


def main(carpeta: str) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    destino = Path(carpeta)
    b, f = anexo_b(), anexo_f()
    (destino / "d2-anexo-b-fichas.md").write_text(b, encoding="utf-8")
    (destino / "j-anexo-f-prompts.md").write_text(f, encoding="utf-8")
    g = anexo_g()
    (destino / "k-anexo-g-ejemplo-hu.md").write_text(g, encoding="utf-8")
    print("Anexo G:", len(re.findall(r"\w+", g)), "palabras")
    print("Anexo B:", len(re.findall(r"\w+", b)), "palabras | Anexo F:", len(re.findall(r"\w+", f)), "palabras,", len(PROMPTS), "prompts")


if __name__ == "__main__":
    main(sys.argv[1])
