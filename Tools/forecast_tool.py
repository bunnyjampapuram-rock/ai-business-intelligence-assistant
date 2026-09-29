import pandas as pd
import numpy as np
import requests

# ============================================================
# RENDER FASTAPI URL
# ============================================================

API_URL = "https://ai-business-intelligence-assistant-kx4k.onrender.com/predict"


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("data/train_cleaned.csv")

df["date"] = pd.to_datetime(df["date"])


# ============================================================
# FAMILY MAPPING
# ============================================================

family_mapping = {
    "AUTOMOTIVE": 0,
    "BABY CARE": 1,
    "BEAUTY": 2,
    "BEVERAGES": 3,
    "BOOKS": 4,
    "BREAD/BAKERY": 5,
    "CELEBRATION": 6,
    "CLEANING": 7,
    "DAIRY": 8,
    "DELI": 9,
    "EGGS": 10,
    "FROZEN FOODS": 11,
    "GROCERY I": 12,
    "GROCERY II": 13,
    "HARDWARE": 14,
    "HOME AND KITCHEN I": 15,
    "HOME AND KITCHEN II": 16,
    "HOME APPLIANCES": 17,
    "HOME CARE": 18,
    "LADIESWEAR": 19,
    "LAWN AND GARDEN": 20,
    "LINGERIE": 21,
    "LIQUOR,WINE,BEER": 22,
    "MAGAZINES": 23,
    "MEATS": 24,
    "PERSONAL CARE": 25,
    "PET SUPPLIES": 26,
    "PLAYERS AND ELECTRONICS": 27,
    "POULTRY": 28,
    "PREPARED FOODS": 29,
    "PRODUCE": 30,
    "SCHOOL AND OFFICE SUPPLIES": 31,
    "SEAFOOD": 32
}


# ============================================================
# FORECAST FUNCTION
# ============================================================

