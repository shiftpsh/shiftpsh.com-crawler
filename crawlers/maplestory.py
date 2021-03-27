import requests
import re
from bs4 import BeautifulSoup
import api
import base64

MAPLESTORY_SOURCE_URL = "https://maplestory.nexon.com/Ranking/World/Total?c=%EC%8B%B6%ED%94%84%ED%8A%B8"


def get_as_base64(url):
    response = requests.get(url)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode('ascii')
    return None


def crawl():
    return requests.get(MAPLESTORY_SOURCE_URL)


def parse(document):
    soup = BeautifulSoup(document, "html.parser")
    row = soup.select(".search_com_chk")
    level = re.findall(r"Lv\.(\d+)", str(row))
    img = soup.select(".search_com_chk span.char_img > img")
    if len(level) > 0 and len(img) > 0:
        img_base64 = get_as_base64(img[0]['src'])
        print(img_base64)
        if img_base64 is None:
               return None
        return {
            "maple_level": level[0],
            "maple_character_image": f"data:image/png;base64, {img_base64}"
        }
    return None


def run():
    response = crawl()
    if response.status_code == 200:
        parsed = parse(response.content)
        if parsed is None:
            print(f"{__file__}: Parsing response failed: {response.content}")
            return
        for key, value in parsed.items():
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
