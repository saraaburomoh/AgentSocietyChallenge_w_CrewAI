import json
import os

def find_matches():
    data_dir = r"c:\Users\MCC\Rag_Crew_Profiler\AgentSocietyChallenge_w_CrewAI\data"
    
    user_ids = set()
    with open(os.path.join(data_dir, "user.json"), 'r', encoding='utf-8') as f:
        for line in f:
            try: user_ids.add(json.loads(line)["user_id"])
            except: pass
            
    item_ids = set()
    with open(os.path.join(data_dir, "item.json"), 'r', encoding='utf-8') as f:
        for line in f:
            try: item_ids.add(json.loads(line)["item_id"])
            except: pass

    test_file = os.path.join(data_dir, "test_review_subset.json")
    
    matches = []
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            rev = json.loads(line)
            if rev["user_id"] in user_ids and rev["item_id"] in item_ids:
                matches.append(rev)

    print(json.dumps(matches, indent=2))

if __name__ == "__main__":
    find_matches()
