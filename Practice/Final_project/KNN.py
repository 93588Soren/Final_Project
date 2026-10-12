import math
import pandas as pd
import numpy as np

confirmed_atmostspheres_df = pd.read_csv('iac_exoplanet_atmospheres-20261012.csv',sep = ';', quotechar= '"', on_bad_lines = 'skip')

print(confirmed_atmostspheres_df.info())






def predict_atmostphere(exoplanet):
    closest_planet = None