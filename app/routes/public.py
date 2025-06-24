# app/routes/public.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from app import db, mail
from app.models import OffreEmploi, Candidat
from flask_mail import Message

public_bp = Blueprint('public', __name__)

# Dossier pour stocker CV + lettres
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Vérifie l'extension (PDF only)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@public_bp.route('/candidature/<int:offre_id>', methods=['GET', 'POST'])
def postuler(offre_id):
    offre = OffreEmploi.query.get_or_404(offre_id)

    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        telephone = request.form['telephone']
        cv_file = request.files['cv']
        lettre_file = request.files['lettre']

        # Vérifie les fichiers
        if not (cv_file and allowed_file(cv_file.filename)) or not (lettre_file and allowed_file(lettre_file.filename)):
            flash("Veuillez télécharger des fichiers PDF valides.", "danger")
            return redirect(request.url)

        # Renomme et sauvegarde fichiers
        timestamp = int(datetime.utcnow().timestamp())
        cv_filename = secure_filename(f"{timestamp}_CV_{cv_file.filename}")
        lettre_filename = secure_filename(f"{timestamp}_Lettre_{lettre_file.filename}")

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crée dossier si pas présent
        cv_file.save(os.path.join(UPLOAD_FOLDER, cv_filename))
        lettre_file.save(os.path.join(UPLOAD_FOLDER, lettre_filename))

        # Crée le candidat en base
        candidat = Candidat(
            nom=nom,
            email=email,
            telephone=telephone,
            cv=cv_filename,
            lettre_motivation=lettre_filename,
            date_soumission=datetime.utcnow().date(),
            statut='en cours d\'examen',
            offre_emploi_id=offre.id
        )
        db.session.add(candidat)
        db.session.commit()

        # Envoie un mail interne sans pièce jointe
#        subject = f"Nouvelle candidature pour {offre.titre}"
#        body = f"""
#        Nouvelle candidature reçue :

#        Nom : {nom}
#        Email : {email}
#        Offre : {offre.titre}
#        """

#        msg = Message(subject, recipients=['mbiadjeutenga@gmail.com']) 
#        msg.body = body
#        mail.send(msg)

        flash("Votre candidature a bien été envoyée ! Merci.", "success")
        return redirect(url_for('public.postuler', offre_id=offre.id))

    return render_template('public/candidature.html', offre=offre)
