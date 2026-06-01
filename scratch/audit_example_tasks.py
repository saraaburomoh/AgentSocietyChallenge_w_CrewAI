import json
import os

def audit_tasks():
    data_dir = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI\data"
    tasks_dir = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI\example\track1\yelp\tasks"
    
    # 1. Load available IDs from your current data folder
    available_users = set()
    with open(os.path.join(data_dir, "user.json"), 'r', encoding='utf-8') as f:
        for line in f:
            try: available_users.add(json.loads(line)["user_id"])
            except: pass
            
    available_items = set()
    with open(os.path.join(data_dir, "item.json"), 'r', encoding='utf-8') as f:
        for line in f:
            try: available_items.add(json.loads(line)["item_id"])
            except: pass

    print(f">>> Your current data has: {len(available_users)} users and {len(available_items)} items.")

    # 2. Check all 400 tasks
    matching_tasks = []
    task_files = [f for f in os.listdir(tasks_dir) if f.endswith(".json")]
    
    for task_file in task_files:
        with open(os.path.join(tasks_dir, task_file), 'r', encoding='utf-8') as f:
            task = json.load(f)
            uid = task.get("user_id")
            iid = task.get("item_id")
            
            if uid in available_users and iid in available_items:
                matching_tasks.append(task_file)

    print(f"\n>>> AUDIT RESULT <<<")
    print(f"Total tasks checked: {len(task_files)}")
    print(f"Tasks that MATCH your current data: {len(matching_tasks)}")
    
    if matching_tasks:
        print(f"Matching file names: {matching_tasks[:10]}...")
    else:
        print("No matches found in the example folder.")

if __name__ == "__main__":
    audit_tasks()
