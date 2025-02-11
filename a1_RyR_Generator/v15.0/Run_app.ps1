# Start PowerShell in the current window (optional, not necessary for most scripts)
# Start-Process -FilePath "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -NoNewWindow

# Construct paths
$env_directory = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"
$src_directory = Join-Path $PSScriptRoot "app\src"

# Activate the virtual environment
& $env_directory
Write-Host "env successfully activated: $env_directory" -ForegroundColor Green

# Change directory to the source directory
Set-Location $src_directory

# Run the main.py script
Write-Host "Database info:" -ForegroundColor Yellow
python main.py
