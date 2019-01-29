import os
import flask
from flask import (
    Flask,
    render_template,
    url_for)
from flask_login import current_user
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, roles_accepted
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect


def setup_db(app):
    # Create database connection object
    db = SQLAlchemy(app)

    # Define models
    roles_users = db.Table('roles_users',
                           db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                           db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

    class Role(db.Model, RoleMixin):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(80), unique=True)
        description = db.Column(db.String(255))

    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(255), unique=True)
        password = db.Column(db.String(255))
        active = db.Column(db.Boolean())
        confirmed_at = db.Column(db.DateTime())
        roles = db.relationship('Role', secondary=roles_users,
                                backref=db.backref('users', lazy='dynamic'))

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    return db, user_datastore, security


def create_app():
    app = Flask('app')
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

    return app
