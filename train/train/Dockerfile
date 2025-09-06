FROM python:3.11 AS base

FROM base AS builder
WORKDIR /app

# uv
RUN pip install --no-cache-dir uv

# copier le projet
COPY ./ /app/

# créer l'environnement
RUN uv venv
# (ne rien "activer" dans une étape RUN, ça n'a pas d'effet persistant)

# respecter timeouts réseau en build
ENV UV_HTTP_TIMEOUT=300
RUN uv sync --no-editable --frozen

# ---- final ----
FROM base AS final

# Créer un utilisateur AVEC home pour éviter les pb de cache Matplotlib/Fontconfig
RUN useradd -m -r -d /home/newuser newuser

# venv au PATH + backends headless
ENV PATH=/.venv/bin:${PATH} \
    MPLBACKEND=Agg \
    MPLCONFIGDIR=/home/newuser/.config/matplotlib \
    XDG_CACHE_HOME=/home/newuser/.cache

# Copier le venv
COPY --from=builder /app/.venv /.venv

# Pré-créer les dossiers de cache/config et donner les droits
RUN mkdir -p /home/newuser/.config/matplotlib /home/newuser/.cache && \
    chown -R newuser:newuser /home/newuser /.venv

USER newuser
WORKDIR /app
