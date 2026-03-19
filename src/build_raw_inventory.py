from pathlib import Path
import pandas as pd

base = Path("data/raw")

files = {
    "collisions": next((base / "collisions").glob("*.csv")),
    "vehicles": next((base / "vehicles").glob("*.csv")),
    "casualties": next((base / "casualties").glob("*.csv")),
}

lines = []
lines.append("# Raw Data Inventory")
lines.append("")

for name, path in files.items():
    df = pd.read_csv(path, low_memory=False)

    lines.append(f"## {name}")
    lines.append(f"- file_name: {path.name}")
    lines.append(f"- rows: {df.shape[0]}")
    lines.append(f"- columns: {df.shape[1]}")
    lines.append(f"- key_columns_preview: {', '.join(df.columns[:10])}")
    lines.append("")
    lines.append("### columns")
    for col in df.columns:
        lines.append(f"- {col}")
    lines.append("")

Path("docs/raw_data_inventory.md").write_text("\n".join(lines), encoding="utf-8")
print("raw_data_inventory_created")
