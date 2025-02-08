from models import Evento

class EventoFactory:
    @staticmethod
    def create_evento(tipo, titulo, descricao, imagem=None):
        return Evento(titulo=titulo, descricao=descricao, tipo=tipo, imagem=imagem)