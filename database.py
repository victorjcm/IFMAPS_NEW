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
class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(300), nullable=True)  # Caminho da imagem no servidor

    def __init__(self, titulo, descricao, imagem=None):
        self.titulo = titulo
        self.descricao = descricao
        self.imagem = imagem

# Função para adicionar eventos de teste automaticamente
def initialize_database():
    eventos_existentes = {evento.titulo for evento in Evento.query.all()}  # Obtém os títulos dos eventos já existentes

    eventos_para_adicionar = [
        Evento(titulo="SISU", descricao="SE INSCREVA NO SISU 2025", imagem="static/img/evento3.png")
    ]

    eventos_novos = [evento for evento in eventos_para_adicionar if evento.titulo not in eventos_existentes]

    if eventos_novos:
        db.session.add_all(eventos_novos)
        db.session.commit()

# Função para inicializar o banco de dados
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        initialize_database()

