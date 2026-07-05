# -*- coding: utf-8 -*-
"""
12_deeper_stats.py -- Profundidad estadística
  - Intervalos de confianza al 95% (transformación Fisher-z) para correlaciones clave
  - Cohen's d para comparaciones de grupos
  - OLS por país
  - Charts: forest plot de CIs, barras Cohen's d, doble panel educación, violines por país
"""

import os
import sys
import glob
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
from scipy.stats import norm
sys.stdout.reconfigure(encoding="utf-8")

df = pd.read_csv("data/latam_finanzas_clean.csv")
for col in ["tiene_tarjeta_credito", "tiene_cuenta_ahorro", "tiene_deuda"]:
    df[col] = df[col].str.strip().str.lower().map({"sí": True, "si": True, "no": False})

df["tasa_ahorro"]        = df["ahorro_mensual_usd"] / df["ingreso_mensual_usd"]
df["pct_vivienda"]       = df["gasto_vivienda_usd"]       / df["ingreso_mensual_usd"]
df["pct_educacion"]      = df["gasto_educacion_usd"]      / df["ingreso_mensual_usd"]
df["pct_entretenimiento"]= df["gasto_entretenimiento_usd"]/ df["ingreso_mensual_usd"]

bins   = [17, 22, 25, 28, 32]
labels = ["18–22", "23–25", "26–28", "29–32"]
df["grupo_edad"] = pd.cut(df["edad"], bins=bins, labels=labels)

SOURCE  = "Fuente: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"
PALETTE = ["#2E4057", "#048A81", "#54C6EB", "#EF946C", "#C4A35A", "#8B5E3C"]
n_existing = len(glob.glob("charts/*.png"))
chart_idx  = n_existing

def next_chart():
    global chart_idx
    chart_idx += 1
    return chart_idx

# ─── Utilidades estadísticas ─────────────────────────────────────

def pearson_ci(r, n, alpha=0.05):
    """IC 95% para r de Pearson via transformación Fisher-z."""
    z  = np.arctanh(r)
    se = 1.0 / np.sqrt(n - 3)
    z_crit = norm.ppf(1 - alpha / 2)
    lo = np.tanh(z - z_crit * se)
    hi = np.tanh(z + z_crit * se)
    return lo, hi

def cohens_d(a, b):
    """Cohen's d para dos grupos independientes."""
    na, nb = len(a), len(b)
    pooled_std = np.sqrt(((na - 1) * a.std(ddof=1)**2 + (nb - 1) * b.std(ddof=1)**2)
                         / (na + nb - 2))
    return (a.mean() - b.mean()) / pooled_std

# ══════════════════════════════════════════════════════════════════
# 1. INTERVALOS DE CONFIANZA — correlaciones significativas
# ══════════════════════════════════════════════════════════════════
correlations = [
    ("Edad → tasa de ahorro (F2)",          "edad",                         "tasa_ahorro"),
    ("Ingreso → tasa de ahorro (F3)",        "ingreso_mensual_usd",          "tasa_ahorro"),
    ("IA → satisfacción (F5)",               "horas_herramientas_ia_semana", "satisfaccion_financiera"),
    ("Vivienda % → tasa de ahorro (F6)",     "pct_vivienda",                 "tasa_ahorro"),
    ("IA → ingreso (F10/F17)",               "horas_herramientas_ia_semana", "ingreso_mensual_usd"),
    ("Satisfacción → ingreso (F16)",         "satisfaccion_financiera",      "ingreso_mensual_usd"),
    ("Satisfacción → tasa ahorro (F16)",     "satisfaccion_financiera",      "tasa_ahorro"),
    ("IA → tasa de ahorro (F17)",            "horas_herramientas_ia_semana", "tasa_ahorro"),
    ("Educ. absoluta → satisfacción (F18)",  "gasto_educacion_usd",          "satisfaccion_financiera"),
    ("Educ. % → satisfacción (F18)",         "pct_educacion",                "satisfaccion_financiera"),
]

