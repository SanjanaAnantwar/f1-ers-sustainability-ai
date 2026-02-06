import pandas as pd
import numpy as np
import joblib
import os
from sklearn.linear_model import LinearRegression

# Create model folder
os.makedirs("model", exist_ok=True)

# Load data
gp = pd.read_csv("GP.csv")

# Engine era: 0 = V8, 1 = Hybrid
gp["engine_era"] = gp["Year"].apply(lambda x: 0 if x < 2014 else 1)

# Simulated values (same as your main.py logic)
np.random.seed(42)

gp["Fuel_Used_kg"] = gp["engine_era"].apply(
    lambda x: np.random.uniform(140, 160) if x == 0 else np.random.uniform(85, 105)
)

gp["ERS_Energy_Recovered_MJ"] = gp["engine_era"].apply(
    lambda x: 0 if x == 0 else np.random.uniform(1.5, 4.0)
)

# Efficiency score
gp["Efficiency_Score"] = gp["ERS_Energy_Recovered_MJ"] / gp["Fuel_Used_kg"]

# ML Model
X = gp[["Fuel_Used_kg", "ERS_Energy_Recovered_MJ"]]
y = gp["Efficiency_Score"]

model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "model/efficiency_model.pkl")

print("✅ Efficiency model trained and saved")
