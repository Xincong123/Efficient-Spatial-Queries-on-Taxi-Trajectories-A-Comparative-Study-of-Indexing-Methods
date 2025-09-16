# INFS 7205 Efficient Spatial Queries on Taxi Trajectories🚗

**Author:** Xincong Ren  
**Course:** INFS4205/7205 Advanced Techniques in High Dimensional Data, Semester 1, 2025

---

## 📦Project Overview
This project evaluates spatial-temporal query efficiency on the Porto taxi dataset by testing three tasks, similar path search, nearby path retrieval and shortest route detection using sequential scan, R-tree and SP-GiST indexes. Results show task-based performance, guiding index selection for large-scale movement data like smart transport systems.

## 📊Dataset

- **Source:** [Kaggle-Taxi Trajectory](https://www.kaggle.com/datasets/crailtap/taxi-trajectory)
- **Records:** 1,710,670 GPS trajectories logs with timestamps
- **Format:** CSV
- **Use Case:** Spatio-temporal analysis, map-matching, mobility behavior, trajectory clustering

---

## 🛠️Environment Requirements
- **Python 3.x**
- **Dependencies:** geopandas  matplotlib  sqlalchemy
- PostgreSQL 15+ with PostGIS 3.4+ enabled.

---
## ⏳Methodology

### 1️⃣Data Preprocessing (Raw CSV to Cleaned Table)
1. Create a **temporary table** and import raw data:
```sql
CREATE TABLE taxi_trips_temp (
  trip_id TEXT,
  call_type TEXT,
  origin_call TEXT,
  origin_stand TEXT,
  taxi_id TEXT,
  timestamp BIGINT,
  day_type TEXT,
  missing_data BOOLEAN,
  polyline TEXT
);
```

2. Import **CSV** into the temp table (adjust path as needed):
```sql
CREATE TABLE taxi_trips_temp (
  trip_id TEXT,
  call_type TEXT,
  origin_call TEXT,
  origin_stand TEXT,
  taxi_id TEXT,
  timestamp BIGINT,
  day_type TEXT,
  missing_data BOOLEAN,
  polyline TEXT
);
```

### 2️⃣Create Main Table & Remove Duplicates
1. Create main table with primary key
```sql
CREATE TABLE taxi_trips (
    trip_id TEXT PRIMARY KEY,
    call_type TEXT,
    origin_call TEXT,
    origin_stand TEXT,
    taxi_id TEXT,
    timestamp BIGINT,
    day_type TEXT,
    missing_data BOOLEAN,
    polyline TEXT
);
```

2. **Insert data from temp table (skip duplicates):**
```sql
INSERT INTO taxi_trips
SELECT * FROM taxi_trips_temp ON CONFLICT (trip_id) DO NOTHING;
```

### 3️⃣Create Main Table & Remove Duplicates
Check and delete rows with missing critical fields:
```sql
-- Check missing values
SELECT COUNT(*) AS null_trip_id FROM taxi_trips WHERE trip_id IS NULL OR trip_id = '';
SELECT COUNT(*) AS null_polyline FROM taxi_trips WHERE polyline IS NULL OR polyline = '[]';
SELECT COUNT(*) AS null_timestamp FROM taxi_trips WHERE timestamp IS NULL;

-- Delete invalid rows
DELETE FROM taxi_trips WHERE polyline IS NULL OR polyline = '[]';
```

### 4️⃣Convert  `polyline` to PostGIS `LINESTRING`
1. Enable PostGIS and add geometry column:
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
-- Remove existing column if needed
ALTER TABLE taxi_trips DROP COLUMN IF EXISTS trajectory_geom;
-- Add geometry column
ALTER TABLE taxi_trips ADD COLUMN trajectory_geom geometry(LineString, 4326);
```

2. Batch update geometry (example with LIMIT 349299):

```sql
UPDATE taxi_trips
SET trajectory_geom = ST_SetSRID(
    ST_MakeLine(ARRAY(SELECT ST_MakePoint((point->>0)::float8, (point->>1)::float8)
            FROM json_array_elements(polyline::json) AS point)), 4326)
WHERE ctid IN (
    SELECT ctid
    FROM taxi_trips
    WHERE trajectory_geom IS NULL
    LIMIT 349299
);
```


### 5️⃣Remove Rows with Missing Data = True
Backup and delete records:
```sql
CREATE TABLE taxi_trips_missing_backup AS SELECT * FROM taxi_trips WHERE missing_data = 'True';
DELETE FROM taxi_trips WHERE missing_data = 'True';
```

### 6️⃣Add Derived Columns (Trip Date)
```sql
-- Add date column from UNIX timestamp
ALTER TABLE taxi_trips ADD COLUMN trip_date date;

UPDATE taxi_trips
SET trip_date = to_timestamp(timestamp)::date;
```

### 7️⃣Example Query: Filter Trajectories by Point Count
(Optional performance tuning for index testing)
```sql
-- Disable index scan for testing
SET enable_indexscan = OFF;
SET enable_bitmapscan = OFF;
SET enable_seqscan = ON;

-- Filter trajectories with 20–49 points
WITH traj_with_points AS (
    SELECT trip_id, trip_date, ST_NPoints(trajectory_geom) AS num_points
    FROM taxi_trips
    WHERE trajectory_geom IS NOT NULL
)
SELECT *
FROM traj_with_points
WHERE num_points >= 20 AND num_points < 50
ORDER BY num_points ASC
LIMIT 5;

```
### **Final Record Count**  
| Stage                  | Record Count |  
|------------------------|--------------|  
| Raw data (original)    | 1,710,670    |  
| After cleaning         | ~1,704,681   |  

---

## 📄 The `INFS7205A2_query_Xincong.sql` file includes:
- Table creation (temp & final)
- Data loading & cleaning from CSV
- PostGIS geometry conversion (`polyline` → `LINESTRING`)
- Derived fields: `trip_date`, `point_count`
- Backup & removal of rows with `missing_data = True`
- Trajectory similarity search using Frechet Distance
- Performance benchmarking via `EXPLAIN (ANALYZE)`

--- 
## 📁File Structure
```
.
├── plot_trajectories.py                 # Python script to visualize GPS trajectories on a map
├── INFS7205A2_query_Xincong.sql         # SQL for data processing, geometry conversion, and spatial queries
└── INFS7205A2_report_Xincong.pdf        # Full report for result analysis and reflection
```

---


