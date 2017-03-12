from __future__ import division

import os

import sys
from flask import redirect, render_template, request, url_for, flash
from sqlalchemy.exc import SQLAlchemyError

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
    avg_time_to_afk = facts['avg_time_to_afk']

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
    for hero, stats in winrate_stats.iteritems():
        stats = sorted(stats.iteritems(), key=lambda x: x[0])
        sorted_winrate_stats.append((hero, stats))

    return render_template('dashboard.html', games=games, players=players, potions=potions, krakens=krakens,
                           duration=duration, avg_duration=avg_duration, died_by_minions=died_by_minions,
                           max_kills=max_kills, max_deaths=max_deaths, avg_cs=avg_cs,
                           infusions=infusions, fountains=fountains, mines=mines, minions=minions,
                           most_wins=0, hero_stats=hero_stats, winrate_stats=sorted_winrate_stats,
                           tierlist=tierlist, turrets=turrets, red_side=red_side, blue_side=blue_side, afks=afks,
                           avg_afk=avg_afk)


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

    return render_template('hero.html', hero=hero, matches_played=matches_played, matches_won=matches_won, playrate=playrate,
                           kda=kda, items=items, builds=builds, players=players,
                           teammates=teammates, skins=skins, enemies=enemies,
                           single_teammates=single_teammates, single_enemies=single_enemies, cs=cs,
                           roles_played=roles_played)


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
    return render_template('winrates.html', winrates=winrates)\


@app.route('/map/')
def telemetry():
    return render_template('telemetry.html')


@app.route('/about/')
def about():
    return render_template('about.html')


