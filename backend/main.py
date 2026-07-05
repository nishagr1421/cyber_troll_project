from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional, List
import json
import os
from datetime import datetime
import pandas as pd
from pathlib import Path

from api.predict import predict_post, predict_comment
from api.feed import get_feed, add_comment, accept_comment, delete_comment, create_post

app = FastAPI(title="InstaGuard API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure data directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:8000"
)

FEED_FILE = "data/feed.json"
ANNOTATIONS_FILE = "data/annotations.csv"

# Initialize feed if it doesn't exist
if not os.path.exists(FEED_FILE):
    with open(FEED_FILE, "w") as f:
        json.dump([], f)

# Initialize annotations CSV if it doesn't exist
if not os.path.exists(ANNOTATIONS_FILE):
    pd.DataFrame(columns=["comment_id", "action", "timestamp", "comment_text", "toxicity_score"]).to_csv(
        ANNOTATIONS_FILE, index=False
    )


@app.get("/")
async def root():
    return {"message": "InstaGuard API is running"}


# Serve uploaded images
@app.get("/uploads/{filename:path}")
async def serve_upload(filename: str):
    """Serve uploaded images"""
    import urllib.parse
    # URL decode the filename
    decoded_filename = urllib.parse.unquote(filename)
    file_path = os.path.join(UPLOAD_DIR, decoded_filename)
    
    # If exact match not found, try to find file with similar name
    if not os.path.exists(file_path):
        # List all files and try to match
        try:
            all_files = os.listdir(UPLOAD_DIR)
            # Remove special chars for comparison
            search_name = decoded_filename.replace(' ', '').replace('\u202f', '')
            for f in all_files:
                if f.replace(' ', '').replace('\u202f', '') == search_name:
                    file_path = os.path.join(UPLOAD_DIR, f)
                    break
        except:
            pass
    
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    raise HTTPException(status_code=404, detail=f"Image not found: {decoded_filename}")


@app.post("/api/predict")
async def predict_post_endpoint(
    caption: str = Form(...),
    image: UploadFile = File(None)
):
    """Predict toxicity for a post (caption + image)"""
    try:
        from api.predict import predict_post
        
        image_path = None
        if image:
            # Save uploaded image temporarily
            image_path = f"data/temp_{image.filename}"
            os.makedirs("data", exist_ok=True)
            with open(image_path, "wb") as f:
                content = await image.read()
                f.write(content)
        
        result = await predict_post(caption, image_path or "")
        
        # Clean up temp file
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/comment/predict")
async def predict_comment_endpoint(comment: dict):
    """Predict toxicity for a comment"""
    try:
        comment_text = comment.get("text", "")
        if not comment_text:
            raise HTTPException(status_code=400, detail="Comment text is required")
        
        from api.predict import predict_comment as predict_comment_func
        result = await predict_comment_func(comment_text)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/feed")
async def get_feed_endpoint():
    """Get the feed with all posts and comments"""
    try:
        feed = await get_feed()
        return JSONResponse(content=feed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/post/create")
async def create_post_endpoint(
    username: str = Form("user"),
    caption: str = Form(...),
    image: UploadFile = File(None)
):
    """Create a new post with caption and optional image"""
    try:
        image_url = None
        if image:
            # Save uploaded image
            image_filename = f"{datetime.now().timestamp()}_{image.filename}"
            image_path = f"data/uploads/{image_filename}"
            os.makedirs("data/uploads", exist_ok=True)
            
            with open(image_path, "wb") as f:
                content = await image.read()
                f.write(content)
            
            # Use backend server URL for image (served as static file)
            #image_url = f"http://localhost:8000/uploads/{image_filename}"
            image_url = f"{BACKEND_URL}/uploads/{image_filename}"
        
        result = await create_post(username, caption, image_url)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/comment/add")
async def add_comment_endpoint(comment_data: dict):
    """Add a new comment to a post"""
    try:
        result = await add_comment(
            post_id=comment_data.get("post_id"),
            text=comment_data.get("text"),
            username=comment_data.get("username", "user")
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/comment/accept")
async def accept_comment_endpoint(comment_data: dict):
    """Accept a comment (mark as safe)"""
    try:
        result = await accept_comment(
            comment_id=comment_data.get("comment_id"),
            post_id=comment_data.get("post_id")
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/comment/delete")
async def delete_comment_endpoint(comment_data: dict):
    """Delete a comment from the feed"""
    try:
        result = await delete_comment(
            comment_id=comment_data.get("comment_id"),
            post_id=comment_data.get("post_id")
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

