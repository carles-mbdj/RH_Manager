from flask import Blueprint, make_response, render_template, redirect, url_for, flash, send_file
from app import db
import pandas as pd
from io import BytesIO
from weasyprint import HTML
from app.models import Employee, Absence, Conge
from app.forms import EmployeeForm, AbsenceForm, CongeForm
from flask_login import login_required
from app.utils.permissions import permission_requise

rh_bp = Blueprint('rh', __name__)

#***************************************************************ADD ON DATA BASE****************************************************************

# ---- Employés ----
@rh_bp.route('/employes')
@login_required
@permission_requise('employes')
def list_employes():
    employes = Employee.query.all()
    form = EmployeeForm()
    return render_template('employes/list.html', employes=employes, form=form)

@rh_bp.route('/employes/add', methods=['POST'])
def add_employe():
    form = EmployeeForm()
    if form.validate_on_submit():
        employe = Employee(
            nom=form.nom.data,
            poste=form.poste.data,
            departement=form.departement.data,
            email=form.email.data,
            telephone=form.telephone.data,
            type_contrat=form.type_contrat.data,
            date_embauche=form.date_embauche.data,
            statut=form.statut.data
        )
        db.session.add(employe)
        db.session.commit()
        flash("L'employé a été ajouté avec succès.", "success")
    else:
        flash("Erreur lors de l'ajout de l'employe. Vérifiez le formulaire.", "danger")

    return redirect(url_for('rh.list_employes'))

# ---- Absences ----
@rh_bp.route('/absences')
@login_required
@permission_requise('absences_conges')
def list_absences():
    absences = Absence.query.all()
    form = AbsenceForm()
    return render_template('absences/list.html', absences=absences, form=form)

@rh_bp.route('/absences/add', methods=['POST'])
def add_absence():
    form = AbsenceForm()
    if form.validate_on_submit():
        absence = Absence(
            employee_id=form.employee_id.data,
            type_absence=form.type_absence.data,
            date_debut=form.date_debut.data,
            date_fin=form.date_fin.data,
            motif=form.motif.data,
            justificatif=form.justificatif.data,
            statut=form.statut.data
        )
        db.session.add(absence)
        db.session.commit()
        flash("L'absence a été ajouté avec succès.", "success")
    else:
        flash("Erreur lors de l'ajout de l'absence. Vérifiez le formulaire.", "danger")

    return redirect(url_for('rh.list_absences'))

# ---- Congés ----
@rh_bp.route('/conges')
@login_required
@permission_requise('absences_conges')
def list_conges():
    conges = Conge.query.all()
    form = CongeForm()
    return render_template('conges/list.html', conges=conges, form=form)

@rh_bp.route('/conges/add', methods=['POST'])
def add_conge():
    form = CongeForm()
    if form.validate_on_submit():
        conge = Conge(
            employee_id=form.employee_id.data,
            type_conge=form.type_conge.data,
            date_debut=form.date_debut.data,
            date_fin=form.date_fin.data,
            motif=form.motif.data,
            statut=form.statut.data
        )
        db.session.add(conge)
        db.session.commit()
        flash("Le congé a été ajouté avec succès.", "success")
    else:
        flash("Erreur lors de l'ajout du congé. Vérifiez le formulaire.", "danger")

    return redirect(url_for('rh.list_conges'))
    
#***************************************************************UPDATE ON DATA BASE***********************************************************

# Modifier un employé
@rh_bp.route('/employes/edit/<int:id>', methods=['POST'])
def edit_employe(id):
    employe = Employee.query.get_or_404(id)
    form = EmployeeForm()

    if form.validate_on_submit():
        employe.nom = form.nom.data
        employe.poste = form.poste.data
        employe.departement = form.departement.data
        employe.email = form.email.data
        employe.telephone = form.telephone.data
        employe.type_contrat = form.type_contrat.data
        employe.date_embauche = form.date_embauche.data
        employe.statut = form.statut.data

        db.session.commit()
        flash(f"L'employé {employe.nom} a été modifié avec succès.", "success")
        return redirect(url_for('rh.list_employes'))
    
    return redirect(url_for('rh.list_employes'))

# Modifier une absence
@rh_bp.route('/absences/edit/<int:id>', methods=['POST'])
def edit_absence(id):
    absence = Absence.query.get_or_404(id)
    form = AbsenceForm()

    if form.validate_on_submit():
        absence.employee_id = form.employee_id.data
        absence.type_absence = form.type_absence.data
        absence.date_debut = form.date_debut.data
        absence.date_fin = form.date_fin.data
        absence.motif = form.motif.data
        absence.justificatif = form.justificatif.data
        absence.statut = form.statut.data

        db.session.commit()
        flash("L'absence a été modifiée avec succès.", "success")
        return redirect(url_for('rh.list_absences'))

    return redirect(url_for('rh.list_absences'))

