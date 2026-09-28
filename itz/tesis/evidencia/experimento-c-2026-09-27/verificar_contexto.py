"""Experimento C (ADR-0089): compara el contexto que recibió la condición «contexto» (Mongo al 2026-09-27) con el que vio la
primera revisión real del piloto (repositorio de control de Loom en el commit anterior a «<paquete>: revisión 1»).

    python verificar_contexto.py

Sirve para detectar contaminación: lo que haya cambiado después de la primera revisión no debe entrar al experimento."""

import subprocess
import sys
from pathlib import Path

from pymongo import MongoClient

TARGET = Path(__file__).resolve().parents[4] / "loom" / "loom_target"
PROYECTOS = {"9c764535fb44470a8dc92fc74c8b835e": "E1c", "b17137fd304348d7a48532ba5db89270": "E3c"}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, encoding="utf-8", check=True).stdout


def commit_previo(repo: Path, referencia: str) -> str:
    """Commit inmediatamente anterior al que registró la primera revisión del paquete."""
    for linea in git(repo, "log", "--format=%H%x09%s").splitlines():
        sha, asunto = linea.split("\t", 1)
        if asunto.startswith(f"{referencia}: revisión 1"):
            return sha + "^"
    raise LookupError(f"sin commit de revisión 1 para {referencia}")


def archivo(repo: Path, rev: str, ruta: str) -> str | None:
    r = subprocess.run(["git", "show", f"{rev}:{ruta}"], cwd=repo, capture_output=True, text=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else None


def carpeta(repo: Path, rev: str, ruta: str) -> dict[str, str]:
    r = subprocess.run(["git", "ls-tree", "--name-only", f"{rev}:{ruta}"], cwd=repo, capture_output=True, text=True, encoding="utf-8")
    return {n: archivo(repo, rev, f"{ruta}/{n}") or "" for n in r.stdout.split()} if r.returncode == 0 else {}


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    db = MongoClient("mongodb://localhost:27017")["loom"]
    for pid, nombre in PROYECTOS.items():
        repo = TARGET / pid
        arquitectura_hoy = {p.name: p.read_text(encoding="utf-8") for p in (repo / "arquitectura").glob("*")}
        for r in sorted((r for r in db.revisiones.find({"proyecto_id": pid, "tipo": "revision"}) if str(r.get("ronda")) == "1"),
                        key=lambda r: r["fecha"]):
            ref, grupo, pt = r["referencia"], r["grupo"], r["pt"]
            rev = commit_previo(repo, ref)
            p = db.paquetes.find_one({"proyecto_id": pid, "grupo": grupo, "id": pt})
            hu = db.hus.find_one({"proyecto_id": pid, "id": grupo}) if grupo != "BASE" else None
            cambios = []
            if (archivo(repo, rev, f"{grupo}/paquetes/{pt}.md") or "").strip() != (p.get("md") or "").strip():
                cambios.append("paquete")
            if hu:
                if (archivo(repo, rev, f"{grupo}/spec.md") or "").strip() != (hu.get("spec_md") or "").strip():
                    cambios.append("spec")
                if (archivo(repo, rev, f"{grupo}/test-cases.md") or "").strip() != (hu.get("test_cases_md") or "").strip():
                    cambios.append("casos")
            if carpeta(repo, rev, "arquitectura") != arquitectura_hoy:
                cambios.append("arquitectura")
            print(f"{nombre} {ref:14} {rev[:8]}  {'difiere: ' + ', '.join(cambios) if cambios else 'igual'}")


if __name__ == "__main__":
    main()
