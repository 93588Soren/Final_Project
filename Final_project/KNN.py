import math
import pandas as pd
import numpy as np

k = 1
near_earth_asteriods_df = pd.read_csv('near_earth_asteroids_2025 (1).csv')

print(near_earth_asteriods_df.info())

x = near_earth_asteriods_df[[
    'diameter_km',
    'H',
    'rot_per',
    'e',
    'a',
    'i',
    'q',
    'ad']].values
y = near_earth_asteriods_df['pha'].values




def predict(new_asteriod):
    closest_match = None
    shortest_distnace = float('inf')
    for x in near_earth_asteriods_df:
        

