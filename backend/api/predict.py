import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infer_text import predict_text_toxicity
from infer_image import predict_image_toxicity
import numpy as np


async def predict_post(caption: str, image_path: str):
    """
    Predict toxicity for a post combining text and image
    Returns: {text_score, text_labels, image_score, fused_score, tokens_flagged}
    """
    try:
        # Predict text toxicity
        text_result = predict_text_toxicity(caption)
        text_score = text_result.get("score", 0.0)
        text_labels = text_result.get("labels", {})
        tokens_flagged = text_result.get("top_tokens", [])
        
        # Predict image toxicity (if image provided)
        image_score = 0.0
        if image_path and image_path.startswith("http://localhost:8000/uploads/"):
            # Extract filename from URL
            filename = image_path.split("/uploads/")[-1]
            local_image_path = f"data/uploads/{filename}"
            if os.path.exists(local_image_path):
                image_result = predict_image_toxicity(local_image_path)
                image_score = image_result.get("score", 0.0)
        elif image_path and os.path.exists(image_path):
            image_result = predict_image_toxicity(image_path)
            image_score = image_result.get("score", 0.0)
        
        # Fused score (average if image exists, otherwise just text)
        if image_score > 0:
            fused_score = (text_score + image_score) / 2.0
        else:
            fused_score = text_score
        
        return {
            "text_score": float(text_score),
            "text_labels": text_labels,
            "image_score": float(image_score),
            "fused_score": float(fused_score),
            "tokens_flagged": tokens_flagged
        }
    except Exception as e:
        # Fallback if models not loaded
        return {
            "text_score": 0.0,
            "text_labels": {"toxic": 0.0, "non-toxic": 1.0},
            "image_score": 0.0,
            "fused_score": 0.0,
            "tokens_flagged": []
        }


async def predict_comment(comment_text: str):
    """
    Predict toxicity for a comment
    Returns: {score, top_tokens}
    """
    try:
        result = predict_text_toxicity(comment_text)
        return {
            "score": float(result.get("score", 0.0)),
            "top_tokens": result.get("top_tokens", [])
        }
    except Exception as e:
        # Fallback
        return {
            "score": 0.0,
            "top_tokens": []
        }

