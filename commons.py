from flask_app import app, appname
import time


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
def seconds_to_minutes(time):
    m, s = divmod(time, 60)
    if s < 10:
        s = "0"+str(s)
    return "{0}:{1}".format(m, s)

def convert_time(time_str):
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)
#
def convert_date(date_str):
    return time.strptime(date_str, "%m/%d/%Y")

def get_today():
    return time.strftime("%m/%d/%Y")