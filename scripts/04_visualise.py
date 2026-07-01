import matplotlib
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.lines as mlines
import seaborn as sns
import numpy as np
from scipy import stats

# ── Global style ──────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams["font.family"] = "DejaVu Sans"

SOURCE = "Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"

COUNTRY_PALETTE = {
    "Mexico":    "#2196F3",
    "Brasil":    "#4CAF50",
    "Argentina": "#FF5722",
    "Chile":     "#9C27B0",
    "Colombia":  "#FF9800",
    "Peru":      "#00BCD4",
}

df = pd.read_csv("data/latam_finanzas_clean.csv")

# Normalize country names for palette lookup (strip accents for key matching)
country_name_map = {
    "México":    "Mexico",
    "Brasil":    "Brasil",
    "Argentina": "Argentina",
    "Chile":     "Chile",
    "Colombia":  "Colombia",
    "Perú":      "Peru",
}
df["pais_key"] = df["pais"].map(country_name_map)

def add_source(fig):
    fig.text(0.5, -0.02, SOURCE, ha="center", va="bottom",
             fontsize=8, color="grey", style="italic")

# ── 1. BOX PLOT — Income by country ──────────────────────────────────────────
print("Generating chart 1...")

medians = df.groupby("pais_key")["ingreso_mensual_usd"].median().sort_values()
country_order = medians.index.tolist()  # lowest to highest (top of h-plot = highest)

fig, ax = plt.subplots(figsize=(10, 6))

data_by_country = [df[df["pais_key"] == c]["ingreso_mensual_usd"].values for c in country_order]
bp = ax.boxplot(data_by_country, orientation="horizontal", patch_artist=True,
                medianprops=dict(color="black", linewidth=2))

for i, (patch, country) in enumerate(zip(bp["boxes"], country_order), start=1):
    patch.set_facecolor(COUNTRY_PALETTE[country])
    patch.set_alpha(0.8)
    median_val = medians[country]
    y_offset = -0.365 if country == "Argentina" else -0.38
    ax.text(median_val, i + y_offset, f"Median: ${median_val:,.0f}",
            va="top", ha="center", fontsize=8.5, fontweight="bold", color="#212121")

display_labels = [k for k in country_order]
ax.set_yticklabels(display_labels, fontsize=11)
ax.set_xlabel("Monthly Income (USD)", fontsize=12)
ax.set_title("Income Distribution by Country\n(sorted by median income)", fontsize=14, fontweight="bold")

median_handle  = mlines.Line2D([], [], color='black', linewidth=2,
                                label='Median income (labeled below each box)')
outlier_handle = mlines.Line2D([], [], marker='o', linestyle='none',
                                markerfacecolor='none', markeredgecolor='#555555',
                                markersize=6,
                                label='Circles = outliers\n(income > 1.5× IQR from box edges)')
ax.legend(handles=[median_handle, outlier_handle], loc='upper right',
          fontsize=8, framealpha=0.6, edgecolor='#aaaaaa', handlelength=1.5)

add_source(fig)
plt.tight_layout()
plt.savefig("charts/01_income_by_country.png", dpi=150, bbox_inches="tight")
plt.close()
print("  -> charts/01_income_by_country.png saved")

# ── 2. SCATTER PLOT — Age vs Savings with trend line ─────────────────────────
print("Generating chart 2...")

fig, ax = plt.subplots(figsize=(10, 6))

for country_key, color in COUNTRY_PALETTE.items():
    subset = df[df["pais_key"] == country_key]
    ax.scatter(subset["edad"], subset["ahorro_mensual_usd"],
               color=color, alpha=0.55, s=35, label=country_key, edgecolors="none")

slope, intercept, r, p, _ = stats.linregress(df["edad"], df["ahorro_mensual_usd"])
x_line = np.linspace(df["edad"].min(), df["edad"].max(), 200)
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, color="#212121", linewidth=2, linestyle="--",
        label=f"Trend (r={r:.2f})")

ax.axhline(0, color="red", linewidth=1.35, linestyle="--", alpha=0.9, label="Zero savings")
ax.set_xlabel("Age", fontsize=12)
ax.set_ylabel("Monthly Savings (USD)", fontsize=12)
ax.set_title("Age vs. Monthly Savings\n(with linear trend)", fontsize=14, fontweight="bold")
ax.legend(title="Country", fontsize=9, title_fontsize=10, loc="upper left")
add_source(fig)
plt.tight_layout()
plt.savefig("charts/02_age_vs_savings.png", dpi=150, bbox_inches="tight")
plt.close()
print("  -> charts/02_age_vs_savings.png saved")

