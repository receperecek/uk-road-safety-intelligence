from pathlib import Path
import pandas as pd

gold = Path("data/processed/gold")
tables = Path("outputs/tables")

df = pd.read_parquet(gold / "mart_collision_risk_labeled_v1.parquet").copy()

work = df[df["light_conditions_label"].notna()].copy()

profile = (
    work.groupby("light_conditions_label", dropna=False)
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

profile["collision_share_pct"] = (
    profile["total_collisions"] / profile["total_collisions"].sum() * 100
).round(2)

profile["fatal_collision_rate_pct"] = (
    profile["fatal_collisions_raw"] / profile["total_collisions"] * 100
).round(2)

profile["ksi_collision_rate_pct"] = (
    profile["ksi_collisions_raw"] / profile["total_collisions"] * 100
).round(2)

profile["avg_casualties_per_collision"] = profile["avg_casualties_per_collision"].round(4)
profile["avg_vehicles_per_collision"] = profile["avg_vehicles_per_collision"].round(4)

profile = profile.sort_values(
    by=["total_collisions", "ksi_collision_rate_pct"],
    ascending=[False, False]
)

profile.to_csv(tables / "light_conditions_severity_profile_decoded_v1.csv", index=False)

print("light_conditions_severity_profile_decoded_v1_created")
print(profile.to_string(index=False))
