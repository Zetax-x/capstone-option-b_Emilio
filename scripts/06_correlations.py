import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import glob, os

df = pd.read_csv("data/latam_finanzas_clean.csv")
df["housing_burden_pct"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100

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

# --- Correlation chart: Housing burden vs savings rate by country ---
n = next_chart_num()
country_stats = df.groupby("pais").agg(
    housing_burden=("housing_burden_pct", "mean"),
    avg_savings=("ahorro_mensual_usd", "mean"),
    avg_income=("ingreso_mensual_usd", "median")
).reset_index()

fig, ax = plt.subplots(figsize=(9, 6))
for i, row in country_stats.iterrows():
    ax.scatter(row["housing_burden"], row["avg_savings"],
               s=row["avg_income"] / 5, color=PALETTE[i], zorder=5, edgecolors="white", linewidth=1.5)
    ax.annotate(row["pais"], (row["housing_burden"], row["avg_savings"]),
                textcoords="offset points", xytext=(8, 4), fontsize=10)

r, p = stats.pearsonr(country_stats["housing_burden"], country_stats["avg_savings"])
m, b = np.polyfit(country_stats["housing_burden"], country_stats["avg_savings"], 1)
x_line = np.linspace(country_stats["housing_burden"].min() - 1, country_stats["housing_burden"].max() + 1, 100)
ax.plot(x_line, m * x_line + b, color="gray", linestyle="--", linewidth=1.5)
ax.text(0.05, 0.92, f"r = {r:.2f}, p = {p:.3f}", transform=ax.transAxes, fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray"))
ax.set_xlabel("Carga de Vivienda (% del ingreso)")
ax.set_ylabel("Ahorro Mensual Promedio (USD)")
ax.set_title("Carga de Vivienda vs. Ahorro Promedio por País\n(tamaño del punto = ingreso mediano)", fontsize=13, fontweight="bold")
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
fname = f"charts/{n:02d}_vivienda_vs_ahorro.png"
plt.savefig(fname, dpi=150, bbox_inches="tight")
plt.close()
save_last_chart(n)
print(f"Chart {n} saved: {fname}")

# --- Correlation chart: IA usage vs satisfaction by country ---
n = next_chart_num()
country_ia = df.groupby("pais").agg(
    avg_ia=("horas_herramientas_ia_semana", "mean"),
    avg_satisfaction=("satisfaccion_financiera", "mean"),
    avg_income=("ingreso_mensual_usd", "median")
).reset_index()

fig, ax = plt.subplots(figsize=(9, 6))
for i, row in country_ia.iterrows():
    ax.scatter(row["avg_ia"], row["avg_satisfaction"],
               s=row["avg_income"] / 5, color=PALETTE[i], zorder=5, edgecolors="white", linewidth=1.5)
    ax.annotate(row["pais"], (row["avg_ia"], row["avg_satisfaction"]),
                textcoords="offset points", xytext=(8, 4), fontsize=10)

r, p = stats.pearsonr(country_ia["avg_ia"], country_ia["avg_satisfaction"])
m, b = np.polyfit(country_ia["avg_ia"], country_ia["avg_satisfaction"], 1)
x_line = np.linspace(country_ia["avg_ia"].min() - 0.3, country_ia["avg_ia"].max() + 0.3, 100)
ax.plot(x_line, m * x_line + b, color="gray", linestyle="--", linewidth=1.5)
ax.text(0.05, 0.92, f"r = {r:.2f}, p = {p:.3f}", transform=ax.transAxes, fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray"))
ax.set_xlabel("Uso Promedio de IA (hrs/semana)")
ax.set_ylabel("Satisfaccion Financiera Promedio (1-5)")
ax.set_title("Uso de IA vs. Satisfaccion Financiera por Pais\n(tamano del punto = ingreso mediano)", fontsize=13, fontweight="bold")
fig.text(0.5, -0.02, SOURCE, ha="center", fontsize=8, color="gray")
plt.tight_layout()
fname = f"charts/{n:02d}_ia_vs_satisfaccion.png"
plt.savefig(fname, dpi=150, bbox_inches="tight")
plt.close()
save_last_chart(n)
print(f"Chart {n} saved: {fname}")

total = len(glob.glob("charts/*.png"))
print(f"\nTotal charts: {total}")
