import os
import sys

import time

import process_data
from api import VaingloryApi
from commons import get_yesterday, get_today

api_key = os.environ.get('API_KEY', None)
api = VaingloryApi(api_key)


def samples():
    s = api.sample(sort="-createdAt", createdAtStart="{0}T00:00:00Z".format(get_yesterday("%Y-%m-%d")),
                   createdAtEnd="{0}T00:00:00Z".format(get_today("%Y-%m-%d")))

    process_data.download_samples(s)
    process_data.process_samples()


def query_matches():
    max_limit = 5
    limit = 1000
    matches = []
    for batch in range(0, limit, max_limit):
        try:
            response = api.matches(offset=batch, limit=max_limit,
                                   createdAtStart="{0}T00:00:00Z".format(get_yesterday("%Y-%m-%d")),
                                   createdAtEnd="{0}T00:00:00Z".format(get_today("%Y-%m-%d")), sort="-createdAt",
                                   gameMode="casual, ranked")
            matches.append(dict(response))
            limit -= max_limit
        except:
            print("Unexpected error:", sys.exc_info()[0])

        if limit % 50 == 0:
            print("time.sleep(60)")
            time.sleep(60)

    process_data.process_batch_query(matches)


if __name__ == "__main__":
    samples()
    # query_matches()
    process_data.update_json_files()