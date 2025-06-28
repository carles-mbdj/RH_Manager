from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Utilisateur, db
from app.forms import FormUtilisateur

parametres_bp = Blueprint('parametres', __name__)

@parametres_bp.route('/parametres', methods=['GET', 'POST'])
def utilisateurs():
    form = FormUtilisateur()
    utilisateurs = Utilisateur.query.all()

    if form.validate_on_submit():
        nouvel_utilisateur = Utilisateur(
            nom_utilisateur=form.nom_utilisateur.data,
            nom_complet=form.nom_complet.data,
            email=form.email.data,
            role=form.role.data,
            actif=form.actif.data
        )
        nouvel_utilisateur.set_password(form.mot_de_passe.data)
        db.session.add(nouvel_utilisateur)
        db.session.commit()
        flash('Nouvel utilisateur ajouté avec succès', 'success')
        return redirect(url_for('parametres.utilisateurs'))

    return render_template('parametres/utilisateurs.html', form=form, utilisateurs=utilisateurs)