def forecast_sales(store_number, family_name, forecast_date):

    # --------------------------------------------------------
    # Convert date
    # --------------------------------------------------------

    forecast_date = pd.to_datetime(forecast_date)

    # --------------------------------------------------------
    # Convert family name to number
    # --------------------------------------------------------

    family_name = str(family_name).upper().strip()

    if family_name not in family_mapping:
        raise ValueError(
            f"Unknown product family: {family_name}"
        )

    family_number = family_mapping[family_name]

    print("\n==============================")
    print("FORECAST REQUEST")
    print("==============================")

    print("Store:", store_number)
    print("Family:", family_name)
    print("Family number:", family_number)
    print("Forecast date:", forecast_date)

    # --------------------------------------------------------
    # Filter history
    # --------------------------------------------------------

    history = df[
        (df["store_nbr"] == store_number) &
        (df["family"] == family_number)
    ].copy()

    history = history.sort_values("date")

    print("History rows:", len(history))

    # ========================================================
    # CREATE FORECAST ROW
    # ========================================================

    forecast_row = {
        "store_nbr": store_number,
        "family": family_number,
        "date": forecast_date
    }

    # ========================================================
    # DATE FEATURES
    # ========================================================

    forecast_row["day"] = forecast_date.day

    forecast_row["day_of_week"] = forecast_date.dayofweek

    forecast_row["is_weekend"] = int(
        forecast_date.dayofweek >= 5
    )

    forecast_row["is_payday"] = int(
        forecast_date.day in [15, 30, 31]
    )

    # ========================================================
    # LAG 21
    # ========================================================

    lag_21_date = forecast_date - pd.Timedelta(days=21)

    lag_21_values = history[
        history["date"] == lag_21_date
    ]["sales"]

    if len(lag_21_values) > 0:
        sale_lag_21 = lag_21_values.iloc[0]
    else:
        sale_lag_21 = 0

    forecast_row["sale_lag_21"] = sale_lag_21

    # ========================================================
    # LAG 28
    # ========================================================

    lag_28_date = forecast_date - pd.Timedelta(days=28)

    lag_28_values = history[
        history["date"] == lag_28_date
    ]["sales"]

    if len(lag_28_values) > 0:
        sale_lag_28 = lag_28_values.iloc[0]
    else:
        sale_lag_28 = 0

    forecast_row["sale_lag_28"] = sale_lag_28

    # ========================================================
    # ROLLING SALES
    # ========================================================

    roll_start = forecast_date - pd.Timedelta(days=27)
    roll_end = forecast_date - pd.Timedelta(days=21)

    rolling_sales = history[
        (history["date"] >= roll_start) &
        (history["date"] <= roll_end)
    ]["sales"]

    if len(rolling_sales) > 0:
        sale_roll_7_21 = rolling_sales.mean()
    else:
        sale_roll_7_21 = 0

    forecast_row["sale_roll_7_21"] = sale_roll_7_21

    # ========================================================
    # PROMOTION
    # ========================================================

    promo_values = df[
        (df["store_nbr"] == store_number) &
        (df["family"] == family_number) &
        (df["date"] == forecast_date)
    ]["onpromotion"]

    if len(promo_values) > 0:
        onpromotion = promo_values.iloc[0]
    else:
        onpromotion = 0

    forecast_row["onpromotion"] = onpromotion

    # ========================================================
    # PROMOTION ROLLING 3 DAYS
    # ========================================================

    promo_start = forecast_date - pd.Timedelta(days=3)
    promo_end = forecast_date - pd.Timedelta(days=1)

    promo_history = history[
        (history["date"] >= promo_start) &
        (history["date"] <= promo_end)
    ]["onpromotion"]

    if len(promo_history) > 0:
        promo_roll_3 = promo_history.mean()
    else:
        promo_roll_3 = 0

    forecast_row["promo_roll_3"] = promo_roll_3

    # ========================================================
    # STORE INFORMATION
    # ========================================================

    store_rows = df[
        df["store_nbr"] == store_number
    ]

    if len(store_rows) > 0:

        store_info = store_rows.iloc[0]

        forecast_row["city"] = store_info["city"]
        forecast_row["state"] = store_info["state"]
        forecast_row["store_type"] = store_info["store_type"]
        forecast_row["cluster"] = store_info["cluster"]

    else:

        forecast_row["city"] = 0
        forecast_row["state"] = 0
        forecast_row["store_type"] = 0
        forecast_row["cluster"] = 0

    # ========================================================
    # OIL FEATURES
    # ========================================================

    oil_row = df[
        df["date"] == forecast_date
    ]

    if len(oil_row) > 0:

        oil_info = oil_row.iloc[0]

        forecast_row["dcoilwtico"] = oil_info["dcoilwtico"]
        forecast_row["oil_roll_7"] = oil_info["oil_roll_7"]
        forecast_row["oil_fwd_1"] = oil_info["oil_fwd_1"]
        forecast_row["oil_fwd_3"] = oil_info["oil_fwd_3"]
        forecast_row["oil_fwd_7"] = oil_info["oil_fwd_7"]

    else:

        forecast_row["dcoilwtico"] = 0
        forecast_row["oil_roll_7"] = 0
        forecast_row["oil_fwd_1"] = 0
        forecast_row["oil_fwd_3"] = 0
        forecast_row["oil_fwd_7"] = 0

    # ========================================================
    # HOLIDAY
    # ========================================================

    holiday_rows = df[
        df["date"] == forecast_date
    ]

    if len(holiday_rows) > 0:

        forecast_row["is_holiday"] = holiday_rows.iloc[0][
            "is_holiday"
        ]

    else:

        forecast_row["is_holiday"] = 0

    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    forecast_df = pd.DataFrame([forecast_row])

    # ========================================================
    # REQUIRED API FEATURES
    # ========================================================

    api_features = [
        "store_nbr",
        "family",
        "onpromotion",
        "is_weekend",
        "city",
        "state",
        "store_type",
        "cluster",
        "dcoilwtico",
        "oil_roll_7",
        "oil_fwd_1",
        "oil_fwd_3",
        "oil_fwd_7",
        "is_holiday",
        "day",
        "day_of_week",
        "is_payday",
        "sale_lag_21",
        "sale_lag_28",
        "sale_roll_7_21",
        "promo_roll_3"
    ]

    X_forecast = forecast_df[api_features].fillna(0)

    # ========================================================
    # CONVERT TO JSON
    # ========================================================

    payload = X_forecast.iloc[0].to_dict()

    # Convert NumPy values into normal Python values
    payload = {
        key: (
            int(value)
            if isinstance(value, (np.integer,))
            else float(value)
            if isinstance(value, (np.floating,))
            else value
        )
        for key, value in payload.items()
    }

    print("\n==============================")
    print("SENDING TO PRODUCTION API")
    print("==============================")

    print(payload)

    # ========================================================
    # CALL RENDER FASTAPI
    # ========================================================

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=60
        )

    except requests.exceptions.RequestException as e:

        raise RuntimeError(
            f"Could not connect to forecasting API: {e}"
        )

    # ========================================================
    # CHECK API RESPONSE
    # ========================================================

    if response.status_code != 200:

        raise RuntimeError(
            f"Forecast API failed. "
            f"Status: {response.status_code}. "
            f"Response: {response.text}"
        )

    result = response.json()

    # ========================================================
    # GET PREDICTION
    # ========================================================

    if "predicted_sales" not in result:

        raise RuntimeError(
            f"API response does not contain predicted_sales: "
            f"{result}"
        )

    predicted_sales = float(
        result["predicted_sales"]
    )

    print("\n==============================")
    print("PRODUCTION PREDICTION")
    print("==============================")

    print(
        "Predicted sales:",
        predicted_sales
    )

    return predicted_sales