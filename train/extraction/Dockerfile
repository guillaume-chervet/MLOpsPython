FROM python:3.10 AS builder

# Copie tout le contexte dans /app
COPY . /app

WORKDIR /app

# Affiche la liste des fichiers copiés (dans le contexte)
RUN echo "=== Contenu du contexte Docker (copié dans /app) ===" && \
    ls -alR /app