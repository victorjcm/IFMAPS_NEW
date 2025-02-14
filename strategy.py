from models import User

class AuthStrategy:
    """
    Interface para a estratégia de autenticação.
    """
    def authenticate(self, username, password):
     """
    Método de autenticação a ser implementado pelas subclasses.

    Args:
        username (str): O nome de usuário.
        password (str): A senha.

    Returns:
        bool: True se a autenticação for bem-sucedida, False caso contrário.
    """
    pass

class MasterAuthStrategy(AuthStrategy):
    """
    Estratégia de autenticação para o usuário administrador.
    """
    def authenticate(self, username, password):
        return username == 'admin' and password == '1234'

class UserAuthStrategy(AuthStrategy):
    """
    Estratégia de autenticação para usuários comuns.
    """
    def authenticate(self, username, password):
        user = User.query.filter_by(username=username, password=password).first()
        return user is not None