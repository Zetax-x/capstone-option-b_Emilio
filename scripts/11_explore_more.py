# -*- coding: utf-8 -*-
"""
11_explore_more.py -- Segunda ronda de exploración autónoma
Explora combinaciones de variables no intentadas en 09_explore_new.py.
Aplica FDR (Benjamini-Hochberg) al lote completo.
Genera charts automáticamente solo para hallazgos que pasen p < 0.05.
"""

import os
import sys
import glob
sys.stdout.reconfigure(encoding="utf-8")
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy import stats
from itertools import product

# ─── Carga y preparación ────────────────────────────────────────
df = pd.read_csv("data/latam_finanzas_clean.csv")
for col in ["tiene_tarjeta_credito", "tiene_cuenta_ahorro", "tiene_deuda"]:
    df[col] = df[col].str.strip().str.lower().map({"sí": True, "si": True, "no": False, "sí": True})

df["tasa_ahorro"]       = df["ahorro_mensual_usd"] / df["ingreso_mensual_usd"]
df["pct_vivienda"]      = df["gasto_vivienda_usd"]      / df["ingreso_mensual_usd"]
df["pct_alimentacion"]  = df["gasto_alimentacion_usd"]  / df["ingreso_mensual_usd"]
df["pct_entretenimiento"]= df["gasto_entretenimiento_usd"] / df["ingreso_mensual_usd"]
df["pct_educacion"]     = df["gasto_educacion_usd"]     / df["ingreso_mensual_usd"]

bins   = [17, 22, 25, 28, 32]
labels = ["18–22", "23–25", "26–28", "29–32"]
df["grupo_edad"] = pd.cut(df["edad"], bins=bins, labels=labels)

SOURCE  = "Fuente: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"
PALETTE = ["#2E4057", "#048A81", "#54C6EB", "#EF946C", "#C4A35A"]
n_existing = len(glob.glob("charts/*.png"))

results = []   # lista de dicts para FDR

# ─── Helper: Pearson r ──────────────────────────────────────────
def pearson(label, x, y):
    mask = x.notna() & y.notna()
    r, p = stats.pearsonr(x[mask], y[mask])
    results.append({"label": label, "type": "pearson", "stat": r, "p": p, "n": mask.sum()})

# ─── Helper: Kruskal-Wallis ─────────────────────────────────────
def kruskal(label, groups_series, values_series):
    grps = [values_series[groups_series == g].dropna()
            for g in groups_series.dropna().unique()]
    grps = [g for g in grps if len(g) >= 5]
    if len(grps) < 2:
        return
    H, p = stats.kruskal(*grps)
    results.append({"label": label, "type": "kruskal", "stat": H, "p": p,
                    "n": sum(len(g) for g in grps)})

# ══════════════════════════════════════════════════════════════════
# BLOQUE A — Categorías de gasto no exploradas
# ══════════════════════════════════════════════════════════════════
pearson("% alimentación vs tasa_ahorro",      df["pct_alimentacion"],   df["tasa_ahorro"])
pearson("% alimentación vs satisfaccion",     df["pct_alimentacion"],   df["satisfaccion_financiera"])
pearson("% entretenimiento vs tasa_ahorro",   df["pct_entretenimiento"],df["tasa_ahorro"])
pearson("% entretenimiento vs satisfaccion",  df["pct_entretenimiento"],df["satisfaccion_financiera"])

# ══════════════════════════════════════════════════════════════════
# BLOQUE B — IA directamente sobre ahorro
# ══════════════════════════════════════════════════════════════════
pearson("horas_ia vs tasa_ahorro",            df["horas_herramientas_ia_semana"], df["tasa_ahorro"])
pearson("horas_ia vs ingreso",                df["horas_herramientas_ia_semana"], df["ingreso_mensual_usd"])

# IA × grupo de edad: ¿ayuda más a jóvenes o mayores?
for grp in df["grupo_edad"].dropna().unique():
    sub = df[df["grupo_edad"] == grp]
    pearson(f"horas_ia vs tasa_ahorro [{grp}]", sub["horas_herramientas_ia_semana"], sub["tasa_ahorro"])

# ══════════════════════════════════════════════════════════════════
# BLOQUE C — Satisfacción como predictor
# ══════════════════════════════════════════════════════════════════
pearson("satisfaccion vs tasa_ahorro",        df["satisfaccion_financiera"], df["tasa_ahorro"])
pearson("satisfaccion vs ingreso",            df["satisfaccion_financiera"], df["ingreso_mensual_usd"])
pearson("% vivienda vs satisfaccion",         df["pct_vivienda"],            df["satisfaccion_financiera"])

