# Planificateur de Tâches — Sondeurs

Application de planification et gestion des tâches pour sondeurs avec interface graphique moderne et calcul d'empreinte carbone.

## Fonctionnalités

### 🎨 Interface Moderne

- Design moderne avec onglets et navigation intuitive
- Formulaires complets avec validation
- Icônes et code couleur pour une meilleure expérience utilisateur

### 📋 Gestion des Données

- **Sondeurs** : CRUD complet avec nom et adresse
- **Essais** : CRUD complet avec nom et description
- **Chantiers** : CRUD complet avec nom, lieu et date
- **Affectations** : Assignation d'essais à des chantiers avec sondeurs, durée et dates

### 🌱 Empreinte Carbone

- **Calcul automatique** : Distance de trajet calculée via Google Maps API
- **Formule** : Distance = (trajet × 2) × nombre de jours
- **Émissions CO₂** : Calcul basé sur un facteur d'émission de 0.120 kg/km
- **Rapports** : Résumé par sondeur et total général

## Installation et Utilisation

### Démarrage Rapide (PowerShell)

1. Créer et activer l'environnement virtuel

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Installer les dépendances

```powershell
pip install -r requirements.txt
```

3. Lancer l'application

```powershell
python -m src.main
```

## Architecture

### Structure Modulaire

```
src/
├── ui/                    # Modules d'interface utilisateur
│   ├── __init__.py
│   ├── main_window.py     # Fenêtre principale avec onglets
│   ├── forms.py           # Formulaires de saisie
│   ├── sondeur_view.py    # Vue de gestion des sondeurs
│   ├── essai_view.py      # Vue de gestion des essais
│   ├── chantier_view.py   # Vue de gestion des chantiers
│   └── affectation_view.py # Vue de gestion des affectations
├── models.py              # Modèles SQLAlchemy
├── db.py                  # Configuration base de données
└── main.py                # Point d'entrée
```

### Base de Données

- **SQLite** : Base de données locale `app.db`
- **SQLAlchemy** : ORM pour la gestion des données
- **Migration automatique** : Script `migrate_db.py` pour les mises à jour

## Utilisation

### 1. Gestion des Sondeurs

- Ajouter, modifier, supprimer des sondeurs
- Formulaire avec nom (obligatoire) et adresse (optionnelle)

### 2. Gestion des Essais

- Ajouter, modifier, supprimer des essais
- Formulaire avec nom (obligatoire) et description (optionnelle)

### 3. Gestion des Chantiers

- Ajouter, modifier, supprimer des chantiers
- Formulaire avec nom, lieu et date de début

### 4. Affectations

- Créer des unités de travail en associant :
  - Un chantier
  - Un essai
  - Un sondeur
  - Une durée en jours
  - Une date de début
- Plusieurs sondeurs peuvent être affectés au même essai/chantier
- Calcul automatique de l'empreinte carbone (si adresses disponibles)

### 5. Empreinte Carbone

- **Calcul automatique** lors de la création d'affectations
- **Formule** : Distance = (distance Google Maps × 2 aller-retour) × nombre de jours
- **Rapport détaillé** par sondeur avec totaux
- **Émissions CO₂** : 0.120 kg/km (facteur véhicule moyen)

## Améliorations Apportées

### ✅ Interface Utilisateur

- Remplacement des boîtes de dialogue simples par des formulaires complets
- Design moderne avec CSS styling
- Navigation par onglets avec nouvel onglet "Empreinte Carbone"
- Icônes et couleurs cohérentes

### ✅ Architecture

- Code modulaire avec séparation des responsabilités
- Formulaires réutilisables avec validation
- Gestion d'erreurs améliorée
- Calculs en arrière-plan (threads) pour ne pas bloquer l'interface

### ✅ Fonctionnalités

- **Calcul d'empreinte carbone** intégré avec Google Maps API
- Support de multiples affectations par essai/chantier
- Filtrage et recherche
- **Rapports environnementaux** avec totaux par sondeur
- Validation des données

### ✅ Base de Données

- Schema amélioré avec ID auto-incrémenté
- Migration automatique des données existantes
- Support des contraintes métier

## Configuration

### Dépendances

- **PyQt5** : Interface graphique
- **SQLAlchemy** : ORM base de données
- **Python 3.8+** : Version minimale requise

### Personnalisation

Le style de l'application peut être modifié dans `src/ui/main_window.py` et les formulaires dans `src/ui/forms.py`.

## Maintenance

### Migration de Base de Données

```powershell
python migrate_db.py
```

### Sauvegarde

La base de données SQLite `app.db` peut être sauvegardée en copiant le fichier.

## Langue

Interface entièrement en français avec messages d'erreur et confirmations localisés.
