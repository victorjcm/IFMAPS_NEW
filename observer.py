class Observer:
    def update(self, evento):
        pass

class AdminObserver(Observer):
    def update(self, evento):
        print(f"Novo {evento.tipo} adicionado: {evento.titulo}")

class EventoNotifier:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, evento):
        for observer in self._observers:
            observer.update(evento)