# ══════════════════════════════════════════════════════════════════
# BLOQUE D — Interacciones entre instrumentos financieros
# ══════════════════════════════════════════════════════════════════
df["combo_tc_deuda"] = (df["tiene_tarjeta_credito"].map({True: "TC=Sí", False: "TC=No"}).fillna("TC=No")
                        + " + " +
                        df["tiene_deuda"].map({True: "Deuda=Sí", False: "Deuda=No"}).fillna("Deuda=No"))
kruskal("combo tarjeta×deuda vs tasa_ahorro",   df["combo_tc_deuda"],   df["tasa_ahorro"])
kruskal("combo tarjeta×deuda vs satisfaccion",  df["combo_tc_deuda"],   df["satisfaccion_financiera"])

df["combo_tc_ca"] = (df["tiene_tarjeta_credito"].map({True: "TC=Sí", False: "TC=No"}).fillna("TC=No")
                     + " + " +
                     df["tiene_cuenta_ahorro"].map({True: "CA=Sí", False: "CA=No"}).fillna("CA=No"))
kruskal("combo tarjeta×cuenta_ahorro vs tasa_ahorro", df["combo_tc_ca"], df["tasa_ahorro"])

# ══════════════════════════════════════════════════════════════════
# BLOQUE E — País × patrones
# ══════════════════════════════════════════════════════════════════
# E1: ¿El efecto de la edad en el ahorro es igual en todos los países?
for pais in df["pais"].dropna().unique():
    sub = df[df["pais"] == pais]
    pearson(f"edad vs tasa_ahorro [{pais}]", sub["edad"], sub["tasa_ahorro"])

# E2: país × meta_financiera → ¿la misma meta funciona en todos los países?
kruskal("meta_financiera vs tasa_ahorro por país (KW global)", df["meta_financiera"], df["tasa_ahorro"])
for pais in df["pais"].dropna().unique():
    sub = df[df["pais"] == pais]
    kruskal(f"meta_financiera vs tasa_ahorro [{pais}]", sub["meta_financiera"], sub["tasa_ahorro"])

# ══════════════════════════════════════════════════════════════════
# BLOQUE F — Educación directa sobre ahorro
# ══════════════════════════════════════════════════════════════════
pearson("gasto_educacion_usd vs tasa_ahorro",     df["gasto_educacion_usd"],  df["tasa_ahorro"])
pearson("gasto_educacion_usd vs satisfaccion",    df["gasto_educacion_usd"],  df["satisfaccion_financiera"])
pearson("% educacion vs satisfaccion",            df["pct_educacion"],        df["satisfaccion_financiera"])

# ══════════════════════════════════════════════════════════════════
# FDR — Benjamini-Hochberg
# ══════════════════════════════════════════════════════════════════
res_df = pd.DataFrame(results)
res_df = res_df.sort_values("p").reset_index(drop=True)
m = len(res_df)
res_df["bh_threshold"] = (res_df.index + 1) / m * 0.05
res_df["sig_fdr"] = res_df["p"] <= res_df["bh_threshold"]
res_df["sig_raw"] = res_df["p"] < 0.05

print("=" * 80)
print("RESULTADOS — 11_explore_more.py")
print("=" * 80)
print(f"Total de tests: {m}")
sig_raw = res_df["sig_raw"].sum()
sig_fdr = res_df["sig_fdr"].sum()
print(f"Significativos p<0.05 (sin corrección): {sig_raw}")
print(f"Significativos tras FDR (BH):           {sig_fdr}")
print()

print("─── Hallazgos que PASAN FDR ──────────────────────────────────────────────────")
passed = res_df[res_df["sig_fdr"]].copy()
if len(passed) == 0:
    print("  (ninguno)")
else:
    for _, row in passed.iterrows():
        stat_lbl = f"r={row['stat']:.3f}" if row["type"] == "pearson" else f"H={row['stat']:.2f}"
        print(f"  ✓  {row['label']:<50}  {stat_lbl}  p={row['p']:.4f}  n={int(row['n'])}")

print()
print("─── Tests que NO pasan FDR ───────────────────────────────────────────────────")
failed = res_df[~res_df["sig_fdr"]].copy()
for _, row in failed.iterrows():
    stat_lbl = f"r={row['stat']:.3f}" if row["type"] == "pearson" else f"H={row['stat']:.2f}"
    print(f"  ✗  {row['label']:<50}  {stat_lbl}  p={row['p']:.4f}")

