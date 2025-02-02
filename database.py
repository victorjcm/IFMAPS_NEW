from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Flask-Login espera esse método para verificar se o usuário está ativo
    @property
    def is_active(self):
        return True

# Função para inicializar o banco de dados
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()