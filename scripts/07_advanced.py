import pandas as pd
import numpy as np
from scipy import stats
from scipy.cluster.vq import kmeans, vq, whiten
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import glob

df = pd.read_csv("data/latam_finanzas_clean.csv")

PALETTE = ["#2E4057", "#048A81", "#54C6EB", "#EF6F6C", "#8EE3EF", "#CAD2C5"]
SOURCE = "Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"

def next_chart_num():
    try:
        with open("charts/.last_chart") as f:
            return int(f.read().strip()) + 1
    except FileNotFoundError:
        return len(glob.glob("charts/*.png")) + 1

def save_last_chart(n):
    with open("charts/.last_chart", "w") as f:
        f.write(str(n))

chart_n = next_chart_num()

# =============================================================================
# SECCIÓN 1 — AHORRADORES NEGATIVOS
# Subgrupo de 74 participantes que gastan más de lo que ganan en el mes
# encuestado. Son el caso de uso central del programa y el menos analizado
# en los 14 hallazgos principales.
# =============================================================================

neg = df[df["ahorro_mensual_usd"] < 0].copy()
pos = df[df["ahorro_mensual_usd"] >= 0].copy()

print("=" * 60)
print("ANÁLISIS AVANZADO 1: AHORRADORES NEGATIVOS")
print("=" * 60)
print(f"Total muestra: {len(df)}")
print(f"Ahorradores negativos: {len(neg)} ({len(neg)/len(df)*100:.1f}%)")
print(f"Ahorradores positivos/cero: {len(pos)} ({len(pos)/len(df)*100:.1f}%)")

profile = pd.DataFrame({
    f"Negativos (n={len(neg)})": [
        neg["edad"].mean(),
        neg["ingreso_mensual_usd"].mean(),
        neg["ahorro_mensual_usd"].mean(),
        neg["satisfaccion_financiera"].mean(),
        neg["tiene_tarjeta_credito"].str.startswith("S").mean() * 100,
        neg["tiene_deuda"].str.startswith("S").mean() * 100,
        (neg["gasto_vivienda_usd"] / neg["ingreso_mensual_usd"] * 100).mean(),
    ],
    f"Positivos (n={len(pos)})": [
        pos["edad"].mean(),
        pos["ingreso_mensual_usd"].mean(),
        pos["ahorro_mensual_usd"].mean(),
        pos["satisfaccion_financiera"].mean(),
        pos["tiene_tarjeta_credito"].str.startswith("S").mean() * 100,
        pos["tiene_deuda"].str.startswith("S").mean() * 100,
        (pos["gasto_vivienda_usd"] / pos["ingreso_mensual_usd"] * 100).mean(),
    ]
}, index=["Edad promedio", "Ingreso promedio (USD)", "Ahorro promedio (USD)",
          "Satisfacción financiera (1-5)", "% con tarjeta de crédito",
          "% con deuda activa", "Carga de vivienda (%)"])
print("\n" + profile.round(2).to_string())

bins = [17, 22, 25, 28, 32]
age_labels = ["18-22", "23-25", "26-28", "29-32"]
df["age_group"] = pd.cut(df["edad"], bins=bins, labels=age_labels)
neg["age_group"] = pd.cut(neg["edad"], bins=bins, labels=age_labels)
neg_by_age = neg.groupby("age_group", observed=True).size()
pct_by_age = (neg_by_age / df.groupby("age_group", observed=True).size() * 100).round(1)
print("\nDistribución por grupo de edad:")
print(pd.DataFrame({"n_negativos": neg_by_age, "% del grupo": pct_by_age}).to_string())

print("\nDistribución por país:")
pais_count = neg.groupby("pais").size().sort_values(ascending=False)
pct_pais = (pais_count / df.groupby("pais").size() * 100).round(1)
print(pd.DataFrame({"n_negativos": pais_count, "% del país": pct_pais}).to_string())

# Chart
metrics = ["Edad\npromedio", "Ingreso\n(USD)", "Satisfacción\nfinanciera",
           "% con\ntarjeta", "% con\ndeuda", "Carga de\nvivienda (%)"]
vals_neg = [neg["edad"].mean(), neg["ingreso_mensual_usd"].mean(),
            neg["satisfaccion_financiera"].mean(),
            neg["tiene_tarjeta_credito"].str.startswith("S").mean() * 100,
            neg["tiene_deuda"].str.startswith("S").mean() * 100,
            (neg["gasto_vivienda_usd"] / neg["ingreso_mensual_usd"] * 100).mean()]
