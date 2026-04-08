$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Virtual environment not found. Create it first: py -3.11 -m venv .venv"
}

& $python -m pip install --upgrade pip
& $python -m pip install -r requirements.txt pyinstaller

& $python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name ScreenOCR `
    screen_ocr.py

Write-Host "Build complete. EXE path: dist\ScreenOCR.exe"
