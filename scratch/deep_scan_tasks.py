import json
import os

def find_extra_tasks():
    data_dir = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI\data"
    review_file = os.path.join(data_dir, "review.json")
    user_file = os.path.join(data_dir, "user.json")
    item_file = os.path.join(data_dir, "item.json")
    
    # 1. Load IDs
    users = set()
    with open(user_file, 'r', encoding='utf-8') as f:
        for line in f:
            try: users.add(json.loads(line)["user_id"])
            except: pass
            
    items = set()
    with open(item_file, 'r', encoding='utf-8') as f:
        for line in f:
            try: items.add(json.loads(line)["item_id"])
            except: pass
            
    print(f"Loaded {len(users)} users and {len(items)} items from subset.")

    # 2. Find matches in review.json
    found_tasks = []
    if os.path.exists(review_file):
        with open(review_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    rev = json.loads(line)
                    uid = rev.get("user_id")
                    iid = rev.get("business_id") or rev.get("item_id")
                    
                    if uid in users and iid in items:
                        found_tasks.append({
                            "user_id": uid,
                            "item_id": iid,
                            "ground_truth": {
                                "stars": rev.get("stars"),
                                "review": rev.get("text", "")[:100] + "..."
                            }
                        })
                except: pass
    
    print(f"\n>>> SCAN RESULT <<<")
    print(f"Total valid tasks found in your data folder: {len(found_tasks)}")
    
    if found_tasks:
        print(f"First 5 tasks: {found_tasks[:5]}")
    
if __name__ == "__main__":
    find_extra_tasks()
