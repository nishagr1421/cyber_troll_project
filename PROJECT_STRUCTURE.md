# InstaGuard MVP - Project Structure

## Complete File Structure

```
cyber_troll_project/
│
├── frontend/                          # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Feed.jsx               # Main feed component
│   │   │   ├── PostCard.jsx           # Individual post display
│   │   │   ├── CommentList.jsx        # List of comments
│   │   │   ├── CommentItem.jsx        # Single comment with actions
│   │   │   ├── ToxicityBadge.jsx      # Toxicity score badge
│   │   │   ├── CommentComposer.jsx    # Comment input with live prediction
│   │   │   ├── Composer.jsx           # Post creation form
│   │   │   └── AdminPanel.jsx         # Admin moderation panel
│   │   ├── App.jsx                    # Main app component
│   │   ├── main.jsx                   # React entry point
│   │   └── index.css                  # Global styles
│   ├── index.html                     # HTML template
│   ├── package.json                   # Frontend dependencies
│   ├── vite.config.js                 # Vite configuration
│   ├── tailwind.config.js             # Tailwind CSS config
│   └── postcss.config.js               # PostCSS config
│
├── backend/                            # FastAPI Backend
│   ├── api/
│   │   ├── __init__.py
│   │   ├── predict.py                 # Prediction logic
│   │   └── feed.py                    # Feed management
│   ├── data/                          # Runtime data (created)
│   │   ├── feed.json                  # Posts and comments
│   │   └── annotations.csv            # Accept/delete logs
│   ├── models/                        # Trained models (created)
│   ├── main.py                        # FastAPI application
│   ├── infer_text.py                  # Text toxicity inference
│   ├── infer_image.py                 # Image toxicity inference
│   ├── train_text.py                  # Text model training
│   ├── train_image.py                 # Image model training
│   ├── initialize_feed.py             # Initialize feed from sample
│   └── requirements.txt               # Python dependencies
│
├── models/                            # Shared model directory
├── sample_data/                       # Sample images for training
│   └── README.md
├── sample_feed.json                   # Sample feed data
├── start.sh                           # Linux/Mac startup script
├── start.bat                          # Windows startup script
├── README.md                          # Main documentation
├── QUICKSTART.md                      # Quick start guide
├── PROJECT_STRUCTURE.md                # This file
└── .gitignore                         # Git ignore rules
```

## Component Overview

### Frontend Components

1. **Feed.jsx** - Main feed container, loads posts, handles comment actions
2. **PostCard.jsx** - Displays a single post with image, caption, comments
3. **CommentList.jsx** - Renders list of comments
4. **CommentItem.jsx** - Single comment with toxicity badge and action buttons
5. **ToxicityBadge.jsx** - Colored badge showing toxicity score (green/yellow/red)
6. **CommentComposer.jsx** - Comment input with real-time toxicity prediction
7. **Composer.jsx** - Post creation form with image upload
8. **AdminPanel.jsx** - Admin view with table of all comments

### Backend Modules

1. **main.py** - FastAPI app with all endpoints
2. **api/predict.py** - Prediction functions for posts and comments
3. **api/feed.py** - Feed CRUD operations
4. **infer_text.py** - Text toxicity inference (DistilBERT/TF-IDF)
5. **infer_image.py** - Image toxicity inference (ResNet18)
6. **train_text.py** - Text model training script
7. **train_image.py** - Image model training script

## API Endpoints

- `GET /` - Health check
- `POST /api/predict` - Predict post toxicity (caption + image)
- `POST /api/comment/predict` - Predict comment toxicity
- `GET /api/feed` - Get all posts
- `POST /api/comment/add` - Add new comment
- `POST /api/comment/accept` - Accept comment
- `POST /api/comment/delete` - Delete comment

## Data Flow

1. **Post Creation:**
   - User uploads image + caption → `/api/predict` → Returns toxicity scores
   - Post saved to `data/feed.json`

2. **Comment Addition:**
   - User types comment → Real-time prediction via `/api/comment/predict`
   - On submit → `/api/comment/add` → Comment added to feed

3. **Comment Moderation:**
   - User clicks ACCEPT/DELETE → `/api/comment/accept` or `/api/comment/delete`
   - Action logged to `data/annotations.csv`
   - Feed updated

## Model Pipeline

1. **Text Model:**
   - Input: Text string
   - Process: DistilBERT or TF-IDF + LogisticRegression
   - Output: Score (0-1), labels, top tokens

2. **Image Model:**
   - Input: Image file
   - Process: ResNet18 with transfer learning
   - Output: Score (0-1)

3. **Fusion:**
   - Average of text and image scores

