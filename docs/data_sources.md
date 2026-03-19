# Data Sources

## Primary Source
Department for Transport (DfT) - Road Safety Open Data

## Core Datasets
1. Collisions (record level)
2. Vehicles (record level)
3. Casualties (record level)

## Official Source Notes
- Data is provided in coded format
- Open data guide is required for decoding category values
- 2024 is the latest final validated full year
- 2025 first-half data is provisional and excluded from v1

## Supporting Files
- Open dataset data guide
- Severity adjustment guidance
- Road safety statistics data tables
- Optional economic context tables (RAS40 family)

## Join Keys
- collision_index
- vehicle_reference
- casualty_reference

## Data Strategy
Raw source files will be downloaded manually and stored under:
- data/raw/collisions
- data/raw/vehicles
- data/raw/casualties

Raw files will not be committed to GitHub.
