import pprint
import datetime
from flask_app import app, db
from models import Match, Roster, Participant, Player
from sqlalchemy.exc import SQLAlchemyError


def process_batch_query(matches):
    for batch in matches:
        for m in batch['data']:
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


def process_query(matches):
    for m in matches['data']:
        process_match(m)

        for roster in m['relationships']['rosters']['data']:
            roster_data = [i for i in matches['included'] if i['id'] == roster['id']]
            assert len(roster_data) == 1
            process_roster(roster_data[0], m['id'])

            for participant in roster_data[0]['relationships']['participants']['data']:
                participant_data = [i for i in matches['included'] if i['id'] == participant['id']]
                assert len(participant_data) == 1


                player_data = [i for i in matches['included'] if i['id'] == participant_data[0]['relationships']['player']['data']['id']]
                assert len(player_data) == 1
                process_player(player_data[0])

                process_participant(participant_data[0], roster['id'])


def process_match(data):
    m = Match(id=data['id'],
              createdAt=datetime.datetime.strptime(data['attributes']['createdAt'], '%Y-%m-%dT%H:%M:%SZ'),
              duration=data['attributes']['duration'],
              gameMode=data['attributes']['gameMode'],
              patchVersion=data['attributes']['patchVersion'],
              shardId=data['attributes']['shardId'],
              endGameReason=data['attributes']['stats']['endGameReason'],
              queue=data['attributes']['stats']['queue'])

    test = db.session.query(Match).get(m.id)
    if not test:
        db.session.add(m)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error('ERROR: Session rollback - reason "%s"' % str(e))


def process_roster(data, match_id):
    r = Roster(id=data['id'], match_id=match_id,
                   acesEarned=data['attributes']['stats']['acesEarned'],
                   gold=data['attributes']['stats']['gold'],
                   heroKills=data['attributes']['stats']['heroKills'],
                   krakenCaptures=data['attributes']['stats']['krakenCaptures'],
                   side=data['attributes']['stats']['side'],
                   turrentKills=data['attributes']['stats']['turretKills'],
                   turrentsRemaining=data['attributes']['stats']['turretsRemaining'])

    test = db.session.query(Roster).get(r.id)
    if not test:
        db.session.add(r)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error('ERROR: Session rollback - reason "%s"' % str(e))


def process_participant(data, roster_id):
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
                    wins=data['attributes']['stats']['wins'])

    test = db.session.query(Participant).get(p.id)
    if not test:
        db.session.add(p)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error('ERROR: Session rollback - reason "%s"' % str(e))


def process_player(data):
    p = Player(id=data['id'], name=data['attributes']['name'],
               lifetimeGold=data['attributes']['stats']['lifetimeGold'],
               lossStreak=data['attributes']['stats']['lossStreak'],
               winStreak=data['attributes']['stats']['winStreak'])

    test = db.session.query(Player).get(p.id)
    if not test:
        db.session.add(p)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error('ERROR: Session rollback - reason "%s"' % str(e))
