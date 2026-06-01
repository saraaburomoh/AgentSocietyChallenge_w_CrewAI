import json
import os

def generate_842_tasks():
    data_dir = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI\data"
    output_tasks = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI\real_tasks_842"
    output_gt = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI\real_groundtruth_842"
    
    os.makedirs(output_tasks, exist_ok=True)
    os.makedirs(output_gt, exist_ok=True)
    
    # 1. Load IDs
    users = set()
    with open(os.path.join(data_dir, "user.json"), 'r', encoding='utf-8') as f:
        for line in f:
            try: users.add(json.loads(line)["user_id"])
            except: pass
            
    items = set()
    with open(os.path.join(data_dir, "item.json"), 'r', encoding='utf-8') as f:
        for line in f:
            try: items.add(json.loads(line)["item_id"])
            except: pass

    # 2. Extract 842 tasks
    count = 0
    with open(os.path.join(data_dir, "review.json"), 'r', encoding='utf-8') as f:
        for line in f:
            try:
                rev = json.loads(line)
                uid = rev.get("user_id")
                iid = rev.get("business_id") or rev.get("item_id")
                
                if uid in users and iid in items:
                    task_id = f"task_{count}"
                    
                    # Task file
                    task_data = {
                        "user_id": uid,
                        "item_id": iid,
                        "description": f"Predict what User {uid} thinks of the restaurant {iid}."
                    }
                    with open(os.path.join(output_tasks, f"{task_id}.json"), 'w', encoding='utf-8') as tf:
                        json.dump(task_data, tf, indent=2)
                        
                    # Ground truth file
                    gt_data = {
                        "stars": float(rev.get("stars", 0)),
                        "review": rev.get("text", "")
                    }
                    with open(os.path.join(output_gt, f"{task_id}.json"), 'w', encoding='utf-8') as gf:
                        json.dump(gt_data, gf, indent=2)
                        
                    count += 1
            except: pass
            
    print(f"Successfully generated {count} tasks and ground truth pairs in real_tasks_842/")

if __name__ == "__main__":
    generate_842_tasks()
