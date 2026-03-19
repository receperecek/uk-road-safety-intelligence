from pathlib import Path
import pandas as pd

gold = Path("data/processed/gold")
tables = Path("outputs/tables")
ref_path = next(Path("data/reference").glob("*.xlsx"))

mart = pd.read_parquet(gold / "mart_collision_risk_v1.parquet").copy()
codes = pd.read_excel(ref_path, sheet_name="2024_code_list")

target_fields = [
    "collision_severity",
    "road_type",
    "light_conditions",
    "weather_conditions",
    "road_surface_conditions",
    "urban_or_rural_area"
]

def build_map(field_name: str) -> dict:
    subset = codes[
        (codes["table"] == "collision") &
        (codes["field name"] == field_name)
    ][["code/format", "label"]].dropna(subset=["code/format", "label"]).copy()

    subset["code_num"] = pd.to_numeric(subset["code/format"], errors="coerce")
    subset = subset.dropna(subset=["code_num"]).copy()
    subset["code_num"] = subset["code_num"].astype(int)

    return dict(zip(subset["code_num"], subset["label"]))

summary_rows = []

for field in target_fields:
    if field in mart.columns:
        mapping = build_map(field)
        numeric_values = pd.to_numeric(mart[field], errors="coerce")
        mart[f"{field}_label"] = numeric_values.map(mapping)

        decoded_count = int(mart[f"{field}_label"].notna().sum())
        total_rows = len(mart)

        summary_rows.append({
            "field": field,
            "label_column": f"{field}_label",
            "decoded_rows": decoded_count,
            "total_rows": total_rows,
            "decoded_rate_pct": round(decoded_count / total_rows * 100, 2)
        })

summary = pd.DataFrame(summary_rows)

mart.to_parquet(gold / "mart_collision_risk_labeled_v1.parquet", index=False)
summary.to_csv(tables / "mart_collision_risk_label_decode_summary_v1.csv", index=False)

print("mart_collision_risk_labeled_v1_created")
print(summary.to_string(index=False))
