"""PI1: cobertura de los criterios de aceptación por los casos de prueba generados (skill 02).

    python calcular_cobertura.py

Lee de Mongo las HUs de los dos pilotos (E1c y E3c). Cada caso de prueba guarda en `criterio_ref` el texto del criterio del que
deriva. Un criterio (explícito o inferido) cuenta como cubierto si al menos un caso lo referencia. El emparejamiento es por texto:
primero exacto (tras normalizar espacios y mayúsculas) y, si no, por similitud (difflib ≥ 0.85) o porque uno contiene al otro.
Los casos cuya referencia no corresponde a ningún criterio de la HU se reportan aparte.

Genera cobertura-pi1.json y cobertura-pi1.md en esta carpeta."""

import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

from pymongo import MongoClient

BASE = Path(__file__).parent
PROYECTOS = {"9c764535fb44470a8dc92fc74c8b835e": "E1c", "b17137fd304348d7a48532ba5db89270": "E3c"}
UMBRAL = 0.85


def norm(t: str) -> str:
    return re.sub(r"\s+", " ", (t or "").strip().lower())


def emparejar(ref: str, criterios: list[str]) -> tuple[int | None, str]:
    """Índice del criterio al que apunta la referencia y cómo se emparejó (exacto, contenido, similar)."""
    r = norm(ref)
    for i, c in enumerate(criterios):
        if norm(c) == r:
            return i, "exacto"
    for i, c in enumerate(criterios):
        n = norm(c)
        if len(r) > 30 and (r in n or n in r):
            return i, "contenido"
    mejor, idx = 0.0, None
    for i, c in enumerate(criterios):
        s = SequenceMatcher(None, r, norm(c)).ratio()
        if s > mejor:
            mejor, idx = s, i
    return (idx, "similar") if mejor >= UMBRAL else (None, "sin_criterio")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    db = MongoClient("mongodb://localhost:27017")["loom"]
    filas, detalle = [], []
    for pid, nombre in PROYECTOS.items():
        for hu in db.hus.find({"proyecto_id": pid, "clasificacion": "hu"}).sort("id", 1):
            explicitos = hu.get("criterios_explicitos") or []
            inferidos = hu.get("criterios_inferidos") or []
            criterios = explicitos + inferidos
            casos_por_criterio = [0] * len(criterios)
            modos = {"exacto": 0, "contenido": 0, "similar": 0, "sin_criterio": 0}
            sin = []
            for caso in hu.get("casos_prueba") or []:
                idx, modo = emparejar(caso.get("criterio_ref") or "", criterios)
                modos[modo] += 1
                if idx is None:
                    sin.append({"caso": caso.get("id"), "criterio_ref": caso.get("criterio_ref")})
                else:
                    casos_por_criterio[idx] += 1
            n_exp = len(explicitos)
            cub_exp = sum(1 for k in casos_por_criterio[:n_exp] if k)
            cub_inf = sum(1 for k in casos_por_criterio[n_exp:] if k)
            no_cubiertos = [c for c, k in zip(criterios, casos_por_criterio) if not k]
            filas.append({
                "proyecto": nombre, "hu": hu["id"], "fuente_ref": hu.get("fuente_ref"),
                "criterios_explicitos": n_exp, "explicitos_cubiertos": cub_exp,
                "criterios_inferidos": len(inferidos), "inferidos_cubiertos": cub_inf,
                "criterios": len(criterios), "cubiertos": cub_exp + cub_inf,
                "casos": len(hu.get("casos_prueba") or []), "casos_sin_criterio": len(sin),
                "max_casos_por_criterio": max(casos_por_criterio, default=0),
                "emparejamiento": modos, "supuestos": len(hu.get("supuestos") or []),
            })
            detalle.append({"proyecto": nombre, "hu": hu["id"], "criterios_no_cubiertos": no_cubiertos, "casos_sin_criterio": sin,
                            "casos_por_criterio": casos_por_criterio})

    def total(clave: str, proyecto: str | None = None) -> int:
        return sum(f[clave] for f in filas if proyecto in (None, f["proyecto"]))

    resumen = {}
    for pr in (*PROYECTOS.values(), None):
        c, k = total("criterios", pr), total("cubiertos", pr)
        resumen[pr or "total"] = {
            "hus": sum(1 for f in filas if pr in (None, f["proyecto"])),
            "criterios": c, "cubiertos": k, "cobertura": round(k / c, 3) if c else None,
            "explicitos": total("criterios_explicitos", pr), "explicitos_cubiertos": total("explicitos_cubiertos", pr),
            "inferidos": total("criterios_inferidos", pr), "inferidos_cubiertos": total("inferidos_cubiertos", pr),
            "casos": total("casos", pr), "casos_sin_criterio": total("casos_sin_criterio", pr),
            "casos_por_criterio_media": round(total("casos", pr) / c, 2) if c else None,
        }
    (BASE / "cobertura-pi1.json").write_text(json.dumps({"umbral_similitud": UMBRAL, "resumen": resumen, "por_hu": filas, "detalle": detalle},
                                                        ensure_ascii=False, indent=1), encoding="utf-8")
    md = ["# Cobertura de criterios de aceptación por los casos de prueba (PI1)", "",
          "| Proyecto | HU | Criterios explícitos (cubiertos) | Criterios inferidos (cubiertos) | Casos | Casos sin criterio | Máx. casos por criterio |",
          "|---|---|---|---|---|---|---|"]
    for f in filas:
        md.append(f"| {f['proyecto']} | {f['hu']} | {f['criterios_explicitos']} ({f['explicitos_cubiertos']}) | "
                  f"{f['criterios_inferidos']} ({f['inferidos_cubiertos']}) | {f['casos']} | {f['casos_sin_criterio']} | {f['max_casos_por_criterio']} |")
    (BASE / "cobertura-pi1.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(resumen, ensure_ascii=False, indent=1))
    for f in filas:
        print(f["proyecto"], f["hu"], f"criterios {f['cubiertos']}/{f['criterios']}", f"casos {f['casos']}", f"sin criterio {f['casos_sin_criterio']}", f["emparejamiento"])
    for d in detalle:
        for c in d["criterios_no_cubiertos"]:
            print("NO CUBIERTO", d["proyecto"], d["hu"], c[:140])
        for c in d["casos_sin_criterio"]:
            print("SIN CRITERIO", d["proyecto"], d["hu"], c["caso"], (c["criterio_ref"] or "")[:140])


if __name__ == "__main__":
    main()
