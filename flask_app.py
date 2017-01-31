from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
import config

appname = "Vainglorious Secret"
app = Flask(__name__)
db = SQLAlchemy(app)

admin = Admin(app, name=appname, template_mode='bootstrap3')

lm = LoginManager()
lm.init_app(app)

app.config.from_object('config.DevelopmentConfig')
app.secret_key = 'anotherplaintextpasswordftw'

#
# @app.teardown_request
# def teardown_request(exception=None):
#     print exception


