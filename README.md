# InstaGuard MVP - Cyber Trolling Detection Platform

A one-night cyber-trolling detection platform that looks and behaves like Instagram posts & comments. Built with React + FastAPI, featuring ML models for text and image toxicity detection.

## 🎯 Features

### Core Features

1. **Instagram-style Feed UI (React)**
   - Posts with username, images, captions, likes, and comments
   - Comments displayed exactly like Instagram
   - Toxicity score badges (0-1) next to each comment (green/yellow/red)
   - ACCEPT and DELETE buttons for each comment
   - Real-time comment moderation

2. **Image Moderation**
   - CNN-based image toxicity detection (ResNet18/MobileNetV2)
   - Image toxicity score displayed under posts
   - Transfer learning with fine-tuning

3. **Text Moderation**
   - DistilBERT or TF-IDF + LogisticRegression for text toxicity
   - Real-time toxicity prediction as users type
   - Top toxic tokens extraction
   - Severity scores and labels

4. **Backend API (FastAPI)**
   - `POST /api/predict` - Predict toxicity for posts (caption + image)
   - `POST /api/comment/predict` - Predict toxicity for comments
   - `POST /api/comment/accept` - Accept a comment (mark as safe)
   - `POST /api/comment/delete` - Delete a comment
   - `GET /api/feed` - Get all posts with comments
   - `POST /api/comment/add` - Add a new comment

5. **Admin/Moderator Panel**
   - Table view of all comments sorted by toxicity
   - Accept/Delete actions
   - Annotations stored in CSV

6. **ML Models**
   - Text model: DistilBERT (with TF-IDF fallback)
   - Image model: ResNet18 with transfer learning
   - Fusion: Average of text and image scores

## 📁 Project Structure

```
cyber_troll_project/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Feed.jsx
│   │   │   ├── PostCard.jsx
│   │   │   ├── CommentList.jsx
│   │   │   ├── CommentItem.jsx
│   │   │   ├── ToxicityBadge.jsx
│   │   │   ├── CommentComposer.jsx
│   │   │   ├── Composer.jsx
│   │   │   └── AdminPanel.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/                  # FastAPI backend
│   ├── api/
│   │   ├── predict.py        # Prediction endpoints
│   │   └── feed.py           # Feed management
│   ├── main.py               # FastAPI app
│   ├── infer_text.py         # Text inference
│   ├── infer_image.py        # Image inference
│   ├── train_text.py         # Text model training
│   ├── train_image.py        # Image model training
│   ├── initialize_feed.py    # Initialize feed from sample
│   └── requirements.txt
├── models/                   # Trained models (created after training)
├── data/                     # Runtime data (created at runtime)
│   ├── feed.json            # Posts and comments
│   └── annotations.csv      # Accept/delete annotations
├── sample_data/             # Sample images for training
├── sample_feed.json         # Sample feed data
├── start.sh                 # Linux/Mac startup script
├── start.bat                # Windows startup script
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation & Setup

**⚠️ Prerequisites:** Make sure you have Python 3.8+ and Node.js 16+ installed before proceeding.

#### Option 1: Automated Setup (Windows)

```bash
start.bat
```

Then start servers:
```bash
start-servers.bat
```

#### Option 2: Automated Setup (Linux/Mac)

```bash
chmod +x start.sh
./start.sh
```

#### Option 3: Manual Setup

1. **Backend Setup:**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   cd backend
   pip install -r requirements.txt
   
   # Initialize feed
   python initialize_feed.py
   
   # Train models (optional, will use fallback if skipped)
   python train_text.py
   python train_image.py
   
   # Start backend
   python main.py
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Access the Application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🎨 Usage

### Feed View

1. **View Posts**: Browse Instagram-style feed with posts and comments
2. **See Toxicity Scores**: Each comment shows a colored badge (green/yellow/red)
3. **Moderate Comments**: Click ACCEPT or DELETE on any comment
4. **Add Comments**: Type in the comment box - see live toxicity prediction
5. **Create Posts**: Use the composer to create new posts with images

### Admin Panel

1. Switch to "Admin" tab in the header
2. View all comments sorted by toxicity
3. Accept or delete comments in bulk
4. All actions are logged to `data/annotations.csv`

### Comment Composer

- As you type, toxicity score updates in real-time
- Flagged tokens are highlighted
- Score appears before posting

## 🤖 ML Models

### Text Model

- **Primary**: DistilBERT fine-tuned on toxicity data
- **Fallback**: TF-IDF + LogisticRegression
- **Output**: Toxicity score (0-1), labels, top toxic tokens

### Image Model

- **Architecture**: ResNet18 with transfer learning
- **Output**: Image toxicity score (0-1)
- **Training**: Fine-tuned on labeled image dataset

### Fusion

- Combined score = (text_score + image_score) / 2

## 📊 Data Storage

- **Feed**: `data/feed.json` - All posts and comments
- **Annotations**: `data/annotations.csv` - Accept/delete actions
- **Models**: `models/` - Trained ML models

## 🔧 API Endpoints

### POST /api/predict
Predict toxicity for a post (caption + image).

**Request:**
- `caption` (form): Post caption text
- `image` (file): Post image file

**Response:**
```json
{
  "text_score": 0.75,
  "text_labels": {"toxic": 0.75, "non-toxic": 0.25},
  "image_score": 0.20,
  "fused_score": 0.475,
  "tokens_flagged": ["hate", "stupid"]
}
```

### POST /api/comment/predict
Predict toxicity for a comment.

**Request:**
```json
{
  "text": "This is a comment"
}
```

**Response:**
```json
{
  "score": 0.65,
  "top_tokens": ["hate"]
}
```

### POST /api/comment/accept
Accept a comment (mark as safe).

**Request:**
```json
{
  "post_id": "post_1",
  "comment_id": "comment_1"
}
```

### POST /api/comment/delete
Delete a comment from feed.

**Request:**
```json
{
  "post_id": "post_1",
  "comment_id": "comment_1"
}
```

### GET /api/feed
Get all posts with comments.

**Response:**
```json
[
  {
    "id": "post_1",
    "username": "user",
    "caption": "Caption text",
    "image_url": "url",
    "comments": [...]
  }
]
```

## 🛠️ Development

### Training Models

**Text Model:**
```bash
cd backend
python train_text.py [path_to_dataset.csv]
```

**Image Model:**
```bash
cd backend
python train_image.py [path_to_image_directory]
```

### Adding Sample Data

1. Add images to `sample_data/` directory
2. Update `sample_feed.json` with new posts
3. Run `python backend/initialize_feed.py` to refresh feed

## 📝 Notes

- Models use fallback heuristics if training data is not available
- First run may be slower as models are loaded
- Image URLs in sample feed use Unsplash - replace with local images if needed
- All toxicity scores are between 0 (safe) and 1 (toxic)

## 🎯 Future Enhancements

- [ ] Grad-CAM heatmap overlay for images
- [ ] OCR for meme text detection
- [ ] Browser extension
- [ ] User authentication
- [ ] Real-time notifications
- [ ] Advanced explainability features

## 📄 License

This project is for demonstration purposes.

## 🤝 Contributing

This is an MVP project. Feel free to extend and improve!

---

**Built with ❤️ for cyber-trolling detection**

