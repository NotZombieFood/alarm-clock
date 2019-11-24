# coding=utf-8
from app import db, login

from datetime import datetime

""" 
    class for database accesses, this will include the melodies and data from the sensors 

""" 

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key =  True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    temperature = db.Column(db.Integer, nullable = False)
    humidity  = db.Column(db.Integer, nullable = False)
    
    
class Song(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    song = db.Column(db.String(2500))


class Alarm(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    hour = db.Column(db.Integer)
    minutes = db.Column(db.Integer)