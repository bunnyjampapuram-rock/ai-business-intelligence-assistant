import json
import subprocess
import sys

REPORT_PATH = "monitoring/drift_report.json"

with open(REPORT_PATH, "r") as f:
    report = json.load(f)

status = report["overall_status"]

print("================================")
print("RETRAINING DECISION")
print("================================")

if status == "DRIFT_DETECTED":

    print("DRIFT DETECTED")
    print("Model retraining is required.")
    print("ACTION: RETRAIN")

    result = subprocess.run(
        [sys.executable, "mlops/train.py"],
        check=False
    )

    if result.returncode == 0:
        print("================================")
        print("RETRAINING COMPLETED")
        print("================================")
    else:
        print("================================")
        print("RETRAINING FAILED")
        print("================================")
        sys.exit(1)

else:

    print("NO DRIFT")
    print("Current model can continue serving.")
    print("ACTION: KEEP CURRENT MODEL")