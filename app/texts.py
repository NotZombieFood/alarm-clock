# coding=utf-8
import html

class Texts(object):
    login = html.escape('Iniciar sesión')
    password = html.escape('Contraseña')
    enter_password = html.escape('Ingresar contraseña')
    user = html.escape('Usuario')
    email = html.escape('Correo electrónico')
    register = html.escape('Registrarse')
    register_message = html.escape('¿No tienes cuenta? Regístrate.')
    login_message = html.escape('¿Tienes cuenta? Inicia sesión.')
    form_error_message = html.escape('Por favor rellena todos los campos.')
    user_exists = html.escape('El usuario ya está registrado.')
    email_exists = html.escape('El correo electrónico ya está registrado.')
    bot_name = html.escape('Bot de prueba')
    bot_status = html.escape('En línea')