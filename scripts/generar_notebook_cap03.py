#!/usr/bin/env python3
"""Genera el cuaderno de R del capítulo 3 a partir de su fuente Quarto."""

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
qmd = project / "03-numeros-complejos.qmd"
text = qmd.read_text(encoding="utf-8")

text = text.replace(
    "# Números complejos\n",
    "# Capítulo 3. Números complejos con R\n\n"
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

cells = []
buffer = []
mode = "markdown"


def flush(kind):
    global buffer
    value = "\n".join(buffer).strip()
    if value:
        cells.append(code_cell(value) if kind == "r" else markdown_cell(value))
    buffer = []


for line in text.splitlines():
    stripped = line.strip()
    if mode == "markdown" and stripped == "~~~{r}":
        flush("markdown")
        mode = "r"
    elif mode == "r" and stripped == "~~~":
        flush("r")
        mode = "markdown"
    elif mode == "markdown" and stripped == "~~~text":
        mode = "text"
    elif mode == "text" and stripped == "~~~":
        mode = "markdown"
    elif mode == "text":
        buffer.append("    " + line)
    else:
        buffer.append(line)

flush("r" if mode == "r" else "markdown")

cells.append(markdown_cell("""
## Autoevaluación computacional

Las comprobaciones siguientes deben terminar sin error. Si alguna falla después de modificar el cuaderno, revise las definiciones, los cuadrantes y la tolerancia numérica.
"""))
cells.append(code_cell("""
stopifnot(
  abs(distancia(c(-2, 3), c(4, -1)) - sqrt(52)) < 1e-12,
  abs(cartesiana_polar(3, 4)$r - 5) < 1e-12,
  abs(polar_cartesiana(2, 5 * pi / 6)$x + sqrt(3)) < 1e-12,
  iguales_vectores(c(1, 2) + c(3, 4), c(4, 6)),
  Mod(3 + 4i) == 5,
  Conj(3 + 4i) == 3 - 4i,
  Mod(dividir_complejos(2 + 3i, 1 - 2i) * (1 - 2i) - (2 + 3i)) < 1e-12,
  Mod(potencia_demoivre(1 + 1i, 8) - 16) < 1e-10,
  max(Mod(raices_n(1, 6)^6 - 1)) < 1e-10
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
            "name": "Capítulo 3 - Números complejos con R.ipynb",
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

target = project / "notebooks" / "capitulo-03-numeros-complejos-R.ipynb"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(
    json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
    encoding="utf-8",
)
print(target)
