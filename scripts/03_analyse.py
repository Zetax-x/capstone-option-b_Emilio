import pandas as pd
from scipy import stats

df = pd.read_csv("data/latam_finanzas_clean.csv")

SEP = "=" * 65

# ── 1. INCOME BY COUNTRY (from country profiles) ─────────────────────────────
print(SEP)
print("1. INCOME BY COUNTRY (USD) — sorted by median (desc)")
print(SEP)

income_data = {
    "Brasil":    {"Median": 1458.03, "Mean": 1387.97, "Min": 300.00,  "Max": 2874.49, "Std": 592.18},
    "Chile":     {"Median": 1246.01, "Mean": 1245.29, "Min": 575.20,  "Max": 1861.10, "Std": 289.66},
    "Mexico":    {"Median": 1066.99, "Mean": 1042.05, "Min": 300.00,  "Max": 1693.16, "Std": 286.61},
    "Colombia":  {"Median":  856.62, "Mean":  848.78, "Min": 405.15,  "Max": 1362.79, "Std": 188.70},
    "Peru":      {"Median":  821.59, "Mean":  817.76, "Min": 361.89,  "Max": 1341.50, "Std": 207.91},
    "Argentina": {"Median":  798.49, "Mean":  766.38, "Min": 372.85,  "Max": 1342.56, "Std": 203.94},
}

income_df = pd.DataFrame(income_data).T.sort_values("Median", ascending=False)
income_df.index.name = "Country"
print(income_df.to_string(
    float_format=lambda x: f"${x:,.2f}"
))

# ── 2. AGE VS. SAVINGS ────────────────────────────────────────────────────────
print("\n" + SEP)
print("2. AGE VS. SAVINGS")
print(SEP)

bins   = [17, 22, 25, 28, 32]
labels = ["18-22", "23-25", "26-28", "29-32"]
df["age_group"] = pd.cut(df["edad"], bins=bins, labels=labels)
df["savings_rate"] = df["ahorro_mensual_usd"] / df["ingreso_mensual_usd"] * 100

age_stats = df.groupby("age_group", observed=True).agg(
    Respondents       = ("id", "count"),
    Avg_Savings_USD   = ("ahorro_mensual_usd", "mean"),
    Avg_Savings_Rate  = ("savings_rate", "mean"),
).rename(columns={
    "Avg_Savings_USD":  "Avg Savings (USD)",
    "Avg_Savings_Rate": "Avg Savings Rate (%)",
})
print(age_stats.to_string(
    float_format=lambda x: f"{x:.2f}"
))

# ── 3. SPENDING BREAKDOWN (full sample) ───────────────────────────────────────
print("\n" + SEP)
print("3. SPENDING BREAKDOWN — full sample (mean % of income)")
print(SEP)

gasto_cols = {
    "gasto_vivienda_usd":       "Housing",
    "gasto_alimentacion_usd":   "Food",
    "gasto_transporte_usd":     "Transport",
    "gasto_entretenimiento_usd":"Entertainment",
    "gasto_educacion_usd":      "Education",
    "gasto_salud_usd":          "Healthcare",
}

spending = {}
for col, label in gasto_cols.items():
    spending[label] = (df[col] / df["ingreso_mensual_usd"] * 100).mean()

spending_df = (
    pd.DataFrame.from_dict(spending, orient="index", columns=["Mean % of Income"])
    .sort_values("Mean % of Income", ascending=False)
)
spending_df.index.name = "Category"
print(spending_df.to_string(float_format=lambda x: f"{x:.2f}%"))

# ── 4. CREDIT CARD HOLDERS VS NON-HOLDERS ────────────────────────────────────
print("\n" + SEP)
print("4. CREDIT CARD HOLDERS vs NON-HOLDERS")
print(SEP)

cc_metrics = ["ingreso_mensual_usd", "gasto_alimentacion_usd",
              "gasto_entretenimiento_usd", "ahorro_mensual_usd"]
cc_labels  = ["Avg Income (USD)", "Avg Food Spending (USD)",
              "Avg Entertainment (USD)", "Avg Savings (USD)"]

cc = df.groupby("tiene_tarjeta_credito")[cc_metrics].mean()
cc.columns = cc_labels
cc.index.name = "Credit Card"

pct_diff = ((cc.loc["Si"] - cc.loc["No"]) / cc.loc["No"] * 100).rename("% Difference")

cc_full = cc.T.copy()
cc_full["% Difference"] = pct_diff.values
print(cc_full.to_string(float_format=lambda x: f"{x:.2f}"))

# ── 5. AI TOOL USAGE VS FINANCIAL SATISFACTION ───────────────────────────────
print("\n" + SEP)
print("5. AI TOOL USAGE vs FINANCIAL SATISFACTION")
print(SEP)

ai_bins   = [-1, 3, 10, 100]
ai_labels = ["Low (0-3 hrs)", "Medium (4-10 hrs)", "High (11+ hrs)"]
df["ai_group"] = pd.cut(df["horas_herramientas_ia_semana"], bins=ai_bins, labels=ai_labels)

ai_stats = df.groupby("ai_group", observed=True).agg(
    Respondents       = ("id", "count"),
    Avg_Satisfaction  = ("satisfaccion_financiera", "mean"),
    Avg_Income_USD    = ("ingreso_mensual_usd", "mean"),
).rename(columns={
    "Avg_Satisfaction": "Avg Satisfaction (1-5)",
    "Avg_Income_USD":   "Avg Income (USD)",
})
print(ai_stats.to_string(float_format=lambda x: f"{x:.2f}"))

pearson_r, p_value = stats.pearsonr(
    df["horas_herramientas_ia_semana"],
    df["satisfaccion_financiera"]
)
print(f"\nPearson correlation (AI hours vs satisfaction): r = {pearson_r:.4f}, p = {p_value:.4f}")
if p_value < 0.05:
    print("-> Statistically significant (p < 0.05)")
else:
    print("-> Not statistically significant (p >= 0.05)")

# ── 6. HOUSING BURDEN BY COUNTRY (from country profiles) ─────────────────────
print("\n" + SEP)
print("6. HOUSING BURDEN BY COUNTRY — sorted highest to lowest")
print(SEP)

housing_data = {
    "Argentina": 34.09,
    "Chile":     32.55,
    "Mexico":    28.15,
    "Brasil":    26.90,
    "Colombia":  25.41,
    "Peru":      24.63,
}

housing_df = (
    pd.DataFrame.from_dict(housing_data, orient="index", columns=["Avg Housing % of Income"])
    .sort_values("Avg Housing % of Income", ascending=False)
)
housing_df.index.name = "Country"
print(housing_df.to_string(float_format=lambda x: f"{x:.2f}%"))
