from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from database import db
from models import User
from proxy import LoginProxy
from strategy import MasterAuthStrategy, UserAuthStrategy

auth = Blueprint('auth', __name__)

# Usuário mestre (admin)
MASTER_USERNAME = 'admin'
MASTER_PASSWORD = '1234'

class MasterUser(UserMixin):
    id = 0
    username = MASTER_USERNAME
    password = MASTER_PASSWORD

    def get_id(self):
        return self.username

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar se é o usuário mestre
        master_auth = MasterAuthStrategy()
        user_auth = UserAuthStrategy()
        login_proxy = LoginProxy(login_user)

        if master_auth.authenticate(username, password):
            user = MasterUser()
            login_user(user)
            return redirect(url_for('routes.admin_dashboard'))
        
        # Verificar se é um usuário normal
        if user_auth.authenticate(username, password):
            if login_proxy.login(username, password):
                return redirect(url_for('routes.admin_dashboard'))
        
        flash("Erro: Usuário ou senha incorretos!", 'danger')
    return render_template('login.html')

@auth.route('/register', methods=['POST'])
@login_required
def register():
    if current_user.username != MASTER_USERNAME:
        return "Erro: Apenas o usuário mestre pode registrar novos usuários!", 403

    username = request.form['username']
    password = request.form['password']
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "Erro: Usuário já existe!", 400
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    flash('Usuário registrado com sucesso!', 'success')
    return redirect(url_for('routes.admin_dashboard'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))