"""
Image toxicity inference using CNN (ResNet18/MobileNetV2)
"""
import os
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import numpy as np

MODEL_DIR = "models"
IMAGE_MODEL_PATH = os.path.join(MODEL_DIR, "image_model.pt")

# Global model variable
image_model = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def create_image_model():
    """Create a ResNet18-based model for image classification"""
    model = models.resnet18(pretrained=True)
    # Replace the final layer
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 1)  # Binary classification: safe/harmful
    return model


def load_image_model():
    """Load image model"""
    global image_model
    
    try:
        if os.path.exists(IMAGE_MODEL_PATH):
            model = create_image_model()
            model.load_state_dict(torch.load(IMAGE_MODEL_PATH, map_location=device))
            model.eval()
            model.to(device)
            image_model = model
            print("Loaded image model")
        else:
            print("No image model found. Using default predictions.")
    except Exception as e:
        print(f"Could not load image model: {e}")


def predict_image_toxicity(image_path: str):
    """
    Predict toxicity score for an image
    Returns: {score: float}
    """
    global image_model
    
    if image_model is None:
        load_image_model()
    
    try:
        # Load and preprocess image
        image = Image.open(image_path).convert("RGB")
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        if image_model is not None:
            with torch.no_grad():
                output = image_model(image_tensor)
                # Apply sigmoid to get probability
                score = torch.sigmoid(output).item()
        else:
            # Fallback: simple heuristic based on image properties
            # In a real scenario, you'd analyze image content
            # For MVP, return a low default score
            score = 0.1
        
        return {"score": float(score)}
    except Exception as e:
        print(f"Image prediction failed: {e}")
        # Fallback
        return {"score": 0.1}


if __name__ == "__main__":
    # Test
    if os.path.exists("sample_data/test.jpg"):
        result = predict_image_toxicity("sample_data/test.jpg")
        print(result)

