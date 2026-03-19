from pathlib import Path
import pandas as pd

silver = Path("data/processed/silver")
gold = Path("data/processed/gold")
tables = Path("outputs/tables")

gold.mkdir(parents=True, exist_ok=True)
tables.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet(silver / "collisions_clean.parquet").copy()

candidate_cols = [
    "collision_index",
    "collision_year",
    "date",
    "time",
    "collision_severity",
    "number_of_vehicles",
    "number_of_casualties",
    "speed_limit",
    "road_type",
    "junction_detail",
    "junction_control",
    "light_conditions",
    "weather_conditions",
    "road_surface_conditions",
    "urban_or_rural_area",
    "local_authority_district",
    "local_authority_ons_district",
    "police_force",
    "latitude",
    "longitude"
]

existing_cols = [c for c in candidate_cols if c in df.columns]
mart = df[existing_cols].copy()

if "date" in mart.columns:
    mart["date"] = pd.to_datetime(mart["date"], errors="coerce")
    mart["month"] = mart["date"].dt.month
    mart["month_name"] = mart["date"].dt.month_name()
    mart["quarter"] = mart["date"].dt.quarter
    mart["day_name"] = mart["date"].dt.day_name()
    mart["is_weekend"] = mart["date"].dt.dayofweek.isin([5, 6])

if "time" in mart.columns:
    time_as_str = mart["time"].astype("string").str.strip()
    mart["hour"] = pd.to_numeric(time_as_str.str.slice(0, 2), errors="coerce")

if "collision_severity" in mart.columns:
    sev = pd.to_numeric(mart["collision_severity"], errors="coerce")
    mart["is_fatal_raw"] = sev.eq(1)
    mart["is_serious_raw"] = sev.eq(2)
    mart["is_slight_raw"] = sev.eq(3)
    mart["is_killed_or_seriously_injured_raw"] = sev.isin([1, 2])

summary = pd.DataFrame([{
    "mart_name": "mart_collision_risk_v1",
    "row_count": len(mart),
    "column_count": mart.shape[1],
    "unique_collision_index": mart["collision_index"].nunique() if "collision_index" in mart.columns else None
}])

mart.to_parquet(gold / "mart_collision_risk_v1.parquet", index=False)
summary.to_csv(tables / "mart_collision_risk_v1_summary.csv", index=False)

print("mart_collision_risk_v1_created")
print(summary.to_string(index=False))
