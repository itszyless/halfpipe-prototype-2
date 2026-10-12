# Run from the project folder after installing requirements.
$ErrorActionPreference = 'Stop'
$ProjectFolder = $PSScriptRoot
Set-Location -LiteralPath $ProjectFolder
python -m pip install 'pyinstaller==6.22.3'
if ($LASTEXITCODE -ne 0) { throw 'Could not install the packager.' }
python -c 'from vision import ensure_model; print(ensure_model())'
if ($LASTEXITCODE -ne 0) { throw 'Could not prepare the model.' }
if (-not (Test-Path -LiteralPath 'models/pose.onnx')) {
    New-Item -ItemType Directory -Path 'models' -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $env:LOCALAPPDATA 'Lip/pose.onnx') -Destination 'models/pose.onnx'
}
$PythonFile = (Get-Command python).Source
$SavedSearchPath = $env:PATH
$env:PATH = "$env:SystemRoot\System32;$env:SystemRoot"
try {
    & $PythonFile -m PyInstaller --noconfirm --clean --onedir --windowed --name Lip --icon assets/icon.ico --add-data 'assets;assets' --add-data 'docs;docs' --add-data 'models;models' --add-data 'LICENSE;.' --add-data 'THIRD_PARTY.md;.' app.py
} finally { $env:PATH = $SavedSearchPath }
if ($LASTEXITCODE -ne 0) { throw 'The desktop build failed.' }
Write-Host 'Open dist/Lip/Lip.exe. Keep its _internal folder beside it.'
