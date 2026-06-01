import sys
import os
import logging
import json
import io

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from websocietysimulator import Simulator
from crewai_simulation_agent import CrewAISimulationAgent
from dotenv import load_dotenv

load_dotenv()

# Inject robust LLM retry logic globally to prevent 429 API crashes
os.environ["LITELLM_NUM_RETRIES"] = "5"
os.environ["LITELLM_BACKOFF_FACTOR"] = "3"
os.environ["LITELLM_RETRY_POLICY"] = "exponential_backoff"

logging.basicConfig(level=logging.INFO)

print("\n" + "=" * 60)
print("Starting Real Data Evaluation (Sequential Crew)")
print("=" * 60)

try:
    # 1. 建立 Simulator，使用 Real Dataset
    print(">>> Loading Real Dataset (data folder)...")
    simulator = Simulator(data_dir="data", device="cpu", cache=True)
    simulator.set_task_and_groundtruth(task_dir="real_tasks", groundtruth_dir="real_groundtruth")
    simulator.set_agent(CrewAISimulationAgent)

    # 2. 運行模擬 (Sequential mode to avoid 429 Rate Limits)
    print("\nStarting inference on the first 5 tasks of the 183-task real data subset...")
    outputs = simulator.run_simulation(number_of_tasks=5, enable_threading=False, max_workers=1)

    print("\nSimulation finished, final output:")
    print("-" * 60)
    print(json.dumps(outputs, indent=2, ensure_ascii=False))
    print("-" * 60)

    # 3. 官方評分
    print("\nCalling official evaluation...")
    evaluation_results = simulator.evaluate()
    print("Evaluation results:")
    print(json.dumps(evaluation_results, indent=2, ensure_ascii=False))

    print("\nReal data test completed!")

except Exception as e:
    print(f"\nTest interrupted: {e}")
    import traceback
    traceback.print_exc()
