import requests
from bs4 import BeautifulSoup

class Crawler:
    def __int__(self):
        pass

    @property
    def contribute_url(self):
        return 'https://github.com/users/saltoyster/contributions'

    @property
    def rgb_table(self):
        return {
            '#ebedf0': 'You didn\'t work that day',
            '#c6e48b': 'you work a little',
            '#7bc96f': 'you work nearly half a day',
            '#239a3b': 'you work hard',
            '#196127': 'you work very Hard'
        }

    def get_contribute(self):
        res = requests.get(self.contribute_url)
        soup = BeautifulSoup(res)
        colors = list(map(lambda x: x['fill'], soup.find_all('rect')))
        for x in colors:
            print(self.rgb_table[x])