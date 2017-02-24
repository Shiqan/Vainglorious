from flask_app import app, appname
import time
from decimal import *
import strings


@app.context_processor
def utility_processor():
    return dict(appname=appname)
#
# @app.template_filter('id_to_position')
# def id_to_position(id):
#     return positions[id]
#
# @app.template_filter('id_to_mode')
# def id_to_mode(id):
#     return modes[id]
#
# # --------- USER
#
# @app.template_filter('id_to_user')
# def id_to_user_name(id):
#     user = db.session.query(User).filter_by(id=id).first()
#     return user.username
#
# def id_to_user(id):
#     user = db.session.query(User).filter_by(id=id).first()
#     return user
#
# # --------- HERO
# @app.template_filter('id_to_hero')
# def id_to_hero_name(id):
#     hero = db.session.query(Hero).filter_by(id=id).first()
#     return hero.name
#
# @app.template_filter('id_to_hero_img')
# def id_to_hero_img(id):
#     hero = db.session.query(Hero).filter_by(id=id).first()
#     return hero.img
#
# @app.template_filter('id_to_hero_splash')
# def id_to_hero_splash(id):
#     hero = db.session.query(Hero).filter_by(id=id).first()
#     splash = hero.name+"_splash.png"
#     return splash.lower()
#
# def id_to_hero(id):
#     hero = db.session.query(Hero).filter_by(id=id).first()
#     return hero
#
#
# # --------- ITEM
# @app.template_filter('id_to_item')
# def id_to_item_name(id):
#     item = db.session.query(Item).filter_by(id=id).first()
#     return item.name
#
# @app.template_filter('id_to_item_img')
# def id_to_item_img(id):
#     item = db.session.query(Item).filter_by(id=id).first()
#     return item.img
#
#
# def id_to_item(id):
#     item = db.session.query(Item).filter_by(id=id).first()
#     return item
#
#
#
# # ---------
@app.template_filter('convert_time')
def seconds_to_hours(time):
    # m, s = divmod(time, 60)
    # if s < 10:
    #     s = "0"+str(s)
    # return "{0}:{1}".format(m, s)
    return time / Decimal(3600)


@app.template_filter('convert_game_time')
def seconds_to_minutes(time):
    m, s = divmod(time, 60)
    if s < 10:
        s = "0"+str(s)
    return "{0}:{1:.2}".format(m, s)


@app.template_filter('convert_hero_name')
def id_to_hero(id):
    return strings.heroes[id]


@app.template_filter('format_number')
def format_currency(value):
    return "{:,}".format(value)


@app.template_filter('get_hero_roles')
def hero_to_role(id):
    if id in strings.hero_roles:
        return strings.hero_roles[id]
    else:
        return strings.hero_roles[strings.heroes_inv[id]]


def convert_date(date_str):
    return time.strptime(date_str, "%m/%d/%Y")


def get_today():
    return time.strftime("%m/%d/%Y")