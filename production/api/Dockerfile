# --------- builder ----------
FROM python:3.10.15 AS builder
WORKDIR /app

SHELL ["/bin/bash", "-lc"]
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Copie minimale pour résoudre les deps + path locals
COPY pyproject.toml uv.lock* ./
COPY packages/ packages/
COPY production/api/pyproject.toml production/api/pyproject.toml
COPY production/api/packages/ production/api/packages/

WORKDIR /app/production/api
RUN uv sync --no-dev

# Copier le reste du code de l'API (si nécessaire)
COPY production/api/ ./

# --------- final ----------
FROM python:3.10.15-slim
WORKDIR /app

# Utilisateur non-root
RUN useradd -ms /bin/bash newuser

# Env virtuel prêt
COPY --from=builder /app/production/api/.venv /app/.venv
COPY --from=builder /app/production/api/ ./

RUN chown -R newuser:newuser /app
USER newuser

ENV PATH="/app/.venv/bin:${PATH}"
CMD ["python", "./main.py"]
