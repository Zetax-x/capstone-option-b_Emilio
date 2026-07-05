import pandas as pd
from scipy import stats

# =============================================================================
# CLAUDE CODE INSTRUCTION — AUTO-EXPANSION (read before running this script)
# =============================================================================
#
# STEP A — MAP THE VARIABLE SPACE
# After running the 6 mandatory analyses, read all columns from
# data/latam_finanzas_clean.csv and build two lists:
#
#   explored_groupers : variables used to split the sample into groups
#                       (e.g. pais, age_group, tiene_tarjeta_credito)
#   explored_outcomes : variables measured as results
#                       (e.g. ingreso_mensual_usd, ahorro_mensual_usd,
#                        satisfaccion_financiera, gasto_* cols)
#
# STEP B — IDENTIFY GAPS
# For every column in the dataset that is NOT in explored_groupers or
# explored_outcomes, ask: "Would using this variable as a grouper or
# outcome produce a finding that is meaningful and not redundant with
# what already exists?"
#
# Also check partial gaps: variables that appear in findings but only
# on one side — e.g. tiene_tarjeta_credito used as grouper but the
# individual gasto_* columns never broken down by it.
#
# Discard: id, nombre, and variables that are direct derivations of
# already-explored ones (e.g. ahorro_negativo derives from ahorro_mensual_usd).
#
# STEP C — RUN THE GAPS
# For each meaningful gap identified in Step B:
#   1. Run the analysis using data/latam_finanzas_clean.csv
#   2. Print the result in the same table format as mandatory findings
#   3. Generate a chart in charts/ (auto-number based on existing PNGs)
#   4. Add a one-paragraph interpretation: the fact, why it matters for
#      Futuro Digital LatAm, and one concrete recommendation
#   5. Label it "FINDING [N] — Supplementary: [title]"
#
# Stop when no new meaningful gaps remain.
# =============================================================================

df = pd.read_csv("data/latam_finanzas_clean.csv")

print("=" * 60)
print("FINDING 1: INCOME COMPARISON BY COUNTRY")
print("=" * 60)
income_by_country = df.groupby("pais")["ingreso_mensual_usd"].agg(
    mediana="median", media="mean", min="min", max="max", std="std"
).sort_values("mediana", ascending=False).round(0)
print(income_by_country.to_string())

print("\n" + "=" * 60)
print("FINDING 2: AGE VS SAVINGS RATE")
print("=" * 60)
bins = [17, 22, 25, 28, 32]
labels = ["18-22", "23-25", "26-28", "29-32"]
df["age_group"] = pd.cut(df["edad"], bins=bins, labels=labels)
age_savings = df.groupby("age_group", observed=True).agg(
    avg_ahorro=("ahorro_mensual_usd", "mean"),
    avg_income=("ingreso_mensual_usd", "mean"),
    count=("ahorro_mensual_usd", "count")
)
age_savings["savings_rate_pct"] = (age_savings["avg_ahorro"] / age_savings["avg_income"] * 100).round(1)
age_savings = age_savings.round(0)
print(age_savings.to_string())

print("\n" + "=" * 60)
print("FINDING 3: SPENDING BREAKDOWN (% OF INCOME)")
print("=" * 60)
gasto_cols = ["gasto_vivienda_usd", "gasto_alimentacion_usd", "gasto_transporte_usd",
              "gasto_entretenimiento_usd", "gasto_educacion_usd", "gasto_salud_usd"]
for col in gasto_cols:
    pct = (df[col] / df["ingreso_mensual_usd"] * 100).mean()
    print(f"  {col.replace('gasto_','').replace('_usd',''):20s}: {pct:.1f}%")

print("\n" + "=" * 60)
print("FINDING 4: CREDIT CARD HOLDERS VS NON-HOLDERS")
print("=" * 60)
cc = df.groupby("tiene_tarjeta_credito")[
    ["ingreso_mensual_usd", "gasto_alimentacion_usd", "gasto_entretenimiento_usd", "ahorro_mensual_usd"]
].mean().round(2)
print(cc.to_string())
holders = df[df["tiene_tarjeta_credito"] == "Sí"]
non_holders = df[df["tiene_tarjeta_credito"] == "No"]
print(f"\nDiferencia % en alimentación: {((holders['gasto_alimentacion_usd'].mean() / non_holders['gasto_alimentacion_usd'].mean()) - 1)*100:.1f}%")
print(f"Diferencia % en entretenimiento: {((holders['gasto_entretenimiento_usd'].mean() / non_holders['gasto_entretenimiento_usd'].mean()) - 1)*100:.1f}%")
print(f"Diferencia % en ahorro: {((holders['ahorro_mensual_usd'].mean() / non_holders['ahorro_mensual_usd'].mean()) - 1)*100:.1f}%")
print(f"Diferencia % en ingreso: {((holders['ingreso_mensual_usd'].mean() / non_holders['ingreso_mensual_usd'].mean()) - 1)*100:.1f}%")

