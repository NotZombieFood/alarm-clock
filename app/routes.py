# coding=utf-8

from app import app, db
from flask import render_template, redirect, url_for, request, send_from_directory, request
from app.forms import LoginForm, RegisterForm
from app.texts import Texts
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Message
import datetime, os
from wit import Wit

WIT_TOKEN = os.environ.get('WIT_KEY')
client = Wit(access_token=WIT_TOKEN)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #form.payment.errors.append('the error message')
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            form.password.errors.append('Auth_error')
        else:
            login_user(user)
        return redirect(url_for('chat'))
    return render_template('login.html', title=Texts.login, form=form, register_message = Texts.register_message, form_error_message = Texts.form_error_message)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        user_object = User.query.filter_by(username=form.username.data).first()
        message = Message(direction='bot',message='Hola, soy el bot :)',user_id=user_object.id, time='{0:%H:%M}'.format(datetime.datetime.now()))
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title=Texts.register, user_exists = Texts.user_exists , email_exists= Texts.email_exists,form=form, login_message = Texts.login_message, form_error_message = Texts.form_error_message)

@app.route('/')
@login_required
def chat():
    return render_template('chat.html',bot_avatar = 'https://image.flaticon.com/icons/svg/1166/1166474.svg',bot_name = Texts.bot_name,bot_status= Texts.bot_status)

# May be adding a payment api for "paid messages", which will be answered by professionals
@app.route('/payments')
def payments():
    return ''

@app.route('/messages', methods=['GET'])
def receive_message():
    user_id = request.args.get("id")
    message = request.args.get("message")
    m = Message(direction='user',message=message,user_id=user_id,time = '{0:%H:%M}'.format(datetime.datetime.now()))
    db.session.add(m)
    db.session.commit()
    response_message = obtainMessage(message)
    m = Message(direction='bot',message=response_message,user_id=user_id,time = '{0:%H:%M}'.format(datetime.datetime.now()))
    db.session.add(m)
    db.session.commit()
    return response_message


@app.route('/static/<path:path>')
def send_static_files(path):
    return send_from_directory('static', path)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Function for handlin with requests
def obtainMessage(message):
    response_wit = client.message(message)
    try:
        if (response_wit['entities']['intent'][0]['confidence'] > .60):
            intent = response_wit['entities']['intent'][0]['value']
            if intent == 'cita':
                response = 'Para agendar una cita por favor comunicate a 3123123131, te atenderemos lo mas pronto posible.'
            elif intent == 'saludo':
                response = 'Hola, estamos para atenderte. Podemos ayudarte a concretar una cita, ver eventos pasados o darte mas informacion'
            elif intent == 'sitio web':
                response = 'Puedes encontrar esta informarcion en shimaraeventos.com.mx'
            elif intent == 'llamada':
                response = 'Puedes llamarnos a los siguientes numeros 13123134141,312312313,1321231321'
            elif intent == 'servicios':
                response = 'Estos son nuestros servicios eh'
        else:
            response = 'No estamos seguros de como responder este mensaje, trabajamos duro para poder ofrecerte una mejor experiencia'
    except:
        response = 'No estamos seguros de como responder este mensaje, trabajamos duro para poder ofrecerte una mejor experiencia'
    return response