# coding=utf-8
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    message = db.relationship("Message")
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return '<User {}>'.format(self.username)  

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direction = db.Column(db.String(64))
    message = db.Column(db.String(2500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.String(6))
    def __repr__(self):
        return '<Message {}>'.format(self.message)  


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
