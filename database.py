from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Modelo de Usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Flask-Login espera esse método para verificar se o usuário está ativo
    @property
    def is_active(self):
        return True

# Modelo de Evento
from database import db

class Evento(db.Model):
    __tablename__ = 'evento'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(300), nullable=True)
    tipo = db.Column(db.String(50), nullable=False)  # Novo campo para tipo (evento, sala, laboratório)

    def __init__(self, titulo, descricao, tipo, imagem=None):
        self.titulo = titulo
        self.descricao = descricao
        self.tipo = tipo
        self.imagem = imagem

def initialize_database():
    # Esta função não adicionará mais eventos de teste
    pass

# Função para inicializar o banco de dados
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        initialize_database()

