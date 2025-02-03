from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, init_db, User, initialize_database
from auth import auth
from routes import routes  # ✅ Certifique-se de que esta linha existe!

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'chave_secreta'

# ✅ Inicializando o banco de dados
init_db(app)

# ✅ Configuração do Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ✅ Registrando os Blueprints corretamente
app.register_blueprint(auth)
app.register_blueprint(routes)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

@app.route('/eventos')
def eventos():
    return render_template('eventos.html')

# ✅ Mantendo o Register no facade.py (Padrão Facade)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Erro: Usuário já existe!", 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('register.html')  # Renderiza a página de cadastro

@app.route('/admin')
@login_required
def admin_dashboard():
    return f"Bem-vindo, {current_user.username}! <a href='/logout'>Logout</a>"

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/buscar_sala', methods=['GET'])
def buscar_sala():
    query = request.args.get('q')
    salas = ["Sala 101", "Sala 102", "Laboratório 1", "Auditório"]
    resultado = [sala for sala in salas if query.lower() in sala.lower()]
    return jsonify(resultado)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ✅ Garante que o banco seja criado antes de rodar o app
        initialize_database()  # ✅ Inicializa os eventos de teste
    app.run(debug=True)
