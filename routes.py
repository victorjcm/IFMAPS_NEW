from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify  # type: ignore
from flask_login import login_required, logout_user, current_user  # type: ignore
from models import Evento, Sala, Laboratorio, User, MasterUser
from database import db
from factory import EventoFactory
from observer import EventoNotifier, AdminObserver
from proxy import LoginProxy
from strategy import MasterAuthStrategy, UserAuthStrategy
import os

# Definição do Blueprint para rotas de eventos
routes = Blueprint('routes', __name__)
auth = Blueprint('auth', __name__)

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

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Escolha a estratégia de autenticação
        if username == 'admin':
            strategy = MasterAuthStrategy()
        else:
            strategy = UserAuthStrategy()

        proxy = LoginProxy(strategy)
        if proxy.login(username, password):
            return redirect(url_for('routes.admin_dashboard'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'danger')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['POST'])
@login_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar se o nome de usuário já existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nome de usuário já existe. Por favor, escolha outro.', 'danger')
            return redirect(url_for('routes.admin_dashboard'))

        new_user = User(username=username)
        new_user.set_password(password)  # Armazenar a senha como hash
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('routes.admin_dashboard'))
