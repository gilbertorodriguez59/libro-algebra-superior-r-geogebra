#!/usr/bin/env python3
"""Genera seis construcciones GeoGebra y sus páginas del capítulo 4."""

from pathlib import Path
from textwrap import dedent
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
INTERACTIVE = ROOT / "interactivos"
GGB_DIR = INTERACTIVE / "geogebra"
GGB_DIR.mkdir(parents=True, exist_ok=True)


CONSTRUCTIONS = [
    {
        "slug": "operaciones-polinomios",
        "title": "Operaciones con polinomios",
        "description": "Compare dos polinomios con su suma y su producto.",
        "expressions": [
            ("f", "x^3-4x", "function", "#2873a8"),
            ("g", "x^2-1", "function", "#2c7a5a"),
            ("s", "f+g", "function", "#b58a2a"),
            ("m", "f*g", "function", "#b4443c"),
        ],
    },
    {
        "slug": "division-residuo",
        "title": "División y teorema del residuo",
        "description": "Observe p(x), el divisor x-2 y el valor p(2).",
        "expressions": [
            ("p", "x^3-3x^2-4x+12", "function", "#2873a8"),
            ("d", "x-2", "function", "#2c7a5a"),
            ("A", "(2,p(2))", "point", "#b4443c"),
            ("a", "x=2", "line", "#b58a2a"),
        ],
    },
    {
        "slug": "raices-multiplicidad",
        "title": "Raíces y multiplicidad",
        "description": "Distinga cruce, contacto y aplanamiento en raíces múltiples.",
        "expressions": [
            ("f", "(x+2)*(x-1)^2*(x-3)^3/25", "function", "#2873a8"),
            ("A", "(-2,0)", "point", "#2c7a5a"),
            ("B", "(1,0)", "point", "#b58a2a"),
            ("C", "(3,0)", "point", "#b4443c"),
        ],
    },
    {
        "slug": "factorizacion-lineal",
        "title": "Factorización en factores lineales",
        "description": "Las intersecciones muestran las raíces de x⁴-5x²+4.",
        "expressions": [
            ("p", "x^4-5x^2+4", "function", "#2873a8"),
            ("A", "(-2,0)", "point", "#2c7a5a"),
            ("B", "(-1,0)", "point", "#b58a2a"),
            ("C", "(1,0)", "point", "#b58a2a"),
            ("D", "(2,0)", "point", "#2c7a5a"),
        ],
    },
    {
        "slug": "raices-conjugadas",
        "title": "Raíces complejas conjugadas",
        "description": "Visualice la simetría de 2+i y 2-i respecto del eje real.",
        "expressions": [
            ("z", "(2,1)", "point", "#2873a8"),
            ("w", "(2,-1)", "point", "#2c7a5a"),
            ("s", "Segment(z,w)", "segment", "#b4443c"),
            ("a", "x=2", "line", "#b58a2a"),
        ],
    },
    {
        "slug": "funciones-racionales",
        "title": "Funciones racionales",
        "description": "Explore un hueco, una asíntota vertical y una asíntota oblicua.",
        "expressions": [
            ("f", "If(x!=1,x+1)", "function", "#2873a8"),
            ("H", "(1,2)", "point", "#b4443c"),
            ("g", "(2x^2+1)/(x-1)", "function", "#2c7a5a"),
            ("a", "x=1", "line", "#b4443c"),
            ("b", "y=2x+2", "line", "#b58a2a"),
        ],
    },
]


