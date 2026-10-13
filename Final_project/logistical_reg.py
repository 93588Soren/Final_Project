import math
import pandas as pd
import numpy as np


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


EPSILON = 1e-15
LEARNING_RATE = .01
EPOCHS = 100
weights = np.zeros(8)
bias = 0

mean = x.mean(axis=0)
std = x.std(axis = 0)

x_scaled = (x-mean)/std

def sigmoid(z):
 z_clipped = np.clip(z, -500, 500)
 return 1/(1+np.exp(-z_clipped))


def calculate_loss(y, probabilities):
    n = len(y)
    p_clipped = np.clip(probabilities, EPSILON, 1-EPSILON)
    loss = (-1/n) * np.sum(y*np.log(p_clipped)+ (1-y) *np.log(1-p_clipped))
    return loss


def fit(weights, bias, LEARNING_RATE, EPOCHS, y, x_scaled):
   losses = []
   for epoch in range(EPOCHS):
      z = x_scaled @ weights+bias
      probabilities = sigmoid(z)
      n = len(x_scaled)
      loss = calculate_loss(y,probabilities)
      losses.append(loss)
      error = probabilities-y
      if epoch % 10 ==0:
        print(f"Epoch {epoch}: Loss is currently {loss}" )
      dw =(1/n)*np.dot(x_scaled.T, error)
      db =(1/n)*np.sum(error)
      weights = weights-LEARNING_RATE*dw
      bias = bias-LEARNING_RATE*db
      z = x_scaled @ weights +bias
      probabilites = sigmoid(z)
      error = probabilities-y
      dw = (1 / len(y)) * (x_scaled.T @ error)
      db = (1 / len(y)) * np.sum(error)
      gradient_size = np.sqrt(np.sum(dw**2) + db**2)

      print("Final loss:", calculate_loss(y, probabilities))
      print("Final gradient magnitude:", gradient_size)
      print("Final weights:", weights)
      print("Final bias:", bias)
      return weights, bias, losses


weights, bias, losses = fit(weights, bias, LEARNING_RATE, EPOCHS, y, x_scaled)

new_asteroid = np.array([
    0.5,   # diameter_km
    20.0,  # H
    12.0,  # rot_per
    0.2,   # e
    1.5,   # a
    10.0,  # i
    1.2,   # q
    1.8,   # ad
], dtype=float)

new_asteroid_scaled = (new_asteroid - mean) / std
z_new = new_asteroid_scaled @ weights+bias
new_probabilities = sigmoid(z_new)

    