# ── 3. HORIZONTAL BAR — Spending breakdown ────────────────────────────────────
print("Generating chart 3...")

gasto_cols = {
    "gasto_vivienda_usd":        "Housing",
    "gasto_alimentacion_usd":    "Food",
    "gasto_transporte_usd":      "Transport",
    "gasto_entretenimiento_usd": "Entertainment",
    "gasto_educacion_usd":       "Education",
    "gasto_salud_usd":           "Healthcare",
}

spending = {label: (df[col] / df["ingreso_mensual_usd"] * 100).mean()
            for col, label in gasto_cols.items()}
spending_s = pd.Series(spending).sort_values(ascending=True)  # ascending for h-bar (top = highest)

bar_colors = sns.color_palette("Blues_d", len(spending_s))

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(spending_s.index, spending_s.values, color=bar_colors, edgecolor="white")

for bar, val in zip(bars, spending_s.values):
    ax.text(val + 0.2, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%", va="center", fontsize=10, color="#212121")

ax.set_xlabel("Mean % of Monthly Income", fontsize=12)
ax.set_title("Spending Breakdown — Average % of Income\n(full sample, n=500)",
             fontsize=14, fontweight="bold")
ax.set_xlim(0, spending_s.max() + 4)
add_source(fig)
plt.tight_layout()
plt.savefig("charts/03_spending_breakdown.png", dpi=150, bbox_inches="tight")
plt.close()
print("  -> charts/03_spending_breakdown.png saved")

# ── 4. BAR CHART — Satisfaction by AI usage ──────────────────────────────────
print("Generating chart 4...")

ai_bins   = [-1, 3, 10, 100]
ai_labels = ["Low\n(0-3 hrs/week)", "Medium\n(4-10 hrs/week)", "High\n(11+ hrs/week)"]
df["ai_group"] = pd.cut(df["horas_herramientas_ia_semana"], bins=ai_bins, labels=ai_labels)

ai_stats = df.groupby("ai_group", observed=True)["satisfaccion_financiera"].mean()

bar_colors_ai = ["#EF9A9A", "#FFCC80", "#A5D6A7"]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(ai_stats.index, ai_stats.values, color=bar_colors_ai,
              edgecolor="white", width=0.5)

for bar, val in zip(bars, ai_stats.values):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.03,
            f"{val:.2f}", ha="center", va="bottom", fontsize=12, fontweight="bold")

ax.set_ylim(0, 5)
ax.set_ylabel("Average Financial Satisfaction (1-5)", fontsize=12)
ax.set_xlabel("AI Tool Usage Group", fontsize=12)
ax.set_title("Financial Satisfaction by AI Tool Usage",
             fontsize=14, fontweight="bold")
add_source(fig)
plt.tight_layout()
plt.savefig("charts/04_satisfaction_by_ai_usage.png", dpi=150, bbox_inches="tight")
plt.close()
print("  -> charts/04_satisfaction_by_ai_usage.png saved")

# ── 5. HORIZONTAL BAR — Housing burden with red-to-green gradient ─────────────
print("Generating chart 5...")

housing = {
    "Argentina": 34.09,
    "Chile":     32.55,
    "Mexico":    28.15,
    "Brasil":    26.90,
    "Colombia":  25.41,
    "Peru":      24.63,
}
housing_s = pd.Series(housing).sort_values(ascending=True)

cmap = mcolors.LinearSegmentedColormap.from_list("rg", ["#1a9850", "#fee08b", "#d73027"])
norm = mcolors.Normalize(vmin=housing_s.min(), vmax=housing_s.max())
bar_colors_h = [cmap(norm(v)) for v in housing_s.values]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(housing_s.index, housing_s.values, color=bar_colors_h, edgecolor="white")

for bar, val in zip(bars, housing_s.values):
    ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%", va="center", fontsize=11, color="#212121")

ax.set_xlabel("Average Housing Cost as % of Income", fontsize=12)
ax.set_title("Housing Burden by Country\n(average housing expense as % of income)",
             fontsize=14, fontweight="bold")
ax.set_xlim(0, housing_s.max() + 5)

sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation="vertical", fraction=0.03, pad=0.02)
cbar.set_label("Burden level", fontsize=9)

add_source(fig)
plt.tight_layout()
plt.savefig("charts/05_housing_burden_by_country.png", dpi=150, bbox_inches="tight")
plt.close()
print("  -> charts/05_housing_burden_by_country.png saved")

# ── 6. AREA CHART — Age vs Spending categories ───────────────────────────────
print("Generating chart 6...")

spend_cols = {
    "gasto_vivienda_usd":        "Housing",
    "gasto_alimentacion_usd":    "Food",
    "gasto_transporte_usd":      "Transport",
    "gasto_entretenimiento_usd": "Entertainment",
    "gasto_educacion_usd":       "Education",
    "gasto_salud_usd":           "Healthcare",
}

# Compute each category as % of income, then group by age and take the mean
for col, label in spend_cols.items():
    df[f"pct_{label}"] = df[col] / df["ingreso_mensual_usd"] * 100

pct_cols  = [f"pct_{label}" for label in spend_cols.values()]
age_spend = df.groupby("edad")[pct_cols].mean()
age_spend.columns = list(spend_cols.values())

area_colors = ["#E53935", "#FB8C00", "#8E24AA", "#1E88E5", "#43A047", "#00ACC1"]

fig, ax = plt.subplots(figsize=(12, 6))

for (category, color) in zip(age_spend.columns, area_colors):
    ax.plot(age_spend.index, age_spend[category], color=color, linewidth=1.8, label=category)
    ax.fill_between(age_spend.index, age_spend[category], alpha=0.12, color=color)

ax.set_xlabel("Age", fontsize=12)
ax.set_ylabel("Mean % of Monthly Income", fontsize=12)
ax.set_title("Spending Breakdown by Age\n(average % of income per category)",
             fontsize=14, fontweight="bold")
ax.legend(title="Category", fontsize=9, title_fontsize=10, loc="upper right")
ax.set_xlim(df["edad"].min(), df["edad"].max())
add_source(fig)
plt.tight_layout()
plt.savefig("charts/06_age_vs_spending.png", dpi=150, bbox_inches="tight")
plt.close()
print("  -> charts/06_age_vs_spending.png saved")

# ── 7. SCATTER PLOT — Age vs. Monthly Income ─────────────────────────────────
print("Generating chart 7...")

slope, intercept, r, p, _ = stats.linregress(df["edad"], df["ingreso_mensual_usd"])
x_line = np.linspace(df["edad"].min(), df["edad"].max(), 200)
y_line = slope * x_line + intercept

fig, ax = plt.subplots(figsize=(10, 6))

for country_key, color in COUNTRY_PALETTE.items():
    subset = df[df["pais_key"] == country_key]
    ax.scatter(subset["edad"], subset["ingreso_mensual_usd"],
               color=color, alpha=0.55, s=35, label=country_key, edgecolors="none")

ax.plot(x_line, y_line, color="#212121", linewidth=2, linestyle="--",
        label=f"Trend (r={r:.2f})")

ax.set_xlabel("Age", fontsize=12)
ax.set_ylabel("Monthly Income (USD)", fontsize=12)
ax.set_title("Age vs. Monthly Income\n(with linear trend)", fontsize=14, fontweight="bold")
ax.legend(title="Country", fontsize=9, title_fontsize=10, loc="upper left")
add_source(fig)
plt.tight_layout()
plt.savefig("charts/07_age_vs_income.png", dpi=150, bbox_inches="tight")
plt.close()
print("  -> charts/07_age_vs_income.png saved")

# ── 8. BOX PLOT — Industry vs. Monthly Income ─────────────────────────────────
print("Generating chart 8...")

industry_medians = df.groupby("industria")["ingreso_mensual_usd"].median().sort_values()
industry_order   = industry_medians.index.tolist()

data_by_industry = [df[df["industria"] == ind]["ingreso_mensual_usd"].values
                    for ind in industry_order]

industry_colors = sns.color_palette("coolwarm", len(industry_order))

fig, ax = plt.subplots(figsize=(11, 7))
bp = ax.boxplot(data_by_industry, orientation="horizontal", patch_artist=True,
                medianprops=dict(color="black", linewidth=2))