ci_rows = []
for label, x_col, y_col in correlations:
    mask = df[x_col].notna() & df[y_col].notna()
    x, y = df.loc[mask, x_col], df.loc[mask, y_col]
    r, p  = stats.pearsonr(x, y)
    lo, hi = pearson_ci(r, mask.sum())
    ci_rows.append({"label": label, "r": r, "ci_lo": lo, "ci_hi": hi, "p": p, "n": mask.sum()})
    print(f"  {label:<42}  r={r:+.3f}  IC95%=[{lo:+.3f}, {hi:+.3f}]  p={p:.4f}")

ci_df = pd.DataFrame(ci_rows).sort_values("r", ascending=True).reset_index(drop=True)

# Chart 30 — Forest plot de intervalos de confianza
fig, ax = plt.subplots(figsize=(10, 6))
y_pos = range(len(ci_df))
colors = [PALETTE[0] if r > 0 else PALETTE[3] for r in ci_df["r"]]

for i, row in ci_df.iterrows():
    ax.plot([row["ci_lo"], row["ci_hi"]], [i, i], color=colors[i], lw=2.5, alpha=0.7)
    ax.scatter(row["r"], i, color=colors[i], s=60, zorder=3)

ax.axvline(0, color="gray", linestyle="--", linewidth=1, alpha=0.6)
ax.set_yticks(list(y_pos))
ax.set_yticklabels(ci_df["label"], fontsize=9)
ax.set_xlabel("Coeficiente de correlación r  (intervalo de confianza al 95%)", fontsize=10)
ax.set_title("Intervalos de Confianza — Correlaciones Significativas del Proyecto",
             fontsize=12, fontweight="bold")
ax.set_xlim(-0.35, 0.75)
pos_patch = mpatches.Patch(color=PALETTE[0], label="Correlación positiva")
neg_patch = mpatches.Patch(color=PALETTE[3], label="Correlación negativa")
ax.legend(handles=[pos_patch, neg_patch], fontsize=9, loc="lower right")
fig.text(0.5, -0.03, SOURCE, ha="center", fontsize=8, color="gray")
fig.tight_layout()
fname = f"charts/{next_chart():02d}_forest_plot_ic95.png"
fig.savefig(fname, dpi=150, bbox_inches="tight")
plt.close()
print(f"\nChart guardado: {fname}")

# ══════════════════════════════════════════════════════════════════
# 2. COHEN'S D — comparaciones de grupos
# ══════════════════════════════════════════════════════════════════
print("\n=== Cohen's d — Comparaciones de Grupos ===")
group_comparisons = []

def add_d(label, g1, g2, outcome_col):
    a = df.loc[g1, outcome_col].dropna()
    b = df.loc[g2, outcome_col].dropna()
    d = cohens_d(a, b)
    t, p = stats.ttest_ind(a, b)
    mag = "pequeño" if abs(d) < 0.5 else ("mediano" if abs(d) < 0.8 else "grande")
    group_comparisons.append({"label": label, "d": d, "p": p, "mag": mag,
                               "n1": len(a), "n2": len(b)})
    print(f"  {label:<50}  d={d:+.3f} ({mag})  p={p:.4f}")

tc_mask  = df["tiene_tarjeta_credito"] == True
ntc_mask = df["tiene_tarjeta_credito"] == False
deu_mask = df["tiene_deuda"] == True
nod_mask = df["tiene_deuda"] == False
ca_mask  = df["tiene_cuenta_ahorro"] == True
nca_mask = df["tiene_cuenta_ahorro"] == False

