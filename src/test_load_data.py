from pathlib import Path
import pandas as pd

base = Path("data/raw")

files = {
    "collisions": next((base / "collisions").glob("*.csv")),
    "vehicles": next((base / "vehicles").glob("*.csv")),
    "casualties": next((base / "casualties").glob("*.csv")),
}

for name, path in files.items():
    df = pd.read_csv(path, low_memory=False)

    print("=" * 70)
    print(f"TABLE: {name}")
    print(f"FILE : {path.name}")
    print(f"SHAPE: {df.shape}")
    print("FIRST 10 COLUMNS:")
    print(df.columns[:10].tolist())
    print()
