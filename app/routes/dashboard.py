from flask import Blueprint, render_template
from app.models import Employee, Absence
from app import db
from datetime import date
from flask_login import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    total_employes = Employee.query.count()

    today = date.today()
    #absences_en_cours = Absence.query.filter(
    #    Absence.date_debut <= today,
    #    Absence.date_fin >= today
    #).count()

    #jours_conges_restants = db.session.query(db.func.sum(Employee.jours_conges_restants)).scalar() or 0

    dernier_recrutement = db.session.query(Employee).order_by(Employee.date_embauche.desc()).first()

    #return render_template('dashboard.html', total_employes=total_employes, absences_en_cours=absences_en_cours, dernier_recrutement=dernier_recrutement)
    return render_template('dashboard.html', total_employes=total_employes, dernier_recrutement=dernier_recrutement)
