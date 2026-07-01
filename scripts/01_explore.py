import pandas as pd

FILE_PATH = "data/latam_finanzas_2025.csv"

df = pd.read_csv(FILE_PATH)

# 1. Rows and columns
print("=" * 60)
print("SHAPE")
print("=" * 60)
print(f"Rows   : {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# 2. Column names and data types
print("\n" + "=" * 60)
print("COLUMNS AND DATA TYPES")
print("=" * 60)
for col in df.columns:
    print(f"  {col:<35} {df[col].dtype}")

# 3. Missing values sorted from most to least
print("\n" + "=" * 60)
print("MISSING VALUES (sorted)")
print("=" * 60)
missing = df.isnull().sum().sort_values(ascending=False)
for col, count in missing.items():
    print(f"  {col:<35} {count}")

# 4. Basic statistics for numeric columns
print("\n" + "=" * 60)
print("NUMERIC STATISTICS")
print("=" * 60)
numeric_cols = df.select_dtypes(include="number").columns
stats = df[numeric_cols].agg(["min", "max", "mean", "median", "std"]).T
stats.columns = ["Min", "Max", "Mean", "Median", "Std"]
print(stats.to_string())

# 5. Unique values and counts for categorical columns
categorical_cols = [
    "pais", "industria", "ocupacion", "meta_financiera",
    "tiene_tarjeta_credito", "tiene_cuenta_ahorro", "tiene_deuda"
]

print("\n" + "=" * 60)
print("CATEGORICAL COLUMNS — VALUE COUNTS")
print("=" * 60)
for col in categorical_cols:
    if col in df.columns:
        print(f"\n--- {col} ---")
        counts = df[col].value_counts(dropna=False)
        for val, count in counts.items():
            print(f"  {str(val):<35} {count}")
    else:
        print(f"\n--- {col} --- NOT FOUND IN DATASET")
