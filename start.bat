@echo off
echo Starting InstaGuard MVP...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js is not installed or not in PATH
    echo Please install Node.js 16+
    pause
    exit /b 1
)

REM Check if npm is installed (try npm.cmd first to avoid PowerShell execution policy issues)
where npm.cmd >nul 2>&1
if errorlevel 1 (
    REM Try npm directly
    npm --version >nul 2>&1
    if errorlevel 1 (
        echo npm is not installed or not in PATH
        echo Please install Node.js which includes npm
        echo.
        echo If you see a PowerShell execution policy error, run: fix-execution-policy.bat
        pause
        exit /b 1
    )
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install backend dependencies
echo Installing backend dependencies...
cd backend
if errorlevel 1 (
    echo ERROR: Could not find backend directory
    pause
    exit /b 1
)
pip install -r requirements.txt

REM Initialize feed
echo Initializing feed...
python initialize_feed.py

REM Train models (optional - skip if they fail)
echo Training models (this may take a while)...
python train_text.py 2>nul
if errorlevel 1 (
    echo WARNING: Text model training skipped or failed
)
python train_image.py 2>nul
if errorlevel 1 (
    echo WARNING: Image model training skipped or failed
)

cd ..

REM Install frontend dependencies
echo Installing frontend dependencies...
cd frontend
if errorlevel 1 (
    echo ERROR: Could not find frontend directory
    pause
    exit /b 1
)

REM Try npm.cmd first (avoids PowerShell execution policy issues)
where npm.cmd >nul 2>&1
if not errorlevel 1 (
    call npm.cmd install
) else (
    REM Fallback to npm (may fail if execution policy is restricted)
    npm install 2>nul
    if errorlevel 1 (
        echo.
        echo WARNING: npm install failed. This might be due to PowerShell execution policy.
        echo.
        echo Solutions:
        echo   1. Run: fix-execution-policy.bat
        echo   2. Or use Command Prompt (cmd) instead of PowerShell
        echo   3. Or manually run: cd frontend ^&^& npm install
        echo.
        pause
    )
)

echo.
echo SUCCESS: Setup complete!
echo.
echo To start the servers:
echo   1. Open a terminal and run: cd backend ^&^& python main.py
echo   2. Open another terminal and run: cd frontend ^&^& npm run dev
echo.
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:3000
echo.
echo Or use the start-servers.bat script to start both automatically.
pause

