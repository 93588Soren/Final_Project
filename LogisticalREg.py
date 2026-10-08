import math 
import pandas as pd
import numpy as np


df = pd.read_csv('dragon_train.csv')
print(df.info())

#ai data
weights = np.zeros(6)
bias = 0
x = df[["nest_temp_c",
        "volcanoe_distance_km",
        "humidity_pct",
        "moonlight_hours",
        "shell_shimmer",
        "egg_weight_kg"]]




y = df["label"].values

#wtf is matrix mul
z = x @ weights+bias

def sigmoid(z):
    return 1/(1+np.exp(-z))




probabilities = sigmoid(z)

print(probabilities)