for i, (patch, ind, color) in enumerate(zip(bp["boxes"], industry_order, industry_colors), start=1):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)
    median_val = industry_medians[ind]
    y_offset = -0.34 if ind == "Marketing" else -0.38
    ax.text(median_val, i + y_offset, f"${median_val:,.0f}",
            va="top", ha="center", fontsize=8, fontweight="bold", color="#212121")

ax.set_yticklabels(industry_order, fontsize=10)
ax.set_xlabel("Monthly Income (USD)", fontsize=12)
ax.set_title("Income Distribution by Industry\n(sorted by median income)",
             fontsize=14, fontweight="bold")
outlier_handle = mlines.Line2D([], [], marker='o', linestyle='none',
                               markerfacecolor='none', markeredgecolor='#555555',
                               markersize=6)
ax.legend(handles=[outlier_handle],
          labels=["Circles = outliers\n(income > 1.5× IQR from box edges)"],
          loc='upper right', fontsize=8, framealpha=0.6,
          edgecolor='#aaaaaa', handlelength=1.5)
add_source(fig)
plt.tight_layout()
plt.savefig("charts/08_income_by_industry.png", dpi=150, bbox_inches="tight")
plt.close()
print("  -> charts/08_income_by_industry.png saved")

# ── 9. BOX PLOT + OVERLAY — Industry income with high AI users highlighted ──────
print("Generating chart 9...")

np.random.seed(42)

industry_medians9 = df.groupby("industria")["ingreso_mensual_usd"].median().sort_values()
industry_order9   = industry_medians9.index.tolist()
data_by_industry9 = [df[df["industria"] == ind]["ingreso_mensual_usd"].values
                     for ind in industry_order9]

high_ai      = df[df["horas_herramientas_ia_semana"] > 10]
high_ai_mean = high_ai["ingreso_mensual_usd"].mean()

industry_colors9 = sns.color_palette("coolwarm", len(industry_order9))

fig, ax = plt.subplots(figsize=(11, 7))
bp = ax.boxplot(data_by_industry9, orientation="horizontal", patch_artist=True,
                medianprops=dict(color="black", linewidth=2),
                flierprops=dict(marker='o', markerfacecolor='none',
                                markeredgecolor='#bbbbbb', markersize=5))

for i, (patch, color) in enumerate(zip(bp["boxes"], industry_colors9)):
    patch.set_facecolor(color)
    patch.set_alpha(0.4)

for i, ind in enumerate(industry_order9, start=1):
    pts = high_ai[high_ai["industria"] == ind]["ingreso_mensual_usd"].values
    jitter = np.random.uniform(-0.18, 0.18, size=len(pts))
    ax.scatter(pts, i + jitter, color="#FF6F00", alpha=0.85,
               s=45, zorder=5, edgecolors="none")

ax.axvline(high_ai_mean, color="#FF6F00", linewidth=1.8, linestyle="--", alpha=0.95)
ax.text(high_ai_mean + 18, 0.62,
        f"High AI users\nmean: ${high_ai_mean:,.0f}",
        color="#FF6F00", fontsize=8, fontweight="bold", va="bottom")

ax.set_yticklabels(industry_order9, fontsize=10)
ax.set_xlabel("Monthly Income (USD)", fontsize=12)
ax.set_title("Income by Industry — High AI Users Highlighted\n"
             "(orange dots = respondents using AI tools 11+ hrs/week)",
             fontsize=14, fontweight="bold")

box_handle     = mpatches.Patch(facecolor="#aaaaaa", alpha=0.4,
                                 label="All workers (box = middle 50%)")
dot_handle     = mlines.Line2D([], [], marker='o', linestyle='none',
                                color="#FF6F00", markersize=7,
                                label="High AI users (11+ hrs/week)")
outlier_handle = mlines.Line2D([], [], marker='o', linestyle='none',
                                markerfacecolor='none', markeredgecolor='#bbbbbb',
                                markersize=6,
                                label="Circles = outliers\n(income > 1.5× IQR from box edges)")
ax.legend(handles=[box_handle, dot_handle, outlier_handle],
          loc='upper right', fontsize=8, framealpha=0.6, edgecolor='#aaaaaa')

add_source(fig)
plt.tight_layout()
plt.savefig("charts/09_ai_users_within_industries.png", dpi=150, bbox_inches="tight")
plt.close()
print("  -> charts/09_ai_users_within_industries.png saved")

print("\nAll 9 charts saved to charts/")
