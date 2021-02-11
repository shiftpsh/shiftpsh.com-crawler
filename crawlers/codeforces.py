import requests
import api
import json

CODEFORCES_SOURCE_URL = "https://codeforces.com/api/user.ratedList?activeOnly=true"


def crawl():
    return requests.get(CODEFORCES_SOURCE_URL)


def parse(document):
    data = json.loads(document)
    if data['status'] != "OK":
        return None

    cf_total_user_count = len(data['result'])
    cf_rank = None
    cf_rating = None
    cf_rating_highest = None
    for idx, item in enumerate(data['result'], start=1):
        if item['handle'] != "shiftpsh":
            continue
        cf_rank = idx
        cf_rating = item["rating"]
        cf_rating_highest = item["maxRating"]
        break
    return {
        "cf_total_user_count": cf_total_user_count,
        "cf_rank": cf_rank,
        "cf_rating": cf_rating,
        "cf_rating_highest": cf_rating_highest
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
