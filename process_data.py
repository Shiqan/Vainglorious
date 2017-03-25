from __future__ import division

import StringIO
import datetime
import json
import operator
import os
import pprint
import uuid
import zipfile
from collections import Counter

import requests
import six
from sqlalchemy import func, case
from sqlalchemy.exc import SQLAlchemyError

import commons
import strings
from flask_app import app, db
from models import Match, Roster, Participant, Player, Participant_Telemetry

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def download_samples(samples):
    for sample in samples['data']:
        pprint.pprint(sample)
        r = requests.get(sample['attributes']['URL'], stream=True)
        z = zipfile.ZipFile(StringIO.StringIO(r.content))
        z.extractall()


def process_samples():
    app.logger.info("Process samples")
    for root, dirs, files in os.walk('D:\\\\vainglory'):
        dirs[:] = [d for d in dirs if d.startswith('sample') or d.startswith('matches')]
        for f in files:
            if f.lower().endswith((".json")):
                json_data = open(os.path.join(root, f), 'r').read()
                m = json.loads(json_data)
                actors = []
                if m['data']['attributes']['gameMode'] in ['ranked', 'casual']:
                    skill = []
                    for roster in m['data']['relationships']['rosters']['data']:
                        roster_data = [i for i in m['included'] if i['id'] == roster['id']]
                        for participant in roster_data[0]['relationships']['participants']['data']:
                            participant_data = [i for i in m['included'] if i['id'] == participant['id']]
                            skill.append(participant_data[0]['attributes']['stats']['skillTier'])

                    if (sum(skill) / len(skill)) > 26:
                        if m['data']['relationships']['assets']['data']:
                            download_telemetry(
                                [i for i in m['included'] if i['id'] == m['data']['relationships']['assets']['data'][0]['id']][0], m['data']['id'])
                        process_match(m['data'])

                        for roster in m['data']['relationships']['rosters']['data']:
                            roster_data = [i for i in m['included'] if i['id'] == roster['id']]
                            assert len(roster_data) == 1
                            process_roster(roster_data[0], m['data']['id'])

                            for participant in roster_data[0]['relationships']['participants']['data']:
                                participant_data = [i for i in m['included'] if i['id'] == participant['id']]
                                assert len(participant_data) == 1

                                player_data = [i for i in m['included'] if
                                               i['id'] == participant_data[0]['relationships']['player']['data']['id']]
                                assert len(player_data) == 1
                                process_player(player_data[0])

                                process_participant(participant_data[0], roster['id'])

                                participant_id = participant_data[0]['id']
                                participant_actor = participant_data[0]['attributes']['actor']
                                actors.append(
                                    (participant_id, participant_actor, roster_data[0]['attributes']['stats']['side']))

                        # process_telemetry(m['data']['id'], actors)


def download_telemetry(telemetry, id):
    try:
        r = requests.get(telemetry['attributes']['URL'])
        root = 'D:\\\\vainglory\\telemetry'
        f = open(os.path.join(root, '{0}.json'.format(id)), 'w+')
        json.dump(r.json(), f)
        f.close()
    except Exception as e:
        app.logger.error("Error when downloading telemetry for match {0}: {1}".format(id, e))
        return


def process_telemetry(match_id, actors=list()):
    app.logger.info("Process telemetry {0} with {1}".format(match_id, actors))
    root = 'D:\\\\vainglory\\telemetry'

    if not os.path.isfile(os.path.join(root, match_id+".json")):
        return

    json_data = open(os.path.join(root, match_id)+".json", 'r').read()
    m = json.loads(json_data)

    stats = dict()

    for i in actors:
        side = i[2].split('/')[0].lower().title()

        stats["{0}_{1}".format(i[1], side)] = {'ability_usage': {}, 'ability_order': [],
                                               'total_damage_dealt': 0, 'total_actual_damage_dealt': 0,
                                               'max_damage_dealt': 0, 'max_actual_damage_dealt': 0,
                                               'kraken_damage': 0, 'turret_damage': 0,
                                               'default_attacks': 0,
                                               'item_damage': {},
                                               'damage_to_heroes': {},
                                               'actual_damage_to_heroes': {},
                                               'damage_curve': [],
                                               'item_bought': [],
                                               'xp_curve': [],
                                               'level_up': []
                                               }

    for row in m:
        time = row['time']
        if 'LearnAbility' == row['type']:
            ability = row['payload']['Ability']
            lvl = row['payload']['Level']
            actor = row['payload']['Actor']
            side = row['payload']['Team']

            stats["{0}_{1}".format(actor, side)]['ability_order'].append((ability, lvl))
            continue

        if 'UseAbility' == row['type']:
            ability = row['payload']['Ability']
            actor = row['payload']['Actor']
            side = row['payload']['Team']

            if ability in stats["{0}_{1}".format(actor, side)]['ability_usage']:
                stats["{0}_{1}".format(actor, side)]['ability_usage'][ability] += 1
            else:
                stats["{0}_{1}".format(actor, side)]['ability_usage'][ability] = 1
            continue

        if 'BuyItem' == row['type']:
            actor = row['payload']['Actor']
            side = row['payload']['Team']
            item = row['payload']['Item']
            stats["{0}_{1}".format(actor, side)]['item_bought'].append((time, item))
            continue

        if 'LevelUp' == row['type']:
            actor = row['payload']['Actor']
            side = row['payload']['Team']
            level = row['payload']['Level']
            stats["{0}_{1}".format(actor, side)]['level_up'].append((time, level))
            continue

        if 'EarnXP' == row['type']:
            actor = row['payload']['Actor']
            side = row['payload']['Team']
            xp = row['payload']['Amount']
            stats["{0}_{1}".format(actor, side)]['xp_curve'].append((time, xp))
            continue

        if 'DealDamage' == row['type']:
            target = row['payload']['Target']
            actor = row['payload']['Actor']
            side = row['payload']['Team']
            damage = row['payload']['Damage']
            delt = row['payload']['Delt']
            source = row['payload']['Source']

            if target == "*Kraken_Jungle*" or target == "*Kraken_Captured*":
                stats["{0}_{1}".format(actor, side)]['kraken_damage'] += delt

            elif target == "*Turret*":
                stats["{0}_{1}".format(actor, side)]['turret_damage'] += delt

            elif target == "*PetalMinion*":
                pass


            elif row['payload']['IsHero']:

                if target in stats["{0}_{1}".format(actor, side)]['damage_to_heroes']:
                    stats["{0}_{1}".format(actor, side)]['damage_to_heroes'][target] += damage
                else:
                    stats["{0}_{1}".format(actor, side)]['damage_to_heroes'][target] = damage

                if target in stats["{0}_{1}".format(actor, side)]['actual_damage_to_heroes']:
                    stats["{0}_{1}".format(actor, side)]['actual_damage_to_heroes'][target] += delt
                else:
                    stats["{0}_{1}".format(actor, side)]['actual_damage_to_heroes'][target] = delt

            else:
                print(row['payload'])


            stats["{0}_{1}".format(actor, side)]['total_damage_dealt'] += damage
            stats["{0}_{1}".format(actor, side)]['total_actual_damage_dealt'] += delt

            stats["{0}_{1}".format(actor, side)]['damage_curve'].append((time, damage))

            if stats["{0}_{1}".format(actor, side)]['max_damage_dealt'] < damage:
                stats["{0}_{1}".format(actor, side)]['max_damage_dealt'] = damage

            if stats["{0}_{1}".format(actor, side)]['max_actual_damage_dealt'] < delt:
                stats["{0}_{1}".format(actor, side)]['max_actual_damage_dealt'] = delt


            if source.startswith("Buff_Item_"):
                item = source.replace("Buff_Item_", "")

                if target in stats["{0}_{1}".format(actor, side)]['item_damage']:
                    stats["{0}_{1}".format(actor, side)]['item_damage'][item] += damage
                else:
                    stats["{0}_{1}".format(actor, side)]['item_damage'][item] = damage

    for i in actors:
        side = i[2].split('/')[0].lower().title()
        process_participant_telemetry(stats["{0}_{1}".format(i[1], side)], i[0])




