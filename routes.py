from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import Evento
from database import db
import os

# Definição do Blueprint para rotas de eventos
routes = Blueprint('routes', __name__)

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


@routes.route('/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        tipo = request.form['tipo']
        imagem = request.files['imagem']

        # Salvar a imagem no servidor
        imagem_path = None
        if imagem:
            imagem_filename = imagem.filename
            imagem_path = os.path.join('static/img', imagem_filename)
            imagem.save(imagem_path)

        novo_evento = Evento(titulo=titulo, descricao=descricao, tipo=tipo, imagem=imagem_filename)
        db.session.add(novo_evento)
        db.session.commit()
        return redirect(url_for('routes.listar_eventos'))

    return render_template('adicionar.html')

@routes.route('/eventos')
def listar_eventos():
    eventos = Evento.query.all()
    return render_template('eventos.html', eventos=eventos)

@routes.route('/evento/<int:evento_id>')
def detalhes_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    return render_template('evento.html', evento=evento)

@routes.route('/evento/<int:evento_id>/delete', methods=['POST'])
@login_required
def deletar_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    db.session.delete(evento)
    db.session.commit()
    flash('Evento deletado com sucesso!', 'success')
    return redirect(url_for('routes.admin_dashboard'))

@routes.route('/admin')
@login_required
def admin_dashboard():
    eventos = Evento.query.all()
    return render_template('admin_dashboard.html', eventos=eventos)

# Adicionar a rota para /mapa
@routes.route('/mapa')
def mapa():
    return render_template('mapa.html')