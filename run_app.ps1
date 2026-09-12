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
    Write-Error "Python 3.11 was not found. Run install_requirements.ps1 after installing Python 3.11."
    exit 1
}

& $python -m streamlit run (Join-Path $PSScriptRoot "app.py")
