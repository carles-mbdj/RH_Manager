from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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
    __tablename__ = 'absence'
    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    date = db.Column(db.Date, nullable=False)
    motif = db.Column(db.String(100), nullable=False)
    justificatif = db.Column(db.String(200))  # fichier PDF/image
    etat = db.Column(db.String(50), default='En attente')  # En attente, Justifiée, Non justifiée
    impact_paie = db.Column(db.Boolean, default=False)

    employe = db.relationship('Employee', backref='absences')

class Conge(db.Model):
    __tablename__ = 'conge'
    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Exemple : "Congé annuel", "Maladie", etc.
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    motif = db.Column(db.String(255))
    statut = db.Column(db.String(20), default='En attente')  # En attente, Approuvé, Rejeté

    employe = db.relationship("Employee", backref="conges")

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

class Evaluation(db.Model):
    __tablename__ = 'evaluation'
    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    periode = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    commentaire = db.Column(db.Text, nullable=True)
    date_evaluation = db.Column(db.Date, default=datetime.utcnow)

    employe = db.relationship('Employee', backref='evaluations')

class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'utilisateur'
    id = db.Column(db.Integer, primary_key=True)
    nom_utilisateur = db.Column(db.String(64), unique=True, nullable=False)
    nom_complet = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    actif = db.Column(db.Boolean, default=True)
    role = db.relationship('Role', backref='utilisateurs')

    def set_password(self, mot_de_passe):
        self.mot_de_passe_hash = generate_password_hash(
            mot_de_passe,
            method='pbkdf2:sha256',
            salt_length=8
        )

    def check_password(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe)

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)
    permissions = db.relationship('Permission', secondary='role_permission', backref='roles')

class Permission(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)

# Table d'association entre rôle et permission
role_permission = db.Table('role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)

class Presence(db.Model):
    __tablename__ = 'presence'
    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    heure_arrivee = db.Column(db.Time, nullable=True)
    heure_depart = db.Column(db.Time, nullable=True)
    retard_minutes = db.Column(db.Integer, default=0)

    employe = db.relationship("Employee", backref="presences")

class TypeConge(db.Model):
    __tablename__ = 'type_conge'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    duree_max_jours = db.Column(db.Integer, nullable=True)
    validation_requise = db.Column(db.Boolean, default=False)

class ParametresPaie(db.Model):
    __tablename__ = 'parametres_paie'
    id = db.Column(db.Integer, primary_key=True)
    smic_horaire = db.Column(db.Float, nullable=False)
    plafond_cnps = db.Column(db.Float, nullable=False)
    taux_transport = db.Column(db.Float, nullable=False)
    auto_calcule = db.Column(db.Boolean, default=False)
    jour_paiement = db.Column(db.Integer, nullable=False)
    heures_hebdo = db.Column(db.Integer, nullable=False)
    hs_25 = db.Column(db.Integer, nullable=False)
    hs_50 = db.Column(db.Integer, nullable=False)

class CotisationSociale(db.Model):
    __tablename__ = 'cotisation_sociale'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(100))
    taux_salarial = db.Column(db.Float)
    taux_patronal = db.Column(db.Float)

class ParametrePresence(db.Model):
    __tablename__ = 'parametre_presence'
    id = db.Column(db.Integer, primary_key=True)
    heure_arrivee = db.Column(db.Time, nullable=False)
    heure_depart = db.Column(db.Time, nullable=False)
    tolerance_retard = db.Column(db.Integer, default=15)  # en minutes
    notifier_retard = db.Column(db.Boolean, default=True)
    notifier_absence = db.Column(db.Boolean, default=True)

class DemandeConge(db.Model):
    __tablename__ = 'demande_conge'
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    type = db.Column(db.String(50))
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    duree = db.Column(db.Integer)
    motif = db.Column(db.Text)
    statut = db.Column(db.String(20), default='En attente')
    approbateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

class PresenceJournal(db.Model):
    __tablename__ = 'presence_journal'
    id = db.Column(db.Integer, primary_key=True)
    employe_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    date = db.Column(db.Date)
    heure_arrivee = db.Column(db.Time)
    heure_depart = db.Column(db.Time)
    retard_minutes = db.Column(db.Integer)
    heures_effectuees = db.Column(db.Float)
    statut = db.Column(db.String(20))  # Présent, Absent, En retard
