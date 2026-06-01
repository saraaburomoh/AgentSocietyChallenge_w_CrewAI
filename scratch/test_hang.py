import os
import subprocess
import sys

env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"

print("Running pipeline for 20 seconds to trace hang...")
with open("scratch/trace.log", "w", encoding="utf-8") as f:
    try:
        subprocess.run(
            [sys.executable, "run_pipeline.py", "--mock", "--tasks", "1"],
            stdout=f,
            stderr=subprocess.STDOUT,
            timeout=20,
            encoding="utf-8",
            env=env
        )
    except subprocess.TimeoutExpired:
        print("Timed out after 20 seconds as planned.")
print("Done.")
