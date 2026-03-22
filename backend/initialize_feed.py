"""
Initialize feed.json from sample_feed.json
"""
import json
import os
import shutil

def initialize_feed():
    """Copy sample_feed.json to data/feed.json"""
    os.makedirs("data", exist_ok=True)
    
    # Try to find sample_feed.json in parent directory
    sample_feed = os.path.join("..", "sample_feed.json")
    if not os.path.exists(sample_feed):
        sample_feed = "sample_feed.json"
    
    feed_file = "data/feed.json"
    
    if os.path.exists(sample_feed):
        shutil.copy(sample_feed, feed_file)
        print(f"Initialized feed from {sample_feed}")
    else:
        # Create empty feed
        with open(feed_file, "w") as f:
            json.dump([], f)
        print("Created empty feed.json")

if __name__ == "__main__":
    initialize_feed()

