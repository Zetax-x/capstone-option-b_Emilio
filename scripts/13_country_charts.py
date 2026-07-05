# -*- coding: utf-8 -*-
"""
13_country_charts.py -- Visualizaciones de perfiles por país
  - Barras agrupadas: 6 métricas × 6 países
  - Desglose de gastos por país (barras apiladas)
  - % ahorradores negativos por país
  - Comparativa ingreso + tasa de ahorro por país
"""

import os
import sys
import glob
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sys.stdout.reconfigure(encoding="utf-8")

df = pd.read_csv("data/latam_finanzas_clean.csv")
for col in ["tiene_tarjeta_credito", "tiene_cuenta_ahorro", "tiene_deuda"]:
    df[col] = df[col].str.strip().str.lower().map({"sí": True, "si": True, "no": False})

df["tasa_ahorro"]   = df["ahorro_mensual_usd"] / df["ingreso_mensual_usd"]
df["pct_vivienda"]  = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"]

SOURCE  = "Fuente: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"
PALETTE = ["#2E4057", "#048A81", "#54C6EB", "#EF946C", "#C4A35A", "#8B5E3C"]

n_existing = len(glob.glob("charts/*.png"))
chart_idx  = n_existing

def next_chart():
    global chart_idx
    chart_idx += 1
    return chart_idx

paises_ord = ["Brasil", "Chile", "México", "Perú", "Colombia", "Argentina"]
paises_ord = [p for p in paises_ord if p in df["pais"].unique()]

# ══════════════════════════════════════════════════════════════════
# Tabla resumen por país
# ══════════════════════════════════════════════════════════════════
summary = df.groupby("pais").agg(
    n             = ("edad", "count"),
    ingreso_med   = ("ingreso_mensual_usd", "median"),
    ahorro_med    = ("ahorro_mensual_usd",  "mean"),
    tasa_ahorro   = ("tasa_ahorro",         "mean"),
    pct_vivienda  = ("pct_vivienda",        "mean"),
    ia_hrs        = ("horas_herramientas_ia_semana", "mean"),
    satisfaccion  = ("satisfaccion_financiera", "mean"),
    pct_neg       = ("ahorro_negativo",     lambda x: (x == "ahorro negativo").sum() / len(x) * 100),
).reindex(paises_ord)

print("=== Tabla resumen por país ===")
print(summary.round(2).to_string())

# ══════════════════════════════════════════════════════════════════
# Chart A — Ingreso mediano + tasa de ahorro por país
# ══════════════════════════════════════════════════════════════════
fig, ax1 = plt.subplots(figsize=(10, 5))
x = np.arange(len(paises_ord))
w = 0.4

bars = ax1.bar(x - w/2, summary["ingreso_med"], width=w,
               color=[PALETTE[i] for i in range(len(paises_ord))],
               alpha=0.85, label="Ingreso mediano (USD)")
ax1.set_ylabel("Ingreso mediano mensual (USD)", fontsize=10)
ax1.set_xticks(x)
ax1.set_xticklabels(paises_ord, fontsize=11)
for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15,
             f"${bar.get_height():.0f}", ha="center", va="bottom", fontsize=9)

ax2 = ax1.twinx()
ax2.bar(x + w/2, summary["tasa_ahorro"] * 100, width=w,
        color=[PALETTE[i] for i in range(len(paises_ord))],
        alpha=0.4, hatch="///", label="Tasa de ahorro (%)")
ax2.set_ylabel("Tasa de ahorro promedio (%)", fontsize=10)

ax1.set_title("Ingreso Mediano y Tasa de Ahorro Promedio por País",
              fontsize=12, fontweight="bold")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)
fig.text(0.5, -0.03, SOURCE, ha="center", fontsize=8, color="gray")
fig.tight_layout()
fname = f"charts/{next_chart():02d}_ingreso_ahorro_pais.png"
fig.savefig(fname, dpi=150, bbox_inches="tight")
plt.close()
print(f"Chart guardado: {fname}")

# ══════════════════════════════════════════════════════════════════
# Chart B — Carga de vivienda + % ahorradores negativos
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(paises_ord))
w = 0.35

b1 = ax.bar(x - w/2, summary["pct_vivienda"] * 100, width=w,
            color=PALETTE[0], alpha=0.85, label="Carga vivienda (% ingreso)")
b2 = ax.bar(x + w/2, summary["pct_neg"], width=w,
            color=PALETTE[3], alpha=0.85, label="Ahorradores negativos (%)")

