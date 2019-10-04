from bs4 import BeautifulSoup
import requests

from .ContributedDay import ContributedDay


def require_login(fun):
    def wrapper(self, *args, **kwargs):
        if self.is_login:
            return fun(self, *args, **kwargs)
        else:
            raise AssertionError('Require Login')

    return wrapper


class Crawler:
    def __init__(self, username):
        self.contribute_days = []
        self.username = username
        self.total_contributes = 0
        self.is_login = False
        self.repositories_links_list = []

    @property
    def BASEURL(self):
        return 'https://github.com/'

    @property
    def contribute_url(self):
        return f'https://github.com/users/{self.username}/contributions'

    @property
    def repositories_url(self):
        return f'https://github.com/{self.username}?tab=repositories'

    def get_contribute(self):
        res = requests.get(self.contribute_url).text
        soup = BeautifulSoup(res, 'html.parser')
        self.total_contributes = int(soup.find('h2').string.split()[0])
        rects = soup.find_all('rect')
        for rect in rects:
            if rect['fill'] == '#ebedf0':
                pass
            else:
                self.contribute_days.append(ContributedDay(rect['data-date'], rect['data-count']))

    def get_repositories(self):
        res = requests.get(self.repositories_url).text
        soup = BeautifulSoup(res, 'html.parser')
        self.repositories_links_list = [self.BASEURL+x['href'] for x in soup.find_all('a', {
            'itemprop': 'name codeRepository'
        })]

    def __repr__(self):
        if len(self.contribute_days) == 0:
            return 'It seems that you have not worked this year'
        return f'You contributions {self.total_contributes} times in the last year\n' +\
               '\n'.join(map(str, self.contribute_days))
