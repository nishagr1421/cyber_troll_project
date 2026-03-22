# Fix PowerShell Execution Policy for npm
# Run this script as Administrator

Write-Host "🔧 Fixing PowerShell Execution Policy..." -ForegroundColor Yellow

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ This script requires Administrator privileges." -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator', then run this script again." -ForegroundColor Yellow
    pause
    exit 1
}

# Set execution policy for current user
Write-Host "Setting execution policy to RemoteSigned for CurrentUser..." -ForegroundColor Cyan
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

Write-Host "✅ Execution policy updated!" -ForegroundColor Green
Write-Host "You can now use npm commands." -ForegroundColor Green
Write-Host ""
Write-Host "Note: If you still have issues, try:" -ForegroundColor Yellow
Write-Host "  1. Close and reopen your terminal" -ForegroundColor Yellow
Write-Host "  2. Or use Command Prompt (cmd) instead of PowerShell" -ForegroundColor Yellow
pause

