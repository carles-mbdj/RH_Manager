from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, BooleanField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class EmployeeForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    poste = StringField('Poste')
    departement = StringField('Département')
    email = StringField('Email', validators=[Email()])
    telephone = StringField('Téléphone')
    type_contrat = StringField('Type de contrat')
    date_embauche = DateField('Date d\'embauche', format='%Y-%m-%d')
    statut = StringField('Statut')
    submit = SubmitField('Enregistrer')

class AbsenceForm(FlaskForm):
    employee_id = StringField('ID Employé', validators=[DataRequired()])
    type_absence = StringField('Type d\'absence')
    date_debut = DateField('Date de début', format='%Y-%m-%d')
    date_fin = DateField('Date de fin', format='%Y-%m-%d')
    motif = TextAreaField('Motif')
    justificatif = BooleanField('Justificatif fourni')
    statut = StringField('Statut')
    submit = SubmitField('Enregistrer')

class CongeForm(FlaskForm):
    employee_id = StringField('ID Employé', validators=[DataRequired()])
    type_conge = StringField('Type de congé')
    date_debut = DateField('Date de début', format='%Y-%m-%d')
    date_fin = DateField('Date de fin', format='%Y-%m-%d')
    motif = TextAreaField('Motif')
    statut = StringField('Statut')
    submit = SubmitField('Enregistrer')

class RecrutementForm(FlaskForm):
    titre_poste = StringField('Titre du poste')
    departement = StringField('Département')
    description_poste = TextAreaField('Description du poste')
    prerequis = TextAreaField('Prérequis')
    date_cloture = DateField('Date de clôture', format='%Y-%m-%d')
    statut = StringField('Statut')
    submit = SubmitField('Enregistrer')

class FormUtilisateur(FlaskForm):
    nom_utilisateur = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(max=50)])
    nom_complet = StringField('Nom complet', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Rôle', choices=[('Administrateur', 'Administrateur'), ('RH', 'RH'), ('Comptable', 'Comptable'), ('Directeur', 'Directeur'), ('Employe', 'Employe')], validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    actif = BooleanField('Compte actif', default=True)
    submit = SubmitField('Ajouter')

class RoleForm(FlaskForm):
    nom = StringField('Nom du rôle', validators=[DataRequired()])
    emp_perm = BooleanField('Employés')
    conge_perm = BooleanField('Congés')
    paie_perm = BooleanField('Paie')
    recrutement_perm = BooleanField('Recrutement')
    parametre_perm = BooleanField('Paramètres')
    submit = SubmitField('Ajouter le rôle')