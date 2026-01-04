# ============================
# Discord Bot Launcher (Windows)
# ============================

$ErrorActionPreference = "Stop"

# Resolve repo root (two levels up from Deploy\Windows)
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $RepoRoot

# Load .env (simple KEY=VALUE, no quotes)
$EnvFile = Join-Path $RepoRoot ".env"
if (-not (Test-Path $EnvFile)) {
    throw ".env not found at $EnvFile"
}

Get-Content $EnvFile | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
        $k, $v = $line.Split("=", 2)
        [Environment]::SetEnvironmentVariable($k.Trim(), $v.Trim(), "Process")
    }
}

$RepoDir = $env:REPO_DIR
$Entry   = $env:ENTRYPOINT
$VenvDir = $env:VENV_DIR

if (-not $RepoDir) { throw "REPO_DIR missing in .env" }
if (-not $Entry)   { throw "ENTRYPOINT missing in .env" }
if (-not $VenvDir) { $VenvDir = ".venv" }

$PythonW = Join-Path $RepoDir "$VenvDir\Scripts\pythonw.exe"
if (-not (Test-Path $PythonW)) {
    throw "pythonw.exe not found at $PythonW"
}

# Launch bot (windowless, detached)
Start-Process `
    -FilePath $PythonW `
    -ArgumentList $Entry `
    -WorkingDirectory $RepoDir `
    -NoNewWindow
