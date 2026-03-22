#!/bin/bash

echo "🚀 Starting InstaGuard MVP..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "📥 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Initialize feed
echo "📋 Initializing feed..."
python initialize_feed.py

# Train models (optional - comment out if you want to skip)
echo "🤖 Training models (this may take a while)..."
python train_text.py || echo "⚠️  Text model training skipped or failed"
python train_image.py || echo "⚠️  Image model training skipped or failed"

cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install

# Start backend in background
echo "🔧 Starting backend server..."
cd ../backend
python main.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ InstaGuard is running!"
echo "   Backend: http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait

