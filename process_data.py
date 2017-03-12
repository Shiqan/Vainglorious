import os
import pprint
import datetime
from flask_app import app, db
from models import Match, Roster, Participant, Player
from sqlalchemy.exc import SQLAlchemyError
import json
import commons
import requests, zipfile, StringIO

def download_samples(samples):
    for sample in samples['data']:
        # pprint.pprint(sample)
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
                if m['data']['attributes']['gameMode'] in ['ranked', 'casual']:
                    skill = []
                    for roster in m['data']['relationships']['rosters']['data']:
                        roster_data = [i for i in m['included'] if i['id'] == roster['id']]
                        for participant in roster_data[0]['relationships']['participants']['data']:
                            participant_data = [i for i in m['included'] if i['id'] == participant['id']]
                            skill.append(participant_data[0]['attributes']['stats']['skillTier'])

                    if (sum(skill) / len(skill)) > 25:
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

def process_batch_query(matches):
    app.logger.info("Process {0} batches".format(len(matches)))
    for batch in matches:
        app.logger.info("Process {0} matches".format(len(batch['data'])))
        for m in batch['data']:

            if m['attributes']['gameMode'] in ['ranked', 'casual']:
                skill = []
                for roster in m['relationships']['rosters']['data']:
                    roster_data = [i for i in batch['included'] if i['id'] == roster['id']]
                    for participant in roster_data[0]['relationships']['participants']['data']:
                        participant_data = [i for i in batch['included'] if i['id'] == participant['id']]
                        skill.append(participant_data[0]['attributes']['stats']['skillTier'])

                if (sum(skill)/len(skill)) > 25:
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