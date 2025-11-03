import subprocess
import sys
import os
from datetime import datetime

TESTS = [
    ["python3", "main.py", "stocks", "AAPL", "summary"],
    ["python3", "main.py", "stocks", "MSFT", "chart"],
    ["python3", "main.py", "commodities", "gold", "summary"],
    ["python3", "main.py", "etfs", "SPY", "summary"],
    ["python3", "main.py", "compare", "AAPL,SPY,GLD", "summary"],
]

def run_test(command):
    print(f"\U0001F9EA Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("\u2705 PASS")
        return True
    else:
        print("\u274C FAIL")
        print(result.stderr or result.stdout)
        return False

def main():
    log_path = os.path.join("logs", "test_report.log")
    os.makedirs("logs", exist_ok=True)
    with open(log_path, "a") as log:
        log.write(f"\n==== Test Run {datetime.now()} ====\n")
        passes = 0
        for test in TESTS:
            success = run_test(test)
            log.write(f"{' '.join(test)} - {'PASS' if success else 'FAIL'}\n")
            if success:
                passes += 1
        log.write(f"\n{passes}/{len(TESTS)} passed.\n")
    print(f"\n\U0001F4DD Log saved to {log_path}")

if __name__ == "__main__":
    main()
