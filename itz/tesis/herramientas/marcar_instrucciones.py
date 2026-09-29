"""Resalta en amarillo lo que parece instrucción y no texto de la tesis, para quitarlo o sustituirlo antes de entregar.

    python herramientas/marcar_instrucciones.py "Loom - Tesis vNN.docx"

Se corre después de llenar_tesis.py y limpiar_obsoleto.py. Marca cuatro clases de párrafos:

1. plantilla: párrafos de la guía institucional fuera de los controles de contenido, desde «AGRADECIMIENTOS» (qué va en cada
   sección, reglas de formato); no marca títulos, leyendas ni campos de índice;
2. marcador: el texto de guía de los controles que siguen sin llenar («Qué escribir: …» de agradecimientos, resumen, abstract);
3. nota: notas de trabajo dentro de los controles ya llenos («[POR COMPLETAR: …]», «Pendiente de integrar»);
4. dato: datos por sustituir en la portada y el oficio (título, nombres, fecha, número de oficio).

No borra nada: solo agrega `<w:highlight w:val="yellow"/>` a los runs. Imprime cuántos párrafos marcó de cada clase."""

import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
# Hijos de w:rPr que van después de w:highlight en el esquema (CT_RPr); highlight se inserta antes del primero que aparezca.
_DESPUES_DE_HIGHLIGHT = {W + t for t in ("u", "effect", "bdr", "shd", "fitText", "vertAlign", "rtl", "cs", "em", "lang",
                                         "eastAsianLayout", "specVanish", "oMath", "rPrChange")}
_NOTAS = re.compile(r"^\[POR COMPLETAR|Pendiente de integrar")
_DATOS = re.compile(r"TÍTULO DEFINITIVO|NOMBRE COMPLETO|NOMBRE DEL O LA DIRECTOR|Mes Año|Oficio: XX|Nombre completo del tesista"
                    r"|a \d\d de \w+ del \d{4}")


def _texto(p) -> str:
    return "".join(t.text or "" for t in p.iter(W + "t")).strip()


def _estilo(p) -> str:
    st = p.find(W + "pPr/" + W + "pStyle")
    return st.get(W + "val") if st is not None else ""


def _es_campo(p) -> bool:
    return p.find(".//" + W + "instrText") is not None or p.find(".//" + W + "fldSimple") is not None


def _resaltar(p, etree) -> None:
    for r in p.iter(W + "r"):
        if r.find(W + "t") is None:
            continue
        rpr = r.find(W + "rPr")
        if rpr is None:
            rpr = etree.Element(W + "rPr")
            r.insert(0, rpr)
        if rpr.find(W + "highlight") is not None:
            continue
        h = etree.Element(W + "highlight")
        h.set(W + "val", "yellow")
        despues = next((c for c in rpr if c.tag in _DESPUES_DE_HIGHLIGHT), None)
        if despues is None:
            rpr.append(h)
        else:
            despues.addprevious(h)


def main(docx: str) -> None:
    from lxml import etree

    sys.stdout.reconfigure(encoding="utf-8")
    ruta = Path(docx)
    with zipfile.ZipFile(ruta) as z:
        partes = {n: z.read(n) for n in z.namelist()}
    root = etree.fromstring(partes["word/document.xml"])
    body = root.find(W + "body")
    marcados: Counter = Counter()
    ejemplos: dict[str, list[str]] = {}

    def marcar(p, clase: str) -> None:
        _resaltar(p, etree)
        marcados[clase] += 1
        ejemplos.setdefault(clase, []).append(_texto(p)[:70])

    en_cuerpo = False
    for el in body:
        if el.tag == W + "p":
            t = _texto(el)
            if not en_cuerpo and _estilo(el).startswith("Heading1") and t.upper().startswith("AGRADECIMIENTOS"):
                en_cuerpo = True
                continue
            if not t or _es_campo(el):
                continue
            estilo = _estilo(el)
            if en_cuerpo and not estilo.startswith(("Heading", "TOC", "Caption", "Title")):
                marcar(el, "plantilla")
            elif not en_cuerpo and _DATOS.search(t):
                marcar(el, "dato")
        elif el.tag == W + "sdt":
            contenido = el.find(W + "sdtContent")
            if contenido is None:
                continue
            placeholder = el.find(W + "sdtPr/" + W + "showingPlcHdr") is not None
            for p in contenido.iter(W + "p"):
                t = _texto(p)
                if not t or _es_campo(p):
                    continue
                if placeholder:
                    marcar(p, "marcador")
                elif _NOTAS.search(t):
                    marcar(p, "nota")

    partes["word/document.xml"] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    temporal = ruta.with_suffix(".tmp.docx")
    with zipfile.ZipFile(temporal, "w", zipfile.ZIP_DEFLATED) as z:
        for nombre, datos in partes.items():
            z.writestr(nombre, datos)
    temporal.replace(ruta)
    print("Párrafos resaltados en amarillo:", dict(marcados), "total", sum(marcados.values()))
    for clase, lista in ejemplos.items():
        print(f"  {clase}: " + " | ".join(lista[:3]) + (" …" if len(lista) > 3 else ""))


if __name__ == "__main__":
    main(sys.argv[1])