def process_batch_query(matches):
    app.logger.info("Process {0} batches".format(len(matches)))
    for batch in matches:
        app.logger.info("Process {0} matches".format(len(batch['data'])))
        for m in batch['data']:
            actors = []
            if m['attributes']['gameMode'] in ['ranked', 'casual']:

                skill = []
                for roster in m['relationships']['rosters']['data']:
                    roster_data = [i for i in batch['included'] if i['id'] == roster['id']]
                    for participant in roster_data[0]['relationships']['participants']['data']:
                        participant_data = [i for i in batch['included'] if i['id'] == participant['id']]
                        skill.append(participant_data[0]['attributes']['stats']['skillTier'])

                if (sum(skill)/len(skill)) > 25:
                    download_telemetry([i for i in batch['included'] if i['id'] == m['relationships']['assets']['data'][0]['id']][0], m['id'])
                    process_match(m)

                    for roster in m['relationships']['rosters']['data']:
                        roster_data = [i for i in batch['included'] if i['id'] == roster['id']]
                        assert len(roster_data) == 1
                        process_roster(roster_data[0], m['id'])

                        for participant in roster_data[0]['relationships']['participants']['data']:
                            participant_data = [i for i in batch['included'] if i['id'] == participant['id']]
                            assert len(participant_data) == 1

                            player_data = [i for i in batch['included'] if i['id'] == participant_data[0]['relationships']['player']['data']['id']]
                            assert len(player_data) == 1
                            process_player(player_data[0])

                            process_participant(participant_data[0], roster['id'])

                            participant_id = participant_data[0]['id']
                            participant_actor = participant_data[0]['attributes']['actor']
                            actors.append((participant_id, participant_actor, roster_data[0]['attributes']['stats']['side']))

                    process_telemetry(m['id'], actors)


def process_match(data):
    test = db.session.query(Match).get(data['id'])
    if not test:
        m = Match(id=data['id'],
                  createdAt=datetime.datetime.strptime(data['attributes']['createdAt'], '%Y-%m-%dT%H:%M:%SZ'),
                  duration=data['attributes']['duration'],
                  gameMode=data['attributes']['gameMode'],
                  patchVersion=data['attributes']['patchVersion'],
                  shardId=data['attributes']['shardId'],
                  endGameReason=data['attributes']['stats']['endGameReason'],
                  queue=data['attributes']['stats']['queue'])

        db.session.add(m)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error('ERROR: Session rollback - reason "%s"' % str(e))


def process_roster(data, match_id):
    test = db.session.query(Roster).get(data['id'])
    if not test:
        r = Roster(id=data['id'], match_id=match_id,
                       acesEarned=data['attributes']['stats']['acesEarned'],
                       gold=data['attributes']['stats']['gold'],
                       heroKills=data['attributes']['stats']['heroKills'],
                       krakenCaptures=data['attributes']['stats']['krakenCaptures'],
                       side=data['attributes']['stats']['side'],
                       turrentKills=data['attributes']['stats']['turretKills'],
                       turrentsRemaining=data['attributes']['stats']['turretsRemaining'])

        db.session.add(r)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error('ERROR: Session rollback - reason "%s"' % str(e))


def process_participant(data, roster_id):
    test = db.session.query(Participant).get(data['id'])
    if not test:
        p = Participant(id=data['id'], roster_id=roster_id,
                        player_id=data['relationships']['player']['data']['id'],
                        actor=data['attributes']['actor'],
                        kills=data['attributes']['stats']['kills'],
                        assists=data['attributes']['stats']['assists'],
                        deaths=data['attributes']['stats']['deaths'],
                        jungleKills=data['attributes']['stats']['jungleKills'],
                        crystalMineCaptures=data['attributes']['stats']['crystalMineCaptures'],
                        goldMindCaptures=data['attributes']['stats']['goldMineCaptures'],
                        krakenCaptures=data['attributes']['stats']['krakenCaptures'],
                        turrentCaptures=data['attributes']['stats']['turretCaptures'],
                        winner=data['attributes']['stats']['winner'],
                        farm=data['attributes']['stats']['farm'],
                        minionKills=data['attributes']['stats']['minionKills'],
                        nonJungleMinionKills=data['attributes']['stats']['nonJungleMinionKills'],
                        firstAfkTime=data['attributes']['stats']['firstAfkTime'],
                        wentAfk=data['attributes']['stats']['wentAfk'],
                        itemGrants=data['attributes']['stats']['itemGrants'],
                        itemSells=data['attributes']['stats']['itemSells'],
                        itemUses=data['attributes']['stats']['itemUses'],
                        items=data['attributes']['stats']['items'],
                        skinKey=data['attributes']['stats']['skinKey'],
                        karmaLevel=data['attributes']['stats']['karmaLevel'],
                        level=data['attributes']['stats']['level'],
                        skillTier=data['attributes']['stats']['skillTier'])

        db.session.add(p)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error('ERROR: Session rollback - reason "%s"' % str(e))


