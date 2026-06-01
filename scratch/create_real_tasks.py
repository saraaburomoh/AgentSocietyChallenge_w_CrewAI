import json
import os

def create_real_tasks():
    # Use the root data folder which has more users (38 instead of 7)
    source_data_dir = r"c:\Users\MCC\Rag_Crew_Profiler\data"
    project_data_dir = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI\data"
    project_dir = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI"
    
    # 1. Load all available users from the root subset
    user_ids = set()
    print(f">>> Loading users from {os.path.join(source_data_dir, 'user_subset.json')}")
    with open(os.path.join(source_data_dir, "user_subset.json"), 'r', encoding='utf-8') as f:
        for line in f:
            try: user_ids.add(json.loads(line)["user_id"])
            except: pass
            
    # 2. Load all available items from the root subset
    item_ids = set()
    print(f">>> Loading items from {os.path.join(source_data_dir, 'item_subset.json')}")
    with open(os.path.join(source_data_dir, "item_subset.json"), 'r', encoding='utf-8') as f:
        for line in f:
            try: item_ids.add(json.loads(line)["item_id"])
            except: pass

    # 3. Load all available reviews from the root subset (for historical context)
    print(f">>> Copying users, items, and reviews to project data folder...")
    for filename, source_name in [("user.json", "user_subset.json"), ("item.json", "item_subset.json"), ("review.json", "review_subset.json")]:
        with open(os.path.join(source_data_dir, source_name), 'r', encoding='utf-8') as src:
            with open(os.path.join(project_data_dir, filename), 'w', encoding='utf-8') as dst:
                dst.write(src.read())

    # 4. Find all tasks that have matching data
    test_file = os.path.join(project_data_dir, "test_review_subset.json")
    matches = []
    print(f">>> Matching tasks against available data...")
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            rev = json.loads(line)
            if rev["user_id"] in user_ids or rev["item_id"] in item_ids:
                matches.append(rev)

    # 5. Create task files
    print(f">>> Creating {len(matches)} task files in real_tasks/...")
    os.makedirs(os.path.join(project_dir, "real_tasks"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "real_groundtruth"), exist_ok=True)
    
    for i, match in enumerate(matches):
        task = {
            "type": "user_behavior_simulation",
            "description": f"Simulate the review for user {match['user_id']} on business {match['item_id']}.",
            "user_id": match["user_id"],
            "item_id": match["item_id"]
        }
        with open(os.path.join(project_dir, f"real_tasks/task_{i}.json"), 'w', encoding='utf-8') as f:
            json.dump(task, f, indent=2)
            
        gt = {
            "stars": match["stars"],
            "review": match["text"]
        }
        with open(os.path.join(project_dir, f"real_groundtruth/groundtruth_{i}.json"), 'w', encoding='utf-8') as f:
            json.dump(gt, f, indent=2)
            
    print(f"\n>>> SUCCESS: Created {len(matches)} real tasks! <<<")

if __name__ == "__main__":
    create_real_tasks()
