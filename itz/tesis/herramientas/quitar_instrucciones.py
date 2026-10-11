"""Quita de una versión generada de la tesis lo que el autor y la dirección decidieron retirar de la plantilla:

1. Instrucciones sueltas (`instrucciones_quitadas.json`): las definiciones de cada sección («El resumen debe:», «Objetivo
   general. Es lo que pretendemos…», «Es la Bibliografía en formato IEEE», etc.). Salieron de comparar la v04 generada con la
   copia que el autor limpió a mano el 2026-10-03; para retirar otra se agrega su texto exacto a la lista. Un párrafo se borra si
   su texto coincide completo con uno de la lista; si cierra una sección de Word o es el único párrafo de su celda o control,
   solo se vacía.
2. Apartados completos (`secciones_quitadas.json`, «apartados»): el título del apartado y su control de contenido, como 1.6
   Hipótesis y 1.7 Variables (ADR-0093).
3. Tramos de varias páginas (`secciones_quitadas.json`, «tramos»): todos los párrafos del cuerpo desde el que dice «desde» hasta
   el que dice «hasta», más los párrafos vacíos que los rodean, sin tocar los que cierran una sección de Word. Así se quitan las
   páginas de la guía institucional antes del índice sin dejar una hoja en blanco.

Uso (después de `limpiar_obsoleto.py` y antes de `marcar_instrucciones.py`):
    python herramientas/quitar_instrucciones.py "Loom - Tesis v05.docx"
"""

import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

from lxml import etree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
LISTA = Path(__file__).with_name("instrucciones_quitadas.json")
SECCIONES = Path(__file__).with_name("secciones_quitadas.json")


def _norm(texto: str) -> str:
    # NFC: la plantilla trae acentos descompuestos («o» + acento combinado) en algunos párrafos.
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", texto)).strip()


def _texto(p) -> str:
    return _norm("".join(t.text or "" for t in p.iter(W + "t")))


def _cierra_seccion(p) -> bool:
    return p.find(f"{W}pPr/{W}sectPr") is not None


def _quitar_instrucciones(raiz, objetivo: set[str]) -> tuple[int, int, set[str]]:
    borrados, vaciados, vistos = 0, 0, set()
    for p in list(raiz.iter(W + "p")):
        texto = _texto(p)
        if texto not in objetivo:
            continue
        vistos.add(texto)
        padre = p.getparent()
        unico = sum(1 for h in padre if h.tag == W + "p") == 1 and padre.tag in (W + "tc", W + "sdtContent")
        if _cierra_seccion(p) or unico:
            for hijo in [h for h in p if h.tag != W + "pPr"]:
                p.remove(hijo)
            vaciados += 1
        else:
            padre.remove(p)
            borrados += 1
    return borrados, vaciados, vistos


def _quitar_apartados(cuerpo, apartados: list[dict]) -> list[str]:
    quitados = []
    for a in apartados:
        titulo = next((p for p in cuerpo if p.tag == W + "p" and _texto(p) == _norm(a["titulo"])), None)
        control = next((s for s in cuerpo if s.tag == W + "sdt"
                        and (t := s.find(f"{W}sdtPr/{W}tag")) is not None and t.get(W + "val") == a["control"]), None)
        for e in (titulo, control):
            if e is not None and not (e.tag == W + "p" and _cierra_seccion(e)):
                cuerpo.remove(e)
        if titulo is not None or control is not None:
            quitados.append(a["control"])
    return quitados


def _quitar_tramos(cuerpo, tramos: list[dict]) -> int:
    total = 0
    for tr in tramos:
        hijos = list(cuerpo)
        ini = next((i for i, e in enumerate(hijos) if e.tag == W + "p" and _texto(e) == _norm(tr["desde"])), None)
        fin = next((i for i, e in enumerate(hijos) if e.tag == W + "p" and _texto(e) == _norm(tr["hasta"])), None)
        if ini is None or fin is None or fin < ini:
            continue
        vacio = lambda e: e.tag == W + "p" and not _texto(e) and not _cierra_seccion(e) and e.find(f".//{W}drawing") is None
        while ini > 0 and vacio(hijos[ini - 1]):
            ini -= 1
        while fin + 1 < len(hijos) and vacio(hijos[fin + 1]):
            fin += 1
        for e in hijos[ini:fin + 1]:
            if e.tag == W + "p" and not _cierra_seccion(e):
                cuerpo.remove(e)
                total += 1
    return total


def main(docx: str) -> None:
    ruta = Path(docx)
    objetivo = {_norm(t) for t in json.loads(LISTA.read_text(encoding="utf-8"))}
    secciones = json.loads(SECCIONES.read_text(encoding="utf-8")) if SECCIONES.exists() else {}
    with zipfile.ZipFile(ruta) as z:
        raiz = etree.fromstring(z.read("word/document.xml"))
        otros = {n: z.read(n) for n in z.namelist() if n != "word/document.xml"}
        orden = z.namelist()
    cuerpo = raiz.find(W + "body")
    apartados = _quitar_apartados(cuerpo, secciones.get("apartados", []))
    en_tramos = _quitar_tramos(cuerpo, secciones.get("tramos", []))
    borrados, vaciados, vistos = _quitar_instrucciones(raiz, objetivo)
    xml = etree.tostring(raiz, xml_declaration=True, encoding="UTF-8", standalone=True)
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        for n in orden:
            z.writestr(n, xml if n == "word/document.xml" else otros[n])
    faltan = objetivo - vistos
    print(f"Instrucciones de la plantilla quitadas: {borrados} párrafos borrados, {vaciados} vaciados"
          + (f"; {len(faltan)} textos de la lista no aparecen" if faltan else "")
          + f". Apartados quitados: {', '.join(apartados) or 'ninguno'}. Párrafos quitados en tramos: {en_tramos}.")


if __name__ == "__main__":
    main(sys.argv[1])
