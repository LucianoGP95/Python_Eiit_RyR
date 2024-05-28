# Get the directory of the current script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Construct the path to the virtual environment activation script
$venvActivateScript = Join-Path $scriptDir ".venv\Scripts\Activate.ps1"

# Check if the virtual environment activation script exists
if (Test-Path $venvActivateScript -PathType Leaf) {
    # Activate the virtual environment
    & $venvActivateScript

    # Optional: Inform the user that the virtual environment is activated
    Write-Host "Virtual environment activated."
} else {
    # Virtual environment activation script not found
    Write-Host "Error: Virtual environment activation script not found." -ForegroundColor Red
    Write-Host "Please make sure the virtual environment is set up correctly." -ForegroundColor Red
}
