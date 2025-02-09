from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models import Evento
from database import db
from factory import EventoFactory
from observer import EventoNotifier, AdminObserver
import os

# Definição do Blueprint para rotas de eventos
routes = Blueprint('routes', __name__)

notifier = EventoNotifier()
admin_observer = AdminObserver()
notifier.add_observer(admin_observer)

@routes.route('/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        tipo = request.form['tipo']
        imagem = request.files['imagem']

        # Diretórios das imagens
        diretorios = ['static/img/eventos', 'static/img/salas', 'static/img/laboratorios']
        for diretorio in diretorios:
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)

        # Salvar a imagem no primeiro diretório válido
        imagem_filename = None
        if imagem:
            imagem_filename = imagem.filename
            imagem_path = os.path.join(diretorios[0], imagem_filename)
            imagem.save(imagem_path)

        # Criar e salvar o evento
        novo_evento = EventoFactory.create_evento(tipo, titulo, descricao, imagem_filename)
        db.session.add(novo_evento)
        db.session.commit()

        # Enviar notificação
        notifier.notify_observers(novo_evento)

        # Redirecionar para admin_dashboard ao invés de eventos
        return redirect(url_for('routes.admin_dashboard'))

    return render_template('adicionar.html')

@routes.route('/eventos')
def listar_eventos():
    eventos = Evento.query.filter_by(tipo='evento').all()
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
    eventos = Evento.query.filter_by(tipo='evento').all()
    salas = Evento.query.filter_by(tipo='sala').all()
    laboratorios = Evento.query.filter_by(tipo='laboratorio').all()
    return render_template('admin_dashboard.html', eventos=eventos, salas=salas, laboratorios=laboratorios)

@routes.route('/mapa')
def mapa():
    salas = Evento.query.filter_by(tipo='sala').all()
    laboratorios = Evento.query.filter_by(tipo='laboratorio').all()
    return render_template('mapa.html', salas=salas, laboratorios=laboratorios)

@routes.route('/notificacoes')
def notificacoes():
    """ Retorna todas as notificações como JSON """
    return jsonify({"notificacoes": admin_observer.get_notifications()})
