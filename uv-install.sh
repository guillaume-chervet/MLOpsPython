#!/usr/bin/env bash
# anciennement "poetry-install.sh" -> maintenant setup uv
set -euo pipefail

# --- helpers ---
have_cmd() { command -v "$1" >/dev/null 2>&1; }

# --- gestion du paramètre d'entrée ---
USE_FROZEN=true
if [[ "${1:-}" == "no-frozen" ]]; then
  echo ">> Paramètre 'no-frozen' détecté, les deps seront installés sans --frozen"
  USE_FROZEN=false
fi

FROZEN_FLAG=""
$USE_FROZEN && FROZEN_FLAG="--frozen"

# 1) Installer uv si absent (Linux/macOS). Sur CI, il est déjà installé.
if ! have_cmd uv; then
  echo ">> Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:${PATH}"
fi

uv --version

uv python install 3.12

# 2) Verrouiller et installer les deps du workspace
echo ">> uv lock (root)"
uv sync $FROZEN_FLAG

echo ">> uv sync (root, dev group)"
uv sync --group dev $FROZEN_FLAG

# 3) Préparer les sous-projets
echo ">> uv sync subprojects (no-dev)"
( cd packages/mlopspython-extraction && uv sync --no-dev $FROZEN_FLAG )
( cd packages/mlopspython-inference && uv sync --no-dev $FROZEN_FLAG )
( cd production/api && uv sync --no-dev $FROZEN_FLAG )
( cd production/integration && uv sync --no-dev $FROZEN_FLAG || true )
( cd train/extraction && uv sync --no-dev $FROZEN_FLAG || true )
( cd train/label_split_data && uv sync --no-dev $FROZEN_FLAG || true )
( cd train/output && uv sync --no-dev $FROZEN_FLAG || true )
( cd train/test && uv sync --no-dev $FROZEN_FLAG || true )
( cd train/train && uv sync --no-dev $FROZEN_FLAG || true )

echo ">> uv setup complete."
