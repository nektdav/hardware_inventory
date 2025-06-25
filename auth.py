from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from users import db, User
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
login_manager.login_view = 'login'

def init_login(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def setup_auth_routes(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
            flash('Λανθασμένο όνομα χρήστη ή κωδικός')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
            role = request.form.get('role', 'user')
            new_user = User(username=username, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html')
