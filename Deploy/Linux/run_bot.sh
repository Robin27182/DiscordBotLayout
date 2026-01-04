#!/usr/bin/env bash
set -uo pipefail

# Repo root (Deploy/Linux -> repo root)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# If systemd already loads EnvironmentFile, you can delete this whole block.
# Keeping it only if you want the script to work when run manually too:
ENV_FILE="$REPO_ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

: "${PY_RUNNER:=system}"
: "${ENTRYPOINT:=bot.py}"
: "${VENV_DIR:=.venv}"

LOG_DIR="$REPO_ROOT/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/bot.log"
exec >>"$LOG_FILE" 2>&1

echo "========================================"
echo "[BOOT] $(date)"
echo "[INFO] REPO_ROOT=$REPO_ROOT"
echo "[INFO] PY_RUNNER=$PY_RUNNER"
echo "[INFO] ENTRYPOINT=$ENTRYPOINT"
echo "========================================"

python_cmd=(python)

if [[ "$PY_RUNNER" == "conda" ]]; then
  : "${CONDA_BASE:?Missing CONDA_BASE for PY_RUNNER=conda}"
  : "${ENV_NAME:?Missing ENV_NAME for PY_RUNNER=conda}"
  # shellcheck disable=SC1090
  source "$CONDA_BASE/etc/profile.d/conda.sh"
  conda activate "$ENV_NAME"
  python_cmd=(python)
elif [[ "$PY_RUNNER" == "venv" ]]; then
  python_cmd=("$REPO_ROOT/$VENV_DIR/bin/python")
elif [[ "$PY_RUNNER" == "system" ]]; then
  python_cmd=(python)
else
  echo "[FATAL] Unknown PY_RUNNER=$PY_RUNNER (use system|venv|conda)"
  exit 1
fi

echo "[GIT] Pulling latest code..."
git pull

echo "[PIP] Installing/upgrading dependencies..."
"${python_cmd[@]}" -m pip install -r requirements.txt --quiet

echo "[BOT] Starting..."
exec "${python_cmd[@]}" "$ENTRYPOINT"
