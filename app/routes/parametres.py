from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.forms import FormUtilisateur, AjouterRoleForm, ModifierMonCompteForm
from flask_login import login_required, current_user
from app.models import Utilisateur, Role, Permission
from app.utils.permissions import permission_requise


parametres_bp = Blueprint('parametres', __name__)

@parametres_bp.route('/parametres', methods=['GET', 'POST'])
@login_required
@permission_requise('parametres')
def utilisateurs():
    form = FormUtilisateur()
    form.role.query = Role.query.all()
    form_role = AjouterRoleForm()
    utilisateurs = Utilisateur.query.all()
    roles = Role.query.all()
    permissions = Permission.query.all()

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

    return render_template('parametres/utilisateurs.html', form=form, form_role=form_role, utilisateurs=utilisateurs, roles=roles, permissions=permissions)

@parametres_bp.route('/parametres/utilisateurs/<int:id>/modifier', methods=['POST'])
@login_required
def modifier_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    utilisateur.nom_utilisateur = request.form['nom_utilisateur']
    utilisateur.nom_complet = request.form['nom_complet']
    utilisateur.email = request.form['email']
    role_id = int(request.form['role'])
    utilisateur.role = Role.query.get(role_id)

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

@parametres_bp.route('/parametres/ajouter-role', methods=['POST'])
@login_required
def ajouter_role():
    nom = request.form.get('nom')
    if nom:
        nouveau_role = Role(nom=nom)
        db.session.add(nouveau_role)
        db.session.commit()
        flash("Rôle ajouté avec succès.", "success")
    return redirect(url_for('parametres.utilisateurs'))

@parametres_bp.route('/parametres/modifier-permissions/<int:role_id>', methods=['POST'])
@login_required
def modifier_permissions(role_id):
    role = Role.query.get_or_404(role_id)
    selected_permissions_ids = request.form.getlist('permissions')
    selected_permissions = Permission.query.filter(Permission.id.in_(selected_permissions_ids)).all()
    role.permissions = selected_permissions
    db.session.commit()
    flash("Permissions mises à jour.", "success")
    return redirect(url_for('parametres.utilisateurs'))

@parametres_bp.route('/mon-compte', methods=['POST'])
@login_required
def modifier_mon_compte():
    form = ModifierMonCompteForm()
    if form.validate_on_submit():
        utilisateur = Utilisateur.query.get(current_user.id)
        utilisateur.nom_utilisateur = form.nom_utilisateur.data
        utilisateur.nom_complet = form.nom_complet.data
        utilisateur.email = form.email.data

        if form.mot_de_passe.data:
            utilisateur.set_password(form.mot_de_passe.data)

        db.session.commit()
        flash("Informations mises à jour avec succès.", "success")
    else:
        flash("Erreur lors de la modification du compte.", "danger")

    return redirect(request.referrer or url_for('dashboard.accueil'))
