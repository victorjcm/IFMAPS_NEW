from flask_sqlalchemy import SQLAlchemy

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.db = SQLAlchemy()

db = Database().db

def initialize_database():
    pass

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        initialize_database()