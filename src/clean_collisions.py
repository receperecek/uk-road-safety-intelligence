from pathlib import Path
import pandas as pd

raw_path = next(Path("data/raw/collisions").glob("*.csv"))
silver_dir = Path("data/processed/silver")
tables_dir = Path("outputs/tables")

silver_dir.mkdir(parents=True, exist_ok=True)
tables_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(raw_path, low_memory=False)
raw_rows = len(df)

exact_duplicate_rows = int(df.duplicated().sum())
if exact_duplicate_rows > 0:
    df = df.drop_duplicates().copy()

duplicate_collision_index_rows = int(df["collision_index"].duplicated().sum())

if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

if "time" in df.columns:
    df["time"] = df["time"].astype("string").str.strip()

profile = pd.DataFrame({
    "column": df.columns,
    "dtype": df.dtypes.astype(str).values,
    "null_count": df.isna().sum().values,
    "null_pct": (df.isna().mean() * 100).round(2).values
})

summary = pd.DataFrame([{
    "table": "collisions",
    "raw_rows": raw_rows,
    "exact_duplicate_rows_removed": exact_duplicate_rows,
    "rows_after_exact_dedup": len(df),
    "duplicate_collision_index_rows": duplicate_collision_index_rows,
    "unique_collision_index": df["collision_index"].nunique(),
    "column_count": df.shape[1]
}])

profile.to_csv(tables_dir / "collisions_column_profile.csv", index=False)
summary.to_csv(tables_dir / "collisions_quality_summary.csv", index=False)

if duplicate_collision_index_rows > 0:
    print("WARNING: duplicate collision_index detected. Clean file not exported.")
else:
    df.to_parquet(silver_dir / "collisions_clean.parquet", index=False)
    print("collisions_clean_created")
