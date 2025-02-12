from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from database import db
from models import User, MasterUser
from proxy import LoginProxy
from strategy import MasterAuthStrategy, UserAuthStrategy

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Escolha a estratégia de autenticação
        if username == 'admin':
            strategy = MasterAuthStrategy()
        else:
            strategy = UserAuthStrategy()

        proxy = LoginProxy(strategy)
        if proxy.login(username, password):
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('routes.admin_dashboard'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'danger')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['POST'])
@login_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar se o nome de usuário já existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nome de usuário já existe. Por favor, escolha outro.', 'danger')
            return redirect(url_for('routes.admin_dashboard'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('routes.admin_dashboard'))