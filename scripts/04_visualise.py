import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy import stats

df = pd.read_csv("data/latam_finanzas_clean.csv")

PALETTE = ["#2E4057", "#048A81", "#54C6EB", "#EF6F6C", "#8EE3EF", "#CAD2C5"]
SOURCE = "Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"

# --- Chart 1: Income by country (box plot) ---
fig, ax = plt.subplots(figsize=(10, 6))
paises_order = df.groupby("pais")["ingreso_mensual_usd"].median().sort_values(ascending=False).index.tolist()
data_by_country = [df[df["pais"] == p]["ingreso_mensual_usd"].values for p in paises_order]
bp = ax.boxplot(data_by_country, vert=False, patch_artist=True, tick_labels=paises_order)
for patch, color in zip(bp["boxes"], PALETTE):
    patch.set_facecolor(color)
ax.set_xlabel("Ingreso Mensual (USD)")
ax.set_title("Distribución de Ingresos por País", fontsize=14, fontweight="bold")
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("charts/01_income_by_country.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 1 saved: charts/01_income_by_country.png")

# --- Chart 2: Age vs savings scatter ---
fig, ax = plt.subplots(figsize=(10, 6))
colors = {p: PALETTE[i] for i, p in enumerate(df["pais"].unique())}
for pais, group in df.groupby("pais"):
    ax.scatter(group["edad"], group["ahorro_mensual_usd"],
               color=colors.get(pais, "#999"), alpha=0.5, s=30, label=pais)
m, b, r, p, _ = stats.linregress(df["edad"], df["ahorro_mensual_usd"])
x_line = np.linspace(df["edad"].min(), df["edad"].max(), 100)
ax.plot(x_line, m * x_line + b, color="black", linewidth=2, label=f"Tendencia (r={r:.2f})")
ax.set_xlabel("Edad")
ax.set_ylabel("Ahorro Mensual (USD)")
ax.set_title("Edad vs. Ahorro Mensual por País", fontsize=14, fontweight="bold")
ax.legend(fontsize=8)
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("charts/02_age_vs_savings.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 2 saved: charts/02_age_vs_savings.png")

# --- Chart 3: Spending breakdown (horizontal bar) ---
gasto_cols = {
    "Vivienda": "gasto_vivienda_usd",
    "Alimentación": "gasto_alimentacion_usd",
    "Transporte": "gasto_transporte_usd",
    "Entretenimiento": "gasto_entretenimiento_usd",
    "Educación": "gasto_educacion_usd",
    "Salud": "gasto_salud_usd",
}
pcts = {k: (df[v] / df["ingreso_mensual_usd"] * 100).mean() for k, v in gasto_cols.items()}
pcts_sorted = dict(sorted(pcts.items(), key=lambda x: x[1], reverse=True))
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(list(pcts_sorted.keys()), list(pcts_sorted.values()), color=PALETTE[:len(pcts_sorted)])
for bar, val in zip(bars, pcts_sorted.values()):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%", va="center", fontsize=10)
ax.set_xlabel("% del Ingreso Mensual")
ax.set_title("Desglose de Gastos Promedio (% del Ingreso)", fontsize=14, fontweight="bold")
ax.invert_yaxis()
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("charts/03_spending_breakdown.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 3 saved: charts/03_spending_breakdown.png")

# --- Chart 4: Financial satisfaction by AI usage (with 95% CI error bars) ---
df["ia_group"] = pd.cut(df["horas_herramientas_ia_semana"],
                         bins=[-1, 3, 10, 100],
                         labels=["Bajo\n(0-3h/sem)", "Medio\n(4-10h/sem)", "Alto\n(11+h/sem)"])
ia_stats = df.groupby("ia_group", observed=True)["satisfaccion_financiera"].agg(["mean", "std", "count"])
ci_95 = 1.96 * ia_stats["std"] / np.sqrt(ia_stats["count"])  # IC 95% = 1.96 * error estándar
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(ia_stats.index, ia_stats["mean"], color=PALETTE[:3], width=0.5,
              yerr=ci_95, capsize=7, error_kw={"color": "black", "linewidth": 1.5, "zorder": 5})
