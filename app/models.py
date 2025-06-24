from . import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    poste = db.Column(db.String(100))
    departement = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    type_contrat = db.Column(db.String(50))
    date_embauche = db.Column(db.Date)
    statut = db.Column(db.String(50))

    def __repr__(self):
        return f"<Employee {self.nom}>"

class Absence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    type_absence = db.Column(db.String(100))
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    motif = db.Column(db.Text)
    justificatif = db.Column(db.Boolean)
    statut = db.Column(db.String(50))

class Conge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    type_conge = db.Column(db.String(100))
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    motif = db.Column(db.Text)
    statut = db.Column(db.String(50))
    employe = db.relationship('Employee', backref='conges')

class OffreEmploi(db.Model):
    __tablename__ = 'offre_emploi'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    departement = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    date_publication = db.Column(db.Date, default=datetime.utcnow)
    date_cloture = db.Column(db.Date)
    date_suppression = db.Column(db.Date)
    statut = db.Column(db.String(50), default='Brouillon')

    candidats = db.relationship('Candidat', backref='offre', cascade='all, delete-orphan', lazy=True)
    entretiens = db.relationship('Entretien', backref='offre', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f"<OffreEmploi {self.titre} ({self.statut})>"

class Candidat(db.Model):
    __tablename__ = 'candidat'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    cv = db.Column(db.String(200))  # Chemin fichier CV
    lettre_motivation = db.Column(db.String(200))  # Chemin fichier lettre
    date_soumission = db.Column(db.Date, default=datetime.utcnow)
    statut = db.Column(db.String(50), default='en cours d\'examen')

    offre_emploi_id = db.Column(db.Integer, db.ForeignKey('offre_emploi.id'), nullable=False)
    entretiens = db.relationship('Entretien', backref='candidat', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f"<Candidat {self.nom} ({self.statut})>"

class Entretien(db.Model):
    __tablename__ = 'entretien'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    duree = db.Column(db.Integer)  # durée en minutes
    participants = db.Column(db.String(255))
    notes = db.Column(db.Text)

    offre_emploi_id = db.Column(db.Integer, db.ForeignKey('offre_emploi.id'), nullable=False)
    candidat_id = db.Column(db.Integer, db.ForeignKey('candidat.id'), nullable=False)

    def __repr__(self):
        return f"<Entretien {self.titre} pour candidat {self.candidat_id}>"

class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(20), unique=True, nullable=False)
    photo_profil = db.Column(db.String(200))
    role = db.Column(db.String(50), default='Utilisateur')
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    derniere_connexion = db.Column(db.DateTime)
