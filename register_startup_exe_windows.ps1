param(
    [switch]$Remove
)

$ErrorActionPreference = "Stop"

$runKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$name = "ScreenOCR"
$exePath = Join-Path $PSScriptRoot "dist\ScreenOCR.exe"

if ($Remove) {
    Remove-ItemProperty -Path $runKey -Name $name -ErrorAction SilentlyContinue
    Write-Host "Startup entry removed: $name"
    exit 0
}

if (-not (Test-Path $exePath)) {
    throw "EXE not found at $exePath. Build first with .\build_exe.ps1"
}

Set-ItemProperty -Path $runKey -Name $name -Value ('"' + $exePath + '"')
Write-Host "Startup entry added for $exePath"
