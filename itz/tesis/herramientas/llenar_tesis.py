"""Llena los controles de contenido de la copia de trabajo de la tesis (`Loom - Tesis vNN.docx`) con los borradores en Markdown ligero.

Uso:
    python herramientas/llenar_tesis.py "Loom - Tesis v01.docx" borrador/v01

Cada archivo `.md` de la carpeta puede traer varias secciones, cada una encabezada por `@@ <tag del control>` (por ejemplo
`@@ tesis_1_1`). Formato dentro de una sección:

    Párrafo normal, con *cursiva* y `código` en línea.
    ### Subtítulo con su número escrito a mano
    TABLA: Título de la tabla        (sin título: `TABLA:`; se numera Tabla <capítulo>.<n> con campo SEQ)
    | Encabezado 1 | Encabezado 2 |
    | dato | dato |
    TABLA-ADR:                       (tabla de registros de decisión, generada de itz/arquitectura/decisiones/)

Solo se tocan los controles cuyo tag aparece en los borradores; lo demás del documento queda igual. La guía original nunca se edita.
"""

import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parents[1]
DECISIONES = RAIZ.parent / "arquitectura" / "decisiones"
_contadores: dict[str, int] = {}


def capitulo_de(tag: str) -> str:
    m = re.match(r"tesis_(\d)_", tag)
    if m:
        return m.group(1)
    if tag == "tesis_cap2":
        return "2"
    return "0"


def _rpr(cursiva: bool = False, codigo: bool = False, negrita: bool = False, tam: int | None = None) -> str:
    partes = []
    if codigo:
        partes.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>')
    if negrita:
        partes.append("<w:b/>")
    if cursiva:
        partes.append("<w:i/>")
    if tam:
        partes.append(f'<w:sz w:val="{tam}"/>')
    return f"<w:rPr>{''.join(partes)}</w:rPr>" if partes else ""


def corridas(texto: str, tam: int | None = None, negrita: bool = False) -> str:
    """Runs de un párrafo: `*cursiva*` y `código`."""
    salida = []
    for trozo in re.split(r"(\*[^*\n]+\*|`[^`\n]+`)", texto):
        if not trozo:
            continue
        if trozo.startswith("*") and trozo.endswith("*") and len(trozo) > 2:
            cursiva, codigo, contenido = True, False, trozo[1:-1]
        elif trozo.startswith("`") and trozo.endswith("`") and len(trozo) > 2:
            cursiva, codigo, contenido = False, True, trozo[1:-1]
        else:
            cursiva, codigo, contenido = False, False, trozo
        salida.append(
            f'<w:r>{_rpr(cursiva, codigo, negrita, tam)}<w:t xml:space="preserve">{escape(contenido)}</w:t></w:r>'
        )
    return "".join(salida)


def parrafo(texto: str) -> str:
    return f"<w:p>{corridas(texto)}</w:p>"


def subtitulo(texto: str) -> str:
    return (
        '<w:p><w:pPr><w:pStyle w:val="Heading3"/><w:ind w:firstLine="0"/><w:jc w:val="left"/>'
        '<w:rPr><w:color w:val="000000"/><w:sz w:val="24"/></w:rPr></w:pPr>'
        f'<w:r><w:rPr><w:color w:val="000000"/><w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">{escape(texto)}</w:t></w:r></w:p>'
    )


def leyenda(capitulo: str, titulo: str) -> str:
    _contadores[capitulo] = _contadores.get(capitulo, 0) + 1
    n = _contadores[capitulo]
    return (
        '<w:p><w:pPr><w:pStyle w:val="Caption"/><w:keepNext/><w:ind w:firstLine="0"/><w:jc w:val="left"/>'
        '<w:rPr><w:b w:val="0"/></w:rPr></w:pPr>'
        f'<w:r><w:t>Tabla {capitulo}.</w:t></w:r>'
        '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> SEQ Tabla \\s 1 </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        f'<w:r><w:rPr><w:noProof/></w:rPr><w:t>{n}</w:t></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
        f'{corridas(". " + titulo) if titulo else ""}</w:p>'
    )


def tabla(filas: list[list[str]], pesos: list[int] | None = None) -> str:
    columnas = len(filas[0])
    pesos = pesos or [1] * columnas
    total = sum(pesos)
    anchos = [round(5000 * p / total) for p in pesos]
    xml = [
        '<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders>'
        + "".join(f'<w:{lado} w:val="single" w:sz="4" w:space="0" w:color="auto"/>' for lado in ("top", "left", "bottom", "right", "insideH", "insideV"))
        + '</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="70" w:type="dxa"/><w:right w:w="70" w:type="dxa"/></w:tblCellMar>'
        '<w:tblLook w:val="0000" w:firstRow="0" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="0"/></w:tblPr>'
        "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{round(8554 * p / total)}"/>' for p in pesos) + "</w:tblGrid>"
    ]
    for i, fila in enumerate(filas):
        cabecera = i == 0
        xml.append("<w:tr><w:trPr><w:cantSplit/>" + ("<w:tblHeader/>" if cabecera else "") + "</w:trPr>")
        for j, celda in enumerate(fila):
            sombra = '<w:shd w:val="clear" w:color="auto" w:fill="E5E5ED"/>' if cabecera else ""
            xml.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{anchos[j]}" w:type="pct"/>{sombra}</w:tcPr>'
                '<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:ind w:firstLine="0"/><w:jc w:val="left"/>'
                f'<w:rPr>{"<w:b/>" if cabecera else ""}<w:sz w:val="17"/></w:rPr></w:pPr>{corridas(celda, tam=17, negrita=cabecera)}</w:p></w:tc>'
            )
        xml.append("</w:tr>")
    xml.append("</w:tbl>")
    xml.append('<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:ind w:firstLine="0"/></w:pPr></w:p>')
    return "".join(xml)


