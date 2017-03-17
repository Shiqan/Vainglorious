from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

appname = "Vainglorious Meta"
app = Flask(__name__)
db = SQLAlchemy(app)

# cache = Cache(app,config={'CACHE_TYPE': 'simple'})

app.config.from_object('config.DevelopmentConfig')
# app.config.from_object('config.ProductionConfig')
# app.config.from_envvar('YOURAPPLICATION_SETTINGS  ')
app.secret_key = 'anotherplaintextpasswordftw'

import models, views

#
# @app.teardown_request
# def teardown_request(exception=None):
#     print exception


