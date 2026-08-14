#!/usr/bin/env python3
"""Genera el cuaderno de R del capítulo 5 a partir de su fuente Quarto."""

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
qmd = project / "05-metodos-raices.qmd"
text = qmd.read_text(encoding="utf-8")

text = text.replace(
    "# Métodos numéricos para la estimación de raíces\n",
    "# Capítulo 5. Métodos numéricos para la estimación de raíces con R\n\n"
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

Las comprobaciones deben terminar sin error. Si alguna falla después de modificar el cuaderno, revise el orden de los coeficientes, los intervalos y las tolerancias.
"""))
cells.append(code_cell("""
stopifnot(
  cota_cauchy(c(1, 1, -7, -1, 6)) == 8,
  evaluar_horner(c(1, 0, -1, -1), 1) == -1,
  evaluar_horner(c(1, 0, -1, -1), 2) == 5,
  contar_raices_sturm(c(1, 0, -1, 0), -2, 2) == 3,
  identical(descartes(c(1, 1, -7, -1, 6))$posibles_positivas, c(2L, 0L)),
  nrow(biseccion(c(1, 0, -1, -1), 1, 2, tol = 1e-8)) <= 30,
  abs(tail(secante(c(1, 0, -1, -1), 1, 2, tol = 1e-10)$fx, 1)) < 1e-8,
  abs(tail(newton_horner(c(1, 0, -1, -1), 1.5, tol = 1e-12)$fx, 1)) < 1e-10,
  abs(horner_valor_derivada(c(1, 0, -1, -1), 1.5)["valor"] - 0.875) < 1e-12,
  abs(horner_valor_derivada(c(1, 0, -1, -1), 1.5)["derivada"] - 5.75) < 1e-12
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
            "name": "Capítulo 5 - Métodos para raíces con R.ipynb",
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

target = project / "notebooks" / "capitulo-05-metodos-raices-R.ipynb"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(
    json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
    encoding="utf-8",
)
print(target)
