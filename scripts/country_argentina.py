import pandas as pd

df = pd.read_csv(r"C:\Users\sanma\OneDrive\Desktop\capstone-option-b\data\latam_finanzas_clean.csv")
arg = df[df["pais"] == "Argentina"].copy()

n = len(arg)
age_min = arg["edad"].min()
age_max = arg["edad"].max()

inc = arg["ingreso_mensual_usd"]
inc_median = inc.median()
inc_mean = inc.mean()
inc_min = inc.min()
inc_max = inc.max()
inc_std = inc.std()

housing_burden = (arg["gasto_vivienda_usd"] / arg["ingreso_mensual_usd"] * 100).mean()

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
    spending[col] = (arg[col] / arg["ingreso_mensual_usd"] * 100).mean()

mean_savings = arg["ahorro_mensual_usd"].mean()
pct_neg = (arg["ahorro_negativo"] == "ahorro negativo").mean() * 100

mean_ia = arg["horas_herramientas_ia_semana"].mean()
mean_sat = arg["satisfaccion_financiera"].mean()

print("## País: Argentina")
print()
print(f"**Sample size:** {n}  ")
print(f"**Age range:** {age_min} – {age_max} years")
print()
print("### Income (ingreso_mensual_usd)")
print(f"| Statistic | Value |")
print(f"|-----------|-------|")
print(f"| Median | ${inc_median:,.2f} |")
print(f"| Mean | ${inc_mean:,.2f} |")
print(f"| Min | ${inc_min:,.2f} |")
print(f"| Max | ${inc_max:,.2f} |")
print(f"| Std Dev | ${inc_std:,.2f} |")
print()
print("### Housing Burden")
print(f"**Mean housing cost as % of income:** {housing_burden:.2f}%")
print()
print("### Spending Breakdown (mean % of income)")
print(f"| Category | Mean % of Income |")
print(f"|----------|-----------------|")
for col, val in spending.items():
    label = col.replace("gasto_", "").replace("_usd", "").replace("_", " ").title()
    print(f"| {label} | {val:.2f}% |")
print()
print("### Savings")
print(f"**Mean monthly savings (ahorro_mensual_usd):** ${mean_savings:,.2f}  ")
print(f"**% with negative savings:** {pct_neg:.2f}%")
print()
print("### AI Tools & Financial Satisfaction")
print(f"**Mean hours/week using AI tools:** {mean_ia:.2f}  ")
print(f"**Mean financial satisfaction score:** {mean_sat:.2f}")
