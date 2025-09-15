# Project Overview
This project evaluates spatial-temporal query efficiency on the Porto taxi dataset by testing three tasks, similar path search, nearby path retrieval and shortest route detection using sequential scan, R-tree and SP-GiST indexes. Results show task-based performance, guiding index selection for large-scale movement data like smart transport systems.
# Environment Requirements
File: plot_trajectories.py
Language: Python
Purpose: Visualiz Trajectory for Spatial Density Analysis
# When Used:
This Python script was used during the analysis how density of path impact the query performance for Task 1  (Trajectory Similarity Search) and Task 2 (Spatial Range Join). It aims to help find how dense or sparse the nearby trajectories are around the target path.
# How It Works:
1. Connects to the PostgreSQL database by using SQLAlchemy and GeoPandas.
2.  Retrieves one target trajectory using its trip_id.
3.  Retrieves (up to 2,000) trajectories that are within 200 meters of the target by using ST_DWithin.
4.  Uses matplotlib and geopandas to plot the target in red and nearby trajectories in blue.
# Why It Was Necessary:
This script provides a more intuitive and visual way to understand spatial distribution by plotting the target and nearby trajectories. It helped explain why some queries were slower, especially in dense regions, as shown in Fig. 2 of the report.
# Dependencies:
geopandas
matplotlib
sqlalchemy
PostgreSQL with PostGIS enabled
# Note:
Make sure the target trip_id is adjusted before running. The x/y limits for the map were manually set to focus on specific cases (case1, case2, etc.).
