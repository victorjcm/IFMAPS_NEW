from flask_login import login_user # type: ignore
from models import User, MasterUser

class LoginProxy:
    """
    Proxy para a lógica de autenticação dos usuários.
    """
    def __init__(self, strategy):
        """
        Inicializa o proxy com a estratégia de autenticação fornecida.

        Args:
            strategy (AuthStrategy): A estratégia de autenticação a ser utilizada.
        """
        self._strategy = strategy

    def login(self, username, password):
        """
        Autentica o usuário utilizando a estratégia fornecida.

        Args:
            username (str): O nome de usuário.
            password (str): A senha.

        Returns:
            bool: True se a autenticação for bem-sucedida, False caso contrário.
        """
        if not username or not password:
            return False

        if self._strategy.authenticate(username, password):
            if username == 'admin':
                user = MasterUser()
            else:
                user = User.query.filter_by(username=username).first()
            if user:
                login_user(user)
                return True
        return False