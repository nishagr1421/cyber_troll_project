# Setup Guide for InstaGuard MVP

## Prerequisites

Before running the setup, make sure you have:

1. **Python 3.8+** installed
   - Download from: https://www.python.org/
   - Make sure to check "Add Python to PATH" during installation
   - Verify: `python --version`

2. **Node.js 16+** installed (includes npm)
   - Download from: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

## Installation Steps

### Option 1: Automated Setup (Recommended)

1. **Run the setup script:**
   ```bash
   start.bat
   ```
   
   This will:
   - Check for Python and Node.js
   - Create virtual environment
   - Install backend dependencies
   - Initialize the feed
   - Optionally train models
   - Install frontend dependencies

2. **Start the servers:**
   ```bash
   start-servers.bat
   ```
   
   This opens two windows - one for backend, one for frontend.

### Option 2: Manual Setup

#### Backend Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

3. **Navigate to backend and install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Initialize feed:**
   ```bash
   python initialize_feed.py
   ```

5. **Start backend server:**
   ```bash
   python main.py
   ```
   
   Backend will run on http://localhost:8000

#### Frontend Setup (in a NEW terminal)

1. **Navigate to frontend:**
   ```bash
   cd frontend
   ```
   (Make sure you're in the project root, not in backend!)

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start frontend server:**
   ```bash
   npm run dev
   ```
   
   Frontend will run on http://localhost:3000

## Troubleshooting

### "npm is not recognized"
- **Solution**: Install Node.js from https://nodejs.org/
- Make sure to restart your terminal after installation
- Verify with: `npm --version`

### "npm.ps1 cannot be loaded because running scripts is disabled"
- **Problem**: PowerShell execution policy is blocking npm
- **Solution 1 (Recommended)**: Run `fix-execution-policy.bat` as Administrator
- **Solution 2**: Use Command Prompt (cmd) instead of PowerShell
- **Solution 3**: Run this command in PowerShell as Administrator:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
  ```
- **Solution 4**: Use `npm.cmd` instead of `npm` (e.g., `npm.cmd install`)

### "Python is not recognized"
- **Solution**: Install Python from https://www.python.org/
- During installation, check "Add Python to PATH"
- Restart your terminal
- Verify with: `python --version`

### "Cannot find path 'backend\frontend'"
- **Problem**: You're trying to `cd frontend` from the `backend` directory
- **Solution**: Make sure you're in the project root directory
- Use: `cd ..` to go back to project root, then `cd frontend`

### Port already in use
- **Backend (port 8000)**: Close any other application using port 8000
- **Frontend (port 3000)**: Close any other application using port 3000
- Or change ports in:
  - Backend: `backend/main.py` (line with `uvicorn.run`)
  - Frontend: `frontend/vite.config.js` (server.port)

### Models not loading
- Models will use fallback heuristics if not trained
- To train models:
  ```bash
  cd backend
  python train_text.py
  python train_image.py
  ```

### Feed is empty
- Run: `python backend/initialize_feed.py`
- This copies `sample_feed.json` to `backend/data/feed.json`

## Verifying Installation

1. **Backend is running:**
   - Visit: http://localhost:8000
   - Should see: `{"message": "InstaGuard API is running"}`
   - API docs: http://localhost:8000/docs

2. **Frontend is running:**
   - Visit: http://localhost:3000
   - Should see the InstaGuard feed interface

## Next Steps

Once both servers are running:
1. Open http://localhost:3000 in your browser
2. You should see the Instagram-style feed
3. Try adding comments to see toxicity detection
4. Use the Admin tab to moderate comments

## Need Help?

- Check the main README.md for detailed documentation
- Check QUICKSTART.md for quick reference
- Check PROJECT_STRUCTURE.md for file organization

