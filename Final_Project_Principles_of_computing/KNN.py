
import pandas as pd
import numpy as np



# Load dataset
df = pd.read_csv("near_earth_asteroids_2025 (1).csv")
#all ai
features = [
    "diameter_km",
    "H",
    "e",
    "q",
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

new_asteroid = np.array([
    0.49,   # diameter_km
    20.19,  # H
    0.204,   # e
    .897,   # q
    5.2      #moid_kn
], dtype=float)


mean = x.mean(axis=0)
std = x.std(axis = 0)
std[std ==0] =1
x_scaled = (x-mean)/std
def predict(new_asteriod):
    new_asteriod = np.asarray(new_asteriod, dtype=float).reshape(-1)

    if len(new_asteriod) != len(features):
        raise ValueError(f"Expected {len(features)} features.")

    new_scaled = (new_asteriod - mean) / std

    k = 15
    matches = []

    for index, row in enumerate(x_scaled):
        distance = np.sqrt(np.sum((row - new_scaled) ** 2))
        matches.append((distance, y[index]))

    matches.sort(key=lambda item: item[0])
    nearest = matches[:k]

    nearest_labels = [label for distance, label in nearest]

    pha_0 = nearest_labels.count(0)
    pha_1 = nearest_labels.count(1)

    print("PHA=0:", pha_0)
    print("PHA=1:", pha_1)

    prediction = 1 if pha_1 > pha_0 else 0

    print("Prediction:", prediction)
    return prediction

   
    

    