add_d("Tarjeta crédito vs. no tarjeta → tasa ahorro",   tc_mask,  ntc_mask, "tasa_ahorro")
add_d("Tarjeta crédito vs. no tarjeta → satisfacción",  tc_mask,  ntc_mask, "satisfaccion_financiera")
add_d("Tarjeta crédito vs. no tarjeta → ingreso",       tc_mask,  ntc_mask, "ingreso_mensual_usd")
add_d("Deuda activa vs. sin deuda → tasa ahorro",       deu_mask, nod_mask, "tasa_ahorro")
add_d("Deuda activa vs. sin deuda → satisfacción",      deu_mask, nod_mask, "satisfaccion_financiera")
add_d("Deuda activa vs. sin deuda → ingreso",           deu_mask, nod_mask, "ingreso_mensual_usd")
add_d("Cuenta ahorro vs. sin cuenta → tasa ahorro",     ca_mask,  nca_mask, "tasa_ahorro")
add_d("Cuenta ahorro vs. sin cuenta → satisfacción",    ca_mask,  nca_mask, "satisfaccion_financiera")

gd_df = pd.DataFrame(group_comparisons).sort_values("d").reset_index(drop=True)

# Chart 31 — Barras de Cohen's d
fig, ax = plt.subplots(figsize=(10, 5))
bar_colors = [PALETTE[0] if d > 0 else PALETTE[3] for d in gd_df["d"]]
bars = ax.barh(range(len(gd_df)), gd_df["d"], color=bar_colors, alpha=0.75, edgecolor="white")
ax.axvline(0, color="gray", linewidth=1)
ax.axvline(0.5, color="gray", linestyle=":", linewidth=1, alpha=0.5)
ax.axvline(-0.5, color="gray", linestyle=":", linewidth=1, alpha=0.5)
ax.axvline(0.8, color="gray", linestyle="--", linewidth=1, alpha=0.4)
ax.axvline(-0.8, color="gray", linestyle="--", linewidth=1, alpha=0.4)
for i, row in gd_df.iterrows():
    ax.text(row["d"] + (0.02 if row["d"] >= 0 else -0.02),
            i, f"d={row['d']:+.2f}", va="center",
            ha="left" if row["d"] >= 0 else "right", fontsize=8)
ax.set_yticks(range(len(gd_df)))
ax.set_yticklabels(gd_df["label"], fontsize=8.5)
ax.set_xlabel("Cohen's d  (| · | < 0.5 pequeño · 0.5–0.8 mediano · > 0.8 grande)", fontsize=9)
ax.set_title("Tamaño del Efecto (Cohen's d) — Comparaciones de Grupos", fontsize=12, fontweight="bold")
fig.text(0.5, -0.04, SOURCE, ha="center", fontsize=8, color="gray")
fig.tight_layout()
fname = f"charts/{next_chart():02d}_cohens_d.png"
fig.savefig(fname, dpi=150, bbox_inches="tight")
plt.close()
print(f"\nChart guardado: {fname}")

# ══════════════════════════════════════════════════════════════════
# 3. OLS POR PAÍS
# ══════════════════════════════════════════════════════════════════
print("\n=== OLS por País (edad + ingreso → tasa_ahorro) ===")
ols_rows = []
for pais in sorted(df["pais"].dropna().unique()):
    sub = df[df["pais"] == pais][["edad", "ingreso_mensual_usd", "tasa_ahorro"]].dropna()
    X = sub[["edad", "ingreso_mensual_usd"]].values
    y = sub["tasa_ahorro"].values
    X_aug = np.column_stack([np.ones(len(X)), X])
    coefs, res, rank, sv = np.linalg.lstsq(X_aug, y, rcond=None)
    y_hat  = X_aug @ coefs
    ss_res = np.sum((y - y_hat)**2)
    ss_tot = np.sum((y - y.mean())**2)
    r2     = 1 - ss_res / ss_tot
    n      = len(sub)
    k      = 2
    r_edad,   p_edad   = stats.pearsonr(sub["edad"],               sub["tasa_ahorro"])
    r_ingr,   p_ingr   = stats.pearsonr(sub["ingreso_mensual_usd"], sub["tasa_ahorro"])
    ols_rows.append({
        "pais": pais, "n": n, "R2": r2,
        "b_edad": coefs[1], "b_ingreso": coefs[2],
        "r_edad": r_edad, "p_edad": p_edad,
        "r_ingreso": r_ingr, "p_ingreso": p_ingr
    })
    print(f"  {pais:<12}  n={n:3d}  R²={r2:.3f}  b_edad={coefs[1]:+.4f}  b_ingreso={coefs[2]:+.5f}"
          f"  r_edad={r_edad:+.3f}(p={p_edad:.3f})  r_ingreso={r_ingr:+.3f}(p={p_ingr:.3f})")

