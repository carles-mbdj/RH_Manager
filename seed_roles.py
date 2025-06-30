from app import create_app, db
from app.models import Role, Permission

app = create_app()
with app.app_context():
    # Créer les permissions de base
    permissions_data = [
        ("Ajouter employé", "ajouter_employe"),
        ("Modifier employé", "modifier_employe"),
        ("Supprimer employé", "supprimer_employe"),
        ("Gérer congés", "gerer_conges"),
        ("Gérer absences", "gerer_absences"),
        ("Voir recrutements", "voir_recrutements"),
        ("Publier offre", "publier_offre"),
        ("Gérer utilisateurs", "gerer_utilisateurs"),
    ]

    for nom, code in permissions_data:
        if not Permission.query.filter_by(code=code).first():
            db.session.add(Permission(nom=nom, code=code))
    db.session.commit()

    # Créer rôle Administrateur avec toutes les permissions
    admin = Role.query.filter_by(nom='Administrateur').first()
    if not admin:
        admin = Role(nom='Administrateur')
        admin.permissions = Permission.query.all()
        db.session.add(admin)
        db.session.commit()

    print("✅ Rôles et permissions créés avec succès.")
