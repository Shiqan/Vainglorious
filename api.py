import requests
from flask_app import app

class VaingloryApi(object):
    def __init__(self, key, datacenter="dc01", region="eu"):
        self.key = key
        self.region = region
        self.datacenter = datacenter
        self.url = "https://api.{datacenter}.gamelockerapp.com/shards/{region}/".format(datacenter=self.datacenter, region=self.region)

    def request(self, endpoint, params=None):
        app.logger.info("Request {0} with params: {1}".format(endpoint, params))
        headers = {
            "Authorization": "Bearer {}".format(self.key),
            "X-TITLE-ID": "semc-vainglory",
            "Accept": "application/vnd.api+json"
        }
        response = requests.get(self.url + endpoint,
                            headers=headers,
                            params=params)
        response.raise_for_status()
        return response.json()

    def query(self, endpoint, elid="", params=None):
        return self.request(endpoint + "/" + elid, params=params)

    def match(self, match_id):
        return self.query("matches", match_id)

    def player(self, player_id):
        return self.query("players", player_id)

    def sample(self):
        return self.query("samples")

    def matches(self,
                offset=None, limit=None, sort=None,
                createdAtStart=None, createdAtEnd=None,
                player=None, team=None):

        params = dict()
        if offset:
            params["page[offset]"] = offset
        if limit:
            params["page[limit]"] = limit
        if sort:
            params["sort"] = sort
        if createdAtStart:
            params["filter[createdAt-start]"] = createdAtStart
        if createdAtEnd:
            params["filter[createdAt-end]"] = createdAtEnd
        if player:
            params["filter[playerNames]"] = player
        if team:
            params["filter[teamNames]"] = team

        return self.query("matches", params=params)