ols_df = pd.DataFrame(ols_rows).sort_values("R2", ascending=False)

# Chart 32 — R² por país (horizontal bars)
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.barh(ols_df["pais"], ols_df["R2"],
               color=[PALETTE[i % len(PALETTE)] for i in range(len(ols_df))], alpha=0.8)
for bar, val in zip(bars, ols_df["R2"]):
    ax.text(val + 0.005, bar.get_y() + bar.get_height()/2,
            f"R²={val:.3f}", va="center", fontsize=10, fontweight="bold")
ax.set_xlabel("R² (proporción de variación en tasa de ahorro explicada por edad + ingreso)", fontsize=9)
ax.set_title("Poder Explicativo del Modelo OLS por País", fontsize=12, fontweight="bold")
ax.set_xlim(0, max(ols_df["R2"]) + 0.12)
fig.text(0.5, -0.04, SOURCE, ha="center", fontsize=8, color="gray")
fig.tight_layout()
fname = f"charts/{next_chart():02d}_ols_por_pais.png"
fig.savefig(fname, dpi=150, bbox_inches="tight")
plt.close()
print(f"\nChart guardado: {fname}")

# ══════════════════════════════════════════════════════════════════
# 4. DOBLE PANEL — Educación: inversión vs. carga (F18)
# ══════════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

r1, p1 = stats.pearsonr(df["gasto_educacion_usd"], df["satisfaccion_financiera"])
m1, b1, *_ = stats.linregress(df["gasto_educacion_usd"], df["satisfaccion_financiera"])
ax1.scatter(df["gasto_educacion_usd"], df["satisfaccion_financiera"],
            alpha=0.4, s=25, color=PALETTE[1], edgecolors="none")
xr1 = np.linspace(df["gasto_educacion_usd"].min(), df["gasto_educacion_usd"].max(), 100)
ax1.plot(xr1, m1*xr1 + b1, color=PALETTE[0], lw=2, linestyle="--")
ax1.annotate(f"r = {r1:.3f}\np = {p1:.4f}", xy=(0.97, 0.95), xycoords="axes fraction",
             ha="right", va="top", fontsize=10,
             bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.85))
ax1.set_xlabel("Gasto en educación (USD/mes)", fontsize=10)
ax1.set_ylabel("Satisfacción financiera (1–5)", fontsize=10)
ax1.set_title("Gasto absoluto → Satisfacción\n(Inversión)", fontsize=11, fontweight="bold")

r2, p2 = stats.pearsonr(df["pct_educacion"], df["satisfaccion_financiera"])
m2, b2, *_ = stats.linregress(df["pct_educacion"], df["satisfaccion_financiera"])
ax2.scatter(df["pct_educacion"], df["satisfaccion_financiera"],
            alpha=0.4, s=25, color=PALETTE[3], edgecolors="none")
xr2 = np.linspace(df["pct_educacion"].min(), df["pct_educacion"].max(), 100)
ax2.plot(xr2, m2*xr2 + b2, color=PALETTE[0], lw=2, linestyle="--")
ax2.annotate(f"r = {r2:.3f}\np = {p2:.4f}", xy=(0.97, 0.95), xycoords="axes fraction",
             ha="right", va="top", fontsize=10,
             bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.85))
