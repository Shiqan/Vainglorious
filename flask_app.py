from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
# from flask_cache import Cache

import config

appname = "Vainglorious Meta"
app = Flask(__name__)
db = SQLAlchemy(app)

admin = Admin(app, name=appname, template_mode='bootstrap3')

lm = LoginManager()
lm.init_app(app)

# cache = Cache(app,config={'CACHE_TYPE': 'simple'})

app.config.from_object('config.ProductionConfig')
# app.config.from_envvar('YOURAPPLICATION_SETTINGS')
app.secret_key = 'anotherplaintextpasswordftw'

import models, views

#
# @app.teardown_request
# def teardown_request(exception=None):
#     print exception


