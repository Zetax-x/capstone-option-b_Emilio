# -*- coding: utf-8 -*-
"""
10_findings_new.py -- Charts para hallazgos autónomos
  Chart 20: Heatmap tasa de ahorro por meta financiera × grupo de edad (F15)
  Chart 21: Scatter ratio_deuda/ingreso vs tasa de ahorro por subgrupo (extensión F12)
"""

import os
import glob
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy import stats

df = pd.read_csv("data/latam_finanzas_clean.csv")
for col in ["tiene_tarjeta_credito", "tiene_cuenta_ahorro", "tiene_deuda"]:
    df[col] = df[col].str.strip().str.lower().map({"sí": True, "si": True, "no": False, "s\xed": True})

df["tasa_ahorro"] = df["ahorro_mensual_usd"] / df["ingreso_mensual_usd"]
df["ratio_deuda_ingreso"] = df["deuda_total_usd"] / df["ingreso_mensual_usd"]

bins  = [17, 22, 25, 28, 32]
labels = ["18–22", "23–25", "26–28", "29–32"]
df["grupo_edad"] = pd.cut(df["edad"], bins=bins, labels=labels)

PALETTE = ["#2E4057", "#048A81", "#54C6EB", "#EF946C", "#C4A35A"]
SOURCE = "Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"

n_existing = len(glob.glob("charts/*.png"))

# ─── CHART 20: Heatmap meta × edad ──────────────────────────────
pivot = (
    df.groupby(["grupo_edad", "meta_financiera"], observed=True)["tasa_ahorro"]
    .mean()
    .unstack("meta_financiera")
    * 100  # porcentaje
)

# Ordenar metas por tasa promedio descendente
meta_order = pivot.mean(axis=0).sort_values(ascending=False).index
pivot = pivot[meta_order]

# Abreviar etiquetas largas
abrev = {
    "Ahorrar para retiro":    "Retiro",
    "Ahorrar para viaje":     "Viaje",
    "Comprar casa":           "Casa",
    "Emprender un negocio":   "Negocio",
    "Estudiar posgrado":      "Posgrado",
    "Fondo de emergencia":    "Emergencia",
    "Invertir en bolsa":      "Bolsa",
    "Pagar deudas":           "Deudas",
}
pivot.columns = [abrev.get(c, c) for c in pivot.columns]

fig, ax = plt.subplots(figsize=(11, 4.5))
cmap = plt.cm.YlOrRd
im = ax.imshow(pivot.values, cmap=cmap, aspect="auto", vmin=3, vmax=22)

ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns, fontsize=11)
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index, fontsize=11)

# Anotar valores en cada celda
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        val = pivot.values[i, j]
        color = "white" if val > 14 else "black"
        ax.text(j, i, f"{val:.1f}%", ha="center", va="center",
                fontsize=10, fontweight="bold", color=color)

cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
cbar.set_label("Tasa de ahorro (%)", fontsize=10)

