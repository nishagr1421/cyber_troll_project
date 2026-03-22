"""
Train text toxicity model using DistilBERT or TF-IDF + LogisticRegression
"""
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import torch
from datasets import Dataset

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Use DistilBERT if available, otherwise TF-IDF
USE_TRANSFORMER = True


def create_sample_data():
    """Create sample training data if no dataset is provided"""
    # Sample toxic and non-toxic comments
    toxic_samples = [
        "You're such an idiot!",
        "I hate you so much",
        "This is stupid and dumb",
        "You should die",
        "What a loser",
        "This is garbage",
        "You're ugly",
        "Go kill yourself",
        "This is trash",
        "You're worthless"
    ]
    
    non_toxic_samples = [
        "Great post! Thanks for sharing.",
        "I love this!",
        "This is really helpful",
        "Amazing work!",
        "Thank you for this",
        "Beautiful picture!",
        "Nice one!",
        "I agree with you",
        "This is interesting",
        "Keep up the good work!"
    ]
    
    data = {
        "text": toxic_samples + non_toxic_samples,
        "label": [1] * len(toxic_samples) + [0] * len(non_toxic_samples)
    }
    
    return pd.DataFrame(data)


def train_tfidf_model(data_path=None):
    """Train TF-IDF + LogisticRegression model"""
    print("Training TF-IDF + LogisticRegression model...")
    
    if data_path and os.path.exists(data_path):
        df = pd.read_csv(data_path)
        texts = df["text"].values
        labels = df["label"].values
    else:
        print("No dataset provided, using sample data...")
        df = create_sample_data()
        texts = df["text"].values
        labels = df["label"].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )
    
    # Vectorize
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    print(classification_report(y_test, y_pred))
    
    # Save model
    model_path = os.path.join(MODEL_DIR, "text_model_tfidf.pkl")
    with open(model_path, "wb") as f:
        pickle.dump((model, vectorizer), f)
    print(f"Model saved to {model_path}")
    
    return model, vectorizer


def train_distilbert_model(data_path=None):
    """Train DistilBERT model"""
    print("Training DistilBERT model...")
    
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
    except ImportError:
        print("Transformers not available, falling back to TF-IDF")
        return train_tfidf_model(data_path)
    
    if data_path and os.path.exists(data_path):
        df = pd.read_csv(data_path)
        texts = df["text"].values.tolist()
        labels = df["label"].values.tolist()
    else:
        print("No dataset provided, using sample data...")
        df = create_sample_data()
        texts = df["text"].values.tolist()
        labels = df["label"].values.tolist()
    
    # Create dataset
    dataset = Dataset.from_dict({"text": texts, "label": labels})
    dataset = dataset.train_test_split(test_size=0.2)
    
    # Load tokenizer and model
    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=2
    )
    
    # Tokenize
    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding=True, max_length=512)
    
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=os.path.join(MODEL_DIR, "distilbert-toxicity"),
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=100,
        logging_dir="./logs",
        logging_steps=10,
        save_strategy="epoch"
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["test"]
    )
    
    # Train
    trainer.train()
    
    # Save
    model.save_pretrained(os.path.join(MODEL_DIR, "distilbert-toxicity"))
    tokenizer.save_pretrained(os.path.join(MODEL_DIR, "distilbert-toxicity"))
    print(f"Model saved to {MODEL_DIR}/distilbert-toxicity")
    
    return model, tokenizer


if __name__ == "__main__":
    import sys
    
    data_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    if USE_TRANSFORMER:
        try:
            train_distilbert_model(data_path)
        except Exception as e:
            print(f"DistilBERT training failed: {e}")
            print("Falling back to TF-IDF...")
            train_tfidf_model(data_path)
    else:
        train_tfidf_model(data_path)

