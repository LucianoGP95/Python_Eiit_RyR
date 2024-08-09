# Start PowerShell in the current window (optional, not necessary for most scripts)
# Start-Process -FilePath "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -NoNewWindow

# Construct paths
$env_directory = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"
$src_directory = Join-Path $PSScriptRoot "app\src"

# Activate the virtual environment
& $env_directory
Write-Host "env succesfully activated: $env_directory" -ForegroundColor Green

# Change directory to the source directory
Set-Location $src_directory

# Run the main.py script
python main.py
