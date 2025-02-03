from database import db

class Evento(db.Model):
    __tablename__ = 'evento'
    __table_args__ = {'extend_existing': True}  # ✅ Isso evita redefinições da tabela

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(300), nullable=True)  # Caminho da imagem no servidor

    def __init__(self, titulo, descricao, imagem=None):
        self.titulo = titulo
        self.descricao = descricao
        self.imagem = imagem