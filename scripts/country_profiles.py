import pandas as pd

df = pd.read_csv("data/latam_finanzas_clean.csv")

paises = ["México", "Colombia", "Argentina", "Chile", "Perú", "Brasil"]
gasto_cols = ["gasto_vivienda_usd", "gasto_alimentacion_usd", "gasto_transporte_usd",
              "gasto_entretenimiento_usd", "gasto_educacion_usd", "gasto_salud_usd"]

output = "# Country Profiles — Análisis LatAm 2025\n\n"

for pais in paises:
    sub = df[df["pais"] == pais]
    if len(sub) == 0:
        # Try without accent
        sub = df[df["pais"].str.contains(pais[:4], case=False, na=False)]

    n = len(sub)
    age_min, age_max = sub["edad"].min(), sub["edad"].max()
    inc = sub["ingreso_mensual_usd"]
    housing_burden = (sub["gasto_vivienda_usd"] / sub["ingreso_mensual_usd"] * 100).mean()
    avg_ahorro = sub["ahorro_mensual_usd"].mean()
    pct_neg = ((sub["ahorro_negativo"] == "ahorro negativo").sum() / n * 100)
    avg_ia = sub["horas_herramientas_ia_semana"].mean()
    avg_sat = sub["satisfaccion_financiera"].mean()

    output += f"## País: {pais}\n\n"
    output += f"**Muestra:** {n} respondentes | **Rango de edad:** {age_min}–{age_max} años\n\n"
    output += f"**Ingreso mensual (USD):**\n"
    output += f"- Mediana: ${inc.median():.0f} | Media: ${inc.mean():.0f} | Min: ${inc.min():.0f} | Max: ${inc.max():.0f} | Std: ${inc.std():.0f}\n\n"
    output += f"**Carga vivienda:** {housing_burden:.1f}% del ingreso\n\n"
    output += f"**Desglose de gastos (% del ingreso promedio):**\n"
    for col in gasto_cols:
        pct = (sub[col] / sub["ingreso_mensual_usd"] * 100).mean()
        output += f"- {col.replace('gasto_','').replace('_usd','')}: {pct:.1f}%\n"
    output += f"\n**Ahorros:** ${avg_ahorro:.0f}/mes promedio | {pct_neg:.1f}% con ahorro negativo\n\n"
    output += f"**Herramientas IA:** {avg_ia:.1f} hrs/semana | Satisfacción financiera: {avg_sat:.2f}/5\n\n"
    output += "---\n\n"

with open("scripts/country_profiles.md", "w", encoding="utf-8") as f:
    f.write(output)

print(output)
print("Guardado en scripts/country_profiles.md")
