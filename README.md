# UK Road Safety Intelligence Platform

A multi-table road safety analytics project built on official UK Department for Transport (DfT) STATS19 collision, vehicle, and casualty data.

## Project Objective
This project is designed as a decision-support oriented analytics workflow rather than a simple EDA notebook.  
The goal is to identify:
- high-volume collision environments
- high-severity risk contexts
- interpretable safety patterns across road, speed, weather, lighting, and urban-rural dimensions

## Dataset Scope
- Source: UK DfT STATS19 open road safety data
- Time window: 2020-2024
- Core tables:
  - collisions
  - vehicles
  - casualties
- Reference guide:
  - official 2024 code list used for semantic decoding of coded fields

## Data Model
This project uses a relational structure:
- collision_index as the parent collision key
- collision_index + vehicle_reference for vehicle-level grain
- collision_index + casualty_reference for casualty-level grain

## Pipeline Status (v1)
Completed:
- project skeleton
- raw data ingestion
- raw data inventory
- join-key validation
- silver layer cleaning
- gold mart creation
- coded field decoding
- KPI overview table
- yearly severity trend
- multiple decoded severity profiles
- finding reports in markdown format

## Core KPI Snapshot
- Total collisions: 503,475
- Total casualties: 640,522
- Total vehicles: 920,692
- Average casualties per collision: 1.2722
- Average vehicles per collision: 1.8287
- Weekend collision rate: 25.06%

## Key Findings
### 1) Speed limit context
- 30 mph roads accounted for the highest collision volume with 269,912 collisions (53.61% share of interpretable speed-limit records).
- 60 mph roads showed the highest severity burden with a 33.76% KSI collision rate and a 3.93% fatal collision rate.

### 2) Road type context
- Single carriageway roads accounted for the highest collision volume with 274,367 collisions (72.66% share of decoded road-type records).
- Single carriageway roads also showed the highest KSI collision rate at 25.00%.
- Dual carriageways showed a sharper fatality profile at 2.05%.

### 3) Weather context
- Fine weather with no high winds accounted for the largest collision volume with 400,956 collisions (79.64% share).
- More severe outcomes appear concentrated in lower-volume adverse weather contexts such as fog/mist and high-wind conditions.

### 4) Urban vs rural context
- Urban areas accounted for 269,491 collisions (67.51% share).
- Rural areas showed materially higher severity:
  - fatal collision rate: 2.87%
  - KSI collision rate: 28.77%
- Urban areas had lower severity rates despite higher volume.

### 5) Lighting context
- Daylight accounted for the highest collision volume with 359,837 collisions (71.47% share).
- Darkness with no lighting showed the strongest severity profile:
  - fatal collision rate: 4.91%
  - KSI collision rate: 34.24%

## Analytical Interpretation
A repeated pattern appears across the project:
high-volume environments are not always the same as high-severity environments.

That makes this project useful for decision support, because it separates:
- exposure-heavy contexts
- severity-heavy contexts
- intervention priority logic

## Repository Structure
- data/raw/ -> original source files
- data/reference/ -> official coding guide
- data/processed/silver/ -> cleaned analytical tables
- data/processed/gold/ -> mart outputs
- outputs/tables/ -> KPI and profile tables
- 
eports/ -> business-style finding summaries
- src/ -> pipeline scripts

## Current Positioning
This portfolio project is designed to demonstrate:
- Data Analyst thinking
- Data Engineering discipline
- relational modeling ability
- decision-support focused analytics
- business-oriented interpretation instead of chart-only exploration

## Next Planned Extensions
- casualty-level severity analysis
- vehicle-driver risk profiling
- hotspot prioritization logic
- intervention scoring framework
- cloud-ready storage and orchestration layer

## How to Run

1) Create and activate the virtual environment
`powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/test_load_data.py
python src/build_raw_inventory.py
python src/validate_join_keys.py
python src/clean_collisions.py
python src/clean_vehicles.py
python src/clean_casualties.py
python src/model_sanity_check.py

## Power BI Dashboard Layer

This project also includes a Power BI dashboard layer built on top of Python-generated analytical output tables.

### Dashboard pages
- **KPI Overview**  
  High-level metrics and yearly collision vs KSI trend

- **Risk Context Analysis**  
  Severity-focused visuals across speed limit, road type, and urban-rural context

### Dashboard assets
See the `dashboard/` folder for:
- Power BI dashboard file (`.pbix`)
- dashboard screenshots
- dashboard notes

### Dashboard purpose
The dashboard is designed to translate analytical outputs into decision-support oriented visuals rather than static chart exports only.


python src/build_mart_collision_risk.py
python src/build_kpi_collision_overview.py
python src/build_yearly_severity_trend.py
python src/decode_collision_mart_labels.pypython src/build_speed_limit_severity_profile.py
python src/build_speed_limit_core_insights.py
python src/build_road_type_severity_profile_decoded.py
python src/build_weather_severity_profile_decoded.py
python src/build_urban_rural_severity_profile_decoded.py
python src/build_light_conditions_severity_profile_decoded.py
