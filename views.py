import os

from flask import render_template, request
import pprint
from commons import *
import process_data
import six

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# ------------------
# METHODS
# ------------------

@app.route('/')

@app.route('/index/')
def index():
    feeds = process_data.read_from_file(os.path.join(__location__, 'data/data.json'))
    tierlist = process_data.read_from_file(os.path.join(__location__, 'data/tierlist.json'))

    latest = get_latest(tierlist.keys())

    tierlist = tierlist[latest]

    facts = feeds[latest]['facts']
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
    turrets = facts['turrets']
    red_side = facts['red_side_winrate']
    blue_side = facts['blue_side_winrate']
    afks = facts['afks']
    avg_afk = facts['afks_per_match']
    great_karma = facts['great_karma']
    crystal_sentries = facts['crystal_sentries']
    gold_miners = facts['gold_miners']
    lowest_player_lvl = facts['lowest_player_lvl']
    surrendered = facts['surrendered']

    hero_stats = feeds[latest]['data']

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

    sorted_winrate_stats = []
    for hero, stats in six.iteritems(winrate_stats):
        stats = sorted(six.iteritems(stats), key=lambda x: x[0])
        sorted_winrate_stats.append((hero, stats[-7:]))

    return render_template('dashboard.html', games=games, players=players, potions=potions, krakens=krakens,
                           duration=duration, avg_duration=avg_duration, died_by_minions=died_by_minions,
                           max_kills=max_kills, max_deaths=max_deaths, avg_cs=avg_cs,
                           infusions=infusions, fountains=fountains, mines=mines, minions=minions,
                           most_wins=0, hero_stats=hero_stats, winrate_stats=sorted_winrate_stats,
                           tierlist=tierlist, turrets=turrets, red_side=red_side, blue_side=blue_side, afks=afks,
                           avg_afk=avg_afk, great_karma=great_karma, crystal_sentries=crystal_sentries,
                           gold_miners=gold_miners, lowest_player_lvl=lowest_player_lvl, surrendered=surrendered)


@app.route('/hero/<hero>/')
def view_hero(hero):
    app.logger.info(hero)

    hero_details = process_data.read_from_file(os.path.join(__location__, 'data/hero_details.json'))
    latest = get_latest(hero_details.keys())

    hero_details = hero_details[latest][hero]

    matches_played=hero_details['matches_played']
    matches_won=hero_details['matches_won']
    playrate=hero_details['playrate']
    kda=hero_details['kda']
    items=hero_details['items']
    builds=hero_details['builds']
    players=hero_details['players']
    teammates=hero_details['teammates']
    skins=hero_details['skins']
    enemies=hero_details['enemies']
    single_teammates=hero_details['single_teammates']
    single_enemies=hero_details['single_enemies']
    cs=hero_details['cs']
    roles_played=hero_details['roles_played']
    buildpaths=hero_details['buildpaths']

    total_actual_damage_dealt=hero_details['total_actual_damage_dealt']
    max_actual_damage_dealt=hero_details['max_actual_damage_dealt']
    turret_damage=hero_details['turret_damage']
    kraken_damage=hero_details['kraken_damage']
    ability_lvl=[(eval(i[0]), i[1]) for i in (hero_details['ability_lvl'])]
    ability_used=hero_details['ability_used']
    ability_order=hero_details['ability_order']
    abilities = strings.abilities[strings.heroes_inv[hero]].keys() # TODO combine the different ability names...

    winrates = process_data.read_from_file(os.path.join(__location__, 'data/winrates_vs.json'))
    winrates = winrates[latest][hero]

    return render_template('hero.html', hero=hero, matches_played=matches_played, matches_won=matches_won, playrate=playrate,
                           kda=kda, items=items, builds=builds, players=players,
                           teammates=teammates, skins=skins, enemies=enemies,
                           single_teammates=single_teammates, single_enemies=single_enemies, cs=cs,
                           roles_played=roles_played, buildpaths=buildpaths, winrates=winrates, fact=fact,
                           total_actual_damage_dealt=total_actual_damage_dealt,
                           max_actual_damage_dealt=max_actual_damage_dealt,
                           turret_damage=turret_damage, kraken_damage=kraken_damage, ability_lvl=ability_lvl,
                           ability_used=ability_used, ability_order=ability_order, abilities=abilities
                           )


@app.route('/tierlist/')
def tierlist():
    tierlist = process_data.read_from_file(os.path.join(__location__, 'data/tierlist.json'))
    latest = get_latest(tierlist.keys())

    tierlist = tierlist[latest]

    return render_template('tierlist.html', tierlist=tierlist)


@app.route('/winrates/')
def winrates():
    winrates = process_data.read_from_file(os.path.join(__location__, 'data/winrates_vs.json'))
    latest = get_latest(winrates.keys())
    winrates = winrates[latest]
    return render_template('winrates.html', winrates=winrates)


@app.route('/map/')
def telemetry():
    return render_template('telemetry.html', beta=True)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/fact/')
def fact():
    return render_template('fact.html')

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
def internal_error(e):
    return render_template('404.html'), 500
