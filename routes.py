from flask import Flask, jsonify
from flask_login import LoginManager
from database import db, init_db
from auth import auth
from routes import routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'chave_secreta'

# Inicializando o banco de dados
init_db(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from database import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registrando Blueprints
app.register_blueprint(auth)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