def process_participant_telemetry(data, participant_id):
    test = db.session.query(Participant_Telemetry).filter_by(participant_id = participant_id).first()
    if not test:
        p = Participant_Telemetry(id=uuid.uuid4(), participant_id=participant_id,
                                  total_damage_dealt=data['total_damage_dealt'],
                                  total_actual_damage_dealt=data['total_actual_damage_dealt'],
                                  max_damage_dealt=data['max_damage_dealt'],
                                  max_actual_damage_dealt=data['max_actual_damage_dealt'],
                                  kraken_damage=data['kraken_damage'],
                                  turret_damage=data['turret_damage'],
                                  default_attacks=data['default_attacks'],
                                  damage_to_heroes=data['damage_to_heroes'],
                                  actual_damage_to_heroes=data['actual_damage_to_heroes'],
                                  ability_order=data['ability_order'],
                                  ability_usage=data['ability_usage'],
                                  item_damage=data['item_damage'],
                                  damage_curve=data['damage_curve'],
                                  xp_curve=data['xp_curve'],
                                  item_bought=data['item_bought'],
                                  level_up=data['level_up'])

        db.session.add(p)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error('ERROR: Session rollback - reason "%s"' % str(e))

def process_player(data):
    test = db.session.query(Player).get(data['id'])
    if not test:

        p = Player(id=data['id'], name=data['attributes']['name'],
                   lifetimeGold=data['attributes']['stats']['lifetimeGold'],
                   lossStreak=data['attributes']['stats']['lossStreak'],
                   winStreak=data['attributes']['stats']['winStreak'],
                   played=data['attributes']['stats']['played'],
                   played_ranked=data['attributes']['stats']['played_ranked'],
                   wins=data['attributes']['stats']['wins'],
                   xp=data['attributes']['stats']['xp'])

        db.session.add(p)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error('ERROR: Session rollback - reason "%s"' % str(e))
    else:
        test.lifetimeGold = data['attributes']['stats']['lifetimeGold']
        test.lossStreak = data['attributes']['stats']['lossStreak']
        test.winStreak = data['attributes']['stats']['winStreak']
        test.played = data['attributes']['stats']['played']
        test.played_ranked = data['attributes']['stats']['played_ranked']
        test.wins = data['attributes']['stats']['wins']
        test.xp = data['attributes']['stats']['xp']

        db.session.commit()

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error('ERROR: Session rollback - reason "%s"' % str(e))


def read_from_file(file):
    with open(file, 'r') as f:
        feeds = json.load(f)

    return feeds


def save_to_file(file, data, facts):
    date = commons.get_today()
    entry = {'data': data, 'facts': facts}
    feeds = read_from_file(file)

    with open(file, 'w') as f:
        feeds[date] = entry
        json.dump(feeds, f)


def save_to_file_winrates(file, data):
    date = commons.get_today()
    feeds = read_from_file(file)

    with open(file, 'w') as f:
        feeds[date] = data
        json.dump(feeds, f)


def save_to_file_tierlist(file, lane, jungle, protector):
    date = commons.get_today()
    result1 = [{'name': i[0][0], 'path': i[0][1], 'value': i[1]} for i in lane]
    result2 = [{'name': i[0][0], 'path': i[0][1], 'value': i[1]} for i in jungle]
    result3 = [{'name': i[0][0], 'path': i[0][1], 'value': i[1]} for i in protector]
    entry = {'lane': result1, 'jungle': result2, 'protector': result3}
    feeds = read_from_file(file)

    with open(file, 'w') as f:
        feeds[date] = entry
        json.dump(feeds, f)


def save_to_file_facts(file, facts):
    date = commons.get_today()
    feeds = read_from_file(file)

    with open(file, 'w') as f:
        if date not in feeds:
            feeds[date] = []

        for fact in facts:
            feeds[date].append(fact)
        json.dump(feeds, f)


def update_json_files():
    update_data()
    update_tierlist()
    update_winrates()
    update_hero_details()


