import pandas as pd

df = pd.read_csv(r"C:\Users\sanma\OneDrive\Desktop\capstone-option-b\data\latam_finanzas_clean.csv")
chile = df[df["pais"] == "Chile"].copy()

n = len(chile)
age_min = chile["edad"].min()
age_max = chile["edad"].max()

inc = chile["ingreso_mensual_usd"]
inc_median = inc.median()
inc_mean = inc.mean()
inc_min = inc.min()
inc_max = inc.max()
inc_std = inc.std()

housing_burden = (chile["gasto_vivienda_usd"] / chile["ingreso_mensual_usd"] * 100).mean()

gasto_cols = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]
spending = {}
for col in gasto_cols:
    spending[col] = (chile[col] / chile["ingreso_mensual_usd"] * 100).mean()

mean_savings = chile["ahorro_mensual_usd"].mean()
pct_neg = (chile["ahorro_negativo"] == "ahorro negativo").mean() * 100

mean_ia = chile["horas_herramientas_ia_semana"].mean()
mean_sat = chile["satisfaccion_financiera"].mean()

print("## País: Chile")
print()
print(f"**Sample size:** {n}")
print(f"**Age range:** {age_min} – {age_max} years")
print()
print("### Income (ingreso_mensual_usd)")
print(f"| Metric | Value |")
print(f"|--------|-------|")
print(f"| Median | ${inc_median:,.2f} |")
print(f"| Mean   | ${inc_mean:,.2f} |")
print(f"| Min    | ${inc_min:,.2f} |")
print(f"| Max    | ${inc_max:,.2f} |")
print(f"| Std    | ${inc_std:,.2f} |")
print()
print("### Housing Burden")
print(f"**Mean housing burden:** {housing_burden:.2f}% of income")
print()
print("### Spending Breakdown (mean % of income)")
print(f"| Category | Mean % of Income |")
print(f"|----------|-----------------|")
for col, pct in spending.items():
    label = col.replace("gasto_", "").replace("_usd", "").replace("_", " ").title()
    print(f"| {label} | {pct:.2f}% |")
print()
print("### Savings")
print(f"**Mean monthly savings:** ${mean_savings:,.2f}")
print(f"**% with negative savings:** {pct_neg:.2f}%")
print()
print("### AI Tools & Financial Satisfaction")
print(f"**Mean hours/week using AI tools:** {mean_ia:.2f}")
print(f"**Mean financial satisfaction:** {mean_sat:.2f}")
