import math 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('dragon_train.csv')
print(df.info())


EPSILON = 1e-15
LEARNING_RATE= .6
EPOCHS = 5000
weights = np.zeros(6) 
bias = 0
x = df[["nest_temp_c",
        "volcano_distance_km",
        "humidity_pct",
        "moonlight_hours",
        "shell_shimmer",
        "egg_weight_kg"]].values
y = df["label"].values



mean= x.mean(axis=0)
devation = x.std(axis=0)
x_scaled = (x-mean)/ devation



def sigmoid(z):
    z_clipped = np.clip(z, -500, 500)
    return 1/(1+np.exp(-z_clipped,))

#log  loss?/BCE
def  calculate_loss(y,probabilities):
    n = len(y)
    p_clipped = np.clip(probabilities,EPSILON, 1-EPSILON , out = None)
    loss = (-1/n) * np.sum(y*np.log(p_clipped) + (1-y) * np.log(1-p_clipped))
    return loss
    



#Gradient Descent 
def fit(weights, bias, LEARNING_RATE, EPOCHS, y,x_scaled):
    losses = []
    for epoch in range(EPOCHS):
        z = x_scaled @ weights+bias
        probabilities = sigmoid(z)
        n = len(x_scaled)
        loss = calculate_loss(y, probabilities)
        losses.append(loss)
        error = probabilities-y
        if epoch % 500 == 0:
         print(f"Epoch {epoch}: Loss is currently {loss}")
           
        dw =(1/n)*np.dot(x_scaled.T, error)
        db =(1/n)*np.sum(error)
        weights = weights-LEARNING_RATE*dw
        bias = bias-LEARNING_RATE*db
    #plt.plot(losses)
   # plt.xlabel("Epoch")
   # plt.ylabel("Binary Cross-Entropy Loss")
   # plt.title("Logistic Regression Training")
   # plt.show() 
    z = x_scaled @ weights + bias
    probabilities = sigmoid(z)
    error = probabilities - y

    dw = (1 / len(y)) * (x_scaled.T @ error)
    db = (1 / len(y)) * np.sum(error)

    gradient_size = np.sqrt(np.sum(dw**2) + db**2)

    print("Final loss:", calculate_loss(y, probabilities))
    print("Final gradient magnitude:", gradient_size)
    print("Final weights:", weights)
    print("Final bias:", bias)

    return weights, bias, losses
    
    





weights, bias, losses = fit(weights, bias, LEARNING_RATE, EPOCHS, y,x_scaled)
test_df = pd.read_csv("dragon_test.csv")
x_test = test_df[["nest_temp_c",
        "volcano_distance_km",
        "humidity_pct",
        "moonlight_hours",
        "shell_shimmer",
        "egg_weight_kg"]].values
y_test= test_df["label"].values
x_test_scaled = (x_test - mean /devation)
z_test = x_test_scaled @ weights+bias 
test_probabilites = sigmoid(z_test)
test_predictions = (test_probabilites >= .5).astype(int)
print(f"Predicted probabilities {test_probabilites}")
print(f"Predicted labels  {test_predictions}")
test_loss = calculate_loss(y_test, test_probabilites)
test_accuracy = np.mean(test_predictions == y_test)
print(f"test loss: {test_loss}")
print(f"test accuracy: {test_accuracy:.2%}")
 
                 















