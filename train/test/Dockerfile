# ------------ base -------------
FROM python:3.10.15 AS base

# ------------ builder -----------
FROM base AS builder
WORKDIR /app
SHELL ["/bin/bash", "-lc"]

# uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# 1) Copier les manifestes NÉCESSAIRES depuis la RACINE
COPY pyproject.toml uv.lock* ./
COPY packages/ packages/
COPY train/test/pyproject.toml train/test/pyproject.toml

# 2) Installer dans le sous-projet
WORKDIR /app/train/test
RUN uv venv && source .venv/bin/activate && uv sync --no-dev

# 3) Copier le code (optionnel si déjà fait)
COPY train/test/ ./

# ------------ final -------------
FROM base AS final
WORKDIR /app
RUN useradd -r newuser
USER newuser
ENV PATH="/app/train/test/.venv/bin:${PATH}"

# On ne copie que l'env et le code du sous-projet
COPY --from=builder /app/train/test/.venv /app/train/test/.venv
COPY --from=builder /app/train/test/ /app/train/test/

# Point d’entrée — adapte si nécessaire
WORKDIR /app/train/test
