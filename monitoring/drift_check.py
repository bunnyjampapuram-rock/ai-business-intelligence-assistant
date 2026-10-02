import pandas as pd
import json
from datetime import datetime
from scipy.stats import ks_2samp


# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = "data/train_cleaned.csv"

DRIFT_THRESHOLD = 0.05

REPORT_PATH = "monitoring/drift_report.json"


# ============================================================
# LOAD DATA
# ============================================================

print("Loading data...")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print("Shape:", df.shape)


# ============================================================
# SORT DATA BY DATE
# ============================================================

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date")


# ============================================================
# CREATE REFERENCE AND CURRENT DATA
# ============================================================

split_index = int(len(df) * 0.8)

reference_data = df.iloc[:split_index].copy()
current_data = df.iloc[split_index:].copy()

print("\nReference rows:", len(reference_data))
print("Current rows:", len(current_data))


# ============================================================
# FEATURES TO MONITOR
# ============================================================

FEATURES = [
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


# ============================================================
# DRIFT DETECTION
# ============================================================

print("\n================================")
print("MODEL DRIFT CHECK")
print("================================")


drift_detected = False

results = []


for feature in FEATURES:

    reference_values = reference_data[feature].dropna()
    current_values = current_data[feature].dropna()

    statistic, p_value = ks_2samp(
        reference_values,
        current_values
    )

    is_drift = p_value < DRIFT_THRESHOLD

    if is_drift:
        status = "DRIFT"
        drift_detected = True
    else:
        status = "NO_DRIFT"

    print(f"\nFeature: {feature}")
    print(f"KS Statistic: {statistic:.4f}")
    print(f"P-Value: {p_value:.6f}")
    print(f"STATUS: {status}")

    results.append({
        "feature": feature,
        "ks_statistic": round(float(statistic), 6),
        "p_value": round(float(p_value), 6),
        "status": status
    })


# ============================================================
# OVERALL STATUS
# ============================================================

if drift_detected:
    overall_status = "DRIFT_DETECTED"
else:
    overall_status = "NO_DRIFT"


# ============================================================
# CREATE DRIFT REPORT
# ============================================================

report = {

    "timestamp": datetime.now().isoformat(),

    "reference_rows": len(reference_data),

    "current_rows": len(current_data),

    "drift_threshold": DRIFT_THRESHOLD,

    "overall_status": overall_status,

    "features": results
}


# ============================================================
# SAVE REPORT
# ============================================================

with open(REPORT_PATH, "w") as file:

    json.dump(
        report,
        file,
        indent=4
    )


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n================================")

print("DRIFT MONITORING COMPLETED")

print("Overall Status:", overall_status)

print("Report saved to:", REPORT_PATH)

print("================================")