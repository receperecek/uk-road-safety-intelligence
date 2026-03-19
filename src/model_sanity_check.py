from pathlib import Path
import pandas as pd

silver = Path("data/processed/silver")
tables = Path("outputs/tables")
tables.mkdir(parents=True, exist_ok=True)

collisions = pd.read_parquet(silver / "collisions_clean.parquet")
vehicles = pd.read_parquet(silver / "vehicles_clean.parquet")
casualties = pd.read_parquet(silver / "casualties_clean.parquet")

vehicle_counts = (
    vehicles.groupby("collision_index")
    .size()
    .reset_index(name="vehicle_count_from_vehicles")
)

casualty_counts = (
    casualties.groupby("collision_index")
    .size()
    .reset_index(name="casualty_count_from_casualties")
)

model_check = (
    collisions[["collision_index", "number_of_vehicles", "number_of_casualties"]]
    .merge(vehicle_counts, on="collision_index", how="left")
    .merge(casualty_counts, on="collision_index", how="left")
)

model_check["vehicle_count_from_vehicles"] = model_check["vehicle_count_from_vehicles"].fillna(0).astype(int)
model_check["casualty_count_from_casualties"] = model_check["casualty_count_from_casualties"].fillna(0).astype(int)

model_check["vehicle_count_match"] = (
    model_check["number_of_vehicles"] == model_check["vehicle_count_from_vehicles"]
)

model_check["casualty_count_match"] = (
    model_check["number_of_casualties"] == model_check["casualty_count_from_casualties"]
)

summary = pd.DataFrame([{
    "collision_rows": len(collisions),
    "vehicle_rows": len(vehicles),
    "casualty_rows": len(casualties),
    "unique_collisions_in_vehicles": vehicles["collision_index"].nunique(),
    "unique_collisions_in_casualties": casualties["collision_index"].nunique(),
    "vehicle_count_match_rate_pct": round(model_check["vehicle_count_match"].mean() * 100, 2),
    "casualty_count_match_rate_pct": round(model_check["casualty_count_match"].mean() * 100, 2),
    "vehicle_count_mismatch_rows": int((~model_check["vehicle_count_match"]).sum()),
    "casualty_count_mismatch_rows": int((~model_check["casualty_count_match"]).sum())
}])

summary.to_csv(tables / "model_sanity_summary.csv", index=False)
model_check.head(100).to_csv(tables / "model_sanity_sample.csv", index=False)

print("model_sanity_check_created")
print(summary.to_string(index=False))