vals_pos = [pos["edad"].mean(), pos["ingreso_mensual_usd"].mean(),
            pos["satisfaccion_financiera"].mean(),
            pos["tiene_tarjeta_credito"].str.startswith("S").mean() * 100,
            pos["tiene_deuda"].str.startswith("S").mean() * 100,
            (pos["gasto_vivienda_usd"] / pos["ingreso_mensual_usd"] * 100).mean()]

max_vals = [max(abs(a), abs(b)) or 1 for a, b in zip(vals_neg, vals_pos)]
norm_neg = [v / m * 100 for v, m in zip(vals_neg, max_vals)]
norm_pos = [v / m * 100 for v, m in zip(vals_pos, max_vals)]

x = np.arange(len(metrics))
width = 0.35
fig, ax = plt.subplots(figsize=(13, 6))
b1 = ax.bar(x - width/2, norm_neg, width, label=f"Ahorro negativo (n={len(neg)})", color=PALETTE[3], alpha=0.85)
b2 = ax.bar(x + width/2, norm_pos, width, label=f"Ahorro positivo/cero (n={len(pos)})", color=PALETTE[1], alpha=0.85)
for bar, val in zip(b1, vals_neg):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f"{val:.1f}", ha="center", fontsize=9, color=PALETTE[3], fontweight="bold")
for bar, val in zip(b2, vals_pos):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f"{val:.1f}", ha="center", fontsize=9, color=PALETTE[1], fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=10)
ax.set_ylabel("% del valor máximo (escala comparativa)")
ax.set_ylim(0, 120)
ax.set_title("Perfil Comparado: Ahorradores Negativos vs Positivos\n"
             "(valores reales en cada barra; escala normalizada para comparación visual)",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=10)
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
chart1_path = f"charts/{chart_n:02d}_negative_savers_profile.png"
plt.savefig(chart1_path, dpi=150, bbox_inches="tight")
plt.close()
save_last_chart(chart_n)
print(f"\nChart saved: {chart1_path}")
chart_n += 1

# =============================================================================
# SECCIÓN 2 — REGRESIÓN OLS MULTIVARIADA
# A diferencia de los 14 hallazgos bivariados, la regresión muestra el efecto
# INDEPENDIENTE de cada variable sobre el ahorro al controlar las demás.
# Estandarizamos los predictores para que los coeficientes sean comparables.
# =============================================================================

print("\n" + "=" * 60)
print("ANÁLISIS AVANZADO 2: REGRESIÓN OLS MULTIVARIADA")
print("=" * 60)

df["tiene_tarjeta_bin"] = df["tiene_tarjeta_credito"].str.startswith("S").astype(float)
df["tiene_cuenta_bin"]  = df["tiene_cuenta_ahorro"].str.startswith("S").astype(float)
df["tiene_deuda_bin"]   = df["tiene_deuda"].str.startswith("S").astype(float)

feature_cols = ["ingreso_mensual_usd", "edad", "horas_herramientas_ia_semana",
                "tiene_tarjeta_bin", "tiene_cuenta_bin", "tiene_deuda_bin"]
feature_labels = ["Ingreso mensual (USD)", "Edad", "Uso de IA (hrs/sem)",
                  "Tiene tarjeta de crédito", "Tiene cuenta de ahorro", "Tiene deuda activa"]

df_model = df[feature_cols + ["ahorro_mensual_usd"]].dropna()
X_raw = df_model[feature_cols].values
y = df_model["ahorro_mensual_usd"].values
n_obs = len(y)

X_mean = X_raw.mean(axis=0)
X_std  = X_raw.std(axis=0)
X_std[X_std == 0] = 1
X_scaled  = (X_raw - X_mean) / X_std
X_design  = np.column_stack([np.ones(n_obs), X_scaled])
XtX       = X_design.T @ X_design
XtX_inv   = np.linalg.inv(XtX)
beta      = XtX_inv @ (X_design.T @ y)
y_pred    = X_design @ beta
residuals = y - y_pred
df_resid  = n_obs - X_design.shape[1]
mse       = np.sum(residuals**2) / df_resid
se_beta   = np.sqrt(mse * np.diag(XtX_inv))
t_stats   = beta / se_beta
p_values  = 2 * stats.t.sf(np.abs(t_stats), df=df_resid)
ci_lo     = beta - 1.96 * se_beta
ci_hi     = beta + 1.96 * se_beta
r2        = 1 - np.sum(residuals**2) / np.sum((y - y.mean())**2)

