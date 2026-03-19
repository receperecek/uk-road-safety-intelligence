from pathlib import Path
import pandas as pd

gold = Path("data/processed/gold")
tables = Path("outputs/tables")

df = pd.read_parquet(gold / "mart_collision_risk_v1.parquet").copy()

yearly = (
    df.groupby("collision_year", dropna=False)
    .agg(
        total_collisions=("collision_index", "count"),
        total_casualties=("number_of_casualties", "sum"),
        total_vehicles=("number_of_vehicles", "sum"),
        fatal_collisions_raw=("is_fatal_raw", "sum"),
        serious_collisions_raw=("is_serious_raw", "sum"),
        slight_collisions_raw=("is_slight_raw", "sum"),
        ksi_collisions_raw=("is_killed_or_seriously_injured_raw", "sum"),
        avg_casualties_per_collision=("number_of_casualties", "mean"),
        avg_vehicles_per_collision=("number_of_vehicles", "mean")
    )
    .reset_index()
)

yearly["ksi_collision_rate_pct"] = (
    yearly["ksi_collisions_raw"] / yearly["total_collisions"] * 100
).round(2)

yearly["fatal_collision_rate_pct"] = (
    yearly["fatal_collisions_raw"] / yearly["total_collisions"] * 100
).round(2)

yearly["avg_casualties_per_collision"] = yearly["avg_casualties_per_collision"].round(4)
yearly["avg_vehicles_per_collision"] = yearly["avg_vehicles_per_collision"].round(4)

yearly.to_csv(tables / "yearly_severity_trend_v1.csv", index=False)

print("yearly_severity_trend_v1_created")
print(yearly.to_string(index=False))
