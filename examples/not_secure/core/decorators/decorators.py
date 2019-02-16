from functools import wraps
from flask import session, render_template,redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return decorated_function


def error_occured(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            return render_template('error.html')

        return decorated_function