#!/usr/bin/env python3
"""Validaciones reproducibles para la edición estable del libro."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {
    "Examen Parcial 1 Algebra Superior (13-09-2017).pdf",
    "Tarea 1.pdf",
    "Preimer Examen Algebra Superior (05-09-2024).pdf",
}
RAW_MARKERS = (
    "::: {.content-visible",
    "~~~text",
    chr(96) * 3 + "{.r}",
    "## Operaciones con vectores en $",
)
STABLE_DEV_TOKEN = "libro-algebra-superior-r-geogebra-dev"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.images_without_alt: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.links.append(("href", values["href"] or ""))
        if tag in {"img", "script", "iframe"} and values.get("src"):
            self.links.append(("src", values["src"] or ""))
        if tag == "link" and values.get("href"):
            self.links.append(("href", values["href"] or ""))
        if tag == "img" and not (values.get("alt") or "").strip():
            self.images_without_alt.append(values.get("src") or "(sin src)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def qmd_files() -> list[Path]:
    return sorted(ROOT.glob("*.qmd"))


def check_sources(errors: list[str]) -> None:
    for name in EXCLUDED:
        if any(path.is_file() for path in ROOT.rglob(name)):
            fail(errors, f"Material de evaluación presente en el repositorio: {name}")

    if not (ROOT / "LICENSE").is_file():
        fail(errors, "Falta el archivo LICENSE en la raíz.")

    for path in qmd_files():
        text = path.read_text(encoding="utf-8")
        if STABLE_DEV_TOKEN in text:
            fail(errors, f"{path.name}: contiene un enlace al repositorio de desarrollo.")

        open_fence: tuple[str, int, int] | None = None
        for line_number, line in enumerate(text.splitlines(), 1):
            match = re.match(r"^\s*([~\x60]{3,})(?:.*)$", line)
            if not match:
                continue
            marker = match.group(1)
            if len(set(marker)) != 1:
                continue
            if open_fence is None:
                open_fence = (marker[0], len(marker), line_number)
            elif marker[0] == open_fence[0] and len(marker) >= open_fence[1]:
                open_fence = None
        if open_fence:
            fail(errors, f"{path.name}:{open_fence[2]}: bloque cercado sin cierre compatible.")

        for match in re.finditer(r"!\[[^\n]*?\]\([^)]+\)\{([^}\n]*)\}", text):
            if "fig-alt=" not in match.group(1):
                line = text.count("\n", 0, match.start()) + 1
                fail(errors, f"{path.name}:{line}: figura sin fig-alt.")

        for match in re.finditer(r"\(([^)\s]+\.qmd)(#[^)\s]+)?\)", text):
            target = ROOT / unquote(match.group(1))
            if not target.is_file():
                fail(errors, f"{path.name}: enlace a archivo inexistente: {match.group(1)}")
                continue
            if match.group(2):
                anchor = match.group(2)[1:]
                target_text = target.read_text(encoding="utf-8")
                if f"#{{{anchor}}}" not in target_text and f"#{anchor}}}" not in target_text:
                    fail(errors, f"{path.name}: ancla inexistente: {match.group(1)}#{anchor}")

    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    for path in notebooks:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            fail(errors, f"{path.relative_to(ROOT)}: JSON inválido: {exc}")
            continue
        if data.get("nbformat") != 4 or not isinstance(data.get("cells"), list):
            fail(errors, f"{path.relative_to(ROOT)}: estructura de cuaderno inválida.")

    ggb_dir = ROOT / "interactivos" / "geogebra"
    if ggb_dir.is_dir():
        for dependency in (
            ROOT / "interactivos" / "geogebra-common.js",
            ROOT / "interactivos" / "geogebra-common.css",
        ):
            if not dependency.is_file():
                fail(errors, f"Falta la dependencia GeoGebra {dependency.name}.")
        required = {
            "localizacion-acotacion-raices.ggb",
            "metodo-biseccion.ggb",
            "secante-newton.ggb",
        }
        present = {path.name for path in ggb_dir.glob("*.ggb")}
        missing = sorted(required - present)
        if missing:
            fail(errors, "Faltan construcciones GeoGebra: " + ", ".join(missing))
        for path in sorted(ggb_dir.glob("*.ggb")):
            try:
                with zipfile.ZipFile(path) as archive:
                    if "geogebra.xml" not in archive.namelist():
                        fail(errors, f"{path.relative_to(ROOT)} no contiene geogebra.xml.")
                    else:
                        archive.read("geogebra.xml")
            except zipfile.BadZipFile:
                fail(errors, f"{path.relative_to(ROOT)} no es un archivo .ggb válido.")


def parse_html(path: Path) -> LinkParser:
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser


def check_rendered(errors: list[str]) -> None:
    docs = ROOT / "docs"
    if not (docs / "index.html").is_file():
        fail(errors, "No existe docs/index.html; ejecute quarto render.")
        return

    html_files = sorted(docs.rglob("*.html"))
    parsed = {path.resolve(): parse_html(path) for path in html_files}
    for path in html_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        if STABLE_DEV_TOKEN in text:
            fail(errors, f"{path.relative_to(ROOT)} contiene un enlace de desarrollo.")
        if any(marker in text for marker in RAW_MARKERS):
            fail(errors, f"{path.relative_to(ROOT)} contiene marcado fuente sin procesar.")

        parser = parsed[path.resolve()]
        for image in parser.images_without_alt:
            fail(errors, f"{path.relative_to(ROOT)}: imagen sin texto alternativo: {image}")

        for _, url in parser.links:
            if not url or url.startswith(("#", "data:", "mailto:", "javascript:")):
                continue
            parts = urlsplit(url)
            if parts.scheme or parts.netloc:
                continue
            if parts.path.startswith("/"):
                fail(errors, f"{path.relative_to(ROOT)}: enlace absoluto incompatible con GitHub Project Pages: {url}")
                continue
            target = (path.parent / unquote(parts.path)).resolve() if parts.path else path.resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                fail(errors, f"{path.relative_to(ROOT)}: recurso local inexistente: {url}")
                continue
            if parts.fragment and target.suffix.lower() == ".html":
                target_parser = parsed.get(target)
                if target_parser is None:
                    target_parser = parse_html(target)
                    parsed[target] = target_parser
                if unquote(parts.fragment) not in target_parser.ids:
                    fail(errors, f"{path.relative_to(ROOT)}: ancla local inexistente: {url}")


def extract_qmd_r(path: Path) -> str:
    code: list[str] = []
    inside = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if not inside and re.match(r"^\s*\x60{3}\{\.r", line):
            inside = True
            continue
        if inside and re.match(r"^\s*\x60{3}\s*$", line):
            inside = False
            code.append("")
            continue
        if inside:
            code.append(line)
    return "\n".join(code)


def run_r_file(label: str, code: str, errors: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="algebra-r-") as tmp:
        script = Path(tmp) / "test.R"
        script.write_text(
            "options(device=function(...) pdf(file=file.path(tempdir(),'plot.pdf')))\n"
            "set.seed(20260814)\n" + code + "\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            ["Rscript", "--vanilla", str(script)],
            cwd=tmp,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if result.returncode:
            tail = "\n".join(result.stdout.splitlines()[-20:])
            fail(errors, f"{label}: R terminó con código {result.returncode}.\n{tail}")


def check_r(errors: list[str]) -> None:
    if shutil.which("Rscript") is None:
        fail(errors, "Se solicitó --run-r, pero Rscript no está instalado.")
        return

    for path in sorted(ROOT.glob("0[1-5]-*.qmd")):
        code = extract_qmd_r(path)
        if code.strip():
            run_r_file(path.name, code, errors)

    for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
        data = json.loads(path.read_text(encoding="utf-8"))
        code = "\n\n".join(
            "".join(cell.get("source", []))
            for cell in data["cells"]
            if cell.get("cell_type") == "code"
        )
        if code.strip():
            run_r_file(str(path.relative_to(ROOT)), code, errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rendered", action="store_true", help="revisar también docs/")
    parser.add_argument("--run-r", action="store_true", help="ejecutar bloques y cuadernos con Rscript")
    args = parser.parse_args()

    errors: list[str] = []
    check_sources(errors)
    if args.rendered:
        check_rendered(errors)
    if args.run_r:
        check_r(errors)

    if errors:
        print("VALIDACIÓN FALLIDA", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1
    print("Validación completada sin errores.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
