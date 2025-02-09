class Observer:
    def update(self, evento):
        pass  # Método abstrato para ser implementado nas subclasses

class AdminObserver(Observer):
    def __init__(self):
        self.notifications = []

    def update(self, evento):
        """ Atualiza a lista de notificações quando um novo evento é adicionado """
        notification = f"🔔 Novo {evento.tipo} adicionado: {evento.titulo}"
        self.notifications.append(notification)
        print(notification)  # Debug: mostra a notificação no console

    def get_notifications(self):
        """ Retorna todas as notificações armazenadas """
        return self.notifications

class EventoNotifier:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        """ Adiciona um novo observador à lista """
        self._observers.append(observer)

    def notify_observers(self, evento):
        """ Notifica todos os observadores quando um novo evento é criado """
        for observer in self._observers:
            observer.update(evento)

#Observer global
notificador_admin = AdminObserver()
notificador_eventos = EventoNotifier()
notificador_eventos.add_observer(notificador_admin)
