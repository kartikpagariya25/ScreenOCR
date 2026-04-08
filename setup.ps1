$ErrorActionPreference = "Stop"
Write-Host "=== ScreenOCR Setup Script ===" -ForegroundColor Cyan
Set-Location $PSScriptRoot

Write-Host "`nStep 1: Checking Python..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    throw "Python not found. Install Python 3.11 from python.org"
}
Write-Host "Python found: $($pythonCmd.Source)" -ForegroundColor Green

Write-Host "`nStep 2: Checking Tesseract OCR..." -ForegroundColor Yellow
try {
    $tesseract = tesseract --version 2>$null
    if ($tesseract) {
        Write-Host "Tesseract found" -ForegroundColor Green
    } else {
        throw "Tesseract not in PATH"
    }
} catch {
    Write-Host "Tesseract not found in PATH" -ForegroundColor Red
    Write-Host "Install from: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Yellow
    Write-Host "Then run: setx TESSERACT_CMD `"C:\Program Files\Tesseract-OCR\tesseract.exe`"" -ForegroundColor Yellow
    throw "Tesseract OCR is required"
}

Write-Host "`nStep 3: Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Virtual environment exists, recreating..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force ".venv"
}
py -3.11 -m venv .venv
Write-Host "Virtual environment created" -ForegroundColor Green

Write-Host "`nStep 4: Installing dependencies..." -ForegroundColor Yellow
$pythonExe = ".\.venv\Scripts\python.exe"
& $pythonExe -m pip install --upgrade pip | Out-Null
& $pythonExe -m pip install -r requirements.txt | Out-Null
Write-Host "Dependencies installed" -ForegroundColor Green

Write-Host "`nStep 5: Verifying installation..." -ForegroundColor Yellow
$testCode = "import cv2, numpy, mss, pytesseract, pyperclip, pynput; from PIL import Image; print('OK')"
$result = & $pythonExe -c $testCode
if ($result.Trim() -eq "OK") {
    Write-Host "All imports verified" -ForegroundColor Green
} else {
    throw "Import test failed: $result"
}

Write-Host "`nStep 6: Registering startup..." -ForegroundColor Yellow
& $pythonExe register_startup_windows.py
Write-Host "Startup registered" -ForegroundColor Green

Write-Host "`nStep 7: Starting ScreenOCR..." -ForegroundColor Yellow
$pythonwExe = ".\.venv\Scripts\pythonw.exe"
Start-Process -FilePath $pythonwExe -ArgumentList "screen_ocr.py" -WorkingDirectory $PSScriptRoot
Write-Host "ScreenOCR started in background" -ForegroundColor Green

Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Write-Host "Hotkey: Shift + Q + W + E" -ForegroundColor White
Write-Host "Stop: Press Esc" -ForegroundColor White
Write-Host "Restart: .\.venv\Scripts\pythonw.exe screen_ocr.py" -ForegroundColor White