# ══════════════════════════════════════════════════════════════════
# CHARTS — Solo para hallazgos que pasan FDR
# ══════════════════════════════════════════════════════════════════
chart_idx = n_existing
new_charts = []

def next_chart():
    global chart_idx
    chart_idx += 1
    return chart_idx

# ─── Función auxiliar: scatter con línea de regresión ──────────
def scatter_regr(x, y, xlabel, ylabel, title, fname, color=None, note=None):
    color = color or PALETTE[1]
    r, p = stats.pearsonr(x.dropna(), y[x.notna()])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, alpha=0.45, s=30, color=color, edgecolors="none")
    m_, b_, *_ = stats.linregress(x.dropna(), y[x.notna()])
    xr = np.linspace(x.min(), x.max(), 100)
    ax.plot(xr, m_ * xr + b_, color=PALETTE[0], lw=1.8, linestyle="--", alpha=0.8)
    ax.annotate(f"r = {r:.3f}\np = {p:.4f}\nn = {x.notna().sum()}",
                xy=(0.97, 0.95), xycoords="axes fraction",
                ha="right", va="top", fontsize=10,
                bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.85))
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=12, fontweight="bold")
    if note:
        ax.set_xlabel(f"{xlabel}\n{note}", fontsize=10)
    fig.text(0.5, -0.04, SOURCE, ha="center", fontsize=8, color="gray")
    fig.tight_layout()
    fig.savefig(fname, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Chart guardado: {fname}")
    new_charts.append(fname)

# ─── Función auxiliar: boxplot por categoría ───────────────────
def boxplot_cat(groups, values, xlabel, ylabel, title, fname, palette=None):
    cats = sorted(groups.dropna().unique())
    data = [values[groups == c].dropna() for c in cats]
    palette = palette or PALETTE
    fig, ax = plt.subplots(figsize=(max(7, len(cats) * 1.2), 5))
    bp = ax.boxplot(data, patch_artist=True, medianprops={"color": "white", "linewidth": 2})
    for patch, col in zip(bp["boxes"], palette * 5):
        patch.set_facecolor(col)
        patch.set_alpha(0.75)
    ax.set_xticklabels(cats, rotation=20, ha="right", fontsize=10)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=12, fontweight="bold")
    fig.text(0.5, -0.06, SOURCE, ha="center", fontsize=8, color="gray")
    fig.tight_layout()
    fig.savefig(fname, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Chart guardado: {fname}")
    new_charts.append(fname)

# ─── Generar charts para hallazgos que pasan FDR ───────────────
for _, row in passed.iterrows():
    label = row["label"]

    if label == "horas_ia vs tasa_ahorro":
        fname = f"charts/{next_chart():02d}_ia_vs_tasa_ahorro.png"
        scatter_regr(
            df["horas_herramientas_ia_semana"], df["tasa_ahorro"],
            "Horas semanales de herramientas IA", "Tasa de ahorro (ratio)",
            "Uso de IA vs Tasa de Ahorro", fname, color=PALETTE[1]
        )

    elif label == "satisfaccion vs tasa_ahorro":
        fname = f"charts/{next_chart():02d}_satisfaccion_vs_ahorro.png"
        scatter_regr(
            df["satisfaccion_financiera"], df["tasa_ahorro"],
            "Satisfacción financiera (1–5)", "Tasa de ahorro (ratio)",
            "Satisfacción Financiera vs Tasa de Ahorro", fname, color=PALETTE[2]
        )

    elif label == "% vivienda vs satisfaccion":
        fname = f"charts/{next_chart():02d}_vivienda_vs_satisfaccion.png"
        scatter_regr(
            df["pct_vivienda"], df["satisfaccion_financiera"],
            "Gasto en vivienda (% del ingreso)", "Satisfacción financiera (1–5)",
            "Carga de Vivienda vs Satisfacción Financiera", fname, color=PALETTE[3]
        )

    elif label == "% entretenimiento vs tasa_ahorro":
        fname = f"charts/{next_chart():02d}_entretenimiento_vs_ahorro.png"
        scatter_regr(
            df["pct_entretenimiento"], df["tasa_ahorro"],
            "Gasto en entretenimiento (% del ingreso)", "Tasa de ahorro (ratio)",
            "Entretenimiento vs Tasa de Ahorro", fname, color=PALETTE[4]
        )

    elif label == "% alimentación vs tasa_ahorro":
        fname = f"charts/{next_chart():02d}_alimentacion_vs_ahorro.png"
        scatter_regr(
            df["pct_alimentacion"], df["tasa_ahorro"],
            "Gasto en alimentación (% del ingreso)", "Tasa de ahorro (ratio)",
            "Gasto en Alimentación vs Tasa de Ahorro", fname, color=PALETTE[0]
        )

    elif label == "combo tarjeta×deuda vs tasa_ahorro":
        fname = f"charts/{next_chart():02d}_combo_tc_deuda_vs_ahorro.png"
        boxplot_cat(
            df["combo_tc_deuda"], df["tasa_ahorro"],
            "Combinación tarjeta crédito + deuda activa", "Tasa de ahorro (ratio)",
            "Interacción Tarjeta × Deuda vs Tasa de Ahorro", fname
        )

    elif label == "combo tarjeta×deuda vs satisfaccion":
        fname = f"charts/{next_chart():02d}_combo_tc_deuda_vs_satisfaccion.png"
        boxplot_cat(
            df["combo_tc_deuda"], df["satisfaccion_financiera"],
            "Combinación tarjeta crédito + deuda activa", "Satisfacción financiera (1–5)",
            "Interacción Tarjeta × Deuda vs Satisfacción", fname
        )

    elif label.startswith("edad vs tasa_ahorro ["):
        pais_name = label.split("[")[1].rstrip("]")
        fn_safe = pais_name.lower().replace(" ", "_")
        fname = f"charts/{next_chart():02d}_edad_ahorro_{fn_safe}.png"
        sub = df[df["pais"] == pais_name]
        scatter_regr(
            sub["edad"], sub["tasa_ahorro"],
            "Edad", "Tasa de ahorro (ratio)",
            f"Edad vs Tasa de Ahorro — {pais_name}", fname, color=PALETTE[1]
        )

    elif label.startswith("meta_financiera vs tasa_ahorro ["):
        pais_name = label.split("[")[1].rstrip("]")
        fn_safe = pais_name.lower().replace(" ", "_")
        fname = f"charts/{next_chart():02d}_meta_ahorro_{fn_safe}.png"
        sub = df[df["pais"] == pais_name]
        boxplot_cat(
            sub["meta_financiera"], sub["tasa_ahorro"],
            "Meta financiera", "Tasa de ahorro (ratio)",
            f"Meta Financiera vs Ahorro — {pais_name}", fname
        )

    elif label == "gasto_educacion_usd vs tasa_ahorro":
        fname = f"charts/{next_chart():02d}_educacion_vs_ahorro.png"
        scatter_regr(
            df["gasto_educacion_usd"], df["tasa_ahorro"],
            "Gasto en educación (USD/mes)", "Tasa de ahorro (ratio)",
            "Gasto en Educación vs Tasa de Ahorro", fname, color=PALETTE[2]
        )

    elif label == "horas_ia vs ingreso":
        fname = f"charts/{next_chart():02d}_ia_vs_ingreso.png"
        scatter_regr(
            df["horas_herramientas_ia_semana"], df["ingreso_mensual_usd"],
            "Horas semanales de herramientas IA", "Ingreso mensual (USD)",
            "Uso de IA vs Ingreso Mensual", fname, color=PALETTE[0]
        )

    elif label.startswith("horas_ia vs tasa_ahorro ["):
        grp_name = label.split("[")[1].rstrip("]")
        fn_safe = grp_name.replace("–", "-")
        fname = f"charts/{next_chart():02d}_ia_ahorro_edad_{fn_safe}.png"
        sub = df[df["grupo_edad"] == grp_name]
        scatter_regr(
            sub["horas_herramientas_ia_semana"], sub["tasa_ahorro"],
            "Horas semanales de herramientas IA", "Tasa de ahorro (ratio)",
            f"IA vs Tasa de Ahorro — grupo {grp_name}", fname, color=PALETTE[2]
        )

# ─── Actualizar contador ────────────────────────────────────────
if chart_idx > n_existing:
    with open("charts/.last_chart", "w") as f:
        f.write(str(chart_idx))
    print(f"\n.last_chart actualizado a {chart_idx}")

print()
print("=" * 80)
print(f"Resumen: {len(new_charts)} chart(s) nuevos generados, {sig_fdr} hallazgo(s) pasan FDR")
print("=" * 80)
