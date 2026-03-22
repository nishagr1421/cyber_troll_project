@echo off
echo 🔧 Fixing PowerShell Execution Policy...
echo.
echo This will set the execution policy to allow npm to run.
echo You may be prompted for Administrator privileges.
echo.
pause

REM Try to set execution policy using PowerShell
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force" 2>nul

if errorlevel 1 (
    echo.
    echo ⚠️  Could not set execution policy automatically.
    echo.
    echo Please run this command manually as Administrator:
    echo   powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
    echo.
    echo Or use Command Prompt (cmd) instead of PowerShell for running npm commands.
    echo.
) else (
    echo.
    echo ✅ Execution policy updated!
    echo.
    echo You may need to close and reopen your terminal for changes to take effect.
    echo.
)

pause

