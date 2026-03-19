from pathlib import Path
import pandas as pd

gold = Path("data/processed/gold")
tables = Path("outputs/tables")

df = pd.read_parquet(gold / "mart_collision_risk_v1.parquet")

def safe_sum(col):
    return int(df[col].fillna(False).astype(bool).sum()) if col in df.columns else None

summary = pd.DataFrame([{
    "total_collisions": len(df),
    "total_casualties": int(df["number_of_casualties"].fillna(0).sum()) if "number_of_casualties" in df.columns else None,
    "total_vehicles": int(df["number_of_vehicles"].fillna(0).sum()) if "number_of_vehicles" in df.columns else None,
    "fatal_collisions_raw": safe_sum("is_fatal_raw"),
    "serious_collisions_raw": safe_sum("is_serious_raw"),
    "slight_collisions_raw": safe_sum("is_slight_raw"),
    "ksi_collisions_raw": safe_sum("is_killed_or_seriously_injured_raw"),
    "avg_casualties_per_collision": round(df["number_of_casualties"].fillna(0).mean(), 4) if "number_of_casualties" in df.columns else None,
    "avg_vehicles_per_collision": round(df["number_of_vehicles"].fillna(0).mean(), 4) if "number_of_vehicles" in df.columns else None,
    "weekend_collision_rate_pct": round(df["is_weekend"].fillna(False).astype(bool).mean() * 100, 2) if "is_weekend" in df.columns else None
}])

summary.to_csv(tables / "kpi_collision_overview_v1.csv", index=False)

print("kpi_collision_overview_v1_created")
print(summary.to_string(index=False))
