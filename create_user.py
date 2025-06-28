from app import create_app, db
from app.models import Utilisateur

app = create_app()

with app.app_context():
    user = Utilisateur.query.filter_by(email="admin@entreprise.com").first()
    if not user:
        user = Utilisateur(
            nom_utilisateur="admin",
            nom_complet="Administrateur RH",
            email="admin@entreprise.com",
            role="Administrateur",
            actif=True
        )
        user.set_password("admin123")
        db.session.add(user)
        db.session.commit()
        print("✅ Utilisateur créé")
    else:
        print("ℹ️ Utilisateur existe déjà")
