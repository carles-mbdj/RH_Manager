# seed.py

from app import create_app, db
from app.models import OffreEmploi, Candidat, Entretien
from datetime import datetime, timedelta

# Crée l'app Flask
app = create_app()

with app.app_context():
    db.create_all()

    # 1) Créer des Offres
    offre1 = OffreEmploi(
        titre='Développeur Backend Python',
        departement='Informatique',
        description='Développement de services REST en Flask',
        requirements='Maîtrise de Flask, SQL, Git',
        date_publication=datetime.utcnow().date(),
        date_cloture=datetime.utcnow().date() + timedelta(days=30),
        statut='Actif'
    )
    offre2 = OffreEmploi(
        titre='Assistant RH',
        departement='Ressources Humaines',
        description='Support au recrutement et gestion administrative',
        requirements='Bon relationnel, maîtrise pack office',
        date_publication=datetime.utcnow().date(),
        date_cloture=datetime.utcnow().date() + timedelta(days=15),
        statut='Brouillon'
    )
    offre3 = OffreEmploi(
        titre='Chef de Projet IT',
        departement='Informatique',
        description='Gestion de projets numériques',
        requirements='Expérience en gestion de projet, Scrum',
        date_publication=datetime.utcnow().date(),
        date_cloture=datetime.utcnow().date() + timedelta(days=45),
        statut='Actif'
    )

    db.session.add_all([offre1, offre2, offre3])
    db.session.commit()

    # 2) Créer des Candidats pour chaque Offre
    for offre in [offre1, offre2, offre3]:
        for i in range(1, 4):  # 3 candidats par offre
            candidat = Candidat(
                nom=f"Candidat {i} pour {offre.titre}",
                email=f"candidat{i}@test.com",
                telephone=f"69195664{i}",
                cv='cv_test.pdf',
                lettre_motivation='lettre_test.pdf',
                date_soumission=datetime.utcnow().date(),
                statut='en cours d\'examen',
                offre_emploi_id=offre.id
            )
            db.session.add(candidat)
    db.session.commit()

    # 3) Créer un Entretien pour le premier candidat de la première offre
    premier_candidat = Candidat.query.filter_by(offre_emploi_id=offre1.id).first()
    if premier_candidat:
        entretien = Entretien(
            titre='Entretien technique Python',
            datetime=datetime.utcnow() + timedelta(days=2),
            duree=45,
            participants='Manager Technique, RH',
            notes='Prévoir questions Flask',
            candidat_id=premier_candidat.id,
            offre_emploi_id=offre1.id
        )
        premier_candidat.statut = 'entretien planifié'
        db.session.add(entretien)
    db.session.commit()

    print("✅ Données de test insérées avec succès !")
