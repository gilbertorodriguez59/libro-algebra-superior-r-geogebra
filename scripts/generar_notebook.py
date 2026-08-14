#!/usr/bin/env python3
"""Genera el cuaderno ejecutable del capítulo 1 con kernel de R."""

import json
from pathlib import Path


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip().splitlines(keepends=True)}


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.strip().splitlines(keepends=True),
    }


cells = [
    md(r"""
# Capítulo 1. Lógica y conjuntos con R

**Álgebra Superior con aplicaciones en R y GeoGebra**  
**Autor:** Jesús Gilberto Rodríguez Escobedo

[Abrir este cuaderno en Google Colab](https://colab.research.google.com/github/gilbertorodriguez59/libro-algebra-superior-r-geogebra/blob/main/notebooks/capitulo-01-logica-conjuntos-R.ipynb)

Este cuaderno sigue exactamente las secciones 1.1–1.9 del libro. Cada bloque presenta una idea, un experimento reproducible y una interpretación. Todo el código utiliza R base.

> Una comprobación exhaustiva es concluyente cuando el dominio es finito y está completamente enumerado. En dominios infinitos, experimentar no reemplaza la demostración matemática.
"""),
    md(r"""
## Cómo trabajar con el cuaderno

1. Ejecute las celdas en orden.
2. Cambie los ejemplos únicamente después de obtener el resultado original.
3. Compare el resultado computacional con la definición matemática.
4. Resuelva los ejercicios antes de consultar las comprobaciones.
"""),
    md(r"""
## 1.1 Lenguaje de conjuntos

Un conjunto finito se representa mediante un vector sin repeticiones. `setequal()` compara conjuntos ignorando el orden; `%in%` comprueba pertenencia.
"""),
    code(r"""
U <- 1:10
A <- c(2, 4, 6, 8, 10)
B <- c(2, 3, 5, 7)

es_subconjunto <- function(X, Y) all(X %in% Y)

list(
  pertenece = 4 %in% A,
  no_pertenece = 5 %in% A,
  subconjunto = es_subconjunto(c(2, 4), A),
  igualdad_sin_orden = setequal(c(1, 2, 3), c(3, 2, 1))
)
"""),
    md(r"""
### Conjunto potencia

Cada elemento puede incluirse o excluirse; por ello, un conjunto con $n$ elementos tiene $2^n$ subconjuntos.
"""),
    code(r"""
conjunto_potencia <- function(A) {
  resultado <- list(A[FALSE])
  if (length(A) > 0) {
    for (k in seq_len(length(A))) {
      resultado <- c(resultado, combn(A, k, simplify = FALSE))
    }
  }
  resultado
}

P <- conjunto_potencia(c("a", "b", "c"))
P
length(P)
"""),
    md(r"""
## 1.2 Proposiciones y conectivos lógicos

R representa verdadero y falso con `TRUE` y `FALSE`. La implicación se programa usando $p\Rightarrow q\equiv \neg p\lor q$.
"""),
    code(r"""
implica <- function(p, q) (!p) | q

tabla <- expand.grid(
  q = c(TRUE, FALSE),
  p = c(TRUE, FALSE)
)[, c("p", "q")]

tabla$no_p <- !tabla$p
tabla$p_y_q <- tabla$p & tabla$q
tabla$p_o_q <- tabla$p | tabla$q
tabla$p_implica_q <- implica(tabla$p, tabla$q)
tabla$p_sii_q <- tabla$p == tabla$q
tabla
"""),
    md(r"""
### Tautología, contradicción y contingencia

Una columna es tautológica si todas sus filas son verdaderas y contradictoria si todas son falsas.
"""),
    code(r"""
clasificar_proposicion <- function(valores) {
  if (all(valores)) "tautologia"
  else if (all(!valores)) "contradiccion"
  else "contingencia"
}

c(
  tercero_excluido = clasificar_proposicion(tabla$p | !tabla$p),
  contradiccion = clasificar_proposicion(tabla$p & !tabla$p),
  implicacion = clasificar_proposicion(tabla$p_implica_q)
)
"""),
    md(r"""
## 1.3 Cuantificadores y equivalencias lógicas

En un dominio finito, `all()` modela “para todo” y `any()` modela “existe”.
"""),
    code(r"""
D <- -4:4
p <- D^2 <= 4

data.frame(x = D, p_x = p)
D[p]

c(
  para_todo_cuadrado_no_negativo = all(D^2 >= 0),
  existe_cuadrado_igual_a_4 = any(D^2 == 4),
  no_para_todo_p = !all(p),
  existe_no_p = any(!p)
)
"""),
    md(r"""
## 1.4 Operaciones y propiedades de los conjuntos

El complemento requiere especificar el universo. La diferencia simétrica conserva los elementos que están exactamente en uno de los dos conjuntos.
"""),
    code(r"""
complemento <- function(X, U) setdiff(U, X)
diferencia_simetrica <- function(X, Y) {
  union(setdiff(X, Y), setdiff(Y, X))
}

list(
  union = union(A, B),
  interseccion = intersect(A, B),
  complemento_A = complemento(A, U),
  A_menos_B = setdiff(A, B),
  diferencia_simetrica = diferencia_simetrica(A, B)
)
"""),
    md(r"""
### Comprobación de De Morgan

Comprobamos $(A\cup B)^c=A^c\cap B^c$ en el universo finito elegido.
"""),
    code(r"""
izquierda <- complemento(union(A, B), U)
derecha <- intersect(complemento(A, U), complemento(B, U))

data.frame(
  lado = c("(A union B)^c", "A^c interseccion B^c"),
  elementos = c(paste(izquierda, collapse = ", "),
                paste(derecha, collapse = ", "))
)
setequal(izquierda, derecha)
"""),
    code(r"""
# Diagrama básico de Venn sin paquetes
plot(0, 0, type = "n", xlim = c(-2, 2), ylim = c(-1.5, 1.5),
     axes = FALSE, xlab = "", ylab = "", asp = 1,
     main = "A y B dentro del universo U")
rect(-1.9, -1.35, 1.9, 1.25, border = "#173f6b", lwd = 2)
symbols(c(-0.55, 0.55), c(0, 0), circles = c(0.9, 0.9),
        inches = FALSE, add = TRUE, fg = "#2f7fbd", lwd = 3)
text(-0.9, 0, "A", cex = 1.3)
text(0.9, 0, "B", cex = 1.3)
text(-1.75, 1.05, "U", cex = 1.2)
"""),
    md(r"""
## 1.5 Cardinalidad de conjuntos finitos y problemas de conteo

El principio de inclusión-exclusión corrige el conteo repetido de las intersecciones.
"""),
    code(r"""
inclusion_exclusion_3 <- function(nA, nB, nC, nAB, nAC, nBC, nABC) {
  nA + nB + nC - nAB - nAC - nBC + nABC
}

total <- 400
al_menos_uno <- inclusion_exclusion_3(
  nA = 170, nB = 150, nC = 140,
  nAB = 70, nAC = 60, nBC = 50, nABC = 20
)

c(al_menos_un_sensor = al_menos_uno, ningun_sensor = total - al_menos_uno)
"""),
    md(r"""
## 1.6 Producto cartesiano y relaciones

Una relación de $A$ en $B$ es un subconjunto de $A\times B$. Representaremos cada par mediante dos columnas.
"""),
    code(r"""
A1 <- c(1, 2)
B1 <- c("x", "y", "z")
AxB <- expand.grid(a = A1, b = B1)
AxB
nrow(AxB)
"""),
    code(r"""
clave_par <- function(x, y) paste(x, y, sep = "|")
claves_relacion <- function(R) clave_par(R$x, R$y)

es_reflexiva <- function(R, X) {
  all(clave_par(X, X) %in% claves_relacion(R))
}
es_simetrica <- function(R) {
  all(clave_par(R$y, R$x) %in% claves_relacion(R))
}
es_antisimetrica <- function(R) {
  reversos <- clave_par(R$y, R$x) %in% claves_relacion(R)
  all((R$x == R$y) | !reversos)
}
es_transitiva <- function(R) {
  claves <- claves_relacion(R)
  for (i in seq_len(nrow(R))) for (j in seq_len(nrow(R))) {
    if (R$y[i] == R$x[j] &&
        !(clave_par(R$x[i], R$y[j]) %in% claves)) return(FALSE)
  }
  TRUE
}

X <- 1:3
R <- data.frame(x = c(1, 1, 2, 3), y = c(1, 2, 2, 3))
c(reflexiva = es_reflexiva(R, X), simetrica = es_simetrica(R),
  antisimetrica = es_antisimetrica(R), transitiva = es_transitiva(R))
"""),
    md(r"""
## 1.7 Funciones: definición, representación y operaciones

Una tabla representa una función si cada elemento del dominio aparece exactamente una vez como entrada y todas las salidas pertenecen al codominio.
"""),
    code(r"""
es_funcion <- function(tabla, dominio, codominio) {
  setequal(tabla$x, dominio) &&
    !anyDuplicated(tabla$x) &&
    all(tabla$y %in% codominio)
}

dominio <- c("s1", "s2", "s3")
codominio <- c("bajo", "medio", "alto")
f_tabla <- data.frame(x = dominio, y = c("bajo", "alto", "medio"))

f_tabla
es_funcion(f_tabla, dominio, codominio)
"""),
    md(r"""
### Composición

En $(g\circ f)(x)$ se aplica primero $f$ y después $g$.
"""),
    code(r"""
f <- function(x) 2 * x + 1
g <- function(x) x^2
g_comp_f <- function(x) g(f(x))
f_comp_g <- function(x) f(g(x))

x <- -3:3
data.frame(x, g_comp_f = g_comp_f(x), f_comp_g = f_comp_g(x))
"""),
    code(r"""
# Diagrama sagital de una función finita
diagrama_funcion <- function(tabla, dominio, codominio) {
  yA <- seq(0.8, 0.2, length.out = length(dominio))
  yB <- seq(0.8, 0.2, length.out = length(codominio))
  plot(0, 0, type = "n", xlim = c(0, 1), ylim = c(0, 1), axes = FALSE,
       xlab = "", ylab = "", main = "Diagrama sagital")
  symbols(c(0.2, 0.8), c(0.5, 0.5), circles = c(0.18, 0.18),
          inches = FALSE, add = TRUE, fg = "#173f6b", lwd = 2)
  text(0.2, yA, dominio); text(0.8, yB, codominio)
  for (i in seq_len(nrow(tabla))) {
    j <- match(tabla$y[i], codominio)
    arrows(0.27, yA[match(tabla$x[i], dominio)], 0.72, yB[j],
           length = 0.08, col = "#2f7fbd", lwd = 2)
  }
}

diagrama_funcion(f_tabla, dominio, codominio)
"""),
    md(r"""
## 1.8 Funciones inyectivas, suprayectivas y biyectivas

La inyectividad impide que dos entradas distintas compartan salida. La suprayectividad exige que todo elemento del codominio aparezca como imagen.
"""),
    code(r"""
clasificar_funcion <- function(tabla, dominio, codominio) {
  if (!es_funcion(tabla, dominio, codominio)) {
    return(data.frame(es_funcion = FALSE, inyectiva = NA,
                      suprayectiva = NA, biyectiva = NA))
  }
  inyectiva <- !anyDuplicated(tabla$y)
  suprayectiva <- setequal(unique(tabla$y), codominio)
  data.frame(es_funcion = TRUE, inyectiva = inyectiva,
             suprayectiva = suprayectiva,
             biyectiva = inyectiva && suprayectiva)
}

clasificar_funcion(f_tabla, dominio, codominio)

h_tabla <- data.frame(x = dominio, y = c("bajo", "bajo", "medio"))
clasificar_funcion(h_tabla, dominio, codominio)
"""),
    md(r"""
### Comprobación del teorema de la inversa en un caso finito

En una función biyectiva, invertir las columnas produce nuevamente una función.
"""),
    code(r"""
biyectiva <- data.frame(x = c("x1", "x2", "x3"), y = c("a", "b", "c"))
inversa <- data.frame(x = biyectiva$y, y = biyectiva$x)

clasificar_funcion(biyectiva, biyectiva$x, biyectiva$y)
es_funcion(inversa, biyectiva$y, biyectiva$x)
inversa
"""),
    md(r"""
## 1.9 Cardinalidad, equipotencia y conjuntos infinitos

La función siguiente enumera los enteros como $0,1,-1,2,-2,\ldots$ a partir de $\mathbb N_0$.
"""),
    code(r"""
phi <- function(n) {
  ifelse(n == 0, 0,
         ifelse(n %% 2 == 1, (n + 1) / 2, -n / 2))
}

n <- 0:20
tabla_biyeccion <- data.frame(n = n, phi_n = phi(n))
tabla_biyeccion

plot(n, phi(n), type = "h", lwd = 2, col = "#2f7fbd",
     xlab = "n en N0", ylab = "phi(n) en Z",
     main = "Primeros valores de la biyección entre N0 y Z")
points(n, phi(n), pch = 19, col = "#173f6b")
abline(h = 0, col = "gray60")
"""),
    md(r"""
## Aplicación integradora: álgebra de Boole y circuitos

Se sigue la progresión del capítulo 3 de Tocci: compuertas, expresiones, tablas de verdad, simplificación, universalidad y formas de onda.
"""),
    code(r"""
NOT <- function(a) !a
OR <- function(a, b) a | b
AND <- function(a, b) a & b
NOR <- function(a, b) !(a | b)
NAND <- function(a, b) !(a & b)

e <- expand.grid(b = c(TRUE, FALSE), a = c(TRUE, FALSE))[, c("a", "b")]
data.frame(e, NOT_a = NOT(e$a), OR = OR(e$a, e$b), AND = AND(e$a, e$b),
           NOR = NOR(e$a, e$b), NAND = NAND(e$a, e$b))
"""),
    md(r"""
### Simplificación verificada por tabla de verdad

Comprobamos $\overline a b+ab+a\overline b=a+b$ en las cuatro combinaciones.
"""),
    code(r"""
F_original <- (!e$a & e$b) | (e$a & e$b) | (e$a & !e$b)
F_simplificada <- e$a | e$b

verificacion <- data.frame(e, F_original, F_simplificada,
                           iguales = F_original == F_simplificada)
verificacion
stopifnot(all(verificacion$iguales))
"""),
    md(r"""
### Universalidad de NOR y NAND
"""),
    code(r"""
nor <- function(x, y) !(x | y)
no_nor <- function(x) nor(x, x)
o_nor <- function(x, y) nor(nor(x, y), nor(x, y))
y_nor <- function(x, y) nor(nor(x, x), nor(y, y))

nand <- function(x, y) !(x & y)
no_nand <- function(x) nand(x, x)
y_nand <- function(x, y) nand(nand(x, y), nand(x, y))
o_nand <- function(x, y) nand(nand(x, x), nand(y, y))

data.frame(
  e,
  NOR_NOT = no_nor(e$a), NOR_OR = o_nor(e$a, e$b), NOR_AND = y_nor(e$a, e$b),
  NAND_NOT = no_nand(e$a), NAND_OR = o_nand(e$a, e$b), NAND_AND = y_nand(e$a, e$b)
)
"""),
    md(r"""
### Diagramas de temporización

El modelo es ideal: todavía no incluye retardos de propagación.
"""),
    code(r"""
t <- 0:8
senal_A <- c(0, 0, 1, 1, 1, 0, 1, 1, 0)
senal_B <- c(1, 1, 1, 0, 0, 1, 0, 0, 0)
salida_AND <- as.integer(as.logical(senal_A) & as.logical(senal_B))
salida_OR <- as.integer(as.logical(senal_A) | as.logical(senal_B))

matplot(t, cbind(senal_A, senal_B, salida_AND, salida_OR),
        type = "s", lty = 1, lwd = 2, xlab = "Tiempo",
        ylab = "Nivel lógico", yaxt = "n",
        col = c("#1f77b4", "#d62728", "#2ca02c", "#9467bd"))
axis(2, at = c(0, 1))
legend("topright", legend = c("A", "B", "A AND B", "A OR B"),
       col = c("#1f77b4", "#d62728", "#2ca02c", "#9467bd"),
       lty = 1, lwd = 2, bty = "n")
"""),
    md(r"""
## Ejercicios

1. Cambie $U,A,B$ y compruebe ambas leyes de De Morgan.
2. Construya la tabla de verdad de $[(p\land\neg q)\Rightarrow(r\land\neg r)]\Leftrightarrow(p\Rightarrow q)$.
3. Modifique una relación para que sea reflexiva y simétrica, pero no transitiva.
4. Construya una función solo inyectiva, otra solo suprayectiva y otra biyectiva.
5. Compruebe con R la ley de absorción $a+ab=a$.
6. Genere dos señales binarias propias y trace XOR y NOR.
"""),
    md(r"""
## Autoevaluación computacional

Las siguientes pruebas deben terminar sin error. Si una falla después de modificar el cuaderno, revise la definición correspondiente.
"""),
    code(r"""
stopifnot(
  es_subconjunto(c(2, 4), A),
  length(conjunto_potencia(c("a", "b", "c"))) == 8,
  setequal(complemento(union(A, B), U),
           intersect(complemento(A, U), complemento(B, U))),
  es_funcion(f_tabla, dominio, codominio),
  all(F_original == F_simplificada),
  all(no_nor(e$a) == !e$a),
  all(o_nand(e$a, e$b) == (e$a | e$b))
)
"""),
    md("""
## Información de la sesión

Ejecute esta celda al terminar para registrar la versión de R utilizada.
"""),
    code("sessionInfo()"),
]

notebook = {
    "cells": cells,
    "metadata": {
        "colab": {"name": "Capítulo 1 - Lógica y conjuntos con R.ipynb", "provenance": []},
        "kernelspec": {"display_name": "R", "language": "R", "name": "ir"},
        "language_info": {"codemirror_mode": "r", "file_extension": ".r", "mimetype": "text/x-r-source", "name": "R", "pygments_lexer": "r", "version": "4.5"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

target = Path(__file__).resolve().parents[1] / "notebooks" / "capitulo-01-logica-conjuntos-R.ipynb"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(target)
