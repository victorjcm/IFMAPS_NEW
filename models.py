from database import db

class Evento(db.Model):
    __tablename__ = 'evento'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(300), nullable=True)
    tipo = db.Column(db.String(50), nullable=False)  # Novo campo para tipo (evento, sala, laboratório)

    def __init__(self, titulo, descricao, tipo, imagem=None):
        self.titulo = titulo
        self.descricao = descricao
        self.tipo = tipo
        self.imagem = imagem