import os
from base64 import encode

import flask
from flask import (
    Flask,
    request,
    render_template,
    session,
    url_for, flash)
from flask_security import SQLAlchemyUserDatastore, LoginForm, utils
from werkzeug.utils import redirect
from core.decorators.decorators import login_required, error_occured

from run import app
import sqlite3


def setup_db(app):
    from core.database import db
    from core.model.user import User, Role
    # Create database connection object

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    return db, user_datastore


def create_app():

    app.config.update()
    app.config.timezone = 'UTC'

    app.config.update(dict(
        DEBUG=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.root_path, 'app.db'),
        SQLALCHEMY_POOL_SIZE=None,
        SECRET_KEY=b'baetorkploggdhrykdorngvhdkdofgndhdfduhfkjg',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,

    ))

    db, user_datastore = setup_db(app)

    # Create a user to test with
    @app.before_first_request
    def create_user():
        db.create_all()
        db.session.commit()

    @app.route('/')
    def home():
        from core.model.user import User, Role
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        else:
            email = session.get('user')
            query = "SELECT * FROM USER WHERE email='" + email + "'"
            conn = sqlite3.connect('app.db')
            c = conn.cursor()
            c.execute(query)
            result = c.fetchone()
            current_user = User()
            current_user.id = result[0]
            current_user.email = result[1]
            current_user.active = result[3]
            current_user.confirmed_at = result[4]
            query = "SELECT * FROM role WHERE id IN (SELECT role_id FROM roles_users WHERE user_id='" + str(current_user.id) + "');"
            c.execute(query)
            result = c.fetchone()
            current_user.roles = []
            while result is not None:
                role = Role()
                role.name = result[1]
                role.description = result[2]
                current_user.roles.append(role)
                result = c.fetchone()
            return render_template('index.html', current_user=current_user)
            conn.close()

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        import hashlib
        try:
            if request.method == 'GET':
                return render_template('login.html')
            else:
                password = request.form['password'].encode('ascii')
                password = hashlib.sha256(password).hexdigest()
                email = request.form['username']
                query = "SELECT * FROM USER WHERE email='" + email + "' and password='" + password + "'"
                conn = sqlite3.connect('app.db')
                c = conn.cursor()
                result = c.execute(query)
                result = c.fetchone()

                conn.close()
                if result is not None:
                    session['logged_in'] = True
                    session['user'] = request.form['username']
                    return redirect(url_for('home'))
                session['logged_in'] = False
                session['user'] = None
                flash('Invalid email or password')
                return render_template('login.html')
        except:
            return render_template('error.html')

    @app.route('/logout', methods=['POST', 'GET'])
    def logout():
        session['logged_in'] = False
        session['user'] = None
        return render_template('login.html')


    # @app.route('/')
    # @login_required
    # def home():
    #     # if 'admin' in [role.name for role in current_user.roles]:
    #     #     return redirect(url_for('admin'))
    #     return render_template('index.html')

    # @app.route('/login', methods=['POST', 'GET'])
    # def login():
    #     from core.forms.forms import LoginForm
    #     form = LoginForm()
    #     if request.method == 'POST':
    #         if form.validate_on_submit():
    #             if request.form['password'] == 'password' and request.form['username'] == 'admin':
    #                 session['logged_in'] = True
    #
    #             else:
    #                 pass
    #                 # flash('wrong password!')
    #             return home()
    #         else:
    #             return render_template('login.html', form=form)
    #     else:
    #         return render_template('login.html', form=form)

    @app.route('/admin')
    @login_required
    # @roles_accepted('admin')
    def admin():
        users = user_datastore.user_model.query.all()
        return render_template('admin.html', users=users)

    @app.route('/add_user', methods=['GET', 'POST'])
    @login_required
    # @roles_accepted('admin')
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
