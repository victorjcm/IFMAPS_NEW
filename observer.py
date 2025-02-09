class Observer:
    def update(self, evento):
        pass

class AdminObserver(Observer):
    def __init__(self):
        self.notifications = []

    def update(self, evento):
        notification = f"Novo {evento.tipo} adicionado: {evento.titulo}"
        self.notifications.append(notification)
        print(notification)

    def get_notifications(self):
        return self.notifications

class EventoNotifier:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, evento):
        for observer in self._observers:
            observer.update(evento)