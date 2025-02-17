class Observer:
    """
    Interface para os observadores.
    """
    def update(self, evento):
        """
        Método a ser implementado pelas subclasses para atualizar o estado com base no evento.

        Args:
            evento (Evento): O evento que foi criado.
        """
        pass  # Método abstrato para ser implementado nas subclasses

class AdminObserver(Observer):
    """
    Observador que mantém uma lista de notificações para o administrador.
    """
    def __init__(self):
        self.notifications = []

    def update(self, evento):
        """
        Atualiza a lista de notificações quando um novo evento é adicionado.

        Args:
            evento (Evento): O evento que foi criado.
        """
        if evento.tipo == 'evento':
            notification = f"🔔 Novo {evento.tipo} adicionado: {evento.titulo}"
            self.notifications.append(notification)
            print(notification)  # Debug: mostra a notificação no console

    def remove_notification(self, evento):
        """
        Remove a notificação correspondente ao evento deletado.

        Args:
            evento (Evento): O evento que foi deletado.
        """
        if evento.tipo == 'evento':
            notification = f"🔔 Novo {evento.tipo} adicionado: {evento.titulo}"
            if notification in self.notifications:
                self.notifications.remove(notification)
                print(f"Notificação removida: {notification}")  # Debug: mostra a remoção no console

    def get_notifications(self):
        """
        Retorna todas as notificações armazenadas.

        Returns:
            list: Lista de notificações.
        """
        return self.notifications

class EventoNotifier:
    """
    Notificador de eventos que mantém uma lista de observadores e os notifica quando um evento é criado.
    """
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        """
        Adiciona um novo observador à lista.

        Args:
            observer (Observer): O observador a ser adicionado.
        """
        self._observers.append(observer)

    def notify_observers(self, evento):
        """
        Notifica todos os observadores quando um novo evento é criado.

        Args:
            evento (Evento): O evento que foi criado.
        """
        for observer in self._observers:
            observer.update(evento)

    def notify_observers_removal(self, evento):
        """
        Notifica todos os observadores quando um evento é deletado.

        Args:
            evento (Evento): O evento que foi deletado.
        """
        for observer in self._observers:
            if hasattr(observer, 'remove_notification'):
                observer.remove_notification(evento)

# Observer global
notificador_admin = AdminObserver()
notificador_eventos = EventoNotifier()
notificador_eventos.add_observer(notificador_admin)
