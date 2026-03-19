from pathlib import Path
import pandas as pd

gold = Path("data/processed/gold")
tables = Path("outputs/tables")

df = pd.read_parquet(gold / "mart_collision_risk_v1.parquet").copy()

work = df[df["speed_limit"].notna()].copy()

speed_profile = (
    work.groupby("speed_limit", dropna=False)
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

speed_profile["collision_share_pct"] = (
    speed_profile["total_collisions"] / speed_profile["total_collisions"].sum() * 100
).round(2)

speed_profile["fatal_collision_rate_pct"] = (
    speed_profile["fatal_collisions_raw"] / speed_profile["total_collisions"] * 100
).round(2)

speed_profile["ksi_collision_rate_pct"] = (
    speed_profile["ksi_collisions_raw"] / speed_profile["total_collisions"] * 100
).round(2)

speed_profile["avg_casualties_per_collision"] = speed_profile["avg_casualties_per_collision"].round(4)
speed_profile["avg_vehicles_per_collision"] = speed_profile["avg_vehicles_per_collision"].round(4)

speed_profile = speed_profile.sort_values(
    by=["total_collisions", "ksi_collision_rate_pct"],
    ascending=[False, False]
)

speed_profile.to_csv(tables / "speed_limit_severity_profile_v1.csv", index=False)

print("speed_limit_severity_profile_v1_created")
print(speed_profile.to_string(index=False))
