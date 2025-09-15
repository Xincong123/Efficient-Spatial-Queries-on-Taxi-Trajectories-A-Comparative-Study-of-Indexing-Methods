import geopandas as gpd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# connect postgres
DB_USER = 'postgres'
DB_PASSWORD = 'congyu123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'train_db'

# dataset
conn_str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(conn_str)
print(engine)  # 检查连接是否成功

# target_trip
TARGET_TRIP_ID = '1403863405620000542'
# TARGET_TRIP_ID = '1388517151620000080'
# TARGET_TRIP_ID = '1372929767620000304'

# sql query
target_sql = f"""
SELECT trip_id, trajectory_geom
FROM taxi_trips
WHERE trip_id = '{TARGET_TRIP_ID}'
"""
target = gpd.read_postgis(target_sql, engine, geom_col='trajectory_geom')

nearby_sql = f"""
SELECT trip_id, trajectory_geom
FROM taxi_trips
WHERE trip_id <> '{TARGET_TRIP_ID}'
  AND trajectory_geom IS NOT NULL
  AND ST_IsValid(trajectory_geom)
  AND ST_DWithin(
        trajectory_geom,
        (SELECT trajectory_geom FROM taxi_trips WHERE trip_id = '{TARGET_TRIP_ID}'),
        0.002
  )
"""
# nerarby path
nearby = gpd.read_postgis(nearby_sql, engine, geom_col='trajectory_geom')
nearby = nearby.head(2000)
print("Trip_ID：", TARGET_TRIP_ID)
print("Target count:", len(target))
print("Nearby count:", len(nearby))

# virualization
fig, ax = plt.subplots(figsize=(10, 10))
nearby.plot(ax=ax, color='blue', linewidth=0.5, label='Nearby Trajectories')
target.plot(ax=ax, color='red', linewidth=2, label='Target Trajectory')
ax.set_aspect('equal', adjustable='datalim')
# case2: '1388517151620000080'
# ax.set_xlim(-8.67, -8.66) 
# ax.set_ylim(41.16, 41.20)

# case1: '1403863405620000542'
ax.set_xlim(-8.63, -8.57) 
ax.set_ylim(41.12, 41.18)

# ax.set_xlim(-8.61, -8.64) 
# ax.set_ylim(41.15, 41.17)
plt.title("Target vs Nearby Trajectories")
plt.legend()
plt.show()
