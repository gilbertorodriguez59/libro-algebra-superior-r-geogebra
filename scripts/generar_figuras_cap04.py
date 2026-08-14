#!/usr/bin/env python3
"""Genera las figuras didácticas del capítulo 4 en PNG y SVG."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
OUT.mkdir(parents=True, exist_ok=True)

AZUL = "#123b6d"
AZUL2 = "#2873a8"
VERDE = "#2c7a5a"
DORADO = "#b58a2a"
ROJO = "#b4443c"
GRIS = "#67798a"


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=180, bbox_inches="tight", facecolor="white")
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def division():
    fig, ax = plt.subplots(figsize=(10.5, 4.7))
    ax.axis("off")
    ax.text(0.5, 0.91, "Algoritmo de la división en K[x]", ha="center", va="center",
            fontsize=19, color=AZUL, weight="bold")
    boxes = [
        (0.06, 0.56, 0.22, 0.18, "Dividendo\np(x)", AZUL2),
        (0.39, 0.56, 0.22, 0.18, "Divisor × cociente\nd(x)q(x)", VERDE),
        (0.72, 0.56, 0.22, 0.18, "Residuo\nr(x)", DORADO),
    ]
    for x, y, w, h, label, color in boxes:
        rect = plt.Rectangle((x, y), w, h, transform=ax.transAxes,
                             facecolor=color + "18", edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, label, transform=ax.transAxes,
                ha="center", va="center", fontsize=14, color=AZUL, weight="bold")
    ax.annotate("=", (0.335, 0.65), xycoords=ax.transAxes, fontsize=24,
                ha="center", va="center", color=AZUL)
    ax.annotate("+", (0.665, 0.65), xycoords=ax.transAxes, fontsize=24,
                ha="center", va="center", color=AZUL)
    ax.text(0.5, 0.38, r"$p(x)=d(x)q(x)+r(x)$", transform=ax.transAxes,
            ha="center", va="center", fontsize=23, color=AZUL)
    ax.text(0.5, 0.20, r"$r(x)=0$  o  $\deg r<\deg d$", transform=ax.transAxes,
            ha="center", va="center", fontsize=17, color=ROJO)
    ax.text(0.5, 0.07, "Comprobación: multiplique divisor y cociente, luego sume el residuo.",
            transform=ax.transAxes, ha="center", fontsize=12.5, color=GRIS)
    save(fig, "division-polinomios")


def multiplicidad():
    x = np.linspace(-1.1, 3.1, 500)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.1), sharex=True, sharey=True)
    for ax, m, color in zip(axes, [1, 2, 3], [AZUL2, DORADO, VERDE]):
        y = (x - 1) ** m
        ax.axhline(0, color="#8fa1b1", lw=1)
        ax.axvline(1, color="#c8d5df", lw=1, ls="--")
        ax.plot(x, y, color=color, lw=2.7)
        ax.scatter([1], [0], color=ROJO, s=42, zorder=3)
        ax.set_title(f"Multiplicidad {m}", color=AZUL, weight="bold")
        ax.set_xlim(-0.8, 2.8)
        ax.set_ylim(-3.5, 4.5)
        ax.grid(alpha=0.17)
        ax.set_xlabel("x")
    axes[0].set_ylabel("p(x)")
    axes[0].text(0.06, 0.92, "cruza", transform=axes[0].transAxes, color=AZUL2, weight="bold")
    axes[1].text(0.06, 0.92, "toca", transform=axes[1].transAxes, color=DORADO, weight="bold")
    axes[2].text(0.06, 0.92, "cruza y se aplana", transform=axes[2].transAxes, color=VERDE, weight="bold")
    fig.suptitle("Comportamiento local cerca de la raíz x = 1", fontsize=17, color=AZUL, weight="bold")
    fig.tight_layout()
    save(fig, "multiplicidad-raices")


def conjugadas():
    fig, ax = plt.subplots(figsize=(7, 5.3))
    ax.axhline(0, color="#8fa1b1", lw=1.3)
    ax.axvline(0, color="#8fa1b1", lw=1.3)
    ax.plot([2, 2], [-1, 1], color="#b9c7d2", ls="--", lw=1.4)
    ax.scatter([2, 2], [1, -1], s=90, color=[AZUL2, VERDE], zorder=3)
    ax.annotate(r"$z=2+i$", (2, 1), xytext=(2.28, 1.35), fontsize=14, color=AZUL2,
                arrowprops=dict(arrowstyle="->", color=AZUL2))
    ax.annotate(r"$\overline{z}=2-i$", (2, -1), xytext=(2.28, -1.55), fontsize=14, color=VERDE,
                arrowprops=dict(arrowstyle="->", color=VERDE))
    ax.annotate("conjugación", xy=(2.04, -0.76), xytext=(2.04, 0.72),
                ha="left", va="center", color=ROJO,
                arrowprops=dict(arrowstyle="->", color=ROJO, lw=1.8))
    ax.set_xlim(-0.7, 4.3)
    ax.set_ylim(-2.4, 2.4)
    ax.set_aspect("equal")
    ax.set_xlabel("Parte real")
    ax.set_ylabel("Parte imaginaria")
    ax.set_title("Raíces conjugadas de un polinomio real", color=AZUL, weight="bold", fontsize=16)
    ax.grid(alpha=0.16)
    save(fig, "raices-conjugadas")


def racional():
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.5))

    ax = axes[0]
    x = np.linspace(-4, 4, 400)
    ax.plot(x, x + 1, color=AZUL2, lw=2.5)
    ax.scatter([1], [2], s=100, facecolor="white", edgecolor=ROJO, linewidth=2.2, zorder=4)
    ax.axhline(0, color="#8fa1b1", lw=1)
    ax.axvline(0, color="#8fa1b1", lw=1)
    ax.set_title(r"Hueco: $(x^2-1)/(x-1)$", color=AZUL, weight="bold")
    ax.annotate("x = 1 queda excluido", (1, 2), xytext=(-2.8, 4.0), color=ROJO,
                arrowprops=dict(arrowstyle="->", color=ROJO))
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 6)
    ax.grid(alpha=0.16)

    ax = axes[1]
    x1 = np.linspace(-4, 0.96, 400)
    x2 = np.linspace(1.04, 5, 400)
    f = lambda t: 2 * t + 2 + 3 / (t - 1)
    ax.plot(x1, f(x1), color=VERDE, lw=2.3)
    ax.plot(x2, f(x2), color=VERDE, lw=2.3)
    ax.axvline(1, color=ROJO, ls="--", lw=1.8, label="x = 1")
    xx = np.linspace(-4, 5, 300)
    ax.plot(xx, 2 * xx + 2, color=DORADO, ls="--", lw=1.8, label="y = 2x + 2")
    ax.axhline(0, color="#8fa1b1", lw=1)
    ax.set_title("Asíntotas vertical y oblicua", color=AZUL, weight="bold")
    ax.set_xlim(-4, 5)
    ax.set_ylim(-10, 12)
    ax.legend(frameon=False, loc="upper left")
    ax.grid(alpha=0.16)

    fig.suptitle("Dominio y comportamiento de funciones racionales", fontsize=17, color=AZUL, weight="bold")
    fig.tight_layout()
    save(fig, "funcion-racional")


if __name__ == "__main__":
    division()
    multiplicidad()
    conjugadas()
    racional()
    print("Figuras del capítulo 4 generadas en", OUT)
