# Simeis TEV

[![CI](https://github.com/Valentin-Droid/simeis_TEV/actions/workflows/ci.yml/badge.svg)](https://github.com/Valentin-Droid/simeis_TEV/actions/workflows/ci.yml)

Un projet de jeu spatial développé en Rust avec une architecture modulaire.

## 🚀 Démarrage rapide

### Compilation et exécution

```bash
RUST_LOG=info cargo run
```

### Tests

```bash
cargo test --all-features --workspace
```

## 📁 Structure du projet

-   `simeis-data/` - Couche de données (structures de jeu, logique métier)
-   `simeis-server/` - Serveur et API
-   `example/` - Exemples d'utilisation et clients
-   `doc/` - Documentation du projet

## 🔧 Développement

### Prérequis

-   Rust 1.70+
-   Cargo

### Workflow de développement

1. **Créer une branche feature**

    ```bash
    git checkout -b feature/ma-nouvelle-fonctionnalite
    ```

2. **Développer et tester**

    ```bash
    cargo test
    cargo fmt
    cargo clippy
    ```

3. **Créer une Pull Request**
    - Le template PR vous guidera
    - Les reviewers sont assignés automatiquement
    - La CI vérifie automatiquement votre code

### CI/CD

Le projet utilise GitHub Actions pour :

-   ✅ Tests automatiques
-   ✅ Vérifications de format (rustfmt)
-   ✅ Linting (clippy)
-   ✅ Build en mode release
-   ✅ Audit de sécurité

## 📋 Contribution

1. Les Pull Requests doivent être approuvées par un code owner
2. Tous les status checks doivent passer
3. Utilisez les templates fournis pour les PR et issues
4. Suivez les conventions de code Rust standard

## 📚 Documentation

-   [Manuel utilisateur](doc/manual.pdf)
