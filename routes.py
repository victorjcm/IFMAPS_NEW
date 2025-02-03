from flask import Blueprint, render_template, request, redirect, url_for
from models import Evento
from database import db

# Definição do Blueprint para rotas de eventos
routes = Blueprint('routes', __name__)

@routes.route('/eventos')
def listar_eventos():
    eventos = Evento.query.all()  # Busca todos os eventos do banco de dados
    return render_template('eventos.html', eventos=eventos)

@routes.route('/evento/<int:evento_id>')
def detalhes_evento(evento_id):
    evento = Evento.query.get(evento_id)  # Busca evento pelo ID
    if not evento:
        return "Evento não encontrado", 404
    return render_template('evento.html', evento=evento)

# Rota para adicionar um novo evento
@routes.route('/adicionar_evento', methods=['GET', 'POST'])
def adicionar_evento():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        imagem = request.form['imagem']  # O caminho da imagem será armazenado

        novo_evento = Evento(titulo=titulo, descricao=descricao, imagem=imagem)
        db.session.add(novo_evento)
        db.session.commit()
        return redirect(url_for('routes.listar_eventos'))  # Redireciona para lista de eventos

    return render_template('adicionar_evento.html')
