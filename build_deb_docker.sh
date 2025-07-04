#!/bin/bash
# Script pour construire un paquet Debian dans Docker depuis macOS
set -e

# Vérifie que Docker est installé
if ! command -v docker &> /dev/null; then
  echo "Docker n'est pas installé. Installez-le d'abord." >&2
  exit 1
fi

# Lance le build dans un conteneur Debian
DOCKER_IMAGE=debian:bookworm
PROJECT_DIR=$(pwd)

# Commande à exécuter dans le conteneur
DOCKER_CMD='apt-get update && apt-get install -y dpkg-dev && dpkg-deb --build mypackage && chown $(id -u):$(id -g) mypackage.deb'

echo "Lancement du build dans Docker..."
docker run --rm -it -v "$PROJECT_DIR":/workspace -w /workspace $DOCKER_IMAGE bash -c "$DOCKER_CMD"

echo "\nFichier .deb généré dans : $PROJECT_DIR/mypackage.deb"