def update_data():
    app.logger.info("Generate data.json")
    games = Match.query.count()
    players = Player.query.count()
    itemUses = [i for i, in db.session.query(Participant.itemUses).all() if i is not None]
    potions = sum([i["Halcyon Potion"] for i in itemUses if "Halcyon Potion" in i])
    infusions = sum([i["Weapon Infusion"] for i in itemUses if "Weapon Infusion" in i])
    fountains = sum([i["Fountain of Renewal"] for i in itemUses if "Fountain of Renewal" in i])
    mines = sum([i["Scout Trap"] for i in itemUses if "Scout Trap" in i])
    # potions = sum([i["Halcyon Potion"] for i, in db.session.query(Participant.itemUses).all() if "Halcyon Potion" in i])
    # infusions = sum([i["Weapon Infusion"] for i, in db.session.query(Participant.itemUses).all() if "Weapon Infusion" in i])
    # fountains = sum([i["Fountain of Renewal"] for i, in db.session.query(Participant.itemUses).all() if "Fountain of Renewal" in i])
    # mines = sum([i["Scout Trap"] for i, in db.session.query(Participant.itemUses).all() if "Scout Trap" in i])
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

    blue_side_total = db.session.query(func.count(Roster.side)).join(Participant).filter(Roster.side == "left/blue").scalar()
    blue_side = db.session.query(func.count(Roster.side)).join(Participant).filter(Roster.side == "left/blue", Participant.winner == 1).scalar()
    red_side_total = db.session.query(func.count(Roster.side)).join(Participant).filter(Roster.side == "right/red").scalar()
    red_side = db.session.query(func.count(Roster.side)).join(Participant).filter(Roster.side == "right/red", Participant.winner == 1).scalar()
    red_side_winrate = red_side / red_side_total
    blue_side_winrate = blue_side / blue_side_total

    great_karma = len([i[0] for i in db.session.query(Participant.karmaLevel).filter(Participant.karmaLevel == 2).group_by(Participant.player_id).all()])
    crystal_sentries = sum([i[0] for i in db.session.query(Participant.crystalMineCaptures,).group_by(Participant.roster_id).all()])
    gold_miners = sum([i[0] for i in db.session.query(Participant.goldMindCaptures,).group_by(Participant.roster_id).all()])
    lowest_player_lvl = db.session.query(func.min(Participant.level)).scalar()
    surrendered = db.session.query(func.count(Match.endGameReason)).filter(Match.endGameReason == "surrender").scalar()

    avg_cs = [i[0] for i in db.session.query(Participant.farm).filter(Participant.actor.in_([h for h, r in six.iteritems(strings.hero_roles) if "Lane" in r])).all()]
    avg_cs = sum(avg_cs) / len(avg_cs)

    heroes = db.session.query(Participant.actor, func.count(Participant.actor))\
        .group_by(Participant.actor).order_by(func.count(Participant.actor)).all()

    heroes_win_rate = db.session.query(Participant.actor, func.sum(case([(Participant.winner == True, 1)], else_=0)).label("winrate"))\
        .group_by(Participant.actor).order_by("winrate").all()

    heroes_win_rate = [(hero[0], (herowr[1] / hero[1]) * 100) for hero in heroes for herowr in heroes_win_rate if hero[0] == herowr[0]]
    heroes_win_rate = sorted(heroes_win_rate, key=operator.itemgetter(1), reverse=True)

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

    facts = {'games': games, 'players': players, 'potions': potions, 'krakens': krakens, 'turrets': turrets, 'duration': duration,
             'avg_duration': avg_duration, 'died_by_minions': died_by_minions, 'max_kills': max_kills,
             'max_deaths': max_deaths, 'avg_cs': avg_cs, 'infusions': infusions, 'fountains': fountains,
             'mines': mines, 'minions': minions, 'blue_side_winrate': blue_side_winrate, 'red_side_winrate': red_side_winrate,
             'afks': afks, 'afks_per_match': afks_per_match, 'great_karma': great_karma, 'crystal_sentries': crystal_sentries,
             'gold_miners': gold_miners, 'lowest_player_lvl': lowest_player_lvl, 'surrendered': surrendered}
    save_to_file(os.path.join(__location__, 'data/data.json'), hero_stats, facts)

    fact_list = list()
    fact_list.append("there are {0} games played with average skill tier Vainglorious".format(games))
    fact_list.append("there are {0} players with skill tier Vainglorious".format(players))
    fact_list.append("there are {0} potions used".format(potions))
    fact_list.append("there are {0} krakens unleashed".format(krakens))
    fact_list.append("there are {0} turrets destroyed".format(krakens))
    fact_list.append("there are {0} minions killed".format(minions))
    fact_list.append("the average duration of a match is {0}".format(avg_duration))
    fact_list.append("the maximum of deaths by a single player is {0}".format(max_deaths))
    fact_list.append("the maximum of kills by a single player is {0}".format(max_kills))
    fact_list.append("there are {0} weapon infusions used".format(infusions))
    fact_list.append("there are {0} fountains of renewal used".format(krakens))
    fact_list.append("the winrate of blue side is {0:.0f}% ".format(blue_side_winrate))
    fact_list.append("{0} games ended with a surrender".format(surrendered))
    save_to_file_facts(os.path.join(__location__, 'data/facts.json'), fact_list)



