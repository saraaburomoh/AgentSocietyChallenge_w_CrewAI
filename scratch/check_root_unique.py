import json
import os

def check_root_data():
    root_dir = r"c:\Users\MCC\Rag_Crew_Profiler\data"
    review_file = os.path.join(root_dir, "review_subset.json")
    
    unique_users = set()
    unique_items = set()
    total_reviews = 0
    
    if os.path.exists(review_file):
        with open(review_file, 'r', encoding='utf-8') as f:
            for line in f:
                total_reviews += 1
                try:
                    rev = json.loads(line)
                    unique_users.add(rev.get("user_id"))
                    unique_items.add(rev.get("item_id"))
                except: pass
        
        print(f"Root Review File: {total_reviews} reviews")
        print(f"Unique Users in reviews: {len(unique_users)}")
        print(f"Unique Items in reviews: {len(unique_items)}")
    else:
        print("Root review_subset.json not found.")

if __name__ == "__main__":
    check_root_data()
