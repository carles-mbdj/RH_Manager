from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.forms import FormUtilisateur, RoleForm
from flask_login import login_required
from app.models import Utilisateur, Role, Permission

parametres_bp = Blueprint('parametres', __name__)

@parametres_bp.route('/parametres', methods=['GET', 'POST'])
@login_required
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

@parametres_bp.route('/parametres/utilisateurs/<int:id>/modifier', methods=['POST'])
@login_required
def modifier_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    utilisateur.nom_utilisateur = request.form['nom_utilisateur']
    utilisateur.nom_complet = request.form['nom_complet']
    utilisateur.email = request.form['email']
    utilisateur.role = request.form['role']
    utilisateur.actif = 'actif' in request.form  
    db.session.commit()
    flash("Utilisateur modifié avec succès", "success")
    return redirect(url_for('parametres.utilisateurs'))

@parametres_bp.route('/parametres/utilisateurs/<int:id>/supprimer', methods=['POST'])
@login_required
def supprimer_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    db.session.delete(utilisateur)
    db.session.commit()
    flash("Utilisateur supprimé avec succès", "success")
    return redirect(url_for('parametres.utilisateurs'))

@parametres_bp.route('/parametres/roles')
@login_required
def roles():
    roles = Role.query.all()
    permissions = Permission.query.all()
    return render_template('parametres/roles.html', roles=roles, permissions=permissions)

@parametres_bp.route('/parametres/roles', methods=['GET', 'POST'])
def ajouter_role():
    form = RoleForm()
    if form.validate_on_submit():
        permissions = {
            'employes': form.emp_perm.data,
            'conges': form.conge_perm.data,
            'paie': form.paie_perm.data,
            'recrutement': form.recrutement_perm.data,
            'parametres': form.parametre_perm.data,
        }
        nouveau_role = Role(nom=form.nom.data, permissions=permissions)
        db.session.add(nouveau_role)
        db.session.commit()
        flash('Rôle ajouté avec succès.', 'success')
        return redirect(url_for('rh.ajouter_role'))

    roles = Role.query.all()
    return render_template('parametres/utilisateurs.html', form=form, roles=roles)
