import joblib
import pandas as pd
import numpy as np


# ============================================================
# 1. LOAD MODEL
# ============================================================

model = joblib.load("models/xgb_model.pkl")


# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv("data/train_cleaned.csv")

df["date"] = pd.to_datetime(df["date"])


# ============================================================
# 3. FAMILY MAPPING
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
# 4. FORECAST FUNCTION
# ============================================================

def forecast_sales(store_number, family_name, forecast_date):

    # --------------------------------------------------------
    # Convert date
    # --------------------------------------------------------

    forecast_date = pd.to_datetime(forecast_date)

    # --------------------------------------------------------
    # Convert family name to number
    # --------------------------------------------------------

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

    print("\nDate features:")
    print("Day:", forecast_row["day"])
    print("Day of week:", forecast_row["day_of_week"])
    print("Is weekend:", forecast_row["is_weekend"])
    print("Is payday:", forecast_row["is_payday"])

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

    print("\nLag 21 date:", lag_21_date)
    print("Sale lag 21:", sale_lag_21)

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

    print("\nLag 28 date:", lag_28_date)
    print("Sale lag 28:", sale_lag_28)

    # ========================================================
    # ROLLING SALES: sale_roll_7_21
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

    print("\nRolling sales:")
    print("Rolling start:", roll_start)
    print("Rolling end:", roll_end)
    print("Rolling rows:", len(rolling_sales))
    print("Sale roll 7 21:", sale_roll_7_21)

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

    print("\nPromotion:")
    print("On promotion:", onpromotion)

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

    print("Promo roll 3:", promo_roll_3)

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
    # GET EXACT MODEL FEATURES
    # ========================================================

    features = model.feature_names_in_

    X_forecast = forecast_df[features]

    # ========================================================
    # HANDLE MISSING VALUES
    # ========================================================

    X_forecast = X_forecast.fillna(0)

    # ========================================================
    # DISPLAY FEATURES
    # ========================================================

    print("\n==============================")
    print("FINAL MODEL INPUT")
    print("==============================")

    print(X_forecast)

    # ========================================================
    # PREDICTION
    # ========================================================
    prediction = model.predict(X_forecast)

    # Convert prediction from log scale
    # back to original sales scale
    predicted_sales = np.expm1(prediction[0])

    print("\n==============================")
    print("PREDICTION")
    print("==============================")

    print("Log prediction:", prediction[0])
    print("Predicted sales:", predicted_sales)

    return predicted_sales