def update_tierlist():
    app.logger.info("Update tierlist.json")
    matches = db.session.query(Participant).all()
    tierlist_lane = Counter()
    tierlist_jungle = Counter()
    tierlist_protector = Counter()

    for m in matches:
        _items = sorted(m.items)
        if _items:
            _items = ', '.join(_items)

            buildpath = commons.hero_determine_buildpath(_items)
            role = commons.hero_determine_role(_items, m.assists, m.kills, m.nonJungleMinionKills, m.jungleKills)

            entry = (strings.heroes[m.actor], buildpath)

            if role == "Lane":
                tierlist_lane[entry] += 1
            elif role == "Jungle":
                tierlist_jungle[entry] += 1
            else:
                tierlist_protector[entry] += 1

    save_to_file_tierlist(os.path.join(__location__, 'data/tierlist.json'), tierlist_lane.most_common(30),
                                       tierlist_jungle.most_common(30), tierlist_protector.most_common(30))


def update_winrates():
    app.logger.info("Update winrates.json")
    matches = db.session.query(Participant).all()
    winrates_vs_heroes = {}
    fact_list = list()

    for m in matches:
        hero = strings.heroes[m.actor].lower()

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
                winrates_vs_heroes[hero][tm_hero] = {'total_with': 1, 'won_with': won, 'total_against': 0,
                                                     'won_against': 0}

        x = [i for i in m.roster.match.rosters if i.id != roster.id][0]
        for enemy in x.participants:
            enemy_hero = strings.heroes[enemy.actor]
            won = enemy.winner

            if enemy_hero in winrates_vs_heroes[hero]:
                winrates_vs_heroes[hero][enemy_hero]['total_against'] += 1
                winrates_vs_heroes[hero][enemy_hero]['won_against'] += won
            else:
                winrates_vs_heroes[hero][enemy_hero] = {'total_with': 0, 'won_with': 0, 'total_against': 1,
                                                        'won_against': won}

    for hero in winrates_vs_heroes.keys():
        for teammate in winrates_vs_heroes[hero].keys():
            total = winrates_vs_heroes[hero][teammate]['total_with']
            won = winrates_vs_heroes[hero][teammate]['won_with']
            if total > 0:
                ratio = (won / total) * 100
            else:
                ratio = 0
            winrates_vs_heroes[hero][teammate]['ratio_with'] = ratio

            fact_list.append("{0} has a winrate of {1}% with {2}".format(hero.title(),  ratio, teammate))
            fact_list.append("{0} has played {1} times with {2}".format(hero.title(),  total, teammate))

        for enemy in winrates_vs_heroes[hero].keys():
            total = winrates_vs_heroes[hero][enemy]['total_against']
            won = winrates_vs_heroes[hero][enemy]['won_against']
            if total > 0:
                ratio = (won / total) * 100
            else:
                ratio = 0
            winrates_vs_heroes[hero][enemy]['ratio_against'] = ratio

            fact_list.append("{0} has a winrate of {1}% against {2}".format(hero.title(),  ratio, enemy))
            fact_list.append("{0} has played {1} times against {2}".format(hero.title(), total, enemy))

    save_to_file_facts(os.path.join(__location__, 'data/facts.json'), fact_list)
    save_to_file_winrates(os.path.join(__location__, 'data/winrates_vs.json'), winrates_vs_heroes)