for bar, val in zip(bars, ia_stats["mean"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
            f"{val:.2f}", ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 5)
ax.set_ylabel("Satisfacción Financiera Promedio (1–5)")
ax.set_title("Satisfacción Financiera por Nivel de Uso de IA\n(barras de error = IC 95%)", fontsize=13, fontweight="bold")
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("charts/04_satisfaction_by_ai_usage.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 4 saved: charts/04_satisfaction_by_ai_usage.png")

# --- Chart 5: Housing burden by country (red-to-green gradient) ---
df["housing_burden_pct"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100
burden = df.groupby("pais")["housing_burden_pct"].mean().sort_values(ascending=False)
n = len(burden)
gradient = [plt.cm.RdYlGn(1 - i / (n - 1)) for i in range(n)]
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(burden.index, burden.values, color=gradient)
for bar, val in zip(bars, burden.values):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%", va="center", fontsize=10)
ax.set_xlabel("Carga de Vivienda (% del Ingreso)")
ax.set_title("Carga de Vivienda por País", fontsize=14, fontweight="bold")
ax.invert_yaxis()
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("charts/05_housing_burden_by_country.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 5 saved: charts/05_housing_burden_by_country.png")

# --- Chart 6: Spending proportions by age group (Finding 8) ---
gasto_labels = ["Vivienda", "Alimentacion", "Transporte", "Entretenimiento", "Educacion", "Salud"]
gasto_pct_cols = [c + "_pct" for c in ["gasto_vivienda_usd", "gasto_alimentacion_usd",
                  "gasto_transporte_usd", "gasto_entretenimiento_usd",
                  "gasto_educacion_usd", "gasto_salud_usd"]]
for col in ["gasto_vivienda_usd","gasto_alimentacion_usd","gasto_transporte_usd",
            "gasto_entretenimiento_usd","gasto_educacion_usd","gasto_salud_usd"]:
    df[col + "_pct"] = df[col] / df["ingreso_mensual_usd"] * 100

bins = [17, 22, 25, 28, 32]
labels_age = ["18-22", "23-25", "26-28", "29-32"]
df["age_group"] = pd.cut(df["edad"], bins=bins, labels=labels_age)
spending_by_age = df.groupby("age_group", observed=True)[gasto_pct_cols].mean()
spending_by_age.columns = gasto_labels

fig, ax = plt.subplots(figsize=(11, 6))
for i, col in enumerate(gasto_labels):
    ax.plot(spending_by_age.index, spending_by_age[col], marker="o",
            color=PALETTE[i % len(PALETTE)], linewidth=2, label=col)
ax.set_xlabel("Grupo de Edad")
ax.set_ylabel("% del Ingreso Mensual")
ax.set_title("Proporciones de Gasto por Grupo de Edad\n(lineas planas = patron estable)", fontsize=13, fontweight="bold")
ax.legend(loc="upper right", fontsize=8)
ax.set_ylim(0, 40)
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("charts/06_spending_by_age_group.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 6 saved: charts/06_spending_by_age_group.png")

# --- Chart 7: Income by industry (Finding 9) ---
industry_order = df.groupby("industria")["ingreso_mensual_usd"].median().sort_values(ascending=False).index.tolist()
data_by_industry = [df[df["industria"] == ind]["ingreso_mensual_usd"].values for ind in industry_order]
fig, ax = plt.subplots(figsize=(12, 7))
bp = ax.boxplot(data_by_industry, vert=False, patch_artist=True, tick_labels=industry_order)
for patch, color in zip(bp["boxes"], PALETTE * 2):
    patch.set_facecolor(color)
ax.set_xlabel("Ingreso Mensual (USD)")
ax.set_title("Distribucion de Ingresos por Industria", fontsize=14, fontweight="bold")
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("charts/07_income_by_industry.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 7 saved: charts/07_income_by_industry.png")

# --- Chart 8: High AI users overlaid on industry boxplot (Finding 10) ---
fig, ax = plt.subplots(figsize=(12, 7))
bp = ax.boxplot(data_by_industry, vert=False, patch_artist=True, tick_labels=industry_order)
for patch in bp["boxes"]:
    patch.set_facecolor("#CCCCCC")
    patch.set_alpha(0.5)
df["high_ia"] = df["horas_herramientas_ia_semana"] >= 11
for i, ind in enumerate(industry_order):
    sub = df[(df["industria"] == ind) & (df["high_ia"])]
    if len(sub) > 0:
        ax.scatter(sub["ingreso_mensual_usd"], [i + 1] * len(sub),
                   color="#EF6F6C", s=60, zorder=5, alpha=0.85)
ax.scatter([], [], color="#EF6F6C", s=60, label="Alto uso IA (11+ hrs/sem)")
ax.legend(fontsize=10)
ax.set_xlabel("Ingreso Mensual (USD)")
ax.set_title("Usuarios de Alto Uso de IA dentro de cada Industria\n(puntos rojos = 11+ hrs/semana)", fontsize=13, fontweight="bold")
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("charts/08_high_ia_by_industry.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 8 saved: charts/08_high_ia_by_industry.png")

# --- Chart 9: Savings account holders vs non-holders (Finding 11) ---
sa_groups = ["Con cuenta\nde ahorro", "Sin cuenta\nde ahorro"]
sa_yes = df[df["tiene_cuenta_ahorro"].str.startswith("S")]
sa_no = df[df["tiene_cuenta_ahorro"] == "No"]
metrics = ["Ahorro mensual\n(USD)", "Satisfaccion\nfinanciera (x40)"]
vals_yes = [sa_yes["ahorro_mensual_usd"].mean(), sa_yes["satisfaccion_financiera"].mean() * 40]
vals_no  = [sa_no["ahorro_mensual_usd"].mean(),  sa_no["satisfaccion_financiera"].mean() * 40]

x = np.arange(len(metrics))
width = 0.35
fig, ax = plt.subplots(figsize=(9, 6))
b1 = ax.bar(x - width/2, vals_yes, width, label="Con cuenta de ahorro", color=PALETTE[0])
b2 = ax.bar(x + width/2, vals_no,  width, label="Sin cuenta de ahorro",  color=PALETTE[3])
for bar in list(b1) + list(b2):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f"{bar.get_height():.1f}", ha="center", fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.set_title("Cuenta de Ahorro: Comportamiento Real vs Expectativa\n(satisfaccion escalada x40 para comparacion visual)", fontsize=12, fontweight="bold")
ax.legend()
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("charts/09_savings_account_vs_behaviour.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 9 saved: charts/09_savings_account_vs_behaviour.png")

# --- Chart 10: Debt holders — savings and satisfaction (Finding 12) ---
has_debt = df[df["tiene_deuda"].str.startswith("S")]
no_debt  = df[df["tiene_deuda"] == "No"]
fig, ax1 = plt.subplots(figsize=(9, 6))
ax2 = ax1.twinx()
groups = ["Con deuda", "Sin deuda"]
ahorro_vals = [has_debt["ahorro_mensual_usd"].mean(), no_debt["ahorro_mensual_usd"].mean()]
sat_vals    = [has_debt["satisfaccion_financiera"].mean(), no_debt["satisfaccion_financiera"].mean()]
x = np.arange(len(groups))
b1 = ax1.bar(x - 0.2, ahorro_vals, 0.35, color=PALETTE[0], label="Ahorro mensual (USD)")
b2 = ax2.bar(x + 0.2, sat_vals,    0.35, color=PALETTE[3], label="Satisfaccion financiera (1-5)")
for bar, val in zip(b1, ahorro_vals):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f"${val:.0f}", ha="center", fontsize=10, color=PALETTE[0])
for bar, val in zip(b2, sat_vals):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f"{val:.2f}", ha="center", fontsize=10, color=PALETTE[3])
ax1.set_xticks(x)
ax1.set_xticklabels(groups, fontsize=12)
ax1.set_ylabel("Ahorro Mensual (USD)", color=PALETTE[0])
ax2.set_ylabel("Satisfaccion Financiera (1-5)", color=PALETTE[3])
ax1.set_title("Deuda: Impacto en Ahorro y Satisfaccion Financiera", fontsize=13, fontweight="bold")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("charts/10_debt_vs_savings_satisfaction.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 10 saved: charts/10_debt_vs_savings_satisfaction.png")

