from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import Utilisateur

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['nom_utilisateur']
        mot_de_passe = request.form['mot_de_passe']
        user = Utilisateur.query.filter_by(nom_utilisateur=user_name).first()

        if not user or not user.check_password(mot_de_passe):
            flash("Pseudo ou mot de passe incorrect", "danger")
            return render_template('auth/login.html')
            
        if not user.actif:
            flash("Votre compte est inactif. Veuillez contacter l’administrateur.", "warning")
            return render_template('auth/login.html')
        
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
