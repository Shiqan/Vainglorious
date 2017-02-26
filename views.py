from __future__ import division

import os

from flask import redirect, render_template, request, url_for, flash
from flask_app import lm, admin
from flask_login import login_user, logout_user, current_user
from flask_admin.contrib.sqla import ModelView

from sqlalchemy import func, case
from functools import wraps

from api import VaingloryApi
from models import *
from commons import *
import process_data
import pprint
import operator
import strings
from collections import Counter

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
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    feeds = process_data.read_from_file(os.path.join(__location__, 'data/data.json'))

    facts = feeds[get_today()]['facts']
    games = facts['games']
    players = facts['players']
    potions = facts['potions']
    krakens = facts['krakens']
    duration = facts['duration']
    avg_duration = facts['avg_duration']
    died_by_minions = facts['died_by_minions']
    max_kills = facts['max_kills']
    max_deaths = facts['max_deaths']
    avg_cs = facts['avg_cs']
    infusions = facts['infusions']
    fountains = facts['fountains']
    mines = facts['mines']
    minions = facts['minions']

    hero_stats = feeds[get_today()]['data']

    top_heroes_win_rate = [i['hero'] for i in sorted(hero_stats, key=lambda x: x['winrate'], reverse=True)[:5]]
    winrate_stats = {}
    for date in feeds:
        s = feeds[date]['data']
        for hero in s:
            if hero['hero'] in top_heroes_win_rate:
                if hero['hero'] in winrate_stats:
                    winrate_stats[hero['hero']][date] = hero['winrate']
                else:
                    winrate_stats[hero['hero']] = {date: hero['winrate']}

    return render_template('blank.html', games=games, players=players, potions=potions, krakens=krakens,
                           duration=duration, avg_duration=avg_duration, died_by_minions=died_by_minions,
                           max_kills=max_kills, max_deaths=max_deaths, avg_cs=avg_cs,
                           infusions=infusions, fountains=fountains, mines=mines, minions=minions,
                           most_wins=0, hero_stats=hero_stats, winrate_stats=winrate_stats)


@app.route('/hero/<hero>/')
def view_hero(hero):
    app.logger.info(hero)

    actor = strings.heroes_inv[hero]

    total_matches = Match.query.count()
    matches = db.session.query(Participant).filter_by(actor=actor).all()
    playrate = (len(matches) / total_matches) * 100
    matches_won = 0
    kda = {'assists': 0, 'deaths': 0, 'kills': 0}
    cs = {'lane': 0, 'jungle': 0}
    items = Counter()
    builds = Counter()
    teammates = Counter()
    single_teammates = Counter()
    enemies = Counter()
    single_enemies = Counter()
    skins = Counter()
    roles_played = Counter()
    players = {}

    for m in matches:
        matches_won += m.winner
        kda['assists'] += m.assists
        kda['deaths'] += m.deaths
        kda['kills'] += m.kills

        cs['lane'] += m.nonJungleMinionKills
        cs['jungle'] += m.jungleKills

        skins[m.skinKey] += 1

        # best players
        p = m.player.name
        if p in players:
            players[p]['total'] += 1
            players[p]['win'] += m.winner
        else:
            players[p] = {'total': 1, 'win': m.winner }

        # common builds
        _items = [strings.items[i] for i in m.items]
        _items.sort()
        if _items:
            for i in _items:
                items[i] += 1
            _items = ', '.join(_items)
            builds[_items] += 1

        _team = [strings.heroes[x.actor] for x in m.roster.participants]
        _team.sort()

        # common teammates
        for i in _team:
            if hero != i.lower():
                single_teammates[i] += 1

        _team = ', '.join(_team)
        if _team:
            teammates[_team] += 1

        # common enemies
        r = m.roster
        x = [i for i in m.roster.match.rosters if i.id != r.id][0]

        _team = [strings.heroes[x.actor] for x in x.participants]
        _team.sort()

        for i in _team:
            if hero != i.lower():
                single_enemies[i] += 1

        _team = ', '.join(_team)
        if _team:
            enemies[_team] += 1

        # roles played
        role = hero_determine_role(_items, m.assists, m.kills, m.nonJungleMinionKills, m.jungleKills)
        roles_played[role] += 1

    threshold = 3
    players2 = {}
    for p, v in players.iteritems():
        if v['total'] > threshold:
            w = v['win'] / v['total'] * 100
            players2[p] = {'total': v['total'], 'win': v['win'], 'ratio': w}

    items = items.most_common(5)
    builds = builds.most_common(5)
    teammates = teammates.most_common(5)
    players2 = sorted(players2.iteritems(), key=lambda x: x[1]['ratio'], reverse=True)[:25]
    skins = skins.most_common(5)
    enemies = enemies.most_common(5)
    single_enemies = single_enemies.most_common(10)
    single_teammates = single_teammates.most_common(10)

    return render_template('hero.html', hero=hero, matches_played=len(matches), matches_won=matches_won, playrate=playrate,
                           kda=kda, items=items, builds=builds, players=players2,
                           teammates=teammates, skins=skins, enemies=enemies,
                           single_teammates=single_teammates, single_enemies=single_enemies, cs=cs,
                           roles_played=roles_played)


