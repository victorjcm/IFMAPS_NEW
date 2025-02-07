from flask import Flask, render_template
from flask_login import LoginManager
from database import db, User, init_db
from auth import auth, MasterUser
from routes import routes
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = 'chave_secreta'

# Inicializando o banco de dados
init_db(app)

# Configuração do Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    if user_id == MasterUser().username:
        return MasterUser()
    return User.query.get(int(user_id))

# Registrando os Blueprints corretamente
app.register_blueprint(auth)
app.register_blueprint(routes)

# Inicializando o Flask-Migrate
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)