from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def permission_requise(code_permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Vous devez être connecté.", "warning")
                return redirect(url_for('auth.login'))
            if current_user.role and any(p.code == code_permission for p in current_user.role.permissions):
                return f(*args, **kwargs)
            flash("Accès refusé : vous n'avez pas la permission requise.", "danger")
            return redirect(url_for('dashboard.index'))
        return wrapper
    return decorator
