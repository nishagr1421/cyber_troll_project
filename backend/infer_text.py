"""
Text toxicity inference using DistilBERT or fallback to TF-IDF + LogisticRegression
"""
import os
import pickle
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Try to use DistilBERT, fallback to TF-IDF
USE_TRANSFORMER = True
MODEL_DIR = "models"
TEXT_MODEL_PATH = os.path.join(MODEL_DIR, "text_model.pt")
TFIDF_MODEL_PATH = os.path.join(MODEL_DIR, "text_model_tfidf.pkl")

# Global model variables
text_model = None
text_tokenizer = None
tfidf_model = None
tfidf_vectorizer = None


def load_text_model():
    """Load text model (DistilBERT or TF-IDF fallback)"""
    global text_model, text_tokenizer, tfidf_model, tfidf_vectorizer
    
    if USE_TRANSFORMER:
        try:
            model_path = os.path.join(MODEL_DIR, "distilbert-toxicity")
            if os.path.exists(model_path):
                text_tokenizer = AutoTokenizer.from_pretrained(model_path)
                text_model = AutoModelForSequenceClassification.from_pretrained(model_path)
                text_model.eval()
                print("Loaded DistilBERT model")
                return
        except Exception as e:
            print(f"Could not load DistilBERT: {e}")
    
    # Fallback to TF-IDF
    try:
        if os.path.exists(TFIDF_MODEL_PATH):
            with open(TFIDF_MODEL_PATH, "rb") as f:
                tfidf_model, tfidf_vectorizer = pickle.load(f)
            print("Loaded TF-IDF model")
        else:
            print("No text model found. Using default predictions.")
    except Exception as e:
        print(f"Could not load TF-IDF model: {e}")


def predict_text_toxicity(text: str):
    """
    Predict toxicity score for text
    Returns: {score: float, labels: dict, top_tokens: list}
    """
    global text_model, text_tokenizer, tfidf_model, tfidf_vectorizer
    
    if text_model is None and tfidf_model is None:
        load_text_model()
    
    # Try DistilBERT first
    if text_model is not None and text_tokenizer is not None:
        try:
            inputs = text_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                outputs = text_model(**inputs)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=-1)
                toxic_prob = probs[0][1].item() if probs.shape[1] > 1 else probs[0][0].item()
            
            # Extract top tokens (simple word-based approach)
            words = text.lower().split()
            top_tokens = [w for w in words if len(w) > 3][:5]
            
            return {
                "score": float(toxic_prob),
                "labels": {"toxic": float(toxic_prob), "non-toxic": 1.0 - float(toxic_prob)},
                "top_tokens": top_tokens
            }
        except Exception as e:
            print(f"Transformer prediction failed: {e}")
    
    # Fallback to TF-IDF
    if tfidf_model is not None and tfidf_vectorizer is not None:
        try:
            X = tfidf_vectorizer.transform([text])
            prob = tfidf_model.predict_proba(X)[0]
            toxic_prob = prob[1] if len(prob) > 1 else prob[0]
            
            # Extract top tokens
            feature_names = tfidf_vectorizer.get_feature_names_out()
            coef = tfidf_model.coef_[0] if hasattr(tfidf_model, "coef_") else None
            if coef is not None:
                indices = X.indices
                scores = [(feature_names[i], coef[i]) for i in indices if i < len(coef)]
                scores.sort(key=lambda x: x[1], reverse=True)
                top_tokens = [w for w, _ in scores[:5]]
            else:
                words = text.lower().split()
                top_tokens = [w for w in words if len(w) > 3][:5]
            
            return {
                "score": float(toxic_prob),
                "labels": {"toxic": float(toxic_prob), "non-toxic": 1.0 - float(toxic_prob)},
                "top_tokens": top_tokens
            }
        except Exception as e:
            print(f"TF-IDF prediction failed: {e}")
    
    # Ultimate fallback: enhanced heuristic with comprehensive toxic word list
    toxic_words = {
        # Strong toxicity (0.9-1.0)
        "hate": 0.95, "kill": 0.95, "die": 0.9, "death": 0.9, "murder": 0.95,
        "racist": 0.95, "nazi": 0.95, "kys": 0.95, "suicide": 0.9,
        # Moderate-high toxicity (0.7-0.85)
        "stupid": 0.75, "idiot": 0.75, "moron": 0.75, "dumb": 0.7, "ugly": 0.7,
        "loser": 0.7, "pathetic": 0.75, "worthless": 0.8, "trash": 0.7,
        "terrible": 0.65, "awful": 0.65, "suck": 0.7, "sucks": 0.7,
        # Moderate toxicity (0.5-0.65)
        "bad": 0.5, "worse": 0.55, "worst": 0.6, "horrible": 0.65,
        "disgusting": 0.65, "gross": 0.6, "nasty": 0.6, "annoying": 0.55,
        # Profanity (0.7-0.85)
        "damn": 0.7, "hell": 0.65, "crap": 0.7, "shit": 0.8, "fuck": 0.85,
        "bitch": 0.85, "ass": 0.75, "bastard": 0.8,
        # Harassment (0.8-0.95)
        "attack": 0.8, "threaten": 0.85, "threat": 0.85, "violence": 0.85,
        "violent": 0.8, "abuse": 0.85, "abusive": 0.8, "harass": 0.85,
    }
    
    text_lower = text.lower()
    words = text_lower.split()
    
    # Calculate score based on detected toxic words and their severity
    max_score = 0.0
    detected_tokens = []
    
    for word in words:
        for toxic_word, severity in toxic_words.items():
            if toxic_word in word:
                max_score = max(max_score, severity)
                detected_tokens.append(word)
    
    # If multiple toxic words, increase score slightly
    if len(detected_tokens) > 1:
        max_score = min(max_score + 0.1 * (len(detected_tokens) - 1), 1.0)
    
    # Check for toxic phrases
    toxic_phrases = [
        ("i hate you", 0.9), ("hate you", 0.85), ("you suck", 0.75),
        ("shut up", 0.7), ("go away", 0.6), ("nobody cares", 0.7),
        ("kill yourself", 0.95), ("die in", 0.9), ("hope you", 0.65)
    ]
    
    for phrase, severity in toxic_phrases:
        if phrase in text_lower:
            max_score = max(max_score, severity)
            detected_tokens.extend(phrase.split())
    
    score = max_score
    top_tokens = list(set(detected_tokens))[:5]
    
    return {
        "score": float(score),
        "labels": {"toxic": float(score), "non-toxic": 1.0 - float(score)},
        "top_tokens": top_tokens
    }


if __name__ == "__main__":
    # Test
    result = predict_text_toxicity("This is a test comment")
    print(result)

