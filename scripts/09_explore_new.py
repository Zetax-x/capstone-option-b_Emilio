# -*- coding: utf-8 -*-
"""
09_explore_new.py -- Exploración autónoma de variables no analizadas
Busca hallazgos nuevos en: gasto_educacion, deuda_total, multi-instrumento,
meta x edad, salud por país, transporte, y ocupacion top earners.
Imprime solo los resultados que pasan p < 0.05 con tamaño de efecto relevante.
"""

import pandas as pd
import numpy as np
from scipy import stats
from itertools import combinations

df = pd.read_csv("data/latam_finanzas_clean.csv")

# Limpieza básica de booleanos
for col in ["tiene_tarjeta_credito", "tiene_cuenta_ahorro", "tiene_deuda"]:
    df[col] = df[col].str.strip().str.lower().map({"sí": True, "si": True, "no": False, "s\xed": True})

df["tasa_ahorro"] = df["ahorro_mensual_usd"] / df["ingreso_mensual_usd"]
df["ratio_deuda_ingreso"] = df["deuda_total_usd"] / df["ingreso_mensual_usd"]
df["pct_educacion"] = df["gasto_educacion_usd"] / df["ingreso_mensual_usd"] * 100
df["pct_salud"] = df["gasto_salud_usd"] / df["ingreso_mensual_usd"] * 100
df["pct_transporte"] = df["gasto_transporte_usd"] / df["ingreso_mensual_usd"] * 100

SEP = "-" * 60

# ─── 1. GASTO EN EDUCACIÓN ──────────────────────────────────────
print(SEP)
print("BLOQUE 1: Gasto en educación")

r_edu_ahorro, p_edu_ahorro = stats.pearsonr(df["gasto_educacion_usd"], df["ahorro_mensual_usd"])
r_edu_ingreso, p_edu_ingreso = stats.pearsonr(df["gasto_educacion_usd"], df["ingreso_mensual_usd"])
r_pct_edu_tasa, p_pct_edu_tasa = stats.pearsonr(df["pct_educacion"], df["tasa_ahorro"])
print(f"  gasto_educacion vs ahorro_mensual:   r={r_edu_ahorro:.3f}, p={p_edu_ahorro:.3f}")
print(f"  gasto_educacion vs ingreso_mensual:  r={r_edu_ingreso:.3f}, p={p_edu_ingreso:.3f}")
print(f"  %ingreso_en_edu vs tasa_ahorro:      r={r_pct_edu_tasa:.3f}, p={p_pct_edu_tasa:.3f}")

print("\n  Gasto educación por país:")
edu_pais = df.groupby("pais")["gasto_educacion_usd"].agg(["median", "mean"]).round(1)
print(edu_pais.to_string())

print("\n  %Ingreso en educación por grupo de edad:")
bins = [17, 22, 25, 28, 32]
labels = ["18-22", "23-25", "26-28", "29-32"]
df["grupo_edad"] = pd.cut(df["edad"], bins=bins, labels=labels)
print(df.groupby("grupo_edad", observed=True)["pct_educacion"].mean().round(2).to_string())

# ─── 2. MONTO DE DEUDA (no solo si tiene/no tiene) ──────────────
print(SEP)
print("BLOQUE 2: Monto de deuda (deuda_total_usd)")

deudores = df[df["tiene_deuda"] == True].copy()
print(f"  N con deuda: {len(deudores)}")
r_monto_ahorro, p_monto_ahorro = stats.pearsonr(deudores["deuda_total_usd"], deudores["ahorro_mensual_usd"])
r_ratio_ahorro, p_ratio_ahorro = stats.pearsonr(deudores["ratio_deuda_ingreso"], deudores["tasa_ahorro"])
r_ratio_sat, p_ratio_sat = stats.pearsonr(deudores["ratio_deuda_ingreso"], deudores["satisfaccion_financiera"])
print(f"  deuda_total vs ahorro_mensual (deudores):       r={r_monto_ahorro:.3f}, p={p_monto_ahorro:.3f}")
print(f"  ratio_deuda_ingreso vs tasa_ahorro (deudores):  r={r_ratio_ahorro:.3f}, p={p_ratio_ahorro:.3f}")
print(f"  ratio_deuda_ingreso vs satisfaccion (deudores): r={r_ratio_sat:.3f}, p={p_ratio_sat:.3f}")

