# Quick Start Guide

## Windows Setup

1. **Install Python 3.8+ and Node.js 16+**

2. **Run the setup script:**
   ```bash
   start.bat
   ```

3. **Or manually:**

   **Backend:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   cd backend
   pip install -r requirements.txt
   python initialize_feed.py
   python main.py
   ```

   **Frontend (in a new terminal):**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Linux/Mac Setup

1. **Run the setup script:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

2. **Or manually:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   cd backend
   pip install -r requirements.txt
   python initialize_feed.py
   python main.py
   ```

   In another terminal:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Training Models (Optional)

Models will use fallback heuristics if not trained. To train:

```bash
cd backend
python train_text.py
python train_image.py
```

## Troubleshooting

- **Backend won't start**: Make sure port 8000 is free
- **Frontend won't start**: Make sure port 3000 is free
- **Models not loading**: Run training scripts or models will use fallback
- **Feed is empty**: Run `python backend/initialize_feed.py`