# ------------------
# DATA
# ------------------
@app.route('/data/')
def store_data():
    app.logger.info("Request data 00")

    games = Match.query.count()
    players = Player.query.count()
    potions = sum([i["*1000_Item_HalcyonPotion*"] for i, in db.session.query(Participant.itemUses).all() if "*1000_Item_HalcyonPotion*" in i])
    infusions = sum([i["*1052_Item_WeaponInfusion*"] for i, in db.session.query(Participant.itemUses).all() if "*1052_Item_WeaponInfusion*" in i])
    fountains = sum([i["*1045_Item_FountainOfRenewal*"] for i, in db.session.query(Participant.itemUses).all() if "*1045_Item_FountainOfRenewal*" in i])
    mines = sum([i["*1054_Item_ScoutTrap*"] for i, in db.session.query(Participant.itemUses).all() if "*1054_Item_ScoutTrap*" in i])
    krakens = sum([i[0] for i in db.session.query(Participant.krakenCaptures, ).group_by(Participant.roster_id).all()])
    minions = float(db.session.query(func.sum(Participant.minionKills)).scalar())
    kills = db.session.query(func.sum(Participant.kills)).scalar()
    max_kills = db.session.query(func.max(Participant.kills)).scalar()
    deaths = db.session.query(func.sum(Participant.deaths)).scalar()
    max_deaths = db.session.query(func.max(Participant.deaths)).scalar()
    died_by_minions = int(deaths - kills)
    duration = int(db.session.query(func.sum(Match.duration).label("duration")).scalar())
    avg_duration = int(duration / games)

    avg_cs = [i[0] for i in db.session.query(Participant.farm).filter(Participant.actor.in_([h for h, r in strings.hero_roles.iteritems() if "Lane" in r])).all()]
    avg_cs = sum(avg_cs) / len(avg_cs)

    heroes = db.session.query(Participant.actor, func.count(Participant.actor))\
        .group_by(Participant.actor).order_by(func.count(Participant.actor)).all()

    app.logger.info("Request data 01")

    heroes_win_rate = db.session.query(Participant.actor, func.sum(case([(Participant.winner == True, 1)], else_=0)).label("winrate"))\
        .group_by(Participant.actor).order_by("winrate").all()

    heroes_win_rate = [(hero[0], (herowr[1] / hero[1]) * 100) for hero in heroes for herowr in heroes_win_rate if hero[0] == herowr[0]]
    heroes_win_rate = sorted(heroes_win_rate, key=operator.itemgetter(1), reverse=True)

    app.logger.info("Request data 02")

    heroes_kda = db.session.query(Participant.actor, func.sum(Participant.kills).label("kills"),
                                  func.sum(Participant.deaths).label("deaths"),
                                  func.sum(Participant.assists).label("assists"))\
        .group_by(Participant.actor).all()

    heroes_cs = db.session.query(Participant.actor, func.sum(Participant.nonJungleMinionKills).label("lane"),
                                  func.sum(Participant.minionKills).label("jungle"),
                                  func.sum(Participant.farm).label("farm")) \
        .group_by(Participant.actor).all()

    hero_stats = []
    for hero in heroes:
        stats = {'hero': strings.heroes[hero[0]], 'games': hero[1], 'playrate': float((hero[1] / games) * 100)}
        for hero2 in heroes_win_rate:
            if hero[0] == hero2[0]:
                stats['winrate'] = float(hero2[1])

        for hero2 in heroes_kda:
            if hero[0] == hero2[0]:
                stats['kills'] = float(hero2.kills)
                stats['deaths'] = float(hero2.deaths)
                stats['assists'] = float(hero2.assists)

        for hero2 in heroes_cs:
            if hero[0] == hero2[0]:
                stats['lane'] = float(hero2.lane)
                stats['jungle'] = float(hero2.jungle)
                stats['farm'] = float(hero2.farm)

        hero_stats.append(stats)


    app.logger.info("Request data 03")

    facts = {'games': games, 'players': players, 'potions': potions, 'krakens': krakens, 'duration': duration,
             'avg_duration': avg_duration, 'died_by_minions': died_by_minions, 'max_kills': max_kills,
             'max_deaths': max_deaths, 'avg_cs': avg_cs, 'infusions': infusions, 'fountains': fountains,
             'mines': mines, 'minions': minions}


    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    process_data.save_to_file(os.path.join(__location__, 'data/data.json'), hero_stats, facts)
    return render_template('200.html')

