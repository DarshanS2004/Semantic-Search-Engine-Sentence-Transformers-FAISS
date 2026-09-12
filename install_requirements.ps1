$pythonCandidates = @(
    (Join-Path $PSScriptRoot ".venv\Scripts\python.exe"),
    "C:\Users\darsh\AppData\Local\Programs\Python\Python311\python.exe"
)

$python = $null
foreach ($candidate in $pythonCandidates) {
    if (Test-Path $candidate) {
        $python = $candidate
        break
    }
}

if (-not $python) {
    Write-Error "Python 3.11 was not found. Install Python 3.11 or create a .venv in this project."
    exit 1
}

& $python -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")
