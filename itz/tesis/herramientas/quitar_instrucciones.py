"""Quita de una versión generada de la tesis las instrucciones de la plantilla que el autor decidió retirar (definiciones de
cada sección: «El resumen debe:», «Objetivo general. Es lo que pretendemos…», «Es la Bibliografía en formato IEEE», etc.).

Uso (después de `limpiar_obsoleto.py` y antes de `marcar_instrucciones.py`):
    python herramientas/quitar_instrucciones.py "Loom - Tesis v04.docx"

La lista de textos está en `instrucciones_quitadas.json` y salió de comparar la v04 generada con la copia que el autor limpió a
mano el 2026-10-03; para retirar otra instrucción se agrega su texto exacto a esa lista. Un párrafo se borra si su texto coincide
completo con uno de la lista; si cierra una sección de Word o es el único párrafo de su celda o control, solo se vacía."""

import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

from lxml import etree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
LISTA = Path(__file__).with_name("instrucciones_quitadas.json")


def _norm(texto: str) -> str:
    # NFC: la plantilla trae acentos descompuestos («o» + acento combinado) en algunos párrafos.
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", texto)).strip()


def main(docx: str) -> None:
    ruta = Path(docx)
    objetivo = {_norm(t) for t in json.loads(LISTA.read_text(encoding="utf-8"))}
    with zipfile.ZipFile(ruta) as z:
        raiz = etree.fromstring(z.read("word/document.xml"))
        otros = {n: z.read(n) for n in z.namelist() if n != "word/document.xml"}
        orden = z.namelist()
    borrados, vaciados, vistos = 0, 0, set()
    for p in list(raiz.iter(W + "p")):
        texto = _norm("".join(t.text or "" for t in p.iter(W + "t")))
        if texto not in objetivo:
            continue
        vistos.add(texto)
        padre = p.getparent()
        unico = sum(1 for h in padre if h.tag == W + "p") == 1 and padre.tag in (W + "tc", W + "sdtContent")
        if p.find(f"{W}pPr/{W}sectPr") is not None or unico:
            for hijo in [h for h in p if h.tag != W + "pPr"]:
                p.remove(hijo)
            vaciados += 1
        else:
            padre.remove(p)
            borrados += 1
    xml = etree.tostring(raiz, xml_declaration=True, encoding="UTF-8", standalone=True)
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        for n in orden:
            z.writestr(n, xml if n == "word/document.xml" else otros[n])
    faltan = objetivo - vistos
    print(f"Instrucciones de la plantilla quitadas: {borrados} párrafos borrados, {vaciados} vaciados"
          + (f"; {len(faltan)} textos de la lista no aparecen" if faltan else ""))


if __name__ == "__main__":
    main(sys.argv[1])
