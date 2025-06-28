from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager

# Initialiser les extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()

from app.models import Utilisateur

login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    login_manager.init_app(app)
    
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

    from .routes.evaluation import evaluation_bp
    app.register_blueprint(evaluation_bp)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.parametres import parametres_bp
    app.register_blueprint(parametres_bp)

    return app