# Modifier un congé
@rh_bp.route('/conges/edit/<int:id>', methods=['POST'])
def edit_conge(id):
    conge = Conge.query.get_or_404(id)
    form = CongeForm()

    if form.validate_on_submit():
        conge.employee_id = form.employee_id.data
        conge.type_conge = form.type_conge.data
        conge.date_debut = form.date_debut.data
        conge.date_fin = form.date_fin.data
        conge.motif = form.motif.data
        conge.statut = form.statut.data

        db.session.commit()
        flash("Le congé a été modifié avec succès.", "success")
        return redirect(url_for('rh.list_conges'))

    return redirect(url_for('rh.list_conges'))


#****************************************************************DELETE ON DATA BASE**********************************************************

# Supprimer un employé
@rh_bp.route('/employes/delete/<int:id>', methods=['POST'])
def delete_employe(id):
    employe = Employee.query.get_or_404(id)
    db.session.delete(employe)
    db.session.commit()
    flash(f"L'employé {employe.nom} a été supprimé.", "success")
    return redirect(url_for('rh.list_employes'))

# Supprimer une absence
@rh_bp.route('/absences/delete/<int:id>', methods=['POST'])
def delete_absence(id):
    absence = Absence.query.get_or_404(id)
    db.session.delete(absence)
    db.session.commit()
    flash("L'absence a été supprimée avec succès.", "success")
    return redirect(url_for('rh.list_absences'))

# Supprimer un congé
@rh_bp.route('/conges/delete/<int:id>', methods=['POST'])
def delete_conge(id):
    conge = Conge.query.get_or_404(id)
    db.session.delete(conge)
    db.session.commit()
    flash("Le congé a été supprimé avec succès.", "success")
    return redirect(url_for('rh.list_conges'))


#*************************************************************************VIEW****************************************************************

# Detail employé
@rh_bp.route("/employes/<int:id>")
def detail_employe(id):
    employe = Employee.query.get_or_404(id)
    return render_template("employe_detail.html", employe=employe)

#***************************************************************EXPORT***********************************************************************

# Exportation employés Excel et PDF
@rh_bp.route('/employes/export/excel')
def export_employes_excel():
    employes = Employee.query.all()
    data = [{
        "Nom": emp.nom,
        "Poste": emp.poste,
        "Département": emp.departement,
        "Email": emp.email,
        "Téléphone": emp.telephone,
        "Contrat": emp.type_contrat,
        "Date embauche": emp.date_embauche
    } for emp in employes]

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Employés')
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="employes.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@rh_bp.route('/employes/export/pdf')
def export_employes_pdf():
    employes = Employee.query.all()
    rendered = render_template('employes/employes_pdf.html', employes=employes)
    pdf = HTML(string=rendered).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=employes.pdf'
    return response

# Exportation Absences Excel et PDF 
@rh_bp.route('/absences/export/excel')
def export_absences_excel():
    absences = Absence.query.all()
    data = [{
        #'Employé': absence.employe.nom,
        'Type': absence.type_absence,
        'Période': f"{absence.date_debut.strftime('%d/%m/%Y')} - {absence.date_fin.strftime('%d/%m/%Y')}",
        'Durée': f"{absence.duree} jours",
        'Justificatif': absence.justificatif,
        'Statut': absence.statut
    } for absence in absences]

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Absences')

    output.seek(0)
    return send_file(output, download_name="absences.xlsx", as_attachment=True)

@rh_bp.route('/absences/export/pdf')
def export_absences_pdf():
    absences = Absence.query.all()
    rendered = render_template('absences/absences_pdf.html', absences=absences)
    pdf = HTML(string=rendered).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=absences.pdf'
    return response

# Exportation Congés Excel et PDF 
@rh_bp.route('/conges/export/excel')
def export_conges_excel():
    conges = Conge.query.all()
    data = [{
        #'Employé': conge.employe.nom, 
        'Type': conge.type_conge,
        'Date Début': conge.date_debut.strftime('%d/%m/%Y'),
        'Date Fin': conge.date_fin.strftime('%d/%m/%Y'),
        'Motif': conge.motif,
        'Statut': conge.statut
    } for conge in conges]

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Conges')

    output.seek(0)
    return send_file(output, download_name="conges.xlsx", as_attachment=True)

@rh_bp.route('/conges/export/pdf')
def export_conges_pdf():
    conges = Conge.query.all()
    rendered = render_template('conges/conges_pdf.html', conges=conges)
    pdf = HTML(string=rendered).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=conges.pdf'
    return response