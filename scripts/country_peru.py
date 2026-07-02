import pandas as pd

df = pd.read_csv(r"C:\Users\sanma\OneDrive\Desktop\capstone-option-b\data\latam_finanzas_clean.csv")
peru = df[df["pais"] == "Perú"].copy()

n = len(peru)
age_min = peru["edad"].min()
age_max = peru["edad"].max()

inc = peru["ingreso_mensual_usd"]
inc_median = inc.median()
inc_mean = inc.mean()
inc_min = inc.min()
inc_max = inc.max()
inc_std = inc.std()

housing_burden = (peru["gasto_vivienda_usd"] / peru["ingreso_mensual_usd"] * 100).mean()

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
    spending[col] = (peru[col] / peru["ingreso_mensual_usd"] * 100).mean()

mean_savings = peru["ahorro_mensual_usd"].mean()
pct_neg = (peru["ahorro_negativo"] == "ahorro negativo").mean() * 100

mean_ia = peru["horas_herramientas_ia_semana"].mean()
mean_sat = peru["satisfaccion_financiera"].mean()

print("## País: Perú")
print()
print("### 1. Sample & Age")
print(f"- Sample size: {n}")
print(f"- Age range: {age_min} – {age_max}")
print()
print("### 2. Income (ingreso_mensual_usd)")
print(f"- Median: {inc_median:.2f}")
print(f"- Mean:   {inc_mean:.2f}")
print(f"- Min:    {inc_min:.2f}")
print(f"- Max:    {inc_max:.2f}")
print(f"- Std:    {inc_std:.2f}")
print()
print("### 3. Housing Burden")
print(f"- Mean housing burden: {housing_burden:.2f}%")
print()
print("### 4. Spending Breakdown (mean % of income)")
for col, val in spending.items():
    print(f"- {col}: {val:.2f}%")
print()
print("### 5. Savings")
print(f"- Mean ahorro_mensual_usd: {mean_savings:.2f}")
print(f"- % with ahorro negativo: {pct_neg:.2f}%")
print()
print("### 6. AI Tools & Financial Satisfaction")
print(f"- Mean horas_herramientas_ia_semana: {mean_ia:.2f}")
print(f"- Mean satisfaccion_financiera: {mean_sat:.2f}")
