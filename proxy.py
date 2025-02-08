from flask_login import login_user
from models import User

class LoginProxy:
    def __init__(self, real_login):
        self._real_login = real_login

    def login(self, username, password):
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return True
        return False