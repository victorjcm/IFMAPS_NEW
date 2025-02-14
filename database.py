from flask_sqlalchemy import SQLAlchemy # type: ignore

class SingletonMeta(type):
    """
    Metaclasse para implementar o padrão Singleton.
    Garante que apenas uma instância da classe seja criada.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    """
    Classe Database que utiliza a metaclasse SingletonMeta para garantir
    que apenas uma instância seja criada.
    """
    def __init__(self):
        self.db = SQLAlchemy()

    @classmethod
    def get_instance(cls):
        """
        Retorna a instância única da classe Database.
        """
        return cls()

class Config(metaclass=SingletonMeta):
    def __init__(self):
        self.settings = {
            'DEBUG': True,
            'SECRET_KEY': 'chave_secreta',
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///user.db'
        }

    @classmethod
    def get_instance(cls):
        """
        Retorna a instância única da classe Config.
        """
        return cls()

    def get(self, key):
        return self.settings.get(key)

    def set(self, key, value):
        self.settings[key] = value

# Instância única do banco de dados
db = Database.get_instance().db

# Instância única de Configurações
config = Config.get_instance()

def initialize_database():
    """
    Função para inicializar o banco de dados.
    Pode ser usada para adicionar dados iniciais ou realizar outras configurações.
    """
    pass

def init_db(app):
    """
    Função para inicializar o banco de dados com o aplicativo Flask.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
        initialize_database()