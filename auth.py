from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from database import db, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        return "Erro: Usuário ou senha incorretos!", 400
    return render_template('login.html')  # Página contendo login e cadastro

@auth.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "Erro: Usuário já existe!", 400
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))