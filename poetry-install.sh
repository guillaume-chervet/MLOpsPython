#!/usr/bin/env bash
# anciennement "poetry-install.sh" -> maintenant setup uv
set -euo pipefail

# --- helpers ---
have_cmd() { command -v "$1" >/dev/null 2>&1; }

# 1) Installer uv si absent (Linux/macOS). Sur CI, il est déjà installé.
if ! have_cmd uv; then
  echo ">> Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # shellcheck disable=SC2086
  export PATH="$HOME/.local/bin:${PATH}"
fi

uv --version

# 2) Verrouiller et installer les deps du workspace
#    - à la racine: pyproject + [tool.uv.workspace]
echo ">> uv lock (root)"
uv lock

echo ">> uv sync (root, dev group)"
uv sync --group dev

# 3) Préparer quelques sous-projets clefs si besoin local (optionnel)
#    Tu peux commenter ces lignes si tu veux un setup minimal.
echo ">> uv sync subprojects (no-dev)"
#( cd production/api && uv sync --no-dev )
#( cd production/integration && uv sync --no-dev || true )
#( cd train/extraction && uv sync --no-dev || true )
#( cd train/label_split_data && uv sync --no-dev || true )
#( cd train/output && uv sync --no-dev || true )
#( cd train/test && uv sync --no-dev || true )
#( cd train/train && uv sync --no-dev || true )

echo ">> uv setup complete."
