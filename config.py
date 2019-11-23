# coding=utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'R4t4t4'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False