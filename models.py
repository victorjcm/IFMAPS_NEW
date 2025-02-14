from database import db
from flask_login import UserMixin

# Modelo de Usuário
class User(db.Model, UserMixin):
    """
    Modelo de dados para os usuários do sistema.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        """
        Armazena a senha como um hash seguro.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.
        """
        return check_password_hash(self.password, password)

# Modelo de Evento
class Evento(db.Model):
    """
    Modelo de dados para os eventos do sistema.
    """
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(300), nullable=True)
    tipo = db.Column(db.String(50), nullable=False)

class MasterUser(UserMixin):
    """
    Modelo de dados para o usuário administrador.
    """
    def __init__(self):
        self.id = 0
        self.username = 'admin'
        self.password = '1234'

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username