from bs4 import BeautifulSoup
import requests

from .ContributedDay import ContributedDay


class Crawler:
    def __init__(self, username):
        self.contribute_days = []
        self.username = username

    @property
    def contribute_url(self):
        return f'https://github.com/users/{self.username}/contributions'

    def get_contribute(self):
        res = requests.get(self.contribute_url).text
        soup = BeautifulSoup(res, 'html.parser')
        rects = soup.find_all('rect')
        for rect in rects:
            if rect['fill'] == '#ebedf0':
                pass
            else:
                self.contribute_days.append(ContributedDay(rect['data-date'], rect['data-count']))

    def __repr__(self):
        if len(self.contribute_days) == 0:
            return 'It seems that you have not worked this year'
        return '\n'.join(map(str, self.contribute_days))
