from flask_login import login_user
from models import User, MasterUser

class LoginProxy:
    def __init__(self, strategy):
        self._strategy = strategy

    def login(self, username, password):
        if self._strategy.authenticate(username, password):
            if username == 'admin':
                user = MasterUser()
            else:
                user = User.query.filter_by(username=username).first()
            if user:
                login_user(user)
                return True
        return False