import json
import os

def create_week11_tasks():
    # Use the week11_data folder
    project_dir = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI"
    week11_data_dir = os.path.join(project_dir, "week11_data")
    week11_tasks_dir = os.path.join(project_dir, "week11_tasks")
    week11_gt_dir = os.path.join(project_dir, "week11_groundtruth")
    
    # 1. Load all available users and items from our new folder
    user_ids = set()
    with open(os.path.join(week11_data_dir, "user.json"), 'r', encoding='utf-8') as f:
        for line in f:
            try: user_ids.add(json.loads(line)["user_id"])
            except: pass
            
    item_ids = set()
    with open(os.path.join(week11_data_dir, "item.json"), 'r', encoding='utf-8') as f:
        for line in f:
            try: item_ids.add(json.loads(line)["item_id"])
            except: pass

    # 2. Match against the 198-task seed file
    seed_file = os.path.join(project_dir, "data", "test_review_subset.json")
    matches = []
    with open(seed_file, 'r', encoding='utf-8') as f:
        for line in f:
            rev = json.loads(line)
            if rev["user_id"] in user_ids and rev["item_id"] in item_ids:
                matches.append(rev)

    # 3. Create task files
    print(f">>> Creating {len(matches)} task files in week11_tasks/...")
    
    for i, match in enumerate(matches):
        task = {
            "type": "user_behavior_simulation",
            "description": f"Week 11 Evaluation Task: Simulate user {match['user_id']} on item {match['item_id']}.",
            "user_id": match["user_id"],
            "item_id": match["item_id"]
        }
        with open(os.path.join(week11_tasks_dir, f"task_{i}.json"), 'w', encoding='utf-8') as f:
            json.dump(task, f, indent=2)
            
        gt = {
            "stars": match["stars"],
            "review": match["text"]
        }
        with open(os.path.join(week11_gt_dir, f"groundtruth_{i}.json"), 'w', encoding='utf-8') as f:
            json.dump(gt, f, indent=2)
            
    print(f"\n>>> SUCCESS: Created {len(matches)} Week 11 tasks! <<<")

if __name__ == "__main__":
    create_week11_tasks()
