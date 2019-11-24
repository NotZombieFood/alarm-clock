# coding=utf-8

from app import app, db
from flask import render_template, redirect, url_for, request, send_from_directory, request
from app.models import SensorData, Song, Alarm
import datetime, os

"""
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
"""



@app.route('/static/<path:path>')
def send_static_files(path):
    return send_from_directory('static', path)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
