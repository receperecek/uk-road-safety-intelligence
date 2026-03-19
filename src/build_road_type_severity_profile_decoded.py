from pathlib import Path
import pandas as pd

gold = Path("data/processed/gold")
tables = Path("outputs/tables")

df = pd.read_parquet(gold / "mart_collision_risk_labeled_v1.parquet").copy()

work = df[df["road_type_label"].notna()].copy()

road_type_profile = (
    work.groupby("road_type_label", dropna=False)
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

road_type_profile["collision_share_pct"] = (
    road_type_profile["total_collisions"] / road_type_profile["total_collisions"].sum() * 100
).round(2)

road_type_profile["fatal_collision_rate_pct"] = (
    road_type_profile["fatal_collisions_raw"] / road_type_profile["total_collisions"] * 100
).round(2)

road_type_profile["ksi_collision_rate_pct"] = (
    road_type_profile["ksi_collisions_raw"] / road_type_profile["total_collisions"] * 100
).round(2)

road_type_profile["avg_casualties_per_collision"] = road_type_profile["avg_casualties_per_collision"].round(4)
road_type_profile["avg_vehicles_per_collision"] = road_type_profile["avg_vehicles_per_collision"].round(4)

road_type_profile = road_type_profile.sort_values(
    by=["total_collisions", "ksi_collision_rate_pct"],
    ascending=[False, False]
)

road_type_profile.to_csv(tables / "road_type_severity_profile_decoded_v1.csv", index=False)

print("road_type_severity_profile_decoded_v1_created")
print(road_type_profile.to_string(index=False))
