import json
import os
import pandas as pd
from datetime import datetime
import uuid

FEED_FILE = "data/feed.json"
ANNOTATIONS_FILE = "data/annotations.csv"


def load_feed():
    """Load feed from JSON file"""
    if not os.path.exists(FEED_FILE):
        return []
    with open(FEED_FILE, "r") as f:
        return json.load(f)


def save_feed(feed):
    """Save feed to JSON file"""
    os.makedirs("data", exist_ok=True)
    with open(FEED_FILE, "w") as f:
        json.dump(feed, f, indent=2)


def log_annotation(comment_id, action, comment_text, toxicity_score):
    """Log annotation to CSV"""
    os.makedirs("data", exist_ok=True)
    
    annotation = {
        "comment_id": comment_id,
        "action": action,
        "timestamp": datetime.now().isoformat(),
        "comment_text": comment_text,
        "toxicity_score": toxicity_score
    }
    
    df = pd.DataFrame([annotation])
    
    if os.path.exists(ANNOTATIONS_FILE):
        df.to_csv(ANNOTATIONS_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(ANNOTATIONS_FILE, index=False)


async def get_feed():
    """Get the entire feed"""
    return load_feed()


async def create_post(username: str, caption: str, image_url: str = None):
    """Create a new post and add it to the feed"""
    feed = load_feed()
    
    # Generate post ID
    post_id = str(uuid.uuid4())
    
    # Import here to avoid circular imports
    from api.predict import predict_post
    
    # Predict toxicity for the post
    prediction = await predict_post(caption, image_url or "")
    
    post = {
        "id": post_id,
        "username": username,
        "caption": caption,
        "image_url": image_url or "https://via.placeholder.com/600x400?text=No+Image",
        "timestamp": datetime.now().isoformat(),
        "likes": 0,
        "image_toxicity_score": prediction.get("image_score", 0.0),
        "text_toxicity_score": prediction.get("text_score", 0.0),
        "fused_toxicity_score": prediction.get("fused_score", 0.0),
        "comments": []
    }
    
    feed.insert(0, post)  # Add to beginning of feed
    save_feed(feed)
    
    return {"success": True, "post": post}


async def add_comment(post_id: str, text: str, username: str = "user"):
    """Add a comment to a post"""
    feed = load_feed()
    
    # Find the post
    post = None
    for p in feed:
        if p.get("id") == post_id:
            post = p
            break
    
    if not post:
        return {"error": "Post not found"}
    
    # Generate comment ID
    comment_id = str(uuid.uuid4())
    
    # Import here to avoid circular imports
    from api.predict import predict_comment
    prediction = await predict_comment(text)
    
    comment = {
        "id": comment_id,
        "text": text,
        "username": username,
        "timestamp": datetime.now().isoformat(),
        "toxicity_score": prediction.get("score", 0.0),
        "top_tokens": prediction.get("top_tokens", []),
        "accepted": False
    }
    
    if "comments" not in post:
        post["comments"] = []
    post["comments"].append(comment)
    
    save_feed(feed)
    
    return {"success": True, "comment": comment}


async def accept_comment(comment_id: str, post_id: str):
    """Accept a comment (mark as safe)"""
    feed = load_feed()
    
    for post in feed:
        if post.get("id") == post_id:
            for comment in post.get("comments", []):
                if comment.get("id") == comment_id:
                    comment["accepted"] = True
                    log_annotation(
                        comment_id,
                        "accept",
                        comment.get("text", ""),
                        comment.get("toxicity_score", 0.0)
                    )
                    save_feed(feed)
                    return {"success": True, "message": "Comment accepted"}
    
    return {"error": "Comment not found"}


async def delete_comment(comment_id: str, post_id: str):
    """Delete a comment from the feed"""
    feed = load_feed()
    
    for post in feed:
        if post.get("id") == post_id:
            comments = post.get("comments", [])
            for i, comment in enumerate(comments):
                if comment.get("id") == comment_id:
                    # Log before deleting
                    log_annotation(
                        comment_id,
                        "delete",
                        comment.get("text", ""),
                        comment.get("toxicity_score", 0.0)
                    )
                    # Remove comment
                    post["comments"] = comments[:i] + comments[i+1:]
                    save_feed(feed)
                    return {"success": True, "message": "Comment deleted"}
    
    return {"error": "Comment not found"}

