@echo off
echo 🚀 Starting InstaGuard Servers...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    pause
    exit /b 1
)

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment not found. Run start.bat first to set up.
    pause
    exit /b 1
)

REM Start backend in a new window
echo 🔧 Starting backend server...
start "InstaGuard Backend" cmd /k "cd backend && python main.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a new window
echo 🎨 Starting frontend server...
REM Use npm.cmd to avoid PowerShell execution policy issues
where npm.cmd >nul 2>&1
if not errorlevel 1 (
    start "InstaGuard Frontend" cmd /k "cd frontend && npm.cmd run dev"
) else (
    start "InstaGuard Frontend" cmd /k "cd frontend && npm run dev"
)

echo.
echo ✅ Servers starting!
echo.
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:3000
echo.
echo Two new windows have opened - one for backend, one for frontend.
echo Close those windows to stop the servers.
echo.
pause

