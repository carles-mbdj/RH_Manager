from app import create_app, db
from app.models import Permission


app = create_app()

permissions = [
    {"nom": "Employés", "code": "employes"},
    {"nom": "Absences et Congés", "code": "absences_conges"},
    {"nom": "Évaluations", "code": "evaluations"},
    {"nom": "Paie", "code": "paie"},
    {"nom": "Recrutement", "code": "recrutement"},
    {"nom": "Paramètres", "code": "parametres"},
]

with app.app_context():
    for perm in permissions:
        # Évite les doublons
        if not Permission.query.filter_by(code=perm["code"]).first():
            new_perm = Permission(nom=perm["nom"], code=perm["code"])
            db.session.add(new_perm)

    db.session.commit()
    print("✅ Permissions ajoutées avec succès.")