@app.route('/query/')
def query_matches():
    api = VaingloryApi("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJkNzYzYTkyMC1kYzMyLTAxMzQtYTc1NC0wMjQyYWMxMTAwMDMiLCJpc3MiOiJnYW1lbG9ja2VyIiwib3JnIjoiZmVycm9uLXNhYW4tbGl2ZS1ubCIsImFwcCI6ImQ3NjFjZDUwLWRjMzItMDEzNC1hNzUzLTAyNDJhYzExMDAwMyIsInB1YiI6InNlbWMiLCJ0aXRsZSI6InZhaW5nbG9yeSIsInNjb3BlIjoiY29tbXVuaXR5IiwibGltaXQiOjEwfQ.o6z5i-2pfAjrcaw_NAchOzWm2ZcGvmNfwA7U7Hgd0Lg")
    # s = api.sample()
    # process_data.process_samples(s)

    # split request to batches of 50
    max_limit = 50
    limit = 450
    matches = []
    for batch in range(0, limit, max_limit):
        response = api.matches(offset=batch, limit=max_limit, sort="-createdAt")
        matches.append(dict(response))
        limit -= max_limit

    process_data.process_batch_query(matches)
    return render_template('200.html')

@app.route('/samples/')
def query_samples():
    api = VaingloryApi("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJkNzYzYTkyMC1kYzMyLTAxMzQtYTc1NC0wMjQyYWMxMTAwMDMiLCJpc3MiOiJnYW1lbG9ja2VyIiwib3JnIjoiZmVycm9uLXNhYW4tbGl2ZS1ubCIsImFwcCI6ImQ3NjFjZDUwLWRjMzItMDEzNC1hNzUzLTAyNDJhYzExMDAwMyIsInB1YiI6InNlbWMiLCJ0aXRsZSI6InZhaW5nbG9yeSIsInNjb3BlIjoiY29tbXVuaXR5IiwibGltaXQiOjEwfQ.o6z5i-2pfAjrcaw_NAchOzWm2ZcGvmNfwA7U7Hgd0Lg")
    s = api.sample()
    process_data.process_samples(s)

    return render_template('200.html')


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
