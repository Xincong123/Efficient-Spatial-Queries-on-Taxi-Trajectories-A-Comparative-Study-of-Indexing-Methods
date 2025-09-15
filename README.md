# INFS 7205 Efficient Spatial Queries on Taxi Trajectories

**Author:** Xincong Ren
**Course:** INFS4205/7205 Advanced Techniques in High Dimensional Data, Semester 1, 2025
---

## Project Overview
This project evaluates spatial-temporal query efficiency on the Porto taxi dataset by testing three tasks, similar path search, nearby path retrieval and shortest route detection using sequential scan, R-tree and SP-GiST indexes. Results show task-based performance, guiding index selection for large-scale movement data like smart transport systems.

## Dataset

## Environment Requirements
- **Python 3.x**
- Dependencies:geopandas  matplotlib  sqlalchemy
- PostgreSQL 15+ with PostGIS 3.4+ enabled.
- Install the following Python packages:
  ```bash
  pip install geopandas matplotlib sqlalchemy psycopg2
  ```
  
---


# File Description
plot_trajectories.py
Purpose: Visualize target and nearby taxi trajectories to analyze spatial density and understand its effect on query performance.
When Used
This script supports the analysis for Task 1 (Trajectory Similarity Search) and Task 2 (Spatial Range Join). It helps identify how dense or sparse the surrounding trajectories are around a selected path.
How It Works
1. Connects to the PostgreSQL database by using SQLAlchemy and GeoPandas.
2.  Retrieves one target trajectory using its trip_id.
3.  Retrieves (up to 2,000) trajectories that are within 200 meters of the target by using ST_DWithin.
4.  Uses matplotlib and geopandas to plot the target in red and nearby trajectories in blue.
Why It’s Important
This script provides a more intuitive and visual way to understand spatial distribution by plotting the target and nearby trajectories. It helped explain why some queries were slower, especially in dense regions, as shown in Fig. 2 of the report.
By visualizing the density of nearby paths, this script explains performance differences across indexing methods—dense regions show slower queries due to heavier I/O and buffer usage. (See Fig. 2 of the report for examples.)
This Python script was used during the analysis how density of path impact the query performance for Task 1  (Trajectory Similarity Search) and Task 2 (Spatial Range Join). It aims to help find how dense or sparse the nearby trajectories are around the target path.

# Note
Make sure the target trip_id is adjusted before running. The x/y limits for the map were manually set to focus on specific cases (case1, case2, etc.).
