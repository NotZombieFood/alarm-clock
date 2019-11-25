# coding=utf-8

from app import app, db
from flask import render_template, redirect, url_for, request, send_from_directory, request
from app.models import SensorData, Alarm
import datetime, os
import threading
import requests


# Definitions
MICROCONTROLLER_IP = "192.168.43.44"
DEBUG = False

# global declares
global alarm_objects
global songs

# initing the global variables
alarm_objects = []
# Dictionary with the available songs
songs = [
        {"Thunderstruck":0},
        {"Zelda Woods":1},
        {"Ocarina":2},
        {"Beethoven":3},
        {"Simpsons":4},
        {"Digitallo":5},
        {"Zelda #2":6},
        {"Starwars":7},
        {"SMB":8},
        {"Xfiles":9}
}]


# in case of failure, we can set this up
if DEBUG == True:
    print(db.query(Alarm))
    print(db.query(SensorData))


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

# alarm object is the responsible of setting the request to the microcontroller to make some noise
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
                    self.just_die()
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
    alarm_objects.append(alarm_object)

@app.route("/set_song", methods=['GET'])
def set_song():
    try:
        song_id = int(request.args.get("song"))
        requests.get('http://%s/seleccionar_cancion:%i'%(MICROCONTROLLER_IP,song_id))
        return "Success"
    except:
        return "Failure"

def get_latest_alarm():
    obj = db.query(Alarm).order_by(Alarm.id.desc()).first()
    return obj

def kill_alarm():
    alarm_object.just_die()

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/song")
def song():
    return render_template('song.html', songs = songs)

@app.route('/static/<path:path>')
def send_static_files(path):
    return send_from_directory('static', path)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
