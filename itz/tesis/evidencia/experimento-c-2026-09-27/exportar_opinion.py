"""Experimento C (ADR-0090): exporta de Mongo la segunda opinión automática a segunda-opinion/opinion-<corrida>.json.

    python exportar_opinion.py c1

El archivo queda fuera de git hasta que termine la calificación humana. Este guion no imprime ninguna calificación: solo cuántas
observaciones hay y el SHA-256 del archivo, para anotarlo en el README."""

import hashlib
import json
import sys
from pathlib import Path

from pymongo import MongoClient

BASE = Path(__file__).parent


def main(corrida: str) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    db = MongoClient("mongodb://localhost:27017")["loom"]
    docs = list(db.experimento_c_opinion.find({"corrida": corrida}, {"_id": 0}).sort("pr_anonimo", 1))
    clave = json.loads((BASE / "clave" / f"clave-{corrida}.json").read_text(encoding="utf-8"))["observaciones"]
    ids = sorted(c["id"] for d in docs for c in d["calificaciones"])
    faltan = sorted(set(clave) - set(ids))
    (BASE / "segunda-opinion").mkdir(exist_ok=True)
    texto = json.dumps({"corrida": corrida, "modelos": sorted({d["modelo"] for d in docs}), "prs": docs}, ensure_ascii=False, indent=1)
    (BASE / "segunda-opinion" / f"opinion-{corrida}.json").write_text(texto, encoding="utf-8")
    print(f"PRs: {len(docs)} | observaciones calificadas: {len(ids)} de {len(clave)} | faltan: {len(faltan)} {faltan[:5]}")
    print("duración total (min):", round(sum(d["duracion_ms"] for d in docs) / 60000, 1))
    print("SHA-256:", hashlib.sha256(texto.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "c1")
