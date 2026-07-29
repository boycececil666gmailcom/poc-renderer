# PowerShell Script to Launch OpenGL Renderer with Toyota Supra GLTF

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ">>> [1/2] Activating Virtual Environment" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

if (Test-Path "venv/Scripts/Activate.ps1") {
    & "venv/Scripts/Activate.ps1"
} else {
    Write-Host "Error: Virtual environment not found." -ForegroundColor Red
    exit 1
}

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host ">>> [2/2] Launching OpenGL Engine with Toyota Supra GLTF" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

& "venv/Scripts/python.exe" main.py gltf/toyota_supra.gltf
