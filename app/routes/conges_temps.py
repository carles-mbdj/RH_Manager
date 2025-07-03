from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required
from app.models import Conge, PresenceJournal, Employee, Absence
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
    form = AbsenceForm()
    form.employe_id.choices = [(e.id, e.nom) for e in Employee.query.all()]
    absences = Absence.query.order_by(Absence.date.desc()).all()
    absences = Absence.query.all()

    if form.validate_on_submit():
        filename = None
        if form.justificatif.data:
            file = form.justificatif.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        absence = Absence(
            employe_id=form.employe_id.data,
            date=form.date.data,
            motif=form.motif.data,
            justificatif=filename,
            impact_paie=form.impact_paie.data,
            etat="En attente"
        )
        db.session.add(absence)
        db.session.commit()
        flash("Absence enregistrée avec succès", "success")
        return redirect(url_for('conges_temps.absences'))

    return render_template('conges_temps/index.html', form_absence=form, absences=absences, active_tab='absences')
