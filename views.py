from __future__ import division
from flask import redirect, render_template, request, url_for, flash
from flask_app import lm, admin
from flask_login import login_user, logout_user, current_user
from flask_admin.contrib.sqla import ModelView

from sqlalchemy import func
from functools import wraps

from api import VaingloryApi
from models import *
from commons import *
import process_data
import pprint

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ------------------
# ADMIN
# -----------------

class MyModelView(ModelView):
    can_delete = False  # disable model deletion
    page_size = 50  # the number of entries to display on the list view

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
            # redirect to login page if user doesn't have access
            return redirect(url_for('login'))
admin.add_view(MyModelView(Match, db.session))

# ------------------
# METHODS
# ------------------

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        remember_me = False
        if 'remember' in request.form:
            remember_me = True

        registered_user = User.query.filter_by(username=username).first()

        if registered_user is None:
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))

        if not registered_user.check_password(password):
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))

        login_user(registered_user, remember = remember_me)
        flash('Logged in successfully')

        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index/')
def index():
    api = VaingloryApi("aaa.bbb.ccc")

    # split request to batches of 50
    # max_limit = 50
    # limit = 15000
    # matches = []
    # for batch in range(10000, limit, max_limit):
    #     response = api.matches(offset=batch, limit=max_limit)
    #     matches.append(dict(response))
    #     limit -= max_limit
    #
    # print len(matches)
    # process_data.process_batch_query(matches)

    # matches = api.matches(player="Shiqan")
    # process_data.process_query(matches)

    # pprint.pprint(matches)

    # api.player("6abb30de-7cb8-11e4-8bd3-06eb725f8a76")
    # match = api.match("f78917d2-d7cf-11e6-ad79-062445d3d668")

    return render_template('404.html')


@app.route('/test/')
def te():
    # m = db.session.query(Match).get("f78917d2-d7cf-11e6-ad79-062445d3d668")
    # print m.rosters[0].participants

    p = db.session.query(Player).get("2537169e-2619-11e5-91a4-06eb725f8a76")
    print p.name
    print p.participated[0].roster.match.duration

    t = db.session.query(Participant).get("00123cd2-e4d2-11e6-9872-0242ac110006")
    print t.actor
    print t.items

    heroes_played = db.session.query(Participant.actor, func.count(Participant.actor)).group_by(Participant.actor).all()
    heroes_won = db.session.query(Participant.actor, func.count(Participant.actor))\
        .filter(Participant.winner == 1).group_by(Participant.actor).all()

    heroes_winrates = [(actor2[1] / actor1[1])*100 for actor1 in heroes_played for actor2 in heroes_won if actor1[0] == actor2[0]]

    best_comps = []

    return render_template('blank.html',
                           heroes_played=heroes_played,
                           heroes_winrates=heroes_winrates)


# ------------------
# ERROR HANDLERS
# ------------------
@app.errorhandler(400)
def bad_request(e):
    return render_template('404.html'), 400

@app.errorhandler(401)
def not_authorized(e):
    return render_template('404.html'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('404.html'), 405

@app.errorhandler(500)
def internal_error(error):
    return render_template('404.html'), 500
