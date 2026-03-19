from pathlib import Path
import pandas as pd

ref_path = next(Path("data/reference").glob("*.xls*"))

xls = pd.ExcelFile(ref_path)

print("REFERENCE_FILE:", ref_path.name)
print("=" * 70)
print("SHEETS:")
for i, sheet in enumerate(xls.sheet_names, start=1):
    print(f"{i}. {sheet}")
