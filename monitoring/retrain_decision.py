import json

REPORT_PATH = "monitoring/drift_report.json"

with open(REPORT_PATH, "r") as f:
    report = json.load(f)

status = report["overall_status"]

print("================================")
print("RETRAINING DECISION")
print("================================")

if status == "DRIFT_DETECTED":
    print("DRIFT DETECTED")
    print("Model retraining is recommended.")
    print("ACTION: RETRAIN")
else:
    print("NO DRIFT")
    print("Current model can continue serving.")
    print("ACTION: KEEP CURRENT MODEL")