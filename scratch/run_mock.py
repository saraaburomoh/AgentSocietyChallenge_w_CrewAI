import os
import subprocess
import sys

os.environ["PYTHONIOENCODING"] = "utf-8"
print("Running mock pipeline...")
try:
    proc = subprocess.run(
        [sys.executable, "run_pipeline.py", "--mock", "--tasks", "1"],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    print("STDOUT:")
    print(proc.stdout)
    print("STDERR:")
    print(proc.stderr)
except Exception as e:
    print(f"Error: {e}")
