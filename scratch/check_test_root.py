import json
import os

def check_test_against_root():
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
    
    test_file = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI\data\test_review_subset.json"
    matches = 0
    total = 0
    
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            total += 1
            try:
                rev = json.loads(line)
                u_id = rev.get("user_id")
                i_id = rev.get("item_id")
                if u_id in unique_users and i_id in unique_items:
                    matches += 1
            except: pass
                
    print(f"test_review_subset (198) Matching Root Reviews: {matches} / {total}")

if __name__ == "__main__":
    check_test_against_root()