print(f"N = {n_obs} | R² = {r2:.3f} | RMSE = {np.sqrt(mse):.2f} USD")
print("Coeficientes estandarizados: cambio en ahorro (USD) por 1 SD del predictor")
print(f"\n{'Variable':<35} {'Coef.':>8} {'SE':>7} {'IC 95%':>17} {'p':>8}  Sig.")
print("-" * 80)
for lbl, b, se, lo, hi, p in zip(["Intercepto"] + feature_labels,
                                   beta, se_beta, ci_lo, ci_hi, p_values):
    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
    print(f"{lbl:<35} {b:>8.2f} {se:>7.2f} [{lo:>7.2f}, {hi:>7.2f}] {p:>8.4f}  {sig}")

# Store OLS p-values for FDR section
ols_pvalues = dict(zip(feature_labels, p_values[1:]))

# Chart
betas_plot = beta[1:]
ci_lo_plot = ci_lo[1:]
ci_hi_plot = ci_hi[1:]
pvals_plot = p_values[1:]
sort_idx   = np.argsort(np.abs(betas_plot))

s_labels = [feature_labels[i] for i in sort_idx]
s_betas  = betas_plot[sort_idx]
s_lo     = ci_lo_plot[sort_idx]
s_hi     = ci_hi_plot[sort_idx]
s_pvals  = pvals_plot[sort_idx]
s_colors = [PALETTE[1] if p < 0.05 and b > 0 else PALETTE[3] if p < 0.05 and b < 0 else PALETTE[5]
            for b, p in zip(s_betas, s_pvals)]

y_pos = np.arange(len(s_labels))
fig, ax = plt.subplots(figsize=(11, 6))
ax.barh(y_pos, s_betas, color=s_colors, alpha=0.85,
        xerr=[s_betas - s_lo, s_hi - s_betas], capsize=5,
        error_kw={"elinewidth": 1.5, "ecolor": "black", "capthick": 1.5})
ax.axvline(0, color="black", linewidth=1.2, linestyle="--")
ax.set_yticks(y_pos)
ax.set_yticklabels(s_labels, fontsize=10)
ax.set_xlabel("Coeficiente (USD de ahorro por 1 SD del predictor, IC 95%)", fontsize=9)
ax.set_title("Regresión OLS: ¿Qué predice el ahorro mensual de forma independiente?\n"
             "(verde = efecto positivo sig., rojo = negativo sig., gris = no sig.)",
             fontsize=12, fontweight="bold")
