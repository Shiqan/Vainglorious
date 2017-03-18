from flask_app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '%r' % (self.username)


class Hero(db.Model):
    __tablename__ = "hero"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(128))
    img = db.Column(db.String(2048))

    def __init__(self, **kwargs):
        super(Hero, self).__init__(**kwargs)


class Item(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(128))
    img = db.Column(db.String(2048))

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)


class Match(db.Model):
    __tablename__ = "match"

    id = db.Column(db.String(128), primary_key=True)
    createdAt = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    gameMode = db.Column(db.String(128))
    shardId = db.Column(db.String(128))
    patchVersion = db.Column(db.String(128))
    endGameReason = db.Column(db.String(128))
    queue = db.Column(db.String(128))

    rosters = db.relationship("Roster", backref="match")
    telemetry = db.relationship("Match_Telemetry", backref="match")

    def __init__(self, **kwargs):
        super(Match, self).__init__(**kwargs)
        # do custom initialization here


class Match_Telemetry(db.Model):
    __tablename__ = "match_telemetry"

    id = db.Column(db.String(128), primary_key=True)
    match_id = db.Column(db.String(128), db.ForeignKey("match.id"))

    first_blood = db.Column(db.String(128))


    def __init__(self, **kwargs):
        super(Match_Telemetry, self).__init__(**kwargs)


class Roster(db.Model):
    __tablename__ = "roster"

    id = db.Column(db.String(128), primary_key=True)
    match_id = db.Column(db.String(128), db.ForeignKey("match.id"))
    acesEarned = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    heroKills = db.Column(db.Integer)
    krakenCaptures = db.Column(db.Integer)
    side = db.Column(db.String(128))
    turrentKills = db.Column(db.Integer)
    turrentsRemaining = db.Column(db.Integer)

    participants = db.relationship("Participant", backref="roster")

    def __init__(self, **kwargs):
        super(Roster, self).__init__(**kwargs)
        # do custom initialization here

class Participant(db.Model):
    __tablename__ = "participant"

    id = db.Column(db.String(128), primary_key=True)
    player_id = db.Column(db.String(128), db.ForeignKey("player.id"))
    roster_id = db.Column(db.String(128), db.ForeignKey("roster.id"))

    actor = db.Column(db.String(128))
    kills = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    crystalMineCaptures = db.Column(db.Integer)
    goldMindCaptures = db.Column(db.Integer)
    krakenCaptures = db.Column(db.Integer)
    turrentCaptures = db.Column(db.Integer)

    winner = db.Column(db.Boolean)

    farm = db.Column(db.Integer)
    minionKills = db.Column(db.Integer)
    nonJungleMinionKills = db.Column(db.Integer)
    jungleKills = db.Column(db.Integer)

    firstAfkTime = db.Column(db.Integer)
    wentAfk = db.Column(db.Boolean)
    itemGrants = db.Column(db.PickleType)
    itemSells = db.Column(db.PickleType)
    itemUses = db.Column(db.PickleType)
    items = db.Column(db.PickleType)

    skinKey = db.Column(db.String(128))
    karmaLevel = db.Column(db.Integer)
    level = db.Column(db.Integer)
    skillTier = db.Column(db.Integer)

    telemetry = db.relationship("Participant_Telemetry", backref="participant", uselist=False)

    def __init__(self, **kwargs):
        super(Participant, self).__init__(**kwargs)
        # do custom initialization here


class Participant_Telemetry(db.Model):
    __tablename__ = "participant_telemetry"

    id = db.Column(db.String(128), primary_key=True)
    participant_id = db.Column(db.String(128), db.ForeignKey("participant.id"))

    total_damage_dealt = db.Column(db.Integer)
    total_actual_damage_dealt = db.Column(db.Integer)

    max_damage_dealt = db.Column(db.Integer)
    max_actual_damage_dealt = db.Column(db.Integer)

    kraken_damage = db.Column(db.Integer)
    turret_damage = db.Column(db.Integer)

    default_attacks = db.Column(db.Integer)

    damage_to_heroes = db.Column(db.PickleType)
    actual_damage_to_heroes = db.Column(db.PickleType)

    ability_order = db.Column(db.PickleType)
    ability_usage = db.Column(db.PickleType)

    item_damage = db.Column(db.PickleType)

    damage_curve = db.Column(db.PickleType)
    xp_curve = db.Column(db.PickleType)
    item_bought = db.Column(db.PickleType)
    level_up = db.Column(db.PickleType)

    def __init__(self, **kwargs):
        super(Participant_Telemetry, self).__init__(**kwargs)


class Player(db.Model):
    __tablename__ = "player"

    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128))
    lifetimeGold = db.Column(db.Integer)
    lossStreak = db.Column(db.Integer)
    winStreak = db.Column(db.Integer)
    played = db.Column(db.Integer)
    played_ranked = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    xp = db.Column(db.Integer)

    participated = db.relationship("Participant", backref="player")

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        # do custom initialization here