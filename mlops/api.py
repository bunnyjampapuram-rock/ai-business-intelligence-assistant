from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import pandas as pd


# =========================================================
# APP CONFIGURATION
# =========================================================

app = FastAPI(
    title="AI BI Sales Forecasting API",
    description="MLOps API for sales forecasting",
    version="1.0"
)


# =========================================================
# MLFLOW CONFIGURATION
# =========================================================

MODEL_PATH = "mlruns/1/models/m-7bb48d02f1b14b9eb2c0c29bfd766a5a/artifacts"

model = mlflow.pyfunc.load_model(MODEL_PATH)

MODEL_NAME = "AI_BI_Sales_Forecasting_Model"
MODEL_VERSION = "1"

# =========================================================
# INPUT SCHEMA
# =========================================================

class SalesPredictionRequest(BaseModel):

    store_nbr: int
    family: int
    onpromotion: int
    is_weekend: int

    city: int
    state: int
    store_type: int
    cluster: int

    dcoilwtico: float
    oil_roll_7: float
    oil_fwd_1: float
    oil_fwd_3: float
    oil_fwd_7: float

    is_holiday: int
    day: int
    day_of_week: int
    is_payday: int

    sale_lag_21: float
    sale_lag_28: float
    sale_roll_7_21: float
    promo_roll_3: float


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "AI BI Sales Forecasting API is running",
        "model": MODEL_NAME,
        "version": MODEL_VERSION
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "version": MODEL_VERSION
    }


# =========================================================
# PREDICTION
# =========================================================

@app.post("/predict")
def predict(request: SalesPredictionRequest):

    input_data = pd.DataFrame([request.model_dump()])

    prediction = model.predict(input_data)

    return {
        "predicted_sales": float(prediction[0])
    }