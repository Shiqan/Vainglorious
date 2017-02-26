from flask_app import app, appname
import time
from decimal import *
import strings


@app.context_processor
def utility_processor():
    return dict(appname=appname)


# # --------- ITEM
@app.template_filter('role_to_img')
def role_to_img(role):
    if role == "Lane":
        return "hero-icon-lane.png"
    if role == "Jungle":
        return "hero-icon-jungle.png"
    if role == "Protector":
        return "hero-icon-protector.png"


@app.template_filter('buildpath_to_img')
def buildpath_to_img(path):
    if path == "CP":
        return "items/shatterglass.png"
    if path == "WP":
        return "items/sorrowblade.png"
    if path == "UT":
        return "items/fountain-of-renewal.png"


@app.template_filter('convert_time')
def seconds_to_hours(time):
    # m, s = divmod(time, 60)
    # if s < 10:
    #     s = "0"+str(s)
    # return "{0}:{1}".format(m, s)
    return time / 3600


@app.template_filter('convert_game_time')
def seconds_to_minutes(time):
    m, s = divmod(time, 60)
    if s < 10:
        s = "0"+str(s)
    return "{0}:{1}".format(int(m), int(s))


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

def hero_determine_role(build, assists, kills, cs_lane, cs_jungle):
    if "Fountain of Renewal" in build and "Crucible" in build and assists > kills:
        return "Protector"
    if cs_lane > cs_jungle:
        return "Lane"

    return "Jungle"


def hero_determine_buildpath(build):
    wp = 0
    cp = 0
    ut = 0
    if build == []:
        return None

    for item in build.split(', '):
        if item in ["Broken Myth", "Shatterglass", "Frostburn", "Alternating Current", "Eve of Harvast", "Aftershock"]:
            cp += 1

        if item in ["Breaking Point", "Sorrowblade", "Tyrant's Monocle", "Tornado Trigger", "Serpent Mask", "Bonesaw"]:
            wp += 1

        if item in ["Fountain of Renewal", "Crucible", "War Treads", "Nullwave Gauntlet", "Contraption", "Atlas Pauldron"]:
            ut += 1

    if cp > wp and cp > ut:
        return "CP"
    if wp > cp and wp > ut:
        return "WP"
    if ut > cp and ut > wp:
        return "UT"

    return None


def convert_date(date_str):
    return time.strptime(date_str, "%m/%d/%Y")


def get_today():
    return time.strftime("%m/%d/%Y")