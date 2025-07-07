#!/bin/bash
set -e

# Vérifie que Docker est installé
command -v docker &>/dev/null || { echo "Docker n'est pas installé. Installez-le d'abord." >&2; exit 1; }

DOCKER_IMAGE=debian:bookworm
PROJECT_DIR=$(pwd)

VERSION=$(awk '/\[workspace.package\]/ {found=1} found && /^version/ {gsub(/\"/, "", $3); print $3; exit}' Cargo.toml)
PKG_NAME="TEV-${VERSION}.deb"

DOCKER_CMD="
  apt-get update &&
  apt-get install -y dpkg-dev &&
  dpkg-deb --build mypackage &&
  mv mypackage.deb $PKG_NAME &&
  chown $(id -u):$(id -g) $PKG_NAME
"

echo "Lancement du build dans Docker..."
docker run --rm -v "$PROJECT_DIR":/workspace -w /workspace $DOCKER_IMAGE bash -c "$DOCKER_CMD"
echo "Fichier .deb généré dans : $PROJECT_DIR/$PKG_NAME"