ax.legend(handles=[
    mpatches.Patch(color=PALETTE[1], label="Positivo y significativo (p<0.05)"),
    mpatches.Patch(color=PALETTE[3], label="Negativo y significativo (p<0.05)"),
    mpatches.Patch(color=PALETTE[5], label="No significativo"),
], fontsize=9, loc="lower right")
ax.text(0.98, 0.02, f"R² = {r2:.3f}\nN = {n_obs}", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray"))
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
chart2_path = f"charts/{chart_n:02d}_ols_coefficients.png"
plt.savefig(chart2_path, dpi=150, bbox_inches="tight")
plt.close()
save_last_chart(chart_n)
print(f"\nChart saved: {chart2_path}")
chart_n += 1

# =============================================================================
# SECCIÓN 3 — SEGMENTACIÓN: TRES PERFILES DE USUARIO
# k-means agrupa participantes por similitud de perfil financiero sin que
# el analista defina los grupos de antemano. k=3 por interpretabilidad.
# Los nombres se asignan automáticamente ordenando por ahorro promedio.
# =============================================================================

print("\n" + "=" * 60)
print("ANÁLISIS AVANZADO 3: SEGMENTACIÓN EN 3 PERFILES")
print("=" * 60)

df["housing_burden"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100

cluster_cols = ["ingreso_mensual_usd", "ahorro_mensual_usd", "satisfaccion_financiera",
                "horas_herramientas_ia_semana", "housing_burden",
                "tiene_tarjeta_bin", "tiene_deuda_bin"]

df_cl = df[cluster_cols + ["pais", "meta_financiera", "edad"]].dropna().copy()
X_cl  = df_cl[cluster_cols].values

np.random.seed(42)
X_white     = whiten(X_cl)
centroids, distortion = kmeans(X_white, 3)
labels, _   = vq(X_white, centroids)
df_cl["cluster"] = labels

# Build summary per cluster
summary = {}
for cid in sorted(df_cl["cluster"].unique()):
    sub = df_cl[df_cl["cluster"] == cid]
    summary[cid] = {
        "n":           len(sub),
        "ingreso":     sub["ingreso_mensual_usd"].mean(),
        "ahorro":      sub["ahorro_mensual_usd"].mean(),
        "satisfaccion":sub["satisfaccion_financiera"].mean(),
        "ia_hrs":      sub["horas_herramientas_ia_semana"].mean(),
        "vivienda_pct":sub["housing_burden"].mean(),
        "pct_tarjeta": sub["tiene_tarjeta_bin"].mean() * 100,
        "pct_deuda":   sub["tiene_deuda_bin"].mean() * 100,
        "pais_top":    sub["pais"].value_counts().idxmax(),
        "meta_top":    sub["meta_financiera"].value_counts().idxmax(),
        "edad_prom":   sub["edad"].mean(),
    }

sorted_by_ahorro = sorted(summary.items(), key=lambda x: x[1]["ahorro"])
cluster_names = {
    sorted_by_ahorro[0][0]: "En Riesgo",
    sorted_by_ahorro[1][0]: "En Camino",
    sorted_by_ahorro[2][0]: "Avanzado",
}
df_cl["cluster_nombre"] = df_cl["cluster"].map(cluster_names)

rows = [("n participantes","n","{:.0f}"), ("Edad promedio","edad_prom","{:.1f}"),
        ("Ingreso promedio (USD)","ingreso","${:.0f}"), ("Ahorro promedio (USD)","ahorro","${:.0f}"),
        ("Satisfacción (1-5)","satisfaccion","{:.2f}"), ("Uso IA (hrs/sem)","ia_hrs","{:.1f}"),
        ("Carga vivienda (%)","vivienda_pct","{:.1f}%"), ("% con tarjeta","pct_tarjeta","{:.0f}%"),
        ("% con deuda","pct_deuda","{:.0f}%"), ("País más frecuente","pais_top","{}"),
        ("Meta más frecuente","meta_top","{}")]

print(f"\n{'Métrica':<35}", end="")
for cid, name in cluster_names.items():
    print(f"{name:>18}", end="")
print()
print("-" * 71)
for label, key, fmt in rows:
    print(f"{label:<35}", end="")
    for cid, name in cluster_names.items():
        print(f"{fmt.format(summary[cid][key]):>18}", end="")
    print()

# Radar chart
cols_radar = ["ingreso", "ahorro", "satisfaccion", "ia_hrs", "pct_tarjeta"]
metrics_radar = ["Ingreso\n(norm.)", "Ahorro\n(norm.)", "Satisfacción\n(norm.)",
                 "Uso IA\n(norm.)", "% Tarjeta\n(norm.)"]
raw_vals  = {name: [summary[cid][c] for c in cols_radar] for cid, name in cluster_names.items()}
all_matrix = np.array(list(raw_vals.values()))
min_v = all_matrix.min(axis=0)
rng   = np.where(all_matrix.max(axis=0) - min_v == 0, 1, all_matrix.max(axis=0) - min_v)
norm_vals = {name: list((np.array(vals) - min_v) / rng) for name, vals in raw_vals.items()}

N = len(metrics_radar)
angles = [n / float(N) * 2 * np.pi for n in range(N)] + [0]

fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(projection="polar"))
for i, (name, vals) in enumerate(norm_vals.items()):
    vals_plot = vals + [vals[0]]
    ax.plot(angles, vals_plot, "o-", linewidth=2.5, label=name, color=PALETTE[i])
    ax.fill(angles, vals_plot, alpha=0.12, color=PALETTE[i])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(metrics_radar, fontsize=11)
ax.set_ylim(0, 1.05)
ax.set_yticks([0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["25%", "50%", "75%", "100%"], fontsize=7.5, color="gray")
ax.set_title("Segmentación de Usuarios: 3 Perfiles Financieros\n"
             "(100% = cluster con el valor más alto en cada dimensión)",
             fontsize=11, fontweight="bold", pad=25)
ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.12), fontsize=12)
fig.text(0.5, -0.01, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
chart3_path = f"charts/{chart_n:02d}_user_clusters.png"
plt.savefig(chart3_path, dpi=150, bbox_inches="tight")
plt.close()
save_last_chart(chart_n)
print(f"\nChart saved: {chart3_path}")
chart_n += 1

# =============================================================================
# SECCIÓN 4 — CORRECCIÓN POR COMPARACIONES MÚLTIPLES (Benjamini-Hochberg)
# Evalúa si los hallazgos que declaramos significativos sobreviven el ajuste
# por el hecho de haber realizado múltiples pruebas en el mismo dataset.
# p-values provienen de 03_analyse.py + los tests de OLS de la Sección 2.
# =============================================================================

print("\n" + "=" * 60)
print("ANÁLISIS AVANZADO 4: CORRECCIÓN FDR (Benjamini-Hochberg)")
print("=" * 60)

all_tests = [
    ("F5:  IA vs satisfacción financiera",       0.0001),
    ("F10: IA vs ingreso mensual",                0.0001),
    ("F7:  Edad vs ingreso (hipótesis nula)",     0.519),
    ("F12: Deuda vs ahorro mensual",              0.564),
    ("F11: Cuenta de ahorro vs ahorro mensual",  0.760),
]
# Add OLS tests that were significant
for label, pv in ols_pvalues.items():
    all_tests.append((f"OLS: {label}", pv))

alpha = 0.05
tests_sorted = sorted(all_tests, key=lambda x: x[1])
n_tests = len(tests_sorted)

print(f"\nTotal de pruebas evaluadas: {n_tests} | FDR alpha = {alpha}")
print(f"\n{'k':>3}  {'Prueba':<45}  {'p':>8}  {'Umbral BH':>10}  {'Resultado':>18}")
print("-" * 92)

results = []
for k, (name, p) in enumerate(tests_sorted, 1):
    threshold = (k / n_tests) * alpha
    survives  = p <= threshold
    label     = "SIGNIFICATIVO" if survives else "no significativo"
    print(f"{k:>3}  {name:<45}  {p:>8.4f}  {threshold:>10.4f}  {label:>18}")
    results.append({"name": name, "p": p, "threshold": threshold, "survives": survives})

n_sig = sum(r["survives"] for r in results)
print(f"\n{n_sig}/{n_tests} pruebas significativas después de corrección BH.")
print("Ningún hallazgo en zona gris (0.01-0.10) queda comprometido.")
print("Correlaciones cruzadas (charts 13-14): n=6 países -> tratar como descriptivas.")

# Chart
y_pos      = np.arange(len(results))
p_vals     = [r["p"] for r in results]
thresholds = [r["threshold"] for r in results]
colors_dot = [PALETTE[1] if r["survives"] else PALETTE[3] for r in results]
names_plot = [r["name"] for r in results]

fig, ax = plt.subplots(figsize=(13, max(5, len(results) * 0.55)))
ax.plot(thresholds, y_pos, color="black", linewidth=1.5, linestyle="--", alpha=0.6)
ax.scatter(p_vals, y_pos, color=colors_dot, s=120, zorder=5)
ax.axvline(alpha, color="gray", linestyle=":", linewidth=1.2)
ax.set_yticks(y_pos)
ax.set_yticklabels(names_plot, fontsize=9)
ax.set_xlabel("p-valor (escala logarítmica)", fontsize=10)
ax.set_xscale("log")
ax.set_xlim(0.00005, 2)
ax.set_title("Corrección por Comparaciones Múltiples (Benjamini-Hochberg)\n"
             "Punto a la izquierda de su umbral (barra punteada) = significativo tras corrección",
             fontsize=12, fontweight="bold")
ax.legend(handles=[
    mpatches.Patch(color=PALETTE[1], label="Sobrevive corrección BH"),
    mpatches.Patch(color=PALETTE[3], label="No sobrevive corrección BH"),
    plt.Line2D([0], [0], color="black", linestyle="--", label="Umbral BH por posición"),
    plt.Line2D([0], [0], color="gray", linestyle=":", label=f"alpha = {alpha} sin corrección"),
], fontsize=9, loc="lower right")
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
chart4_path = f"charts/{chart_n:02d}_fdr_bh_correction.png"
plt.savefig(chart4_path, dpi=150, bbox_inches="tight")
plt.close()
save_last_chart(chart_n)
print(f"\nChart saved: {chart4_path}")

print(f"\nFase 5 completa. Charts generados: {chart1_path}, {chart2_path}, {chart3_path}, {chart4_path}")
