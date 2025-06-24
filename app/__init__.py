from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

# Initialiser les extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Charger la configuration depuis config.py
    app.config.from_object('config.Config')

    # Initialiser les extensions avec l'application Flask
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Importer les modèles pour que Flask-Migrate les connaisse
    from . import models

    # Importer et enregistrer les Blueprints
    from .routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from .routes.recrutement import recrutement_bp
    app.register_blueprint(recrutement_bp)

    from .routes.rh import rh_bp
    app.register_blueprint(rh_bp)

    from .routes.public import public_bp
    app.register_blueprint(public_bp)

    return app
