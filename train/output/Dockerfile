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
COPY train/output/pyproject.toml train/output/pyproject.toml

# 2) Installer dans le sous-projet
WORKDIR /app/train/output
RUN uv venv && source .venv/bin/activate && uv sync --no-editable --no-dev

# 3) Copier le code (optionnel si déjà fait)
COPY train/output/ ./

# ------------ final -------------
FROM base AS final
WORKDIR /app
RUN useradd -r newuser
USER newuser
ENV PATH="/app/train/output/.venv/bin:${PATH}"

# On ne copie que l'env et le code du sous-projet
COPY --from=builder /app/train/output/.venv /app/train/output/.venv
COPY --from=builder /app/train/output/ /app/train/output/

# Point d’entrée — adapte si nécessaire
WORKDIR /app/train/output