def color_parts(value):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def geogebra_xml(spec):
    rows = []
    for label, expression, kind, color in spec["expressions"]:
        r, g, b = color_parts(color)
        rows.append(f'<expression label="{label}" exp="{expression}" type="{kind}"/>')
        point_style = '<pointSize val="6"/><pointStyle val="0"/>' if kind == "point" else ""
        rows.append(
            f'<element type="{kind}" label="{label}">'
            '<show object="true" label="true" ev="4"/>'
            f'<objColor r="{r}" g="{g}" b="{b}" alpha="0"/>'
            '<layer val="0"/><labelMode val="0"/>'
            f'{point_style}<lineStyle thickness="4" type="0" typeHidden="1"/>'
            '</element>'
        )
    content = "\n    ".join(rows)
    return dedent(
        f'''\
        <?xml version="1.0" encoding="utf-8"?>
        <geogebra format="5.0" version="6.0" app="graphing" platform="w" id="cap04-{spec['slug']}">
          <gui>
            <window width="1100" height="660"/>
            <perspectives>
              <perspective id="tmp">
                <panes><pane location="" divider="0.24" orientation="1"/></panes>
                <views>
                  <view id="1" visible="true" inframe="false" stylebar="true" location="1" size="700" window="100,100,700,550"/>
                  <view id="2" visible="true" inframe="false" stylebar="false" location="3" size="280" window="100,100,700,550"/>
                </views>
                <toolbar show="true" items="0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20" position="1" help="false"/>
                <input show="true" cmd="true" top="false"/>
              </perspective>
            </perspectives>
          </gui>
          <euclidianView>
            <viewNumber viewNo="1"/>
            <size width="800" height="600"/>
            <coordSystem xZero="400" yZero="300" scale="70" yscale="70"/>
            <evSettings axes="true" grid="true" gridIsBold="false" pointCapturing="3" rightAngleStyle="1" checkboxSize="26" gridType="3"/>
            <bgColor r="255" g="255" b="255"/>
            <axesColor r="90" g="110" b="130"/>
            <gridColor r="215" g="225" b="233"/>
            <lineStyle axes="1" grid="0"/>
            <axis id="0" show="true" label="x" unitLabel="" tickStyle="1" showNumbers="true"/>
            <axis id="1" show="true" label="y" unitLabel="" tickStyle="1" showNumbers="true"/>
          </euclidianView>
          <kernel><continuous val="false"/><usePathAndRegionParameters val="true"/></kernel>
          <construction title="{spec['title']}" author="Jesús Gilberto Rodríguez Escobedo" date="2026-08-10">
            {content}
          </construction>
        </geogebra>
        '''
    ).lstrip()


def html_page(spec):
    return dedent(
        f'''\
        <!doctype html>
        <html lang="es">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>{spec['title']}</title>
          <style>
            :root {{ --azul:#123b6d; --verde:#2c7a5a; --dorado:#b58a2a; }}
            * {{ box-sizing:border-box; }}
            body {{ margin:0; padding:1rem; font-family:system-ui, sans-serif; color:#18344f; background:#f7fbff; }}
            header {{ display:flex; gap:1rem; align-items:flex-start; justify-content:space-between; flex-wrap:wrap; margin-bottom:.75rem; }}
            h1 {{ margin:0 0 .25rem; color:var(--azul); font-size:1.35rem; }}
            p {{ margin:.15rem 0; }}
            a {{ display:inline-block; padding:.55rem .75rem; color:white; background:var(--verde); border-radius:.4rem; text-decoration:none; font-weight:700; }}
            #ggb-element {{ min-height:560px; background:white; border:1px solid #bed0df; border-radius:.5rem; overflow:hidden; }}
            .note {{ margin-top:.65rem; font-size:.92rem; color:#52687a; }}
          </style>
          <script src="https://www.geogebra.org/apps/deployggb.js"></script>
        </head>
        <body>
          <header>
            <div><h1>{spec['title']}</h1><p>{spec['description']}</p></div>
            <a href="geogebra/{spec['slug']}.ggb" download>Descargar construcción .ggb</a>
          </header>
          <div id="ggb-element" aria-label="Construcción interactiva de GeoGebra"></div>
          <p class="note">Puede mover la vista, cambiar objetos y abrir el archivo descargado en GeoGebra Classic.</p>
          <script>
            const params = {{
              appName: "graphing",
              width: 1100,
              height: 620,
              filename: "geogebra/{spec['slug']}.ggb",
              showToolBar: true,
              showAlgebraInput: true,
              showMenuBar: false,
              enableShiftDragZoom: true,
              language: "es",
              scaleContainerClass: "ggb-container",
              autoHeight: true
            }};
            if (typeof GGBApplet === "function") {{
              const applet = new GGBApplet(params, true);
              window.addEventListener("load", () => applet.inject("ggb-element"));
            }} else {{
              document.getElementById("ggb-element").textContent = "GeoGebra no pudo cargarse. Descargue la construcción con el botón superior.";
            }}
          </script>
        </body>
        </html>
        '''
    ).lstrip()


def main():
    for spec in CONSTRUCTIONS:
        target = GGB_DIR / f"{spec['slug']}.ggb"
        with ZipFile(target, "w", compression=ZIP_DEFLATED) as archive:
            archive.writestr("mimetype", "application/vnd.geogebra.file")
            archive.writestr("geogebra.xml", geogebra_xml(spec))
        (INTERACTIVE / f"{spec['slug']}.html").write_text(html_page(spec), encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()
