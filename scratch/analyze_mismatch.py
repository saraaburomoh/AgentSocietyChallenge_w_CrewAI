import json
import os

def check_missing():
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
    
    missing_user = 0
    missing_item = 0
    both_missing = 0
    both_match = 0
    total = 0
    
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            total += 1
            rev = json.loads(line)
            u_id = rev["user_id"]
            i_id = rev["item_id"]
            
            u_match = u_id in user_ids
            i_match = i_id in item_ids
            
            if u_match and i_match:
                both_match += 1
            elif not u_match and not i_match:
                both_missing += 1
            elif not u_match:
                missing_user += 1
            else:
                missing_item += 1

    print(f"Total Tasks in test_review_subset.json: {total}")
    print(f"Both Match: {both_match}")
    print(f"Missing User ONLY: {missing_user}")
    print(f"Missing Item ONLY: {missing_item}")
    print(f"Both Missing: {both_missing}")

if __name__ == "__main__":
    check_missing()
