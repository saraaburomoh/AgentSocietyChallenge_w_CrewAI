import json
import os

def surgical_extraction():
    # Paths
    base_dir = r"c:\Users\MCC\Rag_Crew_Profiler"
    project_dir = os.path.join(base_dir, "AgentSocietyChallenge_w_CrewAI")
    source_data_dir = os.path.join(base_dir, "data") # The 5GB folder
    target_data_dir = os.path.join(project_dir, "data")
    
    # 1. Get IDs from the 41-task seed file
    seed_file = os.path.join(target_data_dir, "test_review_subset.json")
    target_user_ids = set()
    target_item_ids = set()
    all_tasks = []
    
    print(f">>> Reading seed file: {seed_file}")
    with open(seed_file, 'r', encoding='utf-8') as f:
        for line in f:
            rev = json.loads(line)
            target_user_ids.add(rev["user_id"])
            target_item_ids.add(rev["item_id"])
            all_tasks.append(rev)
    
    print(f">>> Found {len(target_user_ids)} unique users and {len(target_item_ids)} unique items in 41 tasks.")

    # 2. Extract Users
    print(">>> Extracting Users from 5GB source...")
    found_users = []
    with open(os.path.join(source_data_dir, "user.json"), 'r', encoding='utf-8') as f:
        for line in f:
            u = json.loads(line)
            if u["user_id"] in target_user_ids:
                found_users.append(u)
    
    with open(os.path.join(target_data_dir, "user.json"), 'w', encoding='utf-8') as f:
        for u in found_users:
            f.write(json.dumps(u) + "\n")
    print(f"    - Saved {len(found_users)} user profiles.")

    # 3. Extract Items
    print(">>> Extracting Items from 5GB source...")
    found_items = []
    with open(os.path.join(source_data_dir, "item.json"), 'r', encoding='utf-8') as f:
        for line in f:
            i = json.loads(line)
            if i["item_id"] in target_item_ids:
                found_items.append(i)
    
    with open(os.path.join(target_data_dir, "item.json"), 'w', encoding='utf-8') as f:
        for i in found_items:
            f.write(json.dumps(i) + "\n")
    print(f"    - Saved {len(found_items)} item profiles.")

    # 4. Extract Reviews (The most data intensive part)
    print(">>> Extracting Reviews from 5GB source (this may take a minute)...")
    found_reviews = []
    with open(os.path.join(source_data_dir, "review.json"), 'r', encoding='utf-8') as f:
        for line in f:
            r = json.loads(line)
            # Match if it's written BY one of our users OR ABOUT one of our items
            if r["user_id"] in target_user_ids or r["item_id"] in target_item_ids:
                found_reviews.append(r)
    
    with open(os.path.join(target_data_dir, "review.json"), 'w', encoding='utf-8') as f:
        for r in found_reviews:
            f.write(json.dumps(r) + "\n")
    print(f"    - Saved {len(found_reviews)} reviews.")

    # 5. Create Task and Groundtruth files
    print(">>> Creating 41 task/groundtruth pairs...")
    os.makedirs(os.path.join(project_dir, "real_tasks"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "real_groundtruth"), exist_ok=True)
    
    for i, task_data in enumerate(all_tasks):
        # Task file
        task_json = {
            "type": "user_behavior_simulation",
            "description": f"Simulate the review for user {task_data['user_id']} on business {task_data['item_id']}.",
            "user_id": task_data["user_id"],
            "item_id": task_data["item_id"]
        }
        with open(os.path.join(project_dir, f"real_tasks/task_{i}.json"), 'w', encoding='utf-8') as f:
            json.dump(task_json, f, indent=2)
            
        # Groundtruth file
        gt_json = {
            "stars": task_data["stars"],
            "review": task_data["text"]
        }
        with open(os.path.join(project_dir, f"real_groundtruth/groundtruth_{i}.json"), 'w', encoding='utf-8') as f:
            json.dump(gt_json, f, indent=2)

    print("\n>>> EXTRACTION COMPLETE! <<<")
    print(f"Summary: 41 Tasks, {len(found_users)} Users, {len(found_items)} Items, {len(found_reviews)} Reviews.")

if __name__ == "__main__":
    surgical_extraction()
