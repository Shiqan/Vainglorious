from flask_app import app, appname
import time
import strings
import random

@app.context_processor
def utility_processor():
    def get_random_quote():
        q = random.choice(strings.quotes)
        return "{0} - {1}".format(q[1], q[0])
    return dict(appname=appname, random_quote=get_random_quote())

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
    lane = 0
    jungle = 0
    protector = 0

    if build:
        for item in build.split(', '):
            if item in ["Fountain of Renewal", "Crucible", "War Treads", "Nullwave Gauntlet", "Contraption"]:
                protector += 1

    if assists > kills:
        protector += 1
    else:
        jungle += 1
        lane += 1

    if cs_lane > cs_jungle:
        lane += 2
    else:
        jungle += 2


    if lane > jungle and lane > protector:
        return "Lane"
    if jungle > lane and jungle > protector:
        return "Jungle"
    if protector > lane and protector > jungle:
        return "Protector"
    return None

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