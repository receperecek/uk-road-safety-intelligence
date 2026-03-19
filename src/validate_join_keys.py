from pathlib import Path
import pandas as pd

base = Path("data/raw")

collisions_path = next((base / "collisions").glob("*.csv"))
vehicles_path = next((base / "vehicles").glob("*.csv"))
casualties_path = next((base / "casualties").glob("*.csv"))

collisions = pd.read_csv(
    collisions_path,
    usecols=["collision_index"],
    low_memory=False
)

vehicles = pd.read_csv(
    vehicles_path,
    usecols=["collision_index", "vehicle_reference"],
    low_memory=False
)

casualties = pd.read_csv(
    casualties_path,
    usecols=["collision_index", "vehicle_reference", "casualty_reference"],
    low_memory=False
)

collision_keys = set(collisions["collision_index"])
vehicle_collision_keys = set(vehicles["collision_index"])
casualty_collision_keys = set(casualties["collision_index"])

vehicle_missing_in_collisions = len(vehicle_collision_keys - collision_keys)
casualty_missing_in_collisions = len(casualty_collision_keys - collision_keys)

print("=" * 70)
print("JOIN KEY VALIDATION")
print("=" * 70)
print(f"Collisions unique collision_index : {collisions['collision_index'].nunique():,}")
print(f"Vehicles unique collision_index   : {vehicles['collision_index'].nunique():,}")
print(f"Casualties unique collision_index : {casualties['collision_index'].nunique():,}")
print()
print(f"Vehicle collision_index values not found in collisions : {vehicle_missing_in_collisions:,}")
print(f"Casualty collision_index values not found in collisions: {casualty_missing_in_collisions:,}")
print()
print(f"Vehicles unique vehicle_reference count   : {vehicles['vehicle_reference'].nunique():,}")
print(f"Casualties unique vehicle_reference count : {casualties['vehicle_reference'].nunique():,}")
print(f"Casualties unique casualty_reference count: {casualties['casualty_reference'].nunique():,}")
