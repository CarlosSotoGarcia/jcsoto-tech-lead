"""Resalta en amarillo lo que parece instrucción y no texto de la tesis, para quitarlo o sustituirlo antes de entregar.

    python herramientas/marcar_instrucciones.py "Loom - Tesis vNN.docx"

Se corre después de llenar_tesis.py y limpiar_obsoleto.py. Marca cinco clases de texto:

1. plantilla: párrafos de la guía institucional fuera de los controles de contenido, desde «AGRADECIMIENTOS» (qué va en cada
   sección, reglas de formato); no marca títulos, leyendas ni campos de índice;
2. marcador: el texto de guía de los controles que siguen sin llenar («Qué escribir: …» de agradecimientos, resumen, abstract);
3. nota: notas de trabajo dentro de los controles ya llenos («[POR COMPLETAR: …]», «Pendiente de integrar»);
4. dato: datos por sustituir en la portada y el oficio (título, nombres, fecha, número de oficio);
5. frase: notas de trabajo dentro de un párrafo que sí es texto de la tesis (una cita pendiente, «se integrarán…», «sujetas a
   validación con el director»). Solo se resalta la frase, no el párrafo.

No borra nada: solo agrega `<w:highlight w:val="yellow"/>` a los runs. Imprime cuántos párrafos o frases marcó de cada clase."""

import copy
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


# Notas de trabajo dentro de un párrafo de contenido: se resalta solo lo que casa.
_FRASES = [
    re.compile(r"\[(CITA PENDIENTE|POR COMPLETAR|NOTA DE BORRADOR)[^\]]*\]"),
    re.compile(r"(y )?est[áa]n? sujet[ao]s? a validaci[óo]n con el director[^.]*"),
    re.compile(r"[^.]*\bse integrar[áa]n?\b[^.]*\."),
    re.compile(r"[^.]*\b(pendiente de confirmar|por definir con el director|debe confirmarse)\b[^.]*\."),
]


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


def _poner_highlight(r, etree) -> None:
    rpr = r.find(W + "rPr")
    if rpr is None:
        rpr = etree.Element(W + "rPr")
        r.insert(0, rpr)
    if rpr.find(W + "highlight") is not None:
        return
    h = etree.Element(W + "highlight")
    h.set(W + "val", "yellow")
    despues = next((c for c in rpr if c.tag in _DESPUES_DE_HIGHLIGHT), None)
    if despues is None:
        rpr.append(h)
    else:
        despues.addprevious(h)


def _resaltar_frases(p, etree) -> list[str]:
    """Resalta dentro del párrafo lo que casa con `_FRASES`, partiendo los runs donde haga falta. Devuelve lo resaltado."""
    runs = [r for r in p.iter(W + "r") if len(r.findall(W + "t")) == 1 and all(c.tag in (W + "rPr", W + "t") for c in r)]
    texto = "".join(r.find(W + "t").text or "" for r in runs)
    tramos = sorted({(m.start() + len(m.group(0)) - len(m.group(0).lstrip()), m.end()) for pat in _FRASES for m in pat.finditer(texto)})
    if not tramos:
        return []
    inicio = 0
    for r in runs:
        t = r.find(W + "t").text or ""
        a, b = inicio, inicio + len(t)
        inicio = b
        cortes = sorted({a, b} | {x for m0, m1 in tramos for x in (m0, m1) if a < x < b})
        piezas = [(c0, c1) for c0, c1 in zip(cortes, cortes[1:]) if c1 > c0]
        nuevos = []
        for c0, c1 in piezas:
            pieza = copy.deepcopy(r)
            nodo = pieza.find(W + "t")
            nodo.text = t[c0 - a:c1 - a]
            nodo.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            if any(m0 <= c0 and c1 <= m1 for m0, m1 in tramos):
                _poner_highlight(pieza, etree)
            nuevos.append(pieza)
        if len(nuevos) == 1 and nuevos[0].find(W + "rPr/" + W + "highlight") is None:
            continue
        for pieza in nuevos:
            r.addprevious(pieza)
        r.getparent().remove(r)
    return [texto[m0:m1] for m0, m1 in tramos]


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
                else:
                    for frase in _resaltar_frases(p, etree):
                        marcados["frase"] += 1
                        ejemplos.setdefault("frase", []).append(frase[:70])

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
