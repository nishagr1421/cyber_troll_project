# Using Command Prompt Instead of PowerShell

If you're having PowerShell execution policy issues with npm, the easiest solution is to use **Command Prompt (cmd)** instead of PowerShell.

## How to Use Command Prompt

1. **Open Command Prompt:**
   - Press `Win + R`
   - Type `cmd` and press Enter
   - Or search for "Command Prompt" in Start menu

2. **Navigate to project directory:**
   ```cmd
   cd C:\Users\priya\OneDrive\Desktop\cyber_troll_project
   ```

3. **Run the setup:**
   ```cmd
   start.bat
   ```

4. **Start servers:**
   ```cmd
   start-servers.bat
   ```

## Why This Works

- Command Prompt doesn't have execution policy restrictions
- npm works directly without PowerShell script issues
- All batch files work the same way

## Alternative: Fix PowerShell (If You Prefer PowerShell)

If you want to keep using PowerShell:

1. **Run as Administrator:**
   - Right-click PowerShell
   - Select "Run as Administrator"

2. **Run the fix script:**
   ```cmd
   fix-execution-policy.bat
   ```

3. **Or manually set policy:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
   ```

4. **Restart PowerShell** for changes to take effect

## Quick Reference

- **Command Prompt**: No execution policy issues ✅
- **PowerShell**: May need execution policy fix ⚠️
- **Both work the same** for running batch files and npm commands

