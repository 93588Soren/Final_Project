import math 
import pandas as pd
import numpy as np


df = pd.read_csv('dragon_train.csv')
print(df.info())


EPSILON = 1e-15
LEARNING_RATE=.01
EPOCHS = 100
weights = np.zeros(6)
bias = 0
x = df[["nest_temp_c",
        "volcano_distance_km",
        "humidity_pct",
        "moonlight_hours",
        "shell_shimmer",
        "egg_weight_kg"]].values
y = df["label"].values

#z is logit
z = x @ weights+bias

def sigmoid(z):
    return 1/(1+np.exp(-z))

#log  loss?
def  calculate_loss(y,probabilities):
    n = len(y)
    #add probability clipping later
    loss = (-1/n) * np.sum(y*np.log(probabilities+EPSILON) + (1-y) * np.log(1-probabilities+EPSILON))
    print(f"Loss is currently {loss}")
    return loss


#Gradient Descent (not implemented yet)
def fit(weights, bias, LEARNING_RATE, EPOCHS, probabilities, y,x):
    for epoch in range(EPOCHS):
        z = x @ weights+bias
        probabilities = sigmoid(z)


def calculate_gradients()









probabilities = sigmoid(z)
calculate_loss(y,probabilities)