ax.set_title("Tasa de ahorro por meta financiera y grupo de edad",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Meta financiera", fontsize=11)
ax.set_ylabel("Grupo de edad", fontsize=11)
fig.text(0.5, -0.04, SOURCE, ha="center", fontsize=8, color="gray")

# Anotar la "mejor meta" de cada grupo de edad
best_meta_per_age = pivot.idxmax(axis=1)
for i, (age_grp, best) in enumerate(best_meta_per_age.items()):
    j = list(pivot.columns).index(best)
    ax.add_patch(plt.Rectangle((j - 0.48, i - 0.48), 0.96, 0.96,
                                fill=False, edgecolor=PALETTE[0], linewidth=2.5))

fig.tight_layout()
fname20 = f"charts/{n_existing+1:02d}_meta_financiera_por_edad.png"
fig.savefig(fname20, dpi=150, bbox_inches="tight")
plt.close()
print(f"Guardado: {fname20}")

# ─── CHART 21: Ratio deuda/ingreso vs tasa_ahorro ───────────────
deudores = df[df["tiene_deuda"] == True].copy()
r, p = stats.pearsonr(deudores["ratio_deuda_ingreso"], deudores["tasa_ahorro"])

fig, ax = plt.subplots(figsize=(8, 5))

scatter = ax.scatter(
    deudores["ratio_deuda_ingreso"],
    deudores["tasa_ahorro"] * 100,
    c=deudores["satisfaccion_financiera"],
    cmap="RdYlGn", alpha=0.65, s=40, edgecolors="none",
    vmin=1, vmax=5
)

# Línea de regresión
m, b, *_ = stats.linregress(deudores["ratio_deuda_ingreso"], deudores["tasa_ahorro"] * 100)
x_line = np.linspace(deudores["ratio_deuda_ingreso"].min(),
                     deudores["ratio_deuda_ingreso"].max(), 100)
ax.plot(x_line, m * x_line + b, color=PALETTE[0], linewidth=1.8, linestyle="--", alpha=0.7)

cbar = fig.colorbar(scatter, ax=ax, fraction=0.03, pad=0.02)
cbar.set_label("Satisfacción financiera (1–5)", fontsize=9)

ax.annotate(f"r = {r:.3f}\np = {p:.3f}\n(n = {len(deudores)})",
            xy=(0.97, 0.95), xycoords="axes fraction",
            ha="right", va="top", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.8))

ax.set_xlabel("Ratio deuda total / ingreso mensual", fontsize=11)
ax.set_ylabel("Tasa de ahorro (%)", fontsize=11)
ax.set_title("Monto de deuda vs. comportamiento de ahorro\n(participantes con deuda activa, n=234)",
             fontsize=12, fontweight="bold")
fig.text(0.5, -0.04, SOURCE, ha="center", fontsize=8, color="gray")
fig.tight_layout()

fname21 = f"charts/{n_existing+2:02d}_ratio_deuda_vs_ahorro.png"
fig.savefig(fname21, dpi=150, bbox_inches="tight")
plt.close()
print(f"Guardado: {fname21}")

# ─── Estadísticas para el reporte ───────────────────────────────
print()
print("=== Estadísticas F15 ===")
print("Tasa de ahorro por meta × grupo de edad (%):")
print(pivot.round(1).to_string())
print()
print("Mejor meta por grupo:")
for age_grp, best in best_meta_per_age.items():
    val = pivot.loc[age_grp, best]
    worst = pivot.loc[age_grp].idxmin()
    worst_val = pivot.loc[age_grp, worst]
    print(f"  {age_grp}: {best} ({val:.1f}%) vs peor: {worst} ({worst_val:.1f}%)")

print()
print("=== Correlaciones edad-tasa_ahorro por meta (F15 mecanismo deuda) ===")
metas = df["meta_financiera"].value_counts().index
for meta in metas:
    sub = df[df["meta_financiera"] == meta]
    r_m, p_m = stats.pearsonr(sub["edad"], sub["tasa_ahorro"])
    print(f"  {meta[:35]:<35} n={len(sub):3d}  r={r_m:.3f}  p={p_m:.3f}")

print()
print("=== Estadísticas extensión F12 ===")
print(f"  ratio_deuda/ingreso vs tasa_ahorro: r={r:.3f}, p={p:.3f}")
print(f"  ratio_deuda/ingreso vs satisfaccion:")
r2, p2 = stats.pearsonr(deudores["ratio_deuda_ingreso"], deudores["satisfaccion_financiera"])
print(f"    r={r2:.3f}, p={p2:.3f}")
q_stats = deudores.groupby(pd.qcut(deudores["ratio_deuda_ingreso"], 4))["tasa_ahorro"].agg(["mean","median"]) * 100
print("  Tasa de ahorro (%) por cuartil deuda/ingreso:")
print(q_stats.round(1).to_string())

# ─── Actualizar contador de charts ──────────────────────────────
last_chart = n_existing + 2
with open("charts/.last_chart", "w") as f:
    f.write(str(last_chart))
print(f"\n.last_chart actualizado a {last_chart}")