for bar in b1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f"{bar.get_height():.1f}%", ha="center", va="bottom", fontsize=9)
for bar in b2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f"{bar.get_height():.1f}%", ha="center", va="bottom", fontsize=9)

ax.axhline(25, color="gray", linestyle=":", linewidth=1, alpha=0.5)
ax.set_xticks(x)
ax.set_xticklabels(paises_ord, fontsize=11)
ax.set_ylabel("Porcentaje (%)", fontsize=10)
ax.set_title("Carga de Vivienda y Ahorradores Negativos por País",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=9)
fig.text(0.5, -0.03, SOURCE, ha="center", fontsize=8, color="gray")
fig.tight_layout()
fname = f"charts/{next_chart():02d}_vivienda_negativos_pais.png"
fig.savefig(fname, dpi=150, bbox_inches="tight")
plt.close()
print(f"Chart guardado: {fname}")

# ══════════════════════════════════════════════════════════════════
# Chart C — Desglose de gastos por país (barras apiladas)
# ══════════════════════════════════════════════════════════════════
gasto_cols = {
    "Vivienda":       "gasto_vivienda_usd",
    "Alimentación":   "gasto_alimentacion_usd",
    "Transporte":     "gasto_transporte_usd",
    "Entretenimiento":"gasto_entretenimiento_usd",
    "Educación":      "gasto_educacion_usd",
    "Salud":          "gasto_salud_usd",
}
gasto_data = {}
for label, col in gasto_cols.items():
    gasto_data[label] = df.groupby("pais")[col].mean().reindex(paises_ord)

gasto_df = pd.DataFrame(gasto_data)

fig, ax = plt.subplots(figsize=(11, 5))
bottom = np.zeros(len(paises_ord))
cat_colors = ["#2E4057", "#048A81", "#54C6EB", "#EF946C", "#C4A35A", "#8B5E3C"]
for i, (cat, col) in enumerate(zip(gasto_df.columns, cat_colors)):
    vals = gasto_df[cat].values
    bars = ax.bar(paises_ord, vals, bottom=bottom, color=col, alpha=0.85, label=cat)
    for j, (bar, v) in enumerate(zip(bars, vals)):
        if v > 20:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bottom[j] + v/2, f"${v:.0f}",
                    ha="center", va="center", fontsize=8, color="white", fontweight="bold")
    bottom += vals

ax.set_ylabel("Gasto mensual promedio (USD)", fontsize=10)
ax.set_title("Desglose de Gastos Mensuales por País", fontsize=12, fontweight="bold")
ax.legend(loc="upper right", fontsize=9)
fig.text(0.5, -0.03, SOURCE, ha="center", fontsize=8, color="gray")
fig.tight_layout()
fname = f"charts/{next_chart():02d}_gastos_desglose_pais.png"
fig.savefig(fname, dpi=150, bbox_inches="tight")
plt.close()
print(f"Chart guardado: {fname}")

# ══════════════════════════════════════════════════════════════════
# Chart D — IA y satisfacción por país
# ══════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5))
scatter = ax.scatter(
    summary["ia_hrs"],
    summary["satisfaccion"],
    s=[summary.loc[p, "n"] * 2 for p in paises_ord],
    c=range(len(paises_ord)),
    cmap="tab10", alpha=0.85, edgecolors="white", linewidth=1.5, zorder=3
)
for pais in paises_ord:
    ax.annotate(pais,
                (summary.loc[pais, "ia_hrs"] + 0.05, summary.loc[pais, "satisfaccion"] + 0.02),
                fontsize=10)
ax.set_xlabel("Promedio de horas semanales de herramientas IA", fontsize=10)
ax.set_ylabel("Satisfacción financiera promedio (1–5)", fontsize=10)
ax.set_title("Uso de IA vs. Satisfacción Financiera por País\n(tamaño del punto = n de respondentes)",
             fontsize=11, fontweight="bold")
fig.text(0.5, -0.03, SOURCE, ha="center", fontsize=8, color="gray")
fig.tight_layout()
fname = f"charts/{next_chart():02d}_ia_satisfaccion_pais.png"
fig.savefig(fname, dpi=150, bbox_inches="tight")
plt.close()
print(f"Chart guardado: {fname}")

# ─── Actualizar contador ────────────────────────────────────────
with open("charts/.last_chart", "w") as f:
    f.write(str(chart_idx))
print(f"\n.last_chart actualizado a {chart_idx}")
print(f"Script completo — {chart_idx - n_existing} charts generados")
