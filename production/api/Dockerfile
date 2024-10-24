# Étape 1 : Image de construction
FROM python:3.10.15 AS builder

# Définir le répertoire de travail
WORKDIR /app

# Installer Poetry
ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==${POETRY_VERSION}"

# Copier le code de l'application
COPY . /app

# Configurer Poetry pour utiliser un environnement virtuel dans le projet
RUN poetry config virtualenvs.in-project true

# Installer les dépendances sans installer le package racine
RUN poetry install --no-root --only main

# Étape 2 : Image finale
FROM python:3.10.15-slim

# Créer un utilisateur non-root
RUN useradd -ms /bin/bash newuser

# Définir le répertoire de travail
WORKDIR /app

# Copier l'application et l'environnement virtuel depuis l'image de construction
COPY --from=builder /app /app

RUN ls -la /app/core/model

# Changer le propriétaire du répertoire de l'application
RUN chown -R newuser:newuser /app

# Passer à l'utilisateur non-root
USER newuser

RUN ls -la /app/core/model

# Ajouter l'environnement virtuel au PATH
ENV PATH="/app/.venv/bin:${PATH}"

# Démarrer l'application
CMD ["python", "./main.py"]