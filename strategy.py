from models import User

class AuthStrategy:
    def authenticate(self, username, password):
        pass

class MasterAuthStrategy(AuthStrategy):
    def authenticate(self, username, password):
        return username == 'admin' and password == '1234'

class UserAuthStrategy(AuthStrategy):
    def authenticate(self, username, password):
        user = User.query.filter_by(username=username, password=password).first()
        return user is not None