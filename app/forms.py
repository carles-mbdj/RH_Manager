from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, BooleanField, TextAreaField, SelectField, PasswordField, IntegerField, DecimalField, FloatField, TimeField, FileField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileAllowed

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
    role = QuerySelectField('Rôle', get_label='nom', allow_blank=False)
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    actif = BooleanField('Compte actif', default=True)
    submit = SubmitField('Ajouter')

class AjouterRoleForm(FlaskForm):
    nom = StringField('Nom du rôle', validators=[DataRequired()])
    submit = SubmitField("Ajouter")

class ModifierMonCompteForm(FlaskForm):
    nom_utilisateur = StringField('Nom d’utilisateur', validators=[DataRequired()])
    nom_complet = StringField('Nom complet')
    email = StringField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Nouveau mot de passe', validators=[Optional()])
    submit = SubmitField('Enregistrer')

class AjouterTypeCongeForm(FlaskForm):
    nom = StringField('Nom du congé', validators=[DataRequired()])
    duree_max_jours = IntegerField('Durée maximale (en jours)', validators=[DataRequired()])
    validation_requise = BooleanField('Validation requise ?')
    submit = SubmitField('Ajouter')

class FormParametresPaie(FlaskForm):
    smic_horaire = DecimalField("SMIC horaire (fcfa)", validators=[DataRequired(), NumberRange(min=0)], places=0)
    plafond_cnps = DecimalField("Plafond CNPS (fcfa)", validators=[DataRequired(), NumberRange(min=0)], places=0)
    #taux_transport = DecimalField("Taux versement transport (fcfa)", validators=[DataRequired(), NumberRange(min=0)], places=2)

    auto_calcule = BooleanField("Calcul automatique des bulletins")
    jour_paiement = SelectField("Jour de versement de la paie", coerce=int, choices=[(i, str(i)) for i in range(1, 32)])

    heures_hebdo = IntegerField("Heures hebdomadaires", validators=[DataRequired()])
    hs_25 = IntegerField("Taux majoration HS 25%", validators=[DataRequired()])
    hs_50 = IntegerField("Taux majoration HS 50%", validators=[DataRequired()])

    submit = SubmitField("Enregistrer les modifications")

class FormAjouterCotisation(FlaskForm):
    libelle = StringField("Libellé", validators=[DataRequired()])
    taux_salarial = FloatField("Taux salarial (%)", validators=[DataRequired()])
    taux_patronal = FloatField("Taux patronal (%)", validators=[DataRequired()])
    submit = SubmitField("Ajouter")

class FormParametrePresence(FlaskForm):
    heure_arrivee = TimeField("Heure d’arrivée", validators=[DataRequired()])
    heure_depart = TimeField("Heure de départ", validators=[DataRequired()])
    tolerance_retard = IntegerField("Tolérance de retard (minutes)", validators=[DataRequired()])
    notifier_retard = BooleanField("Notifier en cas de retard")
    notifier_absence = BooleanField("Notifier en cas d’absence")
    submit = SubmitField("Enregistrer")

class AbsenceForm(FlaskForm):
    employe_id = SelectField("Employé", coerce=int, validators=[DataRequired()])
    date = DateField("Date de l’absence", format='%Y-%m-%d', validators=[DataRequired()])
    motif = StringField("Motif", validators=[DataRequired()])
    justificatif = FileField("Justificatif (PDF ou image)", validators=[FileAllowed(['pdf', 'jpg', 'png', 'jpeg'], 'Fichier invalide')])
    impact_paie = BooleanField("Impacter la paie ?")
    submit = SubmitField("Enregistrer")
