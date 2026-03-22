"""
Train image toxicity model using ResNet18 with transfer learning
"""
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
import numpy as np

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


class ImageDataset(Dataset):
    """Dataset for image classification"""
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform or transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        try:
            image = Image.open(image_path).convert("RGB")
        except:
            # Return a black image if loading fails
            image = Image.new("RGB", (224, 224))
        
        if self.transform:
            image = self.transform(image)
        
        label = self.labels[idx]
        return image, label


def create_sample_data(data_dir="sample_data"):
    """Create sample training data from sample_data directory"""
    image_paths = []
    labels = []
    
    if os.path.exists(data_dir):
        # Assume all images in sample_data are safe (label 0)
        # In a real scenario, you'd have labeled data
        for filename in os.listdir(data_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                image_paths.append(os.path.join(data_dir, filename))
                labels.append(0)  # Safe
    
    # If no images found, create dummy data
    if len(image_paths) == 0:
        print("No images found in sample_data. Creating dummy dataset...")
        # Create 10 dummy entries (you'd replace this with real data)
        for i in range(10):
            image_paths.append(f"dummy_{i}.jpg")
            labels.append(0)
    
    return image_paths, labels


def create_model():
    """Create ResNet18-based model"""
    model = models.resnet18(pretrained=True)
    # Freeze early layers
    for param in list(model.parameters())[:-10]:
        param.requires_grad = False
    
    # Replace final layer
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 1)  # Binary: safe (0) / harmful (1)
    
    return model


def train_model(data_dir=None, epochs=5, batch_size=8):
    """Train the image model"""
    print("Training image toxicity model...")
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Get data
    if data_dir and os.path.exists(data_dir):
        image_paths, labels = create_sample_data(data_dir)
    else:
        image_paths, labels = create_sample_data()
    
    if len(image_paths) == 0:
        print("No training data available. Creating a dummy model...")
        model = create_model()
        torch.save(model.state_dict(), os.path.join(MODEL_DIR, "image_model.pt"))
        print(f"Model saved to {MODEL_DIR}/image_model.pt")
        return
    
    # Filter out dummy paths that don't exist
    valid_paths = []
    valid_labels = []
    for path, label in zip(image_paths, labels):
        if os.path.exists(path):
            valid_paths.append(path)
            valid_labels.append(label)
    
    if len(valid_paths) == 0:
        print("No valid images found. Creating a dummy model...")
        model = create_model()
        torch.save(model.state_dict(), os.path.join(MODEL_DIR, "image_model.pt"))
        print(f"Model saved to {MODEL_DIR}/image_model.pt")
        return
    
    # Create dataset
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    dataset = ImageDataset(valid_paths, valid_labels, transform=transform)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # Create model
    model = create_model()
    model.to(device)
    
    # Loss and optimizer
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Training loop
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for images, labels in dataloader:
            images = images.to(device)
            labels = labels.float().unsqueeze(1).to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
        
        print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(dataloader):.4f}")
    
    # Save model
    model_path = os.path.join(MODEL_DIR, "image_model.pt")
    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    import sys
    
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "sample_data"
    train_model(data_dir=data_dir, epochs=5)

