from bs4 import BeautifulSoup
import requests
from buffpy.api import API
from buffpy.models.update import Update
from buffpy.managers.updates import Updates


def get_content():
    tweet_content = {}
    r = requests.get("http://nuzzel.com/Level39CW")
    soup = BeautifulSoup(r.content, 'html.parser')
    content = soup.find_all("a", {"class": "js-update-body-link-color"})

    for link in content:
        if "http" in link.get("href"):
            url = link.get("href")
            mess_description = link.text
            desc = mess_description.replace('\n', '').strip()
            tweet_content[desc] = url
    return tweet_content


def show_content():
    for k, v in get_content().items():
        print('\n' + k + '\n' + v)


def set_api():
    api = API(client_id='CLIENT_ID',
              client_secret='CLIENT_SECRET',
              access_token='ACCESS_TOKEN')
    # profile = Profiles(api=api).filter(service='twitter') - is this needed?
    setup = Updates(api=api, profile_id='PROFILE_ID')
    return setup


def update_buffer():
    setup = set_api()
    tweet_content = get_content()
    for k, v in tweet_content.items():
        setup.new(text=k + ': ' + v)


update_buffer()
