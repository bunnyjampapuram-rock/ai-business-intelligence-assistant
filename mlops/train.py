import pandas as pd
import mlflow
import mlflow.xgboost
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


# Remove columns that should NOT be used for training
DROP_COLUMNS = [
    "sales",
    "date",
    "Unnamed: 0"
]

X = df.drop(columns=DROP_COLUMNS)
y = df["sales"]


# ============================================================
# 3. TIME-BASED TRAIN / TEST SPLIT
# ============================================================

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))


# ============================================================
# 4. CREATE XGBOOST MODEL
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


# ============================================================
# 5. START MLFLOW RUN
# ============================================================

mlflow.set_tracking_uri("sqlite:///mlflow.db")

mlflow.set_experiment("AI_BI_Sales_Forecasting")

with mlflow.start_run():

    # --------------------------------------------------------
    # Log parameters
    # --------------------------------------------------------

    mlflow.log_param("model", "XGBRegressor")
    mlflow.log_param("n_estimators", 500)
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("max_depth", 8)
    mlflow.log_param("train_rows", len(X_train))
    mlflow.log_param("test_rows", len(X_test))


    # --------------------------------------------------------
    # Train model
    # --------------------------------------------------------

    print("\nTraining model...")

    model.fit(X_train, y_train)

    print("Training completed")


    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    predictions = model.predict(X_test)


    # --------------------------------------------------------
    # Evaluation
    # --------------------------------------------------------

    mae = mean_absolute_error(y_test, predictions)

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )


    print("\nMODEL RESULTS")
    print("----------------------")
    print("MAE :", mae)
    print("RMSE:", rmse)
    print("R2  :", r2)


    # --------------------------------------------------------
    # Log metrics to MLflow
    # --------------------------------------------------------

    mlflow.log_metric("mae", mae)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)


    # --------------------------------------------------------
    # Save model to MLflow
    # --------------------------------------------------------

    mlflow.xgboost.log_model(
        model,
        artifact_path="sales_forecasting_model"
    )


    print("\nMLflow run completed successfully.")