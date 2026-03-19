from pathlib import Path
import pandas as pd

ref_path = next(Path("data/reference").glob("*.xlsx"))

df = pd.read_excel(ref_path, sheet_name="2024_code_list")

print("COLUMNS:")
print(df.columns.tolist())
print()
print("FIRST 20 ROWS:")
print(df.head(20).to_string(index=False))
