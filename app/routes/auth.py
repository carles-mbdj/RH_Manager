from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import Utilisateur

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        user = Utilisateur.query.filter_by(email=email).first()

        if user and user.check_password(mot_de_passe):
            login_user(user)

            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.dashboard'))

        flash("Email ou mot de passe incorrect", "danger")

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
