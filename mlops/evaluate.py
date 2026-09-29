import pandas as pd
import joblib
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# 1. LOAD DATA
# ============================================================

DATA_PATH = "data/train_cleaned.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print("Shape:", df.shape)


# ============================================================
# 2. PREPARE DATA
# ============================================================

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date")


DROP_COLUMNS = [
    "sales",
    "date",
    "Unnamed: 0"
]

X = df.drop(columns=DROP_COLUMNS)
y = df["sales"]


# ============================================================
# 3. TIME-BASED TEST SPLIT
# ============================================================

split_index = int(len(df) * 0.8)

X_test = X.iloc[split_index:]
y_test = y.iloc[split_index:]


print("Testing rows:", len(X_test))


# ============================================================
# 4. TRAIN MODEL FOR EVALUATION
# ============================================================

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.01,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42
)


print("\nTraining evaluation model...")

X_train = X.iloc[:split_index]
y_train = y.iloc[:split_index]

model.fit(X_train, y_train)

print("Training completed")


# ============================================================
# 5. PREDICTIONS
# ============================================================

predictions = model.predict(X_test)


# ============================================================
# 6. CALCULATE METRICS
# ============================================================

mae = mean_absolute_error(y_test, predictions)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)


# ============================================================
# 7. PRINT RESULTS
# ============================================================

print("\n================================")
print("MODEL EVALUATION RESULTS")
print("================================")

print(f"MAE  : {mae:.6f}")
print(f"RMSE : {rmse:.6f}")
print(f"R2   : {r2:.6f}")

print("================================")

# ============================================================
# 8. MODEL QUALITY GATE
# ============================================================

MIN_R2 = 0.90

if r2 < MIN_R2:
    print(f"\nMODEL QUALITY CHECK FAILED")
    print(f"R2 {r2:.6f} is below required threshold {MIN_R2}")
    raise SystemExit(1)

print("\nMODEL QUALITY CHECK PASSED")
print(f"R2 {r2:.6f} >= {MIN_R2}")