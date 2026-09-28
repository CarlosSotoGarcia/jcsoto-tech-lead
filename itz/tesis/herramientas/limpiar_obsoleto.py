"""Quita de una versión generada de la tesis (`Loom - Tesis vNN.docx`) el contenido obsoleto que la copia de trabajo arrastra
FUERA de los controles de contenido: el capítulo 5 y los anexos del primer piloto (E2, 2026-09-19), escritos antes de que la
tesis se llenara por controles, y la referencia de ejemplo de la plantilla.

Uso (después de `llenar_tesis.py`):
    python herramientas/limpiar_obsoleto.py "Loom - Tesis v02.docx"

Criterio: en los tramos que siguen a los controles `tesis_5_1`, `tesis_5_2`, `tesis_referencias` y `tesis_anexos` se conserva
solo lo que aparece tal cual en la guía oficial (títulos de capítulo, instrucciones de la plantilla, párrafos vacíos) y se
elimina lo demás; nunca se toca un párrafo que cierre una sección de Word. La copia de trabajo y la guía no se modifican."""

import re
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
TRAMOS = {"tesis_5_1", "tesis_5_2", "tesis_referencias", "tesis_anexos"}
EJEMPLO_PLANTILLA = "Mapachez itz"


def _texto(elemento: str) -> str:
    sin_campos = re.sub(r"<w:instrText[^>]*>[^<]*</w:instrText>", "", elemento)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", sin_campos)).strip()


def main(docx: str) -> None:
    ruta = Path(docx)
    guia_xml = zipfile.ZipFile(RAIZ / "GUIA PARA ESTRUCTURA DE TESIS.docx").read("word/document.xml").decode("utf-8")
    guia = {_texto(p) for p in re.findall(r"<w:p[ >].*?</w:p>", guia_xml, flags=re.S)}
    with zipfile.ZipFile(ruta) as z:
        xml = z.read("word/document.xml").decode("utf-8")
        otros = {n: z.read(n) for n in z.namelist() if n != "word/document.xml"}
        orden = z.namelist()
    inicio = xml.find("<w:body>") + len("<w:body>")
    fin = xml.rfind("</w:body>")
    cuerpo = xml[inicio:fin]
    elementos = re.findall(
        r"<w:sdt>.*?</w:sdt>|<w:p(?:\s[^>]*)?/>|<w:p(?:\s[^>]*)?>.*?</w:p>|<w:tbl>.*?</w:tbl>|<w:sectPr[ >].*?</w:sectPr>|<w:bookmark(?:Start|End)[^>]*/>",
        cuerpo, flags=re.S,
    )
    if "".join(elementos) != cuerpo:
        raise SystemExit("El cuerpo tiene elementos que este script no reconoce; no se modifica nada.")
    tag, conservados, quitados = None, [], {"parrafos": 0, "tablas": 0, "imagenes": 0}
    for e in elementos:
        if e.startswith("<w:sdt>"):
            m = re.search(r'<w:tag w:val="([^"]+)"/>', e)
            tag = m.group(1) if m else None
            conservados.append(e)
            continue
        t = _texto(e)
        # Las figuras vigentes viven dentro de los controles; una imagen suelta en estos tramos es del piloto viejo.
        obsoleto = tag in TRAMOS and "<w:sectPr" not in e and ("<w:drawing>" in e or t not in guia or EJEMPLO_PLANTILLA in t)
        if obsoleto:
            quitados["tablas" if e.startswith("<w:tbl>") else "parrafos"] += 1
            quitados["imagenes"] += e.count("<w:drawing>")
        else:
            conservados.append(e)
    xml = xml[:inicio] + "".join(conservados) + xml[fin:]
    from lxml import etree

    etree.fromstring(xml.encode("utf-8"))
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        for n in orden:
            z.writestr(n, xml.encode("utf-8") if n == "word/document.xml" else otros[n])
    print(f"Quitados fuera de los controles: {quitados['parrafos']} párrafos, {quitados['tablas']} tablas, {quitados['imagenes']} imágenes")


if __name__ == "__main__":
    main(sys.argv[1])
