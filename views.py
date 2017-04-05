import os

from flask import render_template, request, jsonify
import pprint
from commons import *
import process_data
import six
from flask_app import cache

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# ------------------
# METHODS
# ------------------


@cache.memoize()
@app.route('/')
@app.route('/index/')
@app.route('/index/<region>/')
def index(region="eu"):
    feeds = process_data.read_from_file(os.path.join(__location__, 'data/{0}/data.json'.format(region)))
    tierlist = process_data.read_from_file(os.path.join(__location__, 'data/{0}/tierlist.json'.format(region)))

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

    return render_template('dashboard.html', region=region, games=games, players=players, potions=potions, krakens=krakens,
                           duration=duration, avg_duration=avg_duration, died_by_minions=died_by_minions,
                           max_kills=max_kills, max_deaths=max_deaths, avg_cs=avg_cs,
                           infusions=infusions, fountains=fountains, mines=mines, minions=minions,
                           most_wins=0, hero_stats=hero_stats, winrate_stats=sorted_winrate_stats,
                           tierlist=tierlist, turrets=turrets, red_side=red_side, blue_side=blue_side, afks=afks,
                           avg_afk=avg_afk, great_karma=great_karma, crystal_sentries=crystal_sentries,
                           gold_miners=gold_miners, lowest_player_lvl=lowest_player_lvl, surrendered=surrendered)


@cache.memoize()
@app.route('/hero/<hero>/')
@app.route('/hero/<hero>/<region>/')
def view_hero(hero, region="eu"):
    app.logger.info(hero)

    hero_details = process_data.read_from_file(os.path.join(__location__, 'data/{0}/hero_details.json'.format(region)))
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

    winrates = process_data.read_from_file(os.path.join(__location__, 'data/{0}/winrates_vs.json'.format(region)))
    winrates = winrates[latest][hero]

    return render_template('hero.html', region=region, hero=hero, matches_played=matches_played, matches_won=matches_won, playrate=playrate,
                           kda=kda, items=items, builds=builds, players=players,
                           teammates=teammates, skins=skins, enemies=enemies,
                           single_teammates=single_teammates, single_enemies=single_enemies, cs=cs,
                           roles_played=roles_played, buildpaths=buildpaths, winrates=winrates, fact=fact,
                           total_actual_damage_dealt=total_actual_damage_dealt,
                           max_actual_damage_dealt=max_actual_damage_dealt,
                           turret_damage=turret_damage, kraken_damage=kraken_damage, ability_lvl=ability_lvl,
                           ability_used=ability_used, ability_order=ability_order, abilities=abilities
                           )


@cache.memoize()
@app.route('/tierlist/')
@app.route('/tierlist/<region>/')
def tierlist(region="eu"):
    tierlist = process_data.read_from_file(os.path.join(__location__, 'data/{0}/tierlist.json'.format(region)))
    latest = get_latest(tierlist.keys())

    tierlist = tierlist[latest]

    return render_template('tierlist.html', region=region, tierlist=tierlist)


@cache.memoize()
@app.route('/winrates/')
@app.route('/winrates/<region>/')
def winrates(region="eu"):
    winrates = process_data.read_from_file(os.path.join(__location__, 'data/{0}/winrates_vs.json'.format(region)))
    latest = get_latest(winrates.keys())
    winrates = winrates[latest]
    return render_template('winrates.html', region=region, winrates=winrates)


@app.route('/map/')
@app.route('/map/<region>/')
def telemetry(region="eu"):
    return render_template('telemetry.html', region=region, beta=True)


@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/compare/')
@app.route('/compare/<region>/')
def compare(region="eu"):

    feeds_ea = process_data.read_from_file(os.path.join(__location__, 'data/{0}/data.json'.format("ea")))
    feeds_eu = process_data.read_from_file(os.path.join(__location__, 'data/{0}/data.json'.format("eu")))
    feeds_na = process_data.read_from_file(os.path.join(__location__, 'data/{0}/data.json'.format("na")))
    feeds_sa = process_data.read_from_file(os.path.join(__location__, 'data/{0}/data.json'.format("sa")))
    feeds_sg = process_data.read_from_file(os.path.join(__location__, 'data/{0}/data.json'.format("sg")))

    latest = get_latest(feeds_eu.keys())
    feeds = {"ea": feeds_ea, "eu": feeds_eu, "na": feeds_na, "sa": feeds_sa, "sg": feeds_sg}

    best_heroes = {}
    for r, feed in six.iteritems(feeds):
        hero_stats = feed[latest]['data']
        best_heroes[r] = sorted(hero_stats, key=lambda x: x['winrate'], reverse=True)[0]



    return render_template('compare.html', region=region, best_heroes=best_heroes, ea=feeds_ea, eu=feeds_eu, na=feeds_na, sa=feeds_sa, sg=feeds_sg)


@app.route('/fact/')
@app.route('/fact/<region>/')
def fact(region="eu"):
    return render_template('fact.html', region=region)


@app.route('/ajax_fact/')
@app.route('/ajax_fact/<region>/')
def ajax_fact(region="eu"):
    facts = process_data.read_from_file(os.path.join(__location__, 'data/{0}/facts.json'.format(region)))
    latest = get_latest(facts.keys())
    facts = facts[latest]
    fact = random.choice(facts)

    return jsonify(fact=fact)

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
