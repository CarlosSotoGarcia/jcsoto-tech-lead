"""Experimento C: arma el plan de calificación por sesiones a partir de la hoja ciega (no usa la clave).

    python armar_sesiones.py

Agrupa los 29 PRs por proyecto y por HU, en el orden de sus paquetes, para que quien califica lea cada especificación una sola
vez, y reparte las 177 observaciones en seis sesiones de tamaño parecido. Copia además el documento de arquitectura de cada
proyecto al contexto del evaluador. Escribe evaluacion-ciega/plan-de-sesiones.md."""

import re
import shutil
import sys
from collections import OrderedDict
from pathlib import Path

from openpyxl import load_workbook

BASE = Path(__file__).parent
CIEGA = BASE / "evaluacion-ciega"
TARGET = Path(__file__).resolve().parents[4] / "loom" / "loom_target"
ARQUITECTURA = {"E1c": ("9c764535fb44470a8dc92fc74c8b835e", "loom-piloto-e1c-claude-cli.md"),
                "E3c": ("b17137fd304348d7a48532ba5db89270", "loom-piloto-e3c-claude-cli.md")}
# Sesiones: (título, [referencias de paquete en orden]).
SESIONES = [
    ("E1c · esqueleto del proyecto (BASE)", ["E1c · BASE/PT-01", "E1c · BASE/PT-02", "E1c · BASE/PT-03", "E1c · BASE/PT-04", "E1c · BASE/PT-05"]),
    ("E1c · HU-001 y primer paquete de la HU-002", ["E1c · HU-001/PT-01", "E1c · HU-001/PT-02", "E1c · HU-002/PT-01"]),
    ("E1c · resto de la HU-002 y HU-003", ["E1c · HU-002/PT-02", "E1c · HU-002/PT-03", "E1c · HU-003/PT-01", "E1c · HU-003/PT-02"]),
    ("E3c · esqueleto del proyecto (BASE)", ["E3c · BASE/PT-01", "E3c · BASE/PT-02", "E3c · BASE/PT-03", "E3c · BASE/PT-04", "E3c · BASE/PT-05"]),
    ("E3c · HU-001 y dos paquetes de la HU-002", ["E3c · HU-001/PT-01", "E3c · HU-001/PT-02", "E3c · HU-001/PT-03", "E3c · HU-001/PT-04",
                                                   "E3c · HU-002/PT-01", "E3c · HU-002/PT-02"]),
    ("E3c · resto de la HU-002 y HU-003", ["E3c · HU-002/PT-03", "E3c · HU-002/PT-04", "E3c · HU-003/PT-01", "E3c · HU-003/PT-02",
                                            "E3c · HU-003/PT-03", "E3c · HU-003/PT-04"]),
]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    ws = load_workbook(CIEGA / "hoja-de-evaluacion.xlsx")["Calificación"]
    obs: "OrderedDict[str, int]" = OrderedDict()
    pr_de: dict[str, str] = {}
    for fila in ws.iter_rows(min_row=2, values_only=True):
        obs[fila[1]] = obs.get(fila[1], 0) + 1
        pr_de[fila[2]] = fila[1]
    assert sorted(p for _, ps in SESIONES for p in ps) == sorted(pr_de), "las sesiones no cubren exactamente los 29 PRs"

    for proyecto, (pid, archivo) in ARQUITECTURA.items():
        shutil.copyfile(TARGET / pid / "arquitectura" / archivo, CIEGA / "contexto" / f"arquitectura-{proyecto}.md")

    def cambio(pr: str) -> str:
        texto = (CIEGA / "contexto" / f"{pr}.md").read_text(encoding="utf-8")
        return re.search(r"Cambio revisado[^:]*: (\S+)", texto).group(1)

    total = sum(obs.values())
    md = ["# Plan de calificación por sesiones (experimento C)", "",
          f"Son {total} observaciones en {len(obs)} Pull Requests. La hoja las trae en orden aleatorio (`P01` a `P29`); para calificar conviene",
          "otro orden: por proyecto y por historia de usuario, de modo que cada especificación se lee una sola vez. El orden en que se",
          "califica no afecta el cegado, porque dentro de cada PR las observaciones de las dos revisiones ya están mezcladas.", "",
          "Se proponen seis sesiones de entre 26 y 38 observaciones. Calcula de una hora a hora y media por sesión: unos diez minutos para",
          "leer el contexto de cada PR la primera vez y uno o dos minutos por observación.", "",
          "## Antes de empezar (una sola vez)", "",
          "1. Lee [guia-del-evaluador.md](guia-del-evaluador.md): la rúbrica y las reglas.",
          "2. Abre `hoja-de-evaluacion.xlsx` y activa el filtro de la columna `pr`.",
          "3. No abras `clave/`, `datos/experimento_c-c1.json`, `segunda-opinion/` ni la colección `experimento_c` de Mongo.", "",
          "## En cada PR", "",
          "1. Abre su archivo de contexto (paquete, especificación y casos de prueba de la HU) y, la primera vez en cada proyecto, su",
          "   documento de arquitectura (`contexto/arquitectura-E1c.md` o `contexto/arquitectura-E3c.md`).",
          "2. Abre el enlace «cambio»: es el código que vio el revisor, antes de cualquier corrección.",
          "3. Filtra la hoja por ese `pr` y califica todas sus observaciones de una vez.",
          "4. Al terminar el PR, revisa si dos observaciones dicen lo mismo y anótalo en «misma que (id)».",
          "5. Guarda la hoja y marca el PR en la lista de abajo.", ""]
    for n, (titulo, paquetes) in enumerate(SESIONES, start=1):
        subtotal = sum(obs[pr_de[p]] for p in paquetes)
        md += [f"## Sesión {n}: {titulo} ({subtotal} observaciones)", "",
               "| Hecho | PR | Paquete | Observaciones | Contexto | Cambio revisado |", "|---|---|---|---|---|---|"]
        for p in paquetes:
            pr = pr_de[p]
            md.append(f"| ☐ | {pr} | {p.split(' · ')[1]} | {obs[pr]} | [contexto/{pr}.md](contexto/{pr}.md) | [cambio]({cambio(pr)}) |")
        md.append("")
    md += ["## Bitácora de calificación", "",
           "Anota cada sesión. El tiempo total y las dudas se reportan en la tesis como parte del método.", "",
           "| Sesión | Fecha | Hora de inicio | Hora de fin | PRs calificados | Dudas o casos difíciles |", "|---|---|---|---|---|---|"]
    md += [f"| {n} | | | | | |" for n in range(1, len(SESIONES) + 1)]
    md += ["", "## Al terminar", "",
           "Avisa para correr `python analizar.py c1`. Hasta entonces, no comentes con nadie a qué revisión crees que pertenece cada",
           "observación: si lo sospechas por su contenido, califícala igual por lo que dice."]
    (CIEGA / "plan-de-sesiones.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
