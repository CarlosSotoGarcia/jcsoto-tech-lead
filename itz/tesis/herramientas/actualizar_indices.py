"""Llena el índice general y los índices de figuras, gráficas y tablas de una versión generada de la tesis.

Uso (al final, después de `marcar_instrucciones.py`; requiere Microsoft Word en Windows):
    python herramientas/actualizar_indices.py "Loom - Tesis v04.docx"

La plantilla arma el «Índice de Figuras» con el rótulo «Ilustración», pero `llenar_tesis.py` rotula las figuras como «Figura»;
primero se corrige ese campo en el XML. Después Word, invisible y sin control de cambios, actualiza solo los campos de índice
(TOC): los números de las leyendas (campos SEQ) quedan como los escribió `llenar_tesis.py`."""

import subprocess
import sys
import zipfile
from pathlib import Path

CAMPO_VIEJO = 'TOC \\h \\z \\c "Ilustración"'
CAMPO_NUEVO = 'TOC \\h \\z \\c "Figura"'

POWERSHELL = r"""
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open('__RUTA__', $false, $false, $false)
    $seguimiento = $doc.TrackRevisions
    $doc.TrackRevisions = $false
    foreach ($t in $doc.TablesOfContents) { $t.Update() }
    foreach ($t in $doc.TablesOfFigures) { $t.Update() }
    $doc.Repaginate()
    foreach ($t in $doc.TablesOfContents) { $t.UpdatePageNumbers() }
    foreach ($t in $doc.TablesOfFigures) { $t.UpdatePageNumbers() }
    $doc.TrackRevisions = $seguimiento
    Write-Output ("indices: " + $doc.TablesOfContents.Count + " general, " + $doc.TablesOfFigures.Count + " de figuras/graficas/tablas; paginas: " + $doc.ComputeStatistics(2))
    $doc.Save()
    $doc.Close()
} finally {
    $word.Quit()
}
"""


def main(docx: str) -> None:
    ruta = Path(docx).resolve()
    with zipfile.ZipFile(ruta) as z:
        xml = z.read("word/document.xml").decode("utf-8")
        otros = {n: z.read(n) for n in z.namelist() if n != "word/document.xml"}
        orden = z.namelist()
    if CAMPO_VIEJO in xml:
        xml = xml.replace(CAMPO_VIEJO, CAMPO_NUEVO)
        with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
            for n in orden:
                z.writestr(n, xml.encode("utf-8") if n == "word/document.xml" else otros[n])
    script = POWERSHELL.replace("__RUTA__", str(ruta).replace("'", "''"))
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script], capture_output=True, text=True, timeout=600)
    print(r.stdout.strip())
    if r.returncode != 0:
        raise SystemExit(r.stderr.strip())


if __name__ == "__main__":
    main(sys.argv[1])
