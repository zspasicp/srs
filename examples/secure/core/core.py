import os
import flask
from flask import (
    Flask,
    render_template,
    url_for)
from flask_login import current_user
from flask_security import Security, SQLAlchemyUserDatastore, \
    login_required, roles_accepted
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from run import app


def setup_db(app):
    from core.database import db
    from core.model.user import User, Role
    from core.forms.forms import ExtendedLoginForm, ExtendedChangePasswordForm
    # Create database connection object

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore, login_form=ExtendedLoginForm,
                        change_password_form=ExtendedChangePasswordForm)
    return db, user_datastore, security


def create_app():

    app.config.update()
    app.config.timezone = 'UTC'

    app.config.update(dict(
        DEBUG=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.root_path, 'app.db'),
        SQLALCHEMY_POOL_SIZE=None,
        SECRET_KEY=b'baetorkploggdhrykdorngvhdkdofgndhdfduhfkjg',
        SECURITY_REGISTERABLE=True,
        SECURITY_CONFIRMABLE=False,
        SECURITY_RECOVERABLE=True,
        SECURITY_CHANGEABLE=True,
        SECURITY_SEND_PASSWORD_CHANGE_EMAIL=False,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECURITY_PASSWORD_SALT=b'xxx',
        SECURITY_SEND_REGISTER_EMAIL=False,
        SECURITY_POST_LOGIN_VIEW='/',
        SECURITY_POST_REGISTER_VIEW='/',

    ))

    db, user_datastore, security = setup_db(app)

    # Create a user to test with
    @app.before_first_request
    def create_user():
        db.create_all()
        db.session.commit()

    @app.route('/')
    @login_required
    def home():
        if 'admin' in [role.name for role in current_user.roles]:
            return redirect(url_for('admin'))
        return render_template('index.html')

    @app.route('/admin')
    @login_required
    @roles_accepted('admin')
    def admin():
        users = user_datastore.user_model.query.all()
        return render_template('admin.html', users=users)

    @app.route('/add_user', methods=['GET', 'POST'])
    @login_required
    @roles_accepted('admin')
    def add_user():
        from core.forms.forms import NewUserForm
        from flask_security import utils
        form = NewUserForm()
        if form.validate_on_submit():
            new_user = user_datastore.create_user(email=form.email.data,
                                                  first_name=form.first_name.data,
                                                  last_name=form.last_name.data,
                                                  active=form.active.data,
                                                  password=utils.hash_password(form.password_.data))
            db.session.flush()
            role = user_datastore.role_model.query.filter(user_datastore.role_model.name == form.role.data).first()
            new_user.roles.append(role)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('add_user.html', form=form)

    return app