print("\n" + "=" * 60)
print("FINDING 5: AI TOOL USAGE VS FINANCIAL SATISFACTION")
print("=" * 60)
df["ia_group"] = pd.cut(df["horas_herramientas_ia_semana"],
                         bins=[-1, 3, 10, 100],
                         labels=["Low (0-3h)", "Medium (4-10h)", "High (11+h)"])
ia_sat = df.groupby("ia_group", observed=True).agg(
    count=("satisfaccion_financiera", "count"),
    avg_satisfaction=("satisfaccion_financiera", "mean"),
    avg_income=("ingreso_mensual_usd", "mean")
).round(2)
print(ia_sat.to_string())
r, p = stats.pearsonr(df["horas_herramientas_ia_semana"], df["satisfaccion_financiera"])
print(f"\nPearson r = {r:.3f}, p = {p:.4f}")

print("\n" + "=" * 60)
print("FINDING 6: HOUSING BURDEN BY COUNTRY")
print("=" * 60)
df["housing_burden_pct"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100
burden = df.groupby("pais")["housing_burden_pct"].mean().sort_values(ascending=False).round(1)
print(burden.to_string())

# --- AUTO-EXPANSION ---
# Finding 2 asserts "age doesn't explain the savings gap because incomes are similar
# across age groups." This needs statistical validation before it can be stated as fact.
print("\n" + "=" * 60)
print("FINDING 7 — Supplementary: AGE DOES NOT PREDICT INCOME")
print("=" * 60)
r_age_inc, p_age_inc = stats.pearsonr(df["edad"], df["ingreso_mensual_usd"])
print(f"Pearson r (edad vs ingreso_mensual_usd) = {r_age_inc:.3f}, p = {p_age_inc:.4f}")
print("Interpretation: " + ("No significant relationship." if p_age_inc > 0.05 else "Significant relationship found."))
age_income = df.groupby("age_group", observed=True)["ingreso_mensual_usd"].agg(
    media="mean", mediana="median", std="std"
).round(0)
print(age_income.to_string())

# Finding 3 shows a global spending breakdown. Does the proportion stay stable
# across age groups, or do younger people allocate income differently?
print("\n" + "=" * 60)
print("FINDING 8 — Supplementary: SPENDING PROPORTIONS BY AGE GROUP")
print("=" * 60)
gasto_cols = ["gasto_vivienda_usd", "gasto_alimentacion_usd", "gasto_transporte_usd",
              "gasto_entretenimiento_usd", "gasto_educacion_usd", "gasto_salud_usd"]
for col in gasto_cols:
    df[col + "_pct"] = df[col] / df["ingreso_mensual_usd"] * 100
pct_cols = [c + "_pct" for c in gasto_cols]
spending_by_age = df.groupby("age_group", observed=True)[pct_cols].mean().round(1)
spending_by_age.columns = [c.replace("gasto_","").replace("_usd_pct","") for c in pct_cols]
print(spending_by_age.to_string())

# Finding 5 shows AI usage correlates with satisfaction. Does this hold within
# every industry, or is it driven by one sector?
print("\n" + "=" * 60)
print("FINDING 9 — Supplementary: INCOME BY INDUSTRY")
print("=" * 60)
industry_income = df.groupby("industria")["ingreso_mensual_usd"].agg(
    mediana="median", media="mean", min="min", max="max", std="std"
).sort_values("mediana", ascending=False).round(0)
print(industry_income.to_string())

# Finding 9 shows wide within-industry income variance. Are high AI users
# concentrated at the top of each industry's income distribution?
print("\n" + "=" * 60)
print("FINDING 10 — Supplementary: HIGH AI USERS WITHIN INDUSTRY INCOME DISTRIBUTION")
print("=" * 60)
df["high_ia"] = df["horas_herramientas_ia_semana"] >= 11
high_ia_by_industry = df[df["high_ia"]].groupby("industria")["ingreso_mensual_usd"].agg(
    count="count", media="mean", mediana="median"
).round(0)
all_by_industry = df.groupby("industria")["ingreso_mensual_usd"].median().round(0)
comparison = high_ia_by_industry.copy()
comparison["mediana_industria"] = all_by_industry
comparison["pct_encima_mediana"] = (
    (comparison["media"] / comparison["mediana_industria"] - 1) * 100
).round(1)
print(comparison.to_string())
r_ia_inc, p_ia_inc = stats.pearsonr(df["horas_herramientas_ia_semana"], df["ingreso_mensual_usd"])
print(f"\nPearson r (horas_ia vs ingreso) = {r_ia_inc:.3f}, p = {p_ia_inc:.4f}")

# --- GAP ANALYSIS RESULTS ---
# Unexplored variables found: tiene_cuenta_ahorro, tiene_deuda, deuda_total_usd,
# meta_financiera, ocupacion
# Partial gap: tiene_tarjeta_credito used as grouper but gasto_* cols never
# broken down individually by it.

print("\n" + "=" * 60)
print("FINDING 11 — Supplementary: SAVINGS ACCOUNT HOLDERS VS NON-HOLDERS")
print("=" * 60)
sa = df.groupby("tiene_cuenta_ahorro")[
    ["ingreso_mensual_usd", "ahorro_mensual_usd", "satisfaccion_financiera"]
].mean().round(2)
print(sa.to_string())
holders_sa = df[df["tiene_cuenta_ahorro"] == "Sí"]
non_holders_sa = df[df["tiene_cuenta_ahorro"] == "No"]
print(f"\nDiferencia % en ahorro: {((holders_sa['ahorro_mensual_usd'].mean() / non_holders_sa['ahorro_mensual_usd'].mean()) - 1)*100:.1f}%")
print(f"Diferencia % en ingreso: {((holders_sa['ingreso_mensual_usd'].mean() / non_holders_sa['ingreso_mensual_usd'].mean()) - 1)*100:.1f}%")
print(f"Diferencia % en satisfaccion: {((holders_sa['satisfaccion_financiera'].mean() / non_holders_sa['satisfaccion_financiera'].mean()) - 1)*100:.1f}%")
r_sa, p_sa = stats.pearsonr(
    (df["tiene_cuenta_ahorro"] == "Sí").astype(int), df["ahorro_mensual_usd"]
)
print(f"Pearson r (cuenta_ahorro vs ahorro_mensual) = {r_sa:.3f}, p = {p_sa:.4f}")

print("\n" + "=" * 60)
print("FINDING 12 — Supplementary: DEBT HOLDERS — SAVINGS AND SATISFACTION")
print("=" * 60)
debt = df.groupby("tiene_deuda")[
    ["ingreso_mensual_usd", "ahorro_mensual_usd", "satisfaccion_financiera", "deuda_total_usd"]
].mean().round(2)
print(debt.to_string())
has_debt = df[df["tiene_deuda"] == "Sí"]
no_debt = df[df["tiene_deuda"] == "No"]
print(f"\nDiferencia % en ahorro: {((has_debt['ahorro_mensual_usd'].mean() / no_debt['ahorro_mensual_usd'].mean()) - 1)*100:.1f}%")
print(f"Diferencia % en satisfaccion: {((has_debt['satisfaccion_financiera'].mean() / no_debt['satisfaccion_financiera'].mean()) - 1)*100:.1f}%")
r_debt, p_debt = stats.pearsonr(
    (df["tiene_deuda"] == "Sí").astype(int), df["ahorro_mensual_usd"]
)
print(f"Pearson r (tiene_deuda vs ahorro_mensual) = {r_debt:.3f}, p = {p_debt:.4f}")

print("\n" + "=" * 60)
print("FINDING 13 — Supplementary: FINANCIAL GOAL VS ACTUAL SAVINGS BEHAVIOUR")
print("=" * 60)
goal_savings = df.groupby("meta_financiera")[
    ["ahorro_mensual_usd", "ingreso_mensual_usd", "satisfaccion_financiera"]
].agg(
    avg_ahorro=("ahorro_mensual_usd", "mean"),
    avg_income=("ingreso_mensual_usd", "mean"),
    avg_sat=("satisfaccion_financiera", "mean"),
    count=("ahorro_mensual_usd", "count")
).round(2)
goal_savings["savings_rate_pct"] = (goal_savings["avg_ahorro"] / goal_savings["avg_income"] * 100).round(1)
goal_savings = goal_savings.sort_values("avg_ahorro", ascending=False)
print(goal_savings.to_string())

print("\n" + "=" * 60)
print("FINDING 14 — Supplementary: CREDIT CARD HOLDERS — SPENDING BY CATEGORY")
print("=" * 60)
gasto_cols = ["gasto_vivienda_usd", "gasto_alimentacion_usd", "gasto_transporte_usd",
              "gasto_entretenimiento_usd", "gasto_educacion_usd", "gasto_salud_usd"]
cc_breakdown = df.groupby("tiene_tarjeta_credito")[gasto_cols].mean().round(2)
print(cc_breakdown.to_string())
print("\nDiferencia % por categoria (tarjeta vs sin tarjeta):")
holders_cc = df[df["tiene_tarjeta_credito"] == "Sí"]
non_holders_cc = df[df["tiene_tarjeta_credito"] == "No"]
for col in gasto_cols:
    diff = ((holders_cc[col].mean() / non_holders_cc[col].mean()) - 1) * 100
    label = col.replace("gasto_","").replace("_usd","")
    print(f"  {label:20s}: {diff:+.1f}%")