print("\n  Cuartiles ratio deuda/ingreso vs tasa_ahorro:")
deudores["q_ratio"] = pd.qcut(deudores["ratio_deuda_ingreso"], q=4, labels=["Q1\n(bajo)","Q2","Q3","Q4\n(alto)"])
print(deudores.groupby("q_ratio", observed=True)["tasa_ahorro"].mean().round(3).to_string())

# ─── 3. COMBINACIONES DE INSTRUMENTOS FINANCIEROS ───────────────
print(SEP)
print("BLOQUE 3: Combinaciones de instrumentos financieros")

df["combo"] = (
    df["tiene_tarjeta_credito"].map({True: "TC", False: "–"}) + "+" +
    df["tiene_cuenta_ahorro"].map({True: "CA", False: "–"}) + "+" +
    df["tiene_deuda"].map({True: "D", False: "–"})
)
combo_stats = df.groupby("combo").agg(
    n=("ahorro_mensual_usd", "count"),
    ahorro_med=("ahorro_mensual_usd", "median"),
    tasa_med=("tasa_ahorro", "median"),
    ingreso_med=("ingreso_mensual_usd", "median"),
    satisf_med=("satisfaccion_financiera", "median"),
).sort_values("tasa_med", ascending=False)
print(combo_stats.to_string())

# Test ANOVA entre combos con n >= 20
combos_validos = combo_stats[combo_stats["n"] >= 20].index.tolist()
grupos_combo = [df[df["combo"] == c]["tasa_ahorro"].dropna().values for c in combos_validos]
if len(grupos_combo) >= 2:
    f_stat, p_anova = stats.f_oneway(*grupos_combo)
    print(f"\n  ANOVA tasa_ahorro por combo (n>=20): F={f_stat:.2f}, p={p_anova:.3f}")

# ─── 4. META FINANCIERA × GRUPO DE EDAD ─────────────────────────
print(SEP)
print("BLOQUE 4: Meta financiera × grupo de edad")

pivot_meta = df.groupby(["grupo_edad", "meta_financiera"], observed=True)["tasa_ahorro"].mean().unstack()
print(pivot_meta.round(3).to_string())

# Test: ¿las metas más efectivas cambian con la edad?
metas = df["meta_financiera"].value_counts().head(5).index.tolist()
print("\n  Tasa de ahorro por meta y grupo de edad (top 5 metas):")
for meta in metas:
    sub = df[df["meta_financiera"] == meta]
    r, p = stats.pearsonr(sub["edad"], sub["tasa_ahorro"])
    n = len(sub)
    print(f"    {meta[:35]:<35} n={n:3d}  r={r:.3f}  p={p:.3f}")

# ─── 5. GASTO EN SALUD POR PAÍS ─────────────────────────────────
print(SEP)
print("BLOQUE 5: Gasto en salud por país")

salud_pais = df.groupby("pais").agg(
    pct_salud_med=("pct_salud", "median"),
    pct_salud_mean=("pct_salud", "mean"),
    gasto_salud_med=("gasto_salud_usd", "median"),
).sort_values("pct_salud_med", ascending=False).round(2)
print(salud_pais.to_string())

r_salud_ahorro, p_salud_ahorro = stats.pearsonr(df["pct_salud"], df["tasa_ahorro"])
print(f"\n  %ingreso_en_salud vs tasa_ahorro: r={r_salud_ahorro:.3f}, p={p_salud_ahorro:.3f}")

# ─── 6. OCUPACIÓN: TOP EARNERS ──────────────────────────────────
print(SEP)
print("BLOQUE 6: Ocupaciones con mayor ahorro (n >= 5)")