# --- Chart 11: Financial goal vs actual savings rate (Finding 13) ---
goal_data = df.groupby("meta_financiera").agg(
    avg_ahorro=("ahorro_mensual_usd", "mean"),
    avg_income=("ingreso_mensual_usd", "mean")
)
goal_data["savings_rate"] = goal_data["avg_ahorro"] / goal_data["avg_income"] * 100
goal_data = goal_data.sort_values("savings_rate", ascending=True)
colors_goal = [PALETTE[3] if v < goal_data["savings_rate"].median() else PALETTE[1]
               for v in goal_data["savings_rate"]]
fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.barh(goal_data.index, goal_data["savings_rate"], color=colors_goal)
for bar, val in zip(bars, goal_data["savings_rate"]):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}%", va="center", fontsize=10)
ax.axvline(goal_data["savings_rate"].median(), color="gray", linestyle="--", linewidth=1.5, label="Mediana")
ax.set_xlabel("Tasa de Ahorro (% del Ingreso)")
ax.set_title("Meta Financiera vs Tasa de Ahorro Real\n(verde = sobre la mediana, rojo = bajo la mediana)", fontsize=12, fontweight="bold")
ax.legend(fontsize=9)
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("charts/11_goal_vs_savings_rate.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 11 saved: charts/11_goal_vs_savings_rate.png")

