$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$pythonw = Join-Path $PSScriptRoot ".venv\Scripts\pythonw.exe"

if (-not (Test-Path $python) -or -not (Test-Path $pythonw)) {
    throw "Virtual environment missing. Create it first: py -3.11 -m venv .venv; .\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt"
}

& $python register_startup_windows.py
Start-Process -FilePath $pythonw -ArgumentList "screen_ocr.py" -WorkingDirectory $PSScriptRoot

Write-Host "ScreenOCR utility installed and started."
Write-Host "It will auto-start on Windows login and listen for Shift+Q+W+E."