def update_hero_details():
    app.logger.info("Update hero_details.json")
    hero_details = {}
    games = Match.query.count()
    fact_list = list()

    for hero, actor in six.iteritems(strings.heroes_inv):

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
        ability_order = Counter()
        ability_lvl = Counter()
        ability_used = Counter()

        total_damage_dealt = 0
        total_actual_damage_dealt = 0

        max_damage_dealt = 0
        max_actual_damage_dealt = 0

        kraken_damage = 0
        turret_damage = 0

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
                players[p] = {'total': 1, 'win': m.winner}

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
            role = commons.hero_determine_role(_items, m.assists, m.kills, m.nonJungleMinionKills, m.jungleKills)
            roles_played[role] += 1

            if _items:
                buildpath = commons.hero_determine_buildpath(_items)
                buildpaths[buildpath] += 1

            # telemetry data
            if m.telemetry:
                total_damage_dealt += m.telemetry.total_damage_dealt
                total_actual_damage_dealt += m.telemetry.total_actual_damage_dealt

                if max_damage_dealt < m.telemetry.max_damage_dealt:
                    max_damage_dealt = m.telemetry.max_damage_dealt

                if max_actual_damage_dealt < m.telemetry.max_actual_damage_dealt:
                    max_actual_damage_dealt = m.telemetry.max_actual_damage_dealt

                kraken_damage += m.telemetry.kraken_damage
                turret_damage += m.telemetry.turret_damage

                ability_lvls = {}
                _ability_order = []
                for i in m.telemetry.ability_order:
                    ability_lvls[i[0]] = i[1]
                    _ability_order.append(i[0])

                ability_lvls = sorted(six.iteritems(ability_lvls))
                ability_order[', '.join(_ability_order)] += 1
                ability_lvl[str(ability_lvls)] += 1

                for ability, n in six.iteritems(m.telemetry.ability_usage):
                    ability_used[ability] += n


        threshold = 3
        players2 = {}
        for p, v in six.iteritems(players):
            if v['total'] > threshold:
                w = v['win'] / v['total'] * 100
                players2[p] = {'total': v['total'], 'win': v['win'], 'ratio': w}

        items = items.most_common(5)
        builds = builds.most_common(5)
        teammates = teammates.most_common(5)
        players2 = sorted(six.iteritems(players2), key=lambda x: x[1]['ratio'], reverse=True)[:25]
        skins = skins.most_common(5)
        enemies = enemies.most_common(5)
        single_enemies = single_enemies.most_common(10)
        single_teammates = single_teammates.most_common(10)

        ability_lvl = ability_lvl.most_common(3)
        ability_order = ability_order.most_common(10)


        hero_details[hero] = {'matches_played': len(matches), 'matches_won': matches_won, 'playrate': playrate,
                              'kda': kda, 'items': items, 'builds': builds, 'players': players2,
                              'teammates': teammates, 'skins': skins, 'enemies': enemies,
                              'single_teammates': single_teammates, 'single_enemies': single_enemies, 'cs': cs,
                              'roles_played': roles_played, 'buildpaths': buildpaths,
                              'total_damage_dealt': total_damage_dealt, 'total_actual_damage_dealt': total_actual_damage_dealt,
                              'max_damage_dealt': max_damage_dealt, 'max_actual_damage_dealt': max_actual_damage_dealt,
                              'turret_damage': turret_damage, 'kraken_damage': kraken_damage, 'ability_lvl': ability_lvl,
                              'ability_used': ability_used, 'ability_order': ability_order}

        hero = hero.title()
        fact_list.append("{0} dealt {1} to the Kraken".format(hero, kraken_damage))
        fact_list.append("{0} dealt {1} to turrets".format(hero, turret_damage))
        fact_list.append("{0} dealt {1} damage in total".format(hero, total_damage_dealt))
        fact_list.append("{0} did {1} damage with one attack / ability".format(hero, max_damage_dealt))
        fact_list.append("{0} has played {1} matches".format(hero, len(matches)))
        fact_list.append("{0} has won {1} matchse".format(hero, matches_won))
        fact_list.append("{0} is played in {1}% of the matches".format(hero, matches_won))
        fact_list.append("{0} most used skin is {1}".format(hero, skins[0][0]))
        fact_list.append("{0} plays most games with {1}".format(hero, single_teammates[0][0]))
        fact_list.append("{0} plays most games against {1}".format(hero, single_enemies[0][0]))
        fact_list.append("{0} most bought item is {1}".format(hero, items[0][0]))

    save_to_file_facts(os.path.join(__location__, 'data/facts.json'), fact_list)
    save_to_file_winrates(os.path.join(__location__, 'data/hero_details.json'), hero_details)