# coding=utf-8

from app import app, db
from flask import render_template, redirect, url_for, request, send_from_directory, request
from app.models import SensorData, Song, Alarm
import datetime, os
import threading
import requests

MICROCONTROLLER_IP = "192.168.43.44"
global alarm_object


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


class AlarmObject(threading.Thread):
    def __init__(self, hours, minutes):
        self.hours = hours
        self.minutes = minutes
        self.keep_running = True

    def run(self):
        try:
            while self.keep_running:
                now = time.localtime()
                if (now.tm_hour == self.hours and now.tm_min == self.minutes):
                    print("ALARM NOW!")
                    # request to the microcontroller
                    requests.get('http://%s/sonar'%(MICROCONTROLLER_IP))
                    return
            time.sleep(60)
        except:
            return
    def just_die(self):
        print("Alarm is eliminated")
        self.keep_running = False



@app.route('/set_alarm', methods=['GET'])
def set_alarm():
    hour = request.args.get("hour")
    minutes = request.args.get("minutes")
    alarm = Alarm(hour = hour, minutes = minutes)
    db.session.add(alarm)
    db.session.commit()
    alarm_object = AlarmObject(hour, minutes)
    alarm_object.run()
    db.session()


def get_latest_alarm():
    obj = db.query(Alarm).order_by(Alarm.id.desc()).first()
    return obj

def kill_alarm():
    alarm_object.just_die()



@app.route("/")
def index():
    return render_template('home.html')

@app.route('/static/<path:path>')
def send_static_files(path):
    return send_from_directory('static', path)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
