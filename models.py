from database import db
from flask_login import UserMixin

# Modelo de Usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    @property
    def is_active(self):
        return True

    @property
    def is_master(self):
        return self.username == 'admin'

# Modelo de Evento
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