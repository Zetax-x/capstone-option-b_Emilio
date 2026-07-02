import pandas as pd

df = pd.read_csv(r"C:\Users\sanma\OneDrive\Desktop\capstone-option-b\data\latam_finanzas_clean.csv")
col = df[df["pais"] == "Colombia"].copy()

n = len(col)
age_min = col["edad"].min()
age_max = col["edad"].max()

inc = col["ingreso_mensual_usd"]
inc_median = inc.median()
inc_mean = inc.mean()
inc_min = inc.min()
inc_max = inc.max()
inc_std = inc.std()

housing_burden = (col["gasto_vivienda_usd"] / col["ingreso_mensual_usd"] * 100).mean()

gasto_cols = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]
spending = {g: (col[g] / col["ingreso_mensual_usd"] * 100).mean() for g in gasto_cols}

mean_savings = col["ahorro_mensual_usd"].mean()
pct_neg = (col["ahorro_negativo"] == "ahorro negativo").mean() * 100

mean_ia = col["horas_herramientas_ia_semana"].mean()
mean_sat = col["satisfaccion_financiera"].mean()

print("## País: Colombia")
print()
print(f"**Sample size:** {n}")
print(f"**Age range:** {age_min} – {age_max} years")
print()
print("### Income (ingreso_mensual_usd)")
print(f"| Stat | Value |")
print(f"|------|-------|")
print(f"| Median | ${inc_median:,.2f} |")
print(f"| Mean | ${inc_mean:,.2f} |")
print(f"| Min | ${inc_min:,.2f} |")
print(f"| Max | ${inc_max:,.2f} |")
print(f"| Std Dev | ${inc_std:,.2f} |")
print()
print("### Housing Burden")
print(f"Mean housing cost as % of income: **{housing_burden:.2f}%**")
print()
print("### Spending Breakdown (mean % of income)")
print(f"| Category | Mean % of Income |")
print(f"|----------|-----------------|")
for g, pct in spending.items():
    label = g.replace("gasto_", "").replace("_usd", "").replace("_", " ").title()
    print(f"| {label} | {pct:.2f}% |")
print()
print("### Savings")
print(f"- Mean monthly savings: **${mean_savings:,.2f}**")
print(f"- Respondents with negative savings: **{pct_neg:.2f}%**")
print()
print("### AI Tools & Financial Satisfaction")
print(f"- Mean hours/week using AI tools: **{mean_ia:.2f}**")
print(f"- Mean financial satisfaction (1–5): **{mean_sat:.2f}**")