def filas_adr() -> list[list[str]]:
    filas = [["ADR", "Título"]]
    for f in sorted(DECISIONES.glob("[0-9][0-9][0-9][0-9]-*.md")):
        primera = f.read_text(encoding="utf-8").splitlines()[0]
        titulo = re.sub(r"^#\s*ADR-\d+:\s*", "", primera).strip()
        filas.append([f.name[:4], titulo])
    return filas


def bloques_a_xml(tag: str, texto: str) -> str:
    capitulo = capitulo_de(tag)
    lineas = texto.strip("\n").splitlines()
    salida, i = [], 0
    while i < len(lineas):
        linea = lineas[i].rstrip()
        if not linea:
            i += 1
        elif linea.startswith("### "):
            salida.append(subtitulo(linea[4:].strip()))
            i += 1
        elif linea.startswith("TABLA-ADR:"):
            salida.append(leyenda(capitulo, "Registros de decisión de arquitectura"))
            salida.append(tabla(filas_adr(), [1, 8]))
            i += 1
        elif linea.startswith("TABLA:"):
            titulo = linea[len("TABLA:"):].strip()
            filas = []
            i += 1
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                filas.append([c.strip() for c in lineas[i].strip().strip("|").split(" | ")])
                i += 1
            if titulo:
                salida.append(leyenda(capitulo, titulo))
            columnas = len(filas[0])
            pesos = [1] * columnas
            if columnas == 2 and filas[0][0].lower() == "sigla":
                pesos = [1, 5]
            salida.append(tabla(filas, pesos))
        else:
            salida.append(parrafo(linea))
            i += 1
    return "".join(salida)


def secciones(carpeta: Path) -> dict[str, str]:
    encontradas: dict[str, str] = {}
    for md in sorted(carpeta.glob("*.md")):
        actual, buffer = None, []
        for linea in md.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^@@\s+(\S+)\s*$", linea)
            if m:
                if actual:
                    encontradas[actual] = "\n".join(buffer)
                actual, buffer = m.group(1), []
            elif actual is not None:
                buffer.append(linea)
        if actual:
            encontradas[actual] = "\n".join(buffer)
    return encontradas


def cargar_referencias() -> dict[str, str]:
    refs = {}
    for linea in (RAIZ / "referencias-candidatas.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^- ([a-z0-9-]+) :: (.+?) :: (.+)$", linea)
        if m:
            refs[m.group(1)] = m.group(2)
    return refs


def resolver_citas(contenido: dict[str, str]) -> dict[str, str]:
    """Sustituye [N:clave] por [n] según el orden de primera aparición y genera la lista IEEE."""
    refs = cargar_referencias()
    numeros: dict[str, int] = {}
    pendientes: list[str] = []

    def sustituir(m: re.Match) -> str:
        clave = m.group(1)
        if clave not in refs:
            pendientes.append(clave)
            return f"[CITA PENDIENTE: {clave}]"
        numeros.setdefault(clave, len(numeros) + 1)
        return f"[{numeros[clave]}]"

    nuevo = {}
    for tag, texto in contenido.items():
        nuevo[tag] = texto if tag == "tesis_referencias" else re.sub(r"\[N:([a-z0-9-]+)\]", sustituir, texto)
    if "tesis_referencias" in nuevo:
        nuevo["tesis_referencias"] = "\n\n".join(f"[{n}] {refs[c]}" for c, n in numeros.items())
    print(f"{len(numeros)} referencias citadas; claves sin definir: {sorted(set(pendientes)) or 'ninguna'}")
    return nuevo


def main(docx: str, carpeta: str) -> None:
    ruta = Path(docx)
    with zipfile.ZipFile(ruta) as z:
        xml = z.read("word/document.xml").decode("utf-8")
        otros = {n: z.read(n) for n in z.namelist() if n != "word/document.xml"}
        orden = z.namelist()
    contenido = secciones(Path(carpeta))
    contenido = resolver_citas(contenido)
    hechas = []
    for tag, texto in contenido.items():
        patron = re.compile(r'(<w:sdt><w:sdtPr>(?:(?!</w:sdtPr>).)*?<w:tag w:val="' + re.escape(tag) + r'"/>(?:(?!</w:sdtPr>).)*?)</w:sdtPr><w:sdtEndPr/><w:sdtContent>.*?</w:sdtContent></w:sdt>', re.S)
        m = patron.search(xml)
        if not m:
            print("AVISO: no se encontró el control", tag)
            continue
        propiedades = m.group(1).replace("<w:showingPlcHdr/>", "")
        nuevo = f"{propiedades}</w:sdtPr><w:sdtEndPr/><w:sdtContent>{bloques_a_xml(tag, texto)}</w:sdtContent></w:sdt>"
        xml = xml[: m.start()] + nuevo + xml[m.end():]
        palabras = len(re.findall(r"\w+", re.sub(r"^(TABLA.*|\|.*|@@.*)$", "", texto, flags=re.M)))
        hechas.append((tag, palabras))
    from lxml import etree

    etree.fromstring(xml.encode("utf-8"))  # falla si el XML quedó mal formado
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        for n in orden:
            z.writestr(n, xml.encode("utf-8") if n == "word/document.xml" else otros[n])
    total = sum(p for _, p in hechas)
    for tag, palabras in hechas:
        print(f"{tag:22} {palabras:>6} palabras")
    print(f"TOTAL {total} palabras (aprox. {total / 280:.0f} cuartillas de ~280 palabras) en {len(hechas)} secciones")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
