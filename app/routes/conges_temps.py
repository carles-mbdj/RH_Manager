from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required
from app.models import Conge, PresenceJournal, Employee, Absence, DemandeConge
from app.forms import AbsenceForm
from app import db
import os
from app.utils.permissions import permission_requise
from werkzeug.utils import secure_filename

conges_temps_bp = Blueprint('conges_temps', __name__, template_folder='../templates/conges_temps')

@conges_temps_bp.route('/conges_temps')
@login_required
@permission_requise('absences_conges')
def conges():
    conges = Conge.query.all()
    return render_template('conges_temps/index.html', active_tab='conges', conges=conges, presences=[])

@conges_temps_bp.route('/conges_temps/presences')
@login_required
def presences():
    presences = PresenceJournal.query.all()
    return render_template('conges_temps/index.html', active_tab='presences', conges=[], presences=presences)

@conges_temps_bp.route('/conges-temps/absences', methods=['GET', 'POST'])
@login_required
def absences():
    form_absence = AbsenceForm()
    form_absence.employe_id.choices = [(emp.id, emp.nom) for emp in Employee.query.all()]
    absences = Absence.query.order_by(Absence.date_absence.desc()).all()

    if form_absence.validate_on_submit():
        fichier = form_absence.justificatif.data
        filename = None
        if fichier:
            filename = secure_filename(fichier.filename)
            fichier.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        absence = Absence(
            employe_id=form_absence.employe_id.data,
            date_absence=form_absence.date_absence.data,
            motif=form_absence.motif.data,
            justificatif=filename
        )
        db.session.add(absence)
        db.session.commit()
        flash("Absence enregistrée avec succès", "success")
        return redirect(url_for('conges_temps.absences'))

    return render_template('conges_temps/index.html', active_tab='absences', form=form_absence, absences=absences)

@conges_temps_bp.route('/absences/<int:id>/valider', methods=['POST'])
@login_required
def valider_absence(id):
    absence = Absence.query.get_or_404(id)
    absence.statut = "Justifiée"
    db.session.commit()
    flash("Absence justifiée", "success")
    return redirect(url_for('conges_temps.absences'))

@conges_temps_bp.route('/absences/<int:id>/refuser', methods=['POST'])
@login_required
def refuser_absence(id):
    absence = Absence.query.get_or_404(id)
    absence.statut = "Non justifiée"
    db.session.commit()
    flash("Absence refusée", "danger")
    return redirect(url_for('conges_temps.absences'))

# ✅ Valider une demande
@conges_temps_bp.route('/demandes_conge/valider/<int:id>', methods=['POST'])
def valider_demande_conge(id):
    demande = DemandeConge.query.get_or_404(id)
    demande.statut = "Approuvé"
    db.session.commit()
    flash("Demande de congé approuvée avec succès.", "success")
    return redirect(url_for('conges_temps.demandes_conge'))

# ✅ Refuser une demande avec motif
@conges_temps_bp.route('/demandes_conge/rejeter/<int:id>', methods=['POST'])
def rejeter_demande_conge(id):
    motif_refus = request.form.get('motif_refus', '')
    if not motif_refus.strip():
        flash("Le motif de refus est requis.", "danger")
        return redirect(url_for('conges_temps.demandes_conge'))

    demande = DemandeConge.query.get_or_404(id)
    demande.statut = f"Rejeté - {motif_refus}"
    db.session.commit()
    flash("Demande de congé rejetée avec motif.", "warning")
    return redirect(url_for('conges_temps.demandes_conge'))