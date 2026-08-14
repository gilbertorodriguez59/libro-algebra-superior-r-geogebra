#!/usr/bin/env python3
"""Genera el cuaderno de R del capítulo 2 a partir de su fuente Quarto."""

import json
import re
from pathlib import Path


def source_lines(text):
    text = text.strip()
    return text.splitlines(keepends=True) if text else []


def markdown_cell(text):
    return {"cell_type": "markdown", "metadata": {}, "source": source_lines(text)}


def code_cell(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_lines(text),
    }


project = Path(__file__).resolve().parents[1]
qmd = project / "02-enteros-reales.qmd"
text = qmd.read_text(encoding="utf-8")

text = text.replace(
    "# Números enteros y reales\n",
    "# Capítulo 2. Números enteros y reales con R\n\n"
    "**Álgebra Superior con aplicaciones en R y GeoGebra**  \n"
    "**Autor:** Jesús Gilberto Rodríguez Escobedo\n",
    1,
)

text = re.sub(r"^:::\s*\{[^\n]*\}\s*$", "", text, flags=re.MULTILINE)
text = re.sub(r"^:::\s*$", "", text, flags=re.MULTILINE)
text = re.sub(r"^<iframe[^\n]*</iframe>\s*$", "", text, flags=re.MULTILINE)
text = re.sub(r"\{\.btn[^}]*\}", "", text)
text = re.sub(r"^(#{1,6} .+?)\s+\{[^}]+\}\s*$", r"\1", text, flags=re.MULTILINE)
text = text.replace(
    "figures/",
    "https://raw.githubusercontent.com/gilbertorodriguez59/"
    "libro-algebra-superior-r-geogebra/main/figures/",
)
text = re.sub(
    r"\(interactivos/([^)]+)\)",
    r"(https://gilbertorodriguez59.github.io/"
    r"libro-algebra-superior-r-geogebra/interactivos/\1)",
    text,
)

parts = re.split(r"^~~~\{r\}\s*$|^~~~\s*$", text, flags=re.MULTILINE)
cells = []
for index, part in enumerate(parts):
    if not part.strip():
        continue
    cells.append(code_cell(part) if index % 2 else markdown_cell(part))

cells.append(markdown_cell("""
## Autoevaluación computacional

Las comprobaciones siguientes deben terminar sin error. Si alguna falla después de modificar el cuaderno, revise el algoritmo y las restricciones de dominio.
"""))
cells.append(code_cell("""
stopifnot(
  all(revisar_identidad(50L)$coincide),
  euclides(252L, 198L)$mcd == 18L,
  252L * euclides_extendido(252L, 198L)["x"] +
    198L * euclides_extendido(252L, 198L)["y"] == 18L,
  identical(factorizar(756L), c(2L, 2L, 3L, 3L, 3L, 7L)),
  mcd(840L, 378L) * mcm(840L, 378L) == 840L * 378L,
  iguales_aprox(0.1 + 0.2, 0.3),
  all(abs(x + y) <= abs(x) + abs(y) + 1e-12)
)
"""))
cells.append(markdown_cell("""
## Información de la sesión

Ejecute esta celda al terminar para registrar la versión de R utilizada.
"""))
cells.append(code_cell("sessionInfo()"))

notebook = {
    "cells": cells,
    "metadata": {
        "colab": {
            "name": "Capítulo 2 - Números enteros y reales con R.ipynb",
            "provenance": [],
        },
        "kernelspec": {"display_name": "R", "language": "R", "name": "ir"},
        "language_info": {
            "codemirror_mode": "r",
            "file_extension": ".r",
            "mimetype": "text/x-r-source",
            "name": "R",
            "pygments_lexer": "r",
            "version": "4.5",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

target = project / "notebooks" / "capitulo-02-enteros-reales-R.ipynb"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(
    json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
    encoding="utf-8",
)
print(target)
