FROM python:3.11.9 AS builder
WORKDIR /app

SHELL ["/bin/bash", "-lc"]
# Installer uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Copie minimale pour la résolution des deps + packages locaux
COPY pyproject.toml uv.lock* ./          # racine monorepo si nécessaire
COPY packages/ packages/
COPY production/api/pyproject.toml production/api/pyproject.toml

WORKDIR /app/production/api
# Créer le venv + installer les deps (sans les dev)
RUN uv venv && source .venv/bin/activate && uv sync --no-dev --frozen

# Copier le reste du code de l'API
COPY production/api/ ./


# --------- final ----------
FROM python:3.11.9-slim
WORKDIR /app

# Utilisateur non-root
RUN useradd -ms /bin/bash newuser

# Copier le venv et l'app depuis le builder
COPY --from=builder /app/production/api/.venv /app/.venv
COPY --from=builder /app/production/api/ ./ 

# Droits + PATH vers le venv
RUN chown -R newuser:newuser /app
USER newuser
ENV PATH="/app/.venv/bin:${PATH}"

CMD ["python", "./main.py"]