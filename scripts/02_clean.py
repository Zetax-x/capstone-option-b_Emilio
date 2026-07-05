import pandas as pd

INPUT  = "data/latam_finanzas_2025.csv"
OUTPUT = "data/latam_finanzas_clean.csv"

df = pd.read_csv(INPUT)
rows_before = len(df)
changes = []

# ── 1. INDUSTRIA — standardize inconsistent values ────────────────────────────
print("=" * 60)
print("1. INDUSTRIA — before")
print("=" * 60)
print(df["industria"].value_counts(dropna=False).to_string())

industria_map = {
    "Tecnologia":   "Tecnología",
    "tech":         "Tecnología",
    "TECNOLOGÍA":   "Tecnología",
}
df["industria"] = df["industria"].replace(industria_map)

print("\nAfter:")
print(df["industria"].value_counts(dropna=False).to_string())
changes.append("industria: merged 'Tecnologia', 'tech', 'TECNOLOGÍA' -> 'Tecnología'")

# ── 2. MISSING VALUES — fill all numeric nulls with column median ─────────────
print("\n" + "=" * 60)
print("2. MISSING VALUES")
print("=" * 60)
numeric_cols = df.select_dtypes(include="number").columns
missing_pct = (df[numeric_cols].isnull().sum() / len(df) * 100).sort_values(ascending=False)
for col, pct in missing_pct.items():
    if pct > 0:
        print(f"  {col:<35} {pct:.1f}% missing  -> fill with median")
    else:
        print(f"  {col:<35} 0.0% missing  -> no action")

for col in numeric_cols:
    n_missing = df[col].isnull().sum()
    if n_missing > 0:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        changes.append(f"{col}: filled {n_missing} nulls with median ({median_val:.2f})")

# ── 3. AHORRO_NEGATIVO flag ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print("3. AHORRO_MENSUAL_USD — negative values")
print("=" * 60)
n_negative = (df["ahorro_mensual_usd"] < 0).sum()
print(f"  Negative savings records: {n_negative}")
df["ahorro_negativo"] = df["ahorro_mensual_usd"].apply(
    lambda x: "ahorro negativo" if x < 0 else "Buen ahorro"
)
changes.append(f"ahorro_negativo: flagged {n_negative} rows as 'ahorro negativo', rest as 'Buen ahorro'")

# ── 4. PAIS — fix encoding issues ────────────────────────────────────────────
print("\n" + "=" * 60)
print("4. PAIS — before")
print("=" * 60)
print(df["pais"].value_counts(dropna=False).to_string())

valid_countries = ["México", "Brasil", "Argentina", "Perú", "Chile", "Colombia"]
pais_map = {}
for val in df["pais"].unique():
    for country in valid_countries:
        if val.encode("ascii", "ignore").lower() == country.encode("ascii", "ignore").lower():
            if val != country:
                pais_map[val] = country

df["pais"] = df["pais"].replace(pais_map)

print("\nAfter:")
print(df["pais"].value_counts(dropna=False).to_string())
if pais_map:
    for old, new in pais_map.items():
        changes.append(f"pais: '{old}' -> '{new}'")
else:
    changes.append("pais: no encoding issues found")

# ── 5-7. Si/No columns — normalize robustly by first letter ──────────────────
si_no_cols = ["tiene_tarjeta_credito", "tiene_cuenta_ahorro", "tiene_deuda"]

def normalize_si_no(val):
    if isinstance(val, str):
        if val.strip()[0].upper() == "S":
            return "Si"
        elif val.strip()[0].upper() == "N":
            return "No"
    return val

for col in si_no_cols:
    print("\n" + "=" * 60)
    print(f"{col.upper()} — before")
    print("=" * 60)
    print(df[col].value_counts(dropna=False).to_string())
    df[col] = df[col].apply(normalize_si_no)
    print("\nAfter:")
    print(df[col].value_counts(dropna=False).to_string())
    changes.append(f"{col}: normalized all values to 'Si' / 'No'")

# ── 8. OCUPACION — normalize encoding artifacts ───────────────────────────────
print("\n" + "=" * 60)
print("8. OCUPACION — before")
print("=" * 60)
print(df["ocupacion"].value_counts(dropna=False).to_string())

df["ocupacion"] = df["ocupacion"].replace(
    {"DiseÃ±ador GrÃ¡fico": "Diseñador Grafico"}
)
df["ocupacion"] = df["ocupacion"].apply(
    lambda x: "Diseñador Grafico"
    if isinstance(x, str) and x.encode("ascii", "ignore").decode() in ("Diseador Grfico", "Diseuador Grufico")
    else x
)

print("\nAfter:")
print(df["ocupacion"].value_counts(dropna=False).to_string())
changes.append("ocupacion: normalized encoding artifacts -> 'Diseñador Grafico'")

# ── 9. SAVE ───────────────────────────────────────────────────────────────────
df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

# ── 10. SUMMARY ──────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)
print(f"  Rows before : {rows_before}")
print(f"  Rows after  : {len(df)}")
print(f"  Columns after: {len(df.columns)} (added 'ahorro_negativo')")
print("\n  Changes applied:")
for i, change in enumerate(changes, 1):
    print(f"    {i}. {change}")
print(f"\n  Saved to: {OUTPUT}")
