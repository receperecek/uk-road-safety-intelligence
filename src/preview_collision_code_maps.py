from pathlib import Path
import pandas as pd

ref_path = next(Path("data/reference").glob("*.xlsx"))

df = pd.read_excel(ref_path, sheet_name="2024_code_list")

target_fields = [
    "collision_severity",
    "road_type",
    "light_conditions",
    "weather_conditions",
    "road_surface_conditions",
    "urban_or_rural_area"
]

filtered = df[
    (df["table"] == "collision") &
    (df["field name"].isin(target_fields))
].copy()

filtered = filtered.sort_values(["field name", "code/format"])

print(filtered.to_string(index=False))