# --- Chart 12: Credit card spending breakdown by category (Finding 14) ---
gasto_cols_labels = {
    "gasto_vivienda_usd": "Vivienda",
    "gasto_alimentacion_usd": "Alimentacion",
    "gasto_transporte_usd": "Transporte",
    "gasto_entretenimiento_usd": "Entretenimiento",
    "gasto_educacion_usd": "Educacion",
    "gasto_salud_usd": "Salud",
}
cc_yes = df[df["tiene_tarjeta_credito"].str.startswith("S")]
cc_no  = df[df["tiene_tarjeta_credito"] == "No"]
diffs = {label: ((cc_yes[col].mean() / cc_no[col].mean()) - 1) * 100
         for col, label in gasto_cols_labels.items()}
diffs_sorted = dict(sorted(diffs.items(), key=lambda x: x[1], reverse=True))
bar_colors = [PALETTE[3] if v >= 10 else PALETTE[1] if v >= 5 else PALETTE[2]
              for v in diffs_sorted.values()]
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(list(diffs_sorted.keys()), list(diffs_sorted.values()), color=bar_colors)
for bar, val in zip(bars, diffs_sorted.values()):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            f"+{val:.1f}%", va="center", fontsize=10)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_xlabel("Diferencia de Gasto vs Sin Tarjeta (%)")
ax.set_title("Tarjetahabientes: Exceso de Gasto por Categoria\n(vs no tarjetahabientes, mismo nivel de ingreso)", fontsize=12, fontweight="bold")
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
plt.savefig("charts/12_credit_card_spending_by_category.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 12 saved: charts/12_credit_card_spending_by_category.png")

total = len([f for f in __import__("os").listdir("charts") if f.endswith(".png")])
print(f"\nTotal: {total} charts generated")

with open("charts/.last_chart", "w") as f:
    f.write("12")
print("charts/.last_chart updated: 12")
