import pandas as pd

df = pd.read_csv("data/latam_finanzas_2025.csv")

print("=== SHAPE ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n=== COLUMNS & DTYPES ===")
print(df.dtypes.to_string())

print("\n=== MISSING VALUES (sorted) ===")
missing = df.isnull().sum().sort_values(ascending=False)
print(missing[missing > 0].to_string())

print("\n=== NUMERIC STATS ===")
print(df.describe().round(2).to_string())

print("\n=== CATEGORICAL UNIQUE VALUES ===")
cat_cols = ["pais", "industria", "ocupacion", "meta_financiera",
            "tiene_tarjeta_credito", "tiene_cuenta_ahorro", "tiene_deuda"]
for col in cat_cols:
    if col in df.columns:
        print(f"\n-- {col} --")
        print(df[col].value_counts().to_string())
