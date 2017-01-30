from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin

appname = "Vainglorious Secret"
app = Flask(__name__)
db = SQLAlchemy(app)

admin = Admin(app, name=appname, template_mode='bootstrap3')

lm = LoginManager()
lm.init_app(app)

SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="root",
    hostname="localhost:3306",
    databasename="vainglory"
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["DEBUG"] = True
app.config["WERKZEUG_DEBUG_PIN"] = "off"
app.secret_key = 'anotherplaintextpasswordftw'

#
# @app.teardown_request
# def teardown_request(exception=None):
#     print exception


