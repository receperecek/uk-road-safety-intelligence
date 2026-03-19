from pathlib import Path
import pandas as pd

tables = Path("outputs/tables")

df = pd.read_csv(tables / "speed_limit_severity_profile_v1.csv")

core_limits = [20, 30, 40, 50, 60, 70]
df["speed_limit"] = pd.to_numeric(df["speed_limit"], errors="coerce")

core = df[df["speed_limit"].isin(core_limits)].copy()

core = core.sort_values(
    by=["total_collisions", "ksi_collision_rate_pct"],
    ascending=[False, False]
)

core.to_csv(tables / "speed_limit_severity_profile_core_v1.csv", index=False)

top_volume = core.sort_values("total_collisions", ascending=False).iloc[0]
top_ksi = core.sort_values("ksi_collision_rate_pct", ascending=False).iloc[0]
top_fatal = core.sort_values("fatal_collision_rate_pct", ascending=False).iloc[0]

lines = []
lines.append("# Speed Limit Insights v1")
lines.append("")
lines.append(f"- Highest collision volume: {int(top_volume['speed_limit'])} mph with {int(top_volume['total_collisions']):,} collisions.")
lines.append(f"- Highest KSI collision rate: {int(top_ksi['speed_limit'])} mph with {top_ksi['ksi_collision_rate_pct']:.2f}% KSI rate.")
lines.append(f"- Highest fatal collision rate: {int(top_fatal['speed_limit'])} mph with {top_fatal['fatal_collision_rate_pct']:.2f}% fatal collision rate.")
lines.append("")
lines.append("## Analyst note")
lines.append("This table is restricted to common interpretable UK speed limits (20, 30, 40, 50, 60, 70 mph) to avoid coded or unknown values affecting the business interpretation.")

(tables / "speed_limit_insights_v1.md").write_text("\n".join(lines), encoding="utf-8")

print("speed_limit_core_and_insights_created")
print(core.to_string(index=False))
print()
print("\n".join(lines))
