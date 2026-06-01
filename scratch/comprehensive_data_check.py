import json
import os
import glob

def check_matches(data_dir, label):
    user_ids = set()
    item_ids = set()
    
    # Try different filenames for root vs subfolder
    u_file = "user.json" if os.path.exists(os.path.join(data_dir, "user.json")) else "user_subset.json"
    i_file = "item.json" if os.path.exists(os.path.join(data_dir, "item.json")) else "item_subset.json"
    r_file = "test_review_subset.json" if os.path.exists(os.path.join(data_dir, "test_review_subset.json")) else "review_subset.json"

    try:
        with open(os.path.join(data_dir, u_file), 'r', encoding='utf-8') as f:
            for line in f:
                try: user_ids.add(json.loads(line)["user_id"])
                except: pass
        
        with open(os.path.join(data_dir, i_file), 'r', encoding='utf-8') as f:
            for line in f:
                try: item_ids.add(json.loads(line)["item_id"])
                except: pass
    except Exception as e:
        print(f"Error loading {label} data: {e}")
        return

    print(f"\n[{label}] Users: {len(user_ids)}, Items: {len(item_ids)}")

    # Check Official Tasks
    official_tasks_dir = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI\example\track1\yelp\tasks"
    task_files = glob.glob(os.path.join(official_tasks_dir, "task_*.json"))
    official_matches = 0
    for tf in task_files:
        with open(tf, 'r', encoding='utf-8') as f:
            task = json.load(f)
            if task.get("user_id") in user_ids and task.get("item_id") in item_ids:
                official_matches += 1
    print(f"[{label}] Official Tasks Match: {official_matches} / {len(task_files)}")

    # Check Test Subset
    test_subset_path = os.path.join(data_dir, r_file)
    test_matches = 0
    total_test = 0
    if os.path.exists(test_subset_path):
        with open(test_subset_path, 'r', encoding='utf-8') as f:
            for line in f:
                total_test += 1
                try:
                    rev = json.loads(line)
                    if rev.get("user_id") in user_ids and rev.get("item_id") in item_ids:
                        test_matches += 1
                except: pass
        print(f"[{label}] {r_file} Match: {test_matches} / {total_test}")

if __name__ == "__main__":
    check_matches(r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI\data", "Subfolder Data")
    check_matches(r"c:\Users\MCC\Rag_Crew_Profiler\data", "Root Data")