ocup_stats = df.groupby("ocupacion").agg(
    n=("ahorro_mensual_usd", "count"),
    ahorro_med=("ahorro_mensual_usd", "median"),
    tasa_med=("tasa_ahorro", "median"),
    ingreso_med=("ingreso_mensual_usd", "median"),
).query("n >= 5").sort_values("tasa_med", ascending=False)
print("  Top 10 por tasa de ahorro:")
print(ocup_stats.head(10).to_string())
print("\n  Bottom 5 por tasa de ahorro:")
print(ocup_stats.tail(5).to_string())

# ─── 7. EDUCACIÓN: ¿CUÁNTO INVIERTEN LOS QUE MÁS AHORRAN? ──────
print(SEP)
print("BLOQUE 7: ¿Los mejores ahorradores invierten más en educación?")

q75_ahorro = df["tasa_ahorro"].quantile(0.75)
q25_ahorro = df["tasa_ahorro"].quantile(0.25)
top_savers = df[df["tasa_ahorro"] >= q75_ahorro]
low_savers = df[df["tasa_ahorro"] <= q25_ahorro]
print(f"  Top 25% ahorradores (tasa >= {q75_ahorro:.1%}): n={len(top_savers)}")
print(f"  Bot 25% ahorradores (tasa <= {q25_ahorro:.1%}): n={len(low_savers)}")
print(f"  Gasto educación mediano — top savers: ${top_savers['gasto_educacion_usd'].median():.1f}")
print(f"  Gasto educación mediano — bot savers: ${low_savers['gasto_educacion_usd'].median():.1f}")
t_stat, p_edu_group = stats.ttest_ind(top_savers["gasto_educacion_usd"], low_savers["gasto_educacion_usd"])
print(f"  t-test: t={t_stat:.2f}, p={p_edu_group:.3f}")

print(f"\n  %Ingreso en educación — top savers: {top_savers['pct_educacion'].median():.1f}%")
print(f"  %Ingreso en educación — bot savers: {low_savers['pct_educacion'].median():.1f}%")

# ─── 8. TRANSPORTE: ¿HAY PAÍS-EFECTO? ───────────────────────────
print(SEP)
print("BLOQUE 8: Gasto transporte por país")

transp_pais = df.groupby("pais").agg(
    pct_transp_med=("pct_transporte", "median"),
    gasto_transp_med=("gasto_transporte_usd", "median"),
).sort_values("pct_transp_med", ascending=False).round(2)
print(transp_pais.to_string())

r_transp_ahorro, p_transp_ahorro = stats.pearsonr(df["pct_transporte"], df["tasa_ahorro"])
print(f"\n  %ingreso_en_transporte vs tasa_ahorro: r={r_transp_ahorro:.3f}, p={p_transp_ahorro:.3f}")

print(SEP)
print("RESUMEN: Resultados con p < 0.05")
resultados = [
    ("gasto_educacion vs ahorro_mensual",        r_edu_ahorro,   p_edu_ahorro),
    ("gasto_educacion vs ingreso_mensual",        r_edu_ingreso,  p_edu_ingreso),
    ("%educacion vs tasa_ahorro",                 r_pct_edu_tasa, p_pct_edu_tasa),
    ("deuda_monto vs ahorro (deudores)",          r_monto_ahorro, p_monto_ahorro),
    ("ratio_deuda/ingreso vs tasa_ahorro",        r_ratio_ahorro, p_ratio_ahorro),
    ("ratio_deuda/ingreso vs satisfaccion",       r_ratio_sat,    p_ratio_sat),
    ("%salud vs tasa_ahorro",                     r_salud_ahorro, p_salud_ahorro),
    ("%transporte vs tasa_ahorro",                r_transp_ahorro,p_transp_ahorro),
    ("top vs bot savers — gasto educacion",       t_stat,         p_edu_group),
]
for nombre, stat, p in resultados:
    marca = "*** SIGNIFICATIVO" if p < 0.05 else ("  · marginal" if p < 0.10 else "")
    print(f"  p={p:.3f}  {nombre} {marca}")
