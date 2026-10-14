import numpy as np
import pandas as pd
import KNN
import logistical_reg
import subprocess
import time




new_asteroid = np.array([
    new_diameter,  # diameter_km
    new_absolute_magnitude,  # H
    new_rotation_period,  # rot_per
    Orbita_eccentricity,  # e
    Semi_major_axis,  # a
    Orbital_inclination,  # i
    Perhelion_Distance,   # q
    Aphelion_Distance,   # ad
    Minimum_orbit_intersect_distance,  # moid_kn
], dtype=float)

def start_site():
    procces = subprocess.Popen(["python","black_globe_ui.py"])
    time.sleep(1)
def run_predictions(new_asteriod):
    knn_result = KNN.predict(new_asteriod)
    
    reg_log_result = logistical_reg.predict(new_asteriod)
    int(np.asarray(reg.log_result.item()))
    print(vote)




start_site()
run_predictions(new_asteroid)




