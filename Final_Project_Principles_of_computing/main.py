import numpy as np
import pandas as pd
import KNN
import logistical_reg
import subprocess
import time




new_asteroid = np.array([
    0.49,   # diameter_km
    20.19,  # H
    0.204,  # e
    0.897,  # q
    5.2,    # moid_km
], dtype=float)

def start_site():
    procces = subprocess.Popen(["python","black_globe_ui.py"])
    time.sleep(1)
def run_predictions(new_asteriod):
    knn_result = KNN.predict(new_asteriod)
    
    reg_log_result = logistical_reg.predict(new_asteriod)
    reg_log_result = int(np.asarray(reg_log_result).item())
    print("KNN:", knn_result, "| Logistic regression:", reg_log_result)




start_site()
run_predictions(new_asteroid)