# ------------------
# DATA
# ------------------
@app.route('/data/')
def store_data():
    app.logger.info("Request data 00")

    games = Match.query.count()
    players = Player.query.count()
    potions = sum([i["Halcyon Potion"] for i, in db.session.query(Participant.itemUses).all() if "Halcyon Potion" in i])
    infusions = sum([i["Weapon Infusion"] for i, in db.session.query(Participant.itemUses).all() if "Weapon Infusion" in i])
    fountains = sum([i["Fountain of Renewal"] for i, in db.session.query(Participant.itemUses).all() if "Fountain of Renewal" in i])
    mines = sum([i["Scout Trap"] for i, in db.session.query(Participant.itemUses).all() if "Scout Trap" in i])
    krakens = sum([i[0] for i in db.session.query(Participant.krakenCaptures, ).group_by(Participant.roster_id).all()])
    turrets = sum([i[0] for i in db.session.query(Participant.turrentCaptures, ).group_by(Participant.roster_id).all()])
    minions = float(db.session.query(func.sum(Participant.minionKills)).scalar())
    kills = db.session.query(func.sum(Participant.kills)).scalar()
    max_kills = db.session.query(func.max(Participant.kills)).scalar()
    deaths = db.session.query(func.sum(Participant.deaths)).scalar()
    max_deaths = db.session.query(func.max(Participant.deaths)).scalar()
    died_by_minions = int(deaths - kills)
    duration = int(db.session.query(func.sum(Match.duration).label("duration")).scalar())
    avg_duration = int(duration / games)
    afks = db.session.query(func.count(Participant.wentAfk)).filter(Participant.wentAfk == 1).scalar()
    afks_per_match = afks / games
    time_to_afk = db.session.query(func.sum(Participant.firstAfkTime)).filter(Participant.firstAfkTime != -1).scalar()
    avg_time_to_afk = int(time_to_afk / afks)

    blue_side_total = db.session.query(func.count(Roster.side)).join(Participant).filter(Roster.side == "left/blue").scalar()
    blue_side = db.session.query(func.count(Roster.side)).join(Participant).filter(Roster.side == "left/blue", Participant.winner == 1).scalar()
    red_side_total = db.session.query(func.count(Roster.side)).join(Participant).filter(Roster.side == "right/red").scalar()
    red_side = db.session.query(func.count(Roster.side)).join(Participant).filter(Roster.side == "right/red", Participant.winner == 1).scalar()
    red_side_winrate = red_side / red_side_total
    blue_side_winrate = blue_side / blue_side_total

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

    facts = {'games': games, 'players': players, 'potions': potions, 'krakens': krakens, 'turrets': turrets, 'duration': duration,
             'avg_duration': avg_duration, 'died_by_minions': died_by_minions, 'max_kills': max_kills,
             'max_deaths': max_deaths, 'avg_cs': avg_cs, 'infusions': infusions, 'fountains': fountains,
             'mines': mines, 'minions': minions, 'blue_side_winrate': blue_side_winrate, 'red_side_winrate': red_side_winrate,
             'afks': afks, 'afks_per_match': afks_per_match, 'avg_time_to_afk': avg_time_to_afk}


    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    process_data.save_to_file(os.path.join(__location__, 'data/data.json'), hero_stats, facts)

    matches = db.session.query(Participant).all()
    tierlist_lane = Counter()
    tierlist_jungle = Counter()
    tierlist_protector = Counter()

    for m in matches:
        _items = sorted(m.items)
        if _items:
            _items = ', '.join(_items)

            buildpath = hero_determine_buildpath(_items)
            role = hero_determine_role(_items, m.assists, m.kills, m.nonJungleMinionKills, m.jungleKills)

            entry = (strings.heroes[m.actor], buildpath)

            if role == "Lane":
                tierlist_lane[entry] += 1
            elif role == "Jungle":
                tierlist_jungle[entry] += 1
            else:
                tierlist_protector[entry] += 1

    process_data.save_to_file_tierlist(os.path.join(__location__, 'data/tierlist.json'), tierlist_lane.most_common(30), tierlist_jungle.most_common(30), tierlist_protector.most_common(30))


    winrates_vs_heroes = {}
    for m in matches:
        hero = strings.heroes[m.actor]

        if hero not in winrates_vs_heroes:
            winrates_vs_heroes[hero] = {}

        roster = m.roster
        for teammate in roster.participants:
            tm_hero = strings.heroes[teammate.actor]
            won = teammate.winner

            if tm_hero in winrates_vs_heroes[hero]:
                winrates_vs_heroes[hero][tm_hero]['total_with'] += 1
                winrates_vs_heroes[hero][tm_hero]['won_with'] += won
            else:
                winrates_vs_heroes[hero][tm_hero] = {'total_with': 1, 'won_with': won, 'total_against': 0, 'won_against': 0}


        x = [i for i in m.roster.match.rosters if i.id != roster.id][0]
        for enemy in x.participants:
            enemy_hero = strings.heroes[enemy.actor]
            won = enemy.winner

            if enemy_hero in winrates_vs_heroes[hero]:
                winrates_vs_heroes[hero][enemy_hero]['total_against'] += 1
                winrates_vs_heroes[hero][enemy_hero]['won_against'] += won
            else:
                winrates_vs_heroes[hero][enemy_hero] = {'total_with': 0, 'won_with': 0, 'total_against': 1, 'won_against': won}

    for hero in winrates_vs_heroes.keys():
        for teammate in winrates_vs_heroes[hero].keys():
            total = winrates_vs_heroes[hero][teammate]['total_with']
            won = winrates_vs_heroes[hero][teammate]['won_with']
            if total > 0:
                ratio = (won / total) * 100
            else:
                ratio = 0
            winrates_vs_heroes[hero][teammate]['ratio_with'] = ratio

        for enemy in winrates_vs_heroes[hero].keys():
            total = winrates_vs_heroes[hero][enemy]['total_against']
            won = winrates_vs_heroes[hero][enemy]['won_against']
            if total > 0:
                ratio = (won / total) * 100
            else:
                ratio = 0
            winrates_vs_heroes[hero][enemy]['ratio_against'] = ratio

    process_data.save_to_file_winrates(os.path.join(__location__, 'data/winrates_vs.json'), winrates_vs_heroes)

    hero_details = {}
    for hero, actor in strings.heroes_inv.iteritems():
        matches = db.session.query(Participant).filter_by(actor=actor).all()
        playrate = (len(matches) / games) * 100
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
        buildpaths = Counter()
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
            _items = sorted(m.items)
            if _items:
                for i in _items:
                    items[i] += 1
                _items = ', '.join(_items)
                builds[_items] += 1

            _team = sorted([strings.heroes[x.actor] for x in m.roster.participants])

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

            _team = sorted([strings.heroes[x.actor] for x in x.participants])

            for i in _team:
                if hero != i.lower():
                    single_enemies[i] += 1

            _team = ', '.join(_team)
            if _team:
                enemies[_team] += 1

            # roles played
            role = hero_determine_role(_items, m.assists, m.kills, m.nonJungleMinionKills, m.jungleKills)
            roles_played[role] += 1

            if _items:
                buildpath = hero_determine_buildpath(_items)
                buildpaths[buildpath] += 1

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

        hero_details[hero] = {'matches_played': len(matches), 'matches_won':matches_won, 'playrate': playrate,
                          'kda':kda, 'items': items, 'builds': builds, 'players': players2,
                          'teammates': teammates, 'skins': skins, 'enemies': enemies,
                          'single_teammates': single_teammates, 'single_enemies': single_enemies, 'cs': cs,
                          'roles_played': roles_played}

    process_data.save_to_file_winrates(os.path.join(__location__, 'data/hero_details.json'), hero_details)

    return redirect(url_for('index'))

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
        try:
            response = api.matches(offset=batch, limit=max_limit, createdAtStart="{0}T00:00:00Z".format(get_yesterday("%Y-%m-%d")), createdAtEnd="{0}T00:00:00Z".format(get_today("%Y-%m-%d")), sort="-createdAt", gameMode="casual, ranked")
            matches.append(dict(response))
            limit -= max_limit
        except:
            app.logger.error("Unexpected error:", sys.exc_info()[0])

        if limit % 450 == 0:
            app.logger.info("time.sleep(60)")
            time.sleep(60)

    process_data.process_batch_query(matches)
    return render_template('200.html')

@app.route('/samples/')
def query_samples():
    api = VaingloryApi("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJkNzYzYTkyMC1kYzMyLTAxMzQtYTc1NC0wMjQyYWMxMTAwMDMiLCJpc3MiOiJnYW1lbG9ja2VyIiwib3JnIjoiZmVycm9uLXNhYW4tbGl2ZS1ubCIsImFwcCI6ImQ3NjFjZDUwLWRjMzItMDEzNC1hNzUzLTAyNDJhYzExMDAwMyIsInB1YiI6InNlbWMiLCJ0aXRsZSI6InZhaW5nbG9yeSIsInNjb3BlIjoiY29tbXVuaXR5IiwibGltaXQiOjEwfQ.o6z5i-2pfAjrcaw_NAchOzWm2ZcGvmNfwA7U7Hgd0Lg")
    s = api.sample(sort="-createdAt")

    process_data.download_samples(s)
    process_data.process_samples()

    return render_template('200.html')


@app.route('/telemetry/')
def query_telemetry():
    process_data.process_telemetry()
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
