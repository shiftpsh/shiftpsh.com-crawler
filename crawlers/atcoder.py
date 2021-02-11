import requests
import re
from bs4 import BeautifulSoup
import api

ATCODER_PROFILE_URL = "https://atcoder.jp/users/shiftpsh?lang=en"
ATCODER_RANKING_URL = "https://atcoder.jp/ranking?lang=en"


def crawl_profile():
    return requests.get(ATCODER_PROFILE_URL)


def parse_profile(document):
    soup = BeautifulSoup(document, "html.parser")
    rows = soup.find_all("tr")

    ac_rating = None
    ac_rating_highest = None
    ac_rank = None

    for row in rows:
        th = row.find('th')
        td = row.find('td')
        if th is None or td is None:
            continue
        if th.text == "Rank":
            match = re.findall(r"\d+", td.text)
            if len(match) > 0:
                ac_rank = match[0]
        if th.text == "Rating":
            match = re.findall(r"\d+", td.text)
            if len(match) > 0:
                ac_rating = match[0]
        if th.text == "Highest Rating":
            match = re.findall(r"\d+", td.text)
            if len(match) > 0:
                ac_rating_highest = match[0]
    return {
        "ac_rank": ac_rank,
        "ac_rating": ac_rating,
        "ac_rating_highest": ac_rating_highest
    }


def crawl_rank_page_count():
    return requests.get(ATCODER_RANKING_URL)


def parse_rank_page_count(document):
    soup = BeautifulSoup(document, "html.parser")
    items = soup.select("ul.pagination > li")
    max_page = 0

    for item in items:
        match = re.findall(r"\d+", item.text)
        if len(match) > 0:
            max_page = max(max_page, int(match[0]))

    return max_page


def run():
    response_profile = crawl_profile()
    if response_profile.status_code != 200:
        print(f"{__file__}: Request failed with status code {response_profile.status_code}")
        return

    for key, value in parse_profile(response_profile.content).items():
        if value is None:
            print(f"{__file__}: Parsing {key} failed")
            return
        update_response = api.update(key, value)
        if update_response.status_code != 200:
            print(f"{__file__}: Update of value {key} failed with status code {update_response.status_code}")
            return

    response_rank_page_count = crawl_rank_page_count()
    if response_rank_page_count.status_code != 200:
        print(f"{__file__}: Request failed with status code {response_rank_page_count.status_code}")
        return

    rank_page_count = parse_rank_page_count(response_rank_page_count.content)
    if rank_page_count == 0:
        print(f"rank_page_count was zero")
        return

    update_response = api.update("ac_total_user_count", rank_page_count * 100)
    if update_response.status_code != 200:
        print(f"{__file__}: Update failed with status code {update_response.status_code}")
        return

    print(f"{__file__}: Successfully updated")
