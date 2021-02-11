import requests
import api
import json

TOPCODER_SOURCE_URL = "http://api.topcoder.com/v2/users/shiftpsh"


def crawl():
    return requests.get(TOPCODER_SOURCE_URL)


def parse(document):
    data = json.loads(document)
    if data['ratingSummary'] is None:
        return None

    if len(data['ratingSummary']) == 0:
        return None

    tc_rating = None

    for item in data['ratingSummary']:
        if item['name'] != "Algorithm":
            continue
        tc_rating = item["rating"]
        break
    return {
        "tc_rating": tc_rating
    }


def run():
    response = crawl()
    if response.status_code == 200:
        for key, value in parse(response.content).items():
            if value is None:
                print(f"{__file__}: Parsing {key} failed")
                return
            update_response = api.update(key, value)
            if update_response.status_code != 200:
                print(f"{__file__}: Update of value {key} failed with status code {update_response.status_code}")
                return
    else:
        print(f"{__file__}: Request failed with status code {response.status_code}")
        return
    print(f"{__file__}: Successfully updated")