ax2.set_xlabel("Gasto en educación (% del ingreso)", fontsize=10)
ax2.set_ylabel("Satisfacción financiera (1–5)", fontsize=10)
ax2.set_title("Gasto relativo → Satisfacción\n(Carga)", fontsize=11, fontweight="bold")

fig.suptitle("El Gasto en Educación: Inversión para Quienes Pueden, Carga para Quienes No",
             fontsize=12, fontweight="bold", y=1.02)
fig.text(0.5, -0.03, SOURCE, ha="center", fontsize=8, color="gray")
fig.tight_layout()
fname = f"charts/{next_chart():02d}_educacion_dual_panel.png"
fig.savefig(fname, dpi=150, bbox_inches="tight")
plt.close()
print(f"Chart guardado: {fname}")

# ══════════════════════════════════════════════════════════════════
# 5. VIOLINES — satisfacción y tasa de ahorro por país
# ══════════════════════════════════════════════════════════════════
paises_ord = ["Brasil", "Chile", "México", "Perú", "Colombia", "Argentina"]
paises_ord = [p for p in paises_ord if p in df["pais"].unique()]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
data_sat  = [df[df["pais"] == p]["satisfaccion_financiera"].dropna().values for p in paises_ord]
data_aho  = [df[df["pais"] == p]["tasa_ahorro"].dropna().values             for p in paises_ord]

for ax, data, title, ylabel in [
    (ax1, data_sat, "Distribución de Satisfacción Financiera por País",  "Satisfacción (1–5)"),
    (ax2, data_aho, "Distribución de Tasa de Ahorro por País",           "Tasa de ahorro (ratio)"),
]:
    parts = ax.violinplot(data, positions=range(len(paises_ord)), showmedians=True, showextrema=False)
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(PALETTE[i % len(PALETTE)])
        pc.set_alpha(0.7)
    parts["cmedians"].set_color("white")
    parts["cmedians"].set_linewidth(2)
    ax.set_xticks(range(len(paises_ord)))
    ax.set_xticklabels(paises_ord, rotation=20, ha="right", fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_title(title, fontsize=11, fontweight="bold")

fig.text(0.5, -0.04, SOURCE, ha="center", fontsize=8, color="gray")
fig.tight_layout()
fname = f"charts/{next_chart():02d}_violines_pais.png"
fig.savefig(fname, dpi=150, bbox_inches="tight")
plt.close()
print(f"Chart guardado: {fname}")

# ─── Actualizar contador ────────────────────────────────────────
with open("charts/.last_chart", "w") as f:
    f.write(str(chart_idx))

print(f"\n.last_chart actualizado a {chart_idx}")
print(f"Script completo — {chart_idx - n_existing} charts generados")

# ── Exportar resultados para el reporte ────────────────────────
print("\n=== TABLA CI95% PARA EL REPORTE ===")
for _, row in ci_df.sort_values("r", ascending=False).iterrows():
    sig = "p < 0.001" if row["p"] < 0.001 else f"p = {row['p']:.3f}"
    print(f"| {row['label']:<42} | r = {row['r']:+.3f} | [{row['ci_lo']:+.3f}, {row['ci_hi']:+.3f}] | {sig} | n={int(row['n'])} |")

print("\n=== TABLA COHEN'S D PARA EL REPORTE ===")
for _, row in gd_df.sort_values("d").iterrows():
    sig = "p < 0.001" if row["p"] < 0.001 else f"p = {row['p']:.3f}"
    print(f"| {row['label']:<50} | d = {row['d']:+.3f} | {row['mag']} | {sig} |")

print("\n=== OLS POR PAÍS PARA EL REPORTE ===")
for _, row in ols_df.iterrows():
    print(f"| {row['pais']:<12} | n={int(row['n'])} | R²={row['R2']:.3f} | b_edad={row['b_edad']:+.4f} | r_edad={row['r_edad']:+.3f}(p={row['p_edad']:.3f}) |")
