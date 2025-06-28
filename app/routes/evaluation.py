from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app import db
from app.models import Evaluation, Employee


evaluation_bp = Blueprint('evaluation', __name__)

@evaluation_bp.route('/employes/<int:employe_id>/evaluations')
def list_evaluations(employe_id):
    employe = Employee.query.get_or_404(employe_id)
    return render_template('evaluations/list.html', employe=employe)

@evaluation_bp.route('/employes/<int:employe_id>/evaluations/add', methods=['POST'])
def add_evaluation(employe_id):
    employe = Employee.query.get_or_404(employe_id)
    periode = request.form['periode']
    score = float(request.form['score'])
    commentaire = request.form['commentaire']

    evaluation = Evaluation(
        employe_id=employe_id,
        periode=periode,
        score=score,
        commentaire=commentaire,
        date_evaluation=datetime.utcnow()
    )

    db.session.add(evaluation)
    db.session.commit()
    flash("Évaluation ajoutée avec succès", "success")
    return redirect(url_for('evaluation.list_evaluations', employe_id=employe_id))
