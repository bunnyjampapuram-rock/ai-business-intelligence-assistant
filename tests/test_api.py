import requests


# ============================================================
# PRODUCTION API
# ============================================================

BASE_URL = "https://ai-business-intelligence-assistant-kx4k.onrender.com"


# ============================================================
# TEST 1 — HOME
# ============================================================

def test_home():

    response = requests.get(
        f"{BASE_URL}/",
        timeout=60
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "AI BI Sales Forecasting API is running"
    assert data["model"] == "AI_BI_Sales_Forecasting_Model"
    assert data["version"] == "1"


# ============================================================
# TEST 2 — HEALTH
# ============================================================

def test_health():

    response = requests.get(
        f"{BASE_URL}/health",
        timeout=60
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["model"] == "AI_BI_Sales_Forecasting_Model"
    assert data["version"] == "1"


# ============================================================
# TEST 3 — PREDICTION
# ============================================================

def test_prediction():

    payload = {

        "store_nbr": 1,
        "family": 3,
        "onpromotion": 11,
        "is_weekend": 0,

        "city": 18,
        "state": 12,
        "store_type": 3,
        "cluster": 13,

        "dcoilwtico": 47.57,
        "oil_roll_7": 48.35714285714285,
        "oil_fwd_1": 46.8,
        "oil_fwd_3": 48.59,
        "oil_fwd_7": 47.65,

        "is_holiday": 0,
        "day": 15,
        "day_of_week": 1,
        "is_payday": 1,

        "sale_lag_21": 2438.0,
        "sale_lag_28": 2589.0,
        "sale_roll_7_21": 2158.8571428571427,
        "promo_roll_3": 7.0
    }


    response = requests.post(
        f"{BASE_URL}/predict",
        json=payload,
        timeout=60
    )


    assert response.status_code == 200


    data = response.json()


    assert "predicted_sales" in data


    assert isinstance(
        data["predicted_sales"],
        (int, float)
    )


    assert data["predicted_sales"] >= 0