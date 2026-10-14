
import pandas as pd
import numpy as np



# Load dataset
df = pd.read_csv("near_earth_asteroids_2025 (1).csv")

features = [
    "diameter_km",
    "H",
    "rot_per",
    "e",
    "a",
    "i",
    "q",
    "ad",
    "moid_km"
]

target = "pha"

# THIS TO THE NEXT COMMEMENT IS AI GENERATE
df[features] = df[features].apply(
    pd.to_numeric, errors="coerce"
)


df[features] = df[features].replace(
    [np.inf, -np.inf], np.nan
)


print("Missing values before cleaning:")
print(df[features + [target]].isna().sum())


df = df.dropna(subset=[target]).copy()


if df[target].dtype == object:
    labels = df[target].astype(str).str.strip().str.lower()
    label_map = {
        "true": 1,
        "false": 0,
        "1": 1,
        "0": 0
    }
    df[target] = labels.map(label_map)
else:
    df[target] = df[target].astype(int)

# Remove any rows with invalid target labels
df = df[df[target].isin([0, 1])].copy()

# Fill missing feature values with each column's median
df[features] = df[features].fillna(
    df[features].median()
)

# Remove features that are entirely missing
features = [
    col for col in features
    if df[col].notna().any()
]

# Remove rows still missing feature values
df = df.dropna(subset=features).copy()

# Create feature matrix and target vector
x = df[features].to_numpy(dtype=float)
y = df[target].to_numpy(dtype=int)

# Verify the cleaned dataset
print("\nRows remaining:", len(df))
print("Features:", features)
print("Target counts:")
print(pd.Series(y).value_counts().sort_index())

print("NaN in x:", np.isnan(x).any())
print("Infinity in x:", np.isinf(x).any())
print("NaN in y:", np.isnan(y).any())

assert np.isfinite(x).all()
assert set(np.unique(y)).issubset({0, 1})
assert len(x) == len(y)
#any thing past this point is not ai

EPSILON = 1e-15
LEARNING_RATE = .09
EPOCHS = 5000
weights = np.zeros(len(features))
bias = 0

mean = x.mean(axis=0)
std = x.std(axis = 0)
std[std ==0] =1
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

      #if epoch % 1000 ==0:
         #print(f"Epoch {epoch}: Loss = {loss}")
      
      dw = (x_scaled.T @ error)/n
      db = np.mean(error)
      weights = weights - LEARNING_RATE*dw
      bias = bias-LEARNING_RATE*db
      
      

   
   z = x_scaled @ weights+bias
   probabilities = sigmoid(z)

   final_loss = calculate_loss(y, probabilities)
   error = probabilities-y

   dw = (x_scaled.T @ error)/n
   db = np.mean(error)
   gradient_size = np.sqrt(np.sum(dw**2)+db**2)
   print("Final loss:", final_loss)
   print("Final gradient magnitude:", gradient_size)
   print("Final weights:", weights)
   print("Final bias:", bias)
   print(losses[0], losses[99], losses[-1])
   print(len(losses), losses[0], losses[99], losses[-1])
   return weights, bias, losses


      


weights, bias, losses = fit(weights, bias, LEARNING_RATE, EPOCHS, y, x_scaled)

new_asteroid = np.array([
    0.49,   # diameter_km
    20.19,  # H
    4.296,  # rot_per
    0.204,   # e
    1.126,   # a
    6.03,  # i
    .897,   # q
    1.355,   # ad
    5.2      #moid_kn
], dtype=float)


new_x_scaled = (new_asteroid-mean)/std
new_z = new_x_scaled @ weights+bias
new_probabilities = sigmoid(new_z)
   
new_predictions = (new_probabilities >=.5).astype(int)

print(f"Predicted probabilities {new_probabilities}")
print(f"Predicted labels  {new_predictions}")




 






    

