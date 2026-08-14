#!/usr/bin/env python3
"""Genera el cuaderno de R del capítulo 4 a partir de la fuente Quarto."""

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
qmd = project / "04-polinomios.qmd"
text = qmd.read_text(encoding="utf-8")

text = text.replace(
    "# Polinomios\n",
    "# Capítulo 4. Polinomios con R y GeoGebra\n\n"
    "**Álgebra Superior con aplicaciones en R y GeoGebra**  \n"
    "**Autor:** Jesús Gilberto Rodríguez Escobedo\n",
    1,
)

# Quitar contenedores propios de Quarto y elementos incrustados que Colab no necesita.
text = re.sub(r"^:::\s*\{[^\n]*\}\s*$", "", text, flags=re.MULTILINE)
text = re.sub(r"^:::\s*$", "", text, flags=re.MULTILINE)
text = re.sub(r"^<iframe[^\n]*</iframe>\s*$", "", text, flags=re.MULTILINE)
text = re.sub(r"^<p><a[^\n]*</p>\s*$", "", text, flags=re.MULTILINE)
text = re.sub(r"\{\.btn[^}]*\}", "", text)
text = re.sub(r"^(#{1,6} .+?)\s+\{[^}]+\}\s*$", r"\1", text, flags=re.MULTILINE)

# Usar direcciones absolutas para que las figuras funcionen dentro de Colab.
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

Las comprobaciones siguientes deben terminar sin error. Una tolerancia pequeña evita confundir el redondeo numérico con una desigualdad matemática.
"""))
cells.append(code_cell("""
stopifnot(
  horner(c(2, -3, 0, 4, -5), 2) == 7,
  identical(sumar_polinomios(c(2, -1, 3), c(1, 4, -1)), c(3, 3, 2)),
  identical(multiplicar_polinomios(c(2, -1, 3), c(1, 4, -1)), c(2, 7, -3, 13, -3)),
  division_sintetica(c(2, -3, -11, 6), 3)$residuo == 0,
  multiplicidad_raiz(c(1, 1, -5, -1, 8, -4), 1) == 3,
  multiplicidad_raiz(c(1, 1, -5, -1, 8, -4), -2) == 2,
  max(Mod(vapply(polyroot(c(4, 0, -5, 0, 1)),
                 function(z) horner(c(1, 0, -5, 0, 4), z), complex(1)))) < 1e-8,
  max(abs(izquierda - derecha)) < 1e-12
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
            "name": "Capítulo 4 - Polinomios con R y GeoGebra.ipynb",
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

target = project / "notebooks" / "capitulo-04-polinomios-R.ipynb"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(target)
