import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load Dataset
df = pd.read_csv("training_data.csv")

# Features & Target
features = ["ema_5", "ema_10", "rsi", "macd", "bb_high", "bb_low"]
X = df[features]
y = df["target"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost Model
model = xgb.XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.05)
model.fit(X_train, y_train)

# Model Accuracy
y_pred = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# Save Model
joblib.dump(model, "strategy/ml/models/xgboost_model.pkl")
