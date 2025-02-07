from flask import Flask, render_template
from flask_login import LoginManager
from database import db, User, init_db
from auth import auth, MasterUser
from routes import routes
from flask_migrate import Migrate

class FlaskAppFacade:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
        self.app.config['SECRET_KEY'] = 'chave_secreta'
        
        # Inicializando o banco de dados
        init_db(self.app)
        
        # Configuração do Flask-Login
        self.login_manager = LoginManager(self.app)
        self.login_manager.login_view = 'auth.login'
        
        @self.login_manager.user_loader
        def load_user(user_id):
            if user_id == MasterUser().username:
                return MasterUser()
            return User.query.get(int(user_id))
        
        # Registrando os Blueprints corretamente
        self.app.register_blueprint(auth)
        self.app.register_blueprint(routes)
        
        # Inicializando o Flask-Migrate
        self.migrate = Migrate(self.app, db)
        
        @self.app.route('/')
        def index():
            return render_template('index.html')

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    facade = FlaskAppFacade()
    facade.run()