# RH_Manager 

**RH_Manager** est un **Système de Gestion des Ressources Humaines (SIRH)** conçu pour les PME camerounaises.

## Fonctionnalités principales

- Gestion des informations sur les employés
- Gestion de la paie et des avantages sociaux
- Suivi des absences et des congés
- Gestion des performances et des évaluations
- Module de recrutement et intégration des candidats

## Technologies

- Python
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Mail
- MySQL

## Mise en place

```bash
# Clone le dépôt
git clone https://github.com/ton_utilisateur/RH_Manager.git

# Crée l'environnement virtuel
python -m venv venv

# Active l'environnement virtuel
# Windows :
venv\Scripts\activate
# Linux/macOS :
source venv/bin/activate

# Installe les dépendances
pip install -r requirements.txt

# Configure la base de données et initialise la migration
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Lancer l'application
flask run
