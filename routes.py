from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify  # type: ignore
from flask_login import login_required  # type: ignore
from models import Evento, Sala, Laboratorio
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
        imagem = request.files.get('imagem')
        
        capacidade = request.form.get('capacidade') if tipo == 'sala' else None
        equipamentos = request.form.get('equipamentos') if tipo == 'laboratorio' else None

        # Diretórios das imagens
        diretorios = {
            'evento': 'static/img/eventos',
            'sala': 'static/img/salas',
            'laboratorio': 'static/img/laboratorios'
        }

        if not os.path.exists(diretorios[tipo]):
            os.makedirs(diretorios[tipo])

        imagem_filename = None
        if imagem:
            imagem_filename = imagem.filename
            imagem_path = os.path.join(diretorios[tipo], imagem_filename)
            imagem.save(imagem_path)

        # Criar e salvar o objeto correto
        novo_item = EventoFactory.create(tipo, titulo, descricao, imagem_filename, capacidade, equipamentos)
        db.session.add(novo_item)
        db.session.commit()

        # Enviar notificação apenas para eventos
        if tipo == 'evento':
            notifier.notify_observers(novo_item)

        return redirect(url_for('routes.admin_dashboard'))

    return render_template('adicionar.html')

@routes.route('/eventos')
def listar_eventos():
    eventos = Evento.query.all()
    return render_template('eventos.html', eventos=eventos)

@routes.route('/evento/<int:evento_id>')
def detalhes_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    return render_template('evento.html', evento=evento)

@routes.route('/item/<int:item_id>/delete', methods=['POST'])
@login_required
def deletar_item(item_id):
    tipo = request.args.get('tipo')  # Pega o tipo enviado no formulário

    if tipo == "evento":
        item = Evento.query.get(item_id)
    elif tipo == "sala":
        item = Sala.query.get(item_id)
    elif tipo == "laboratorio":
        item = Laboratorio.query.get(item_id)
    else:
        flash("Tipo inválido!", "danger")
        return redirect(url_for("routes.admin_dashboard"))

    if not item:
        flash("Item não encontrado.", "danger")
        return redirect(url_for("routes.admin_dashboard"))

    db.session.delete(item)
    db.session.commit()

    # Notificar a remoção apenas para eventos
    if tipo == 'evento':
        notifier.notify_observers_removal(item)

    flash(f"{tipo.capitalize()} deletado com sucesso!", "success")
    return redirect(url_for("routes.admin_dashboard"))

@routes.route('/admin')
@login_required
def admin_dashboard():
    eventos = Evento.query.all()
    salas = Sala.query.all()
    laboratorios = Laboratorio.query.all()
    return render_template('admin_dashboard.html', eventos=eventos, salas=salas, laboratorios=laboratorios)

@routes.route('/mapa')
def mapa():
    salas = Sala.query.all()
    laboratorios = Laboratorio.query.all()
    return render_template('mapa.html', salas=salas, laboratorios=laboratorios)

@routes.route('/notificacoes')
def notificacoes():
    return jsonify({"notificacoes": admin_observer.get_notifications()})
