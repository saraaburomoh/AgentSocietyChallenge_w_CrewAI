import json
import os
import glob

def check_official_against_root():
    root_dir = r"c:\Users\MCC\Rag_Crew_Profiler\data"
    review_file = os.path.join(root_dir, "review_subset.json")
    
    unique_users = set()
    unique_items = set()
    
    if os.path.exists(review_file):
        with open(review_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    rev = json.loads(line)
                    unique_users.add(rev.get("user_id"))
                    unique_items.add(rev.get("item_id"))
                except: pass
    
    official_tasks_dir = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI\example\track1\yelp\tasks"
    task_files = glob.glob(os.path.join(official_tasks_dir, "task_*.json"))
    
    matches = 0
    for tf in task_files:
        with open(tf, 'r', encoding='utf-8') as f:
            task = json.load(f)
            u_id = task.get("user_id")
            i_id = task.get("item_id")
            if u_id in unique_users and i_id in unique_items:
                matches += 1
                
    print(f"Official Tasks (400) Matching Root Reviews: {matches}")

if __name__ == "__main__":
    check_official_against_root()
