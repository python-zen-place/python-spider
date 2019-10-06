import multiprocessing

from bs4 import BeautifulSoup
import requests

from .ContributedDay import ContributedDay
from collections import Counter


def require_login(fun):
    def wrapper(self, *args, **kwargs):
        if self.is_login:
            return fun(self, *args, **kwargs)
        else:
            raise AssertionError('Require Login')
    return wrapper

# warning: it seems that using class variable to record the total use of language may cause error when you try to
#          get two or more user's language information and I can't think out a solution to it.
#          so you should avoid using more than one instance at one time.


class Crawler:
    def __init__(self, username, password=None):
        self.username = username
        self.password = password
        self.is_login = False
        self.session = requests.session()
        self.contributed_days = []
        self.repositories_links_list = []
        self.language = Counter()

    @property
    def BASEURL(self):
        return 'https://github.com/'

    @property
    def login_url(self):
        return 'https://github.com/login'

    @property
    def session_url(self):
        return 'https://github.com/session'

    @property
    def contribution_url(self):
        return f'https://github.com/users/{self.username}/contributions'

    @property
    def repositories_url(self):
        return f'https://github.com/{self.username}?tab=repositories'

    def login(self):
        assert self.password, 'Password required'
        res = self.session.get(self.login_url).text
        soup = BeautifulSoup(res, 'html.parser')
        token = soup.find('input', {'name': 'authenticity_token'})['value']
        res = self.session.post(self.session_url, data={
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': token,
            'login': self.username,
            'password': self.password,
        }).text
        soup = BeautifulSoup(res, 'html.parser')
        if 'logged-in' in soup.body['class']:
            self.is_login = True
            return True
        raise TimeoutError

    def get_contributions(self):
        res = self.session.get(self.contribution_url).text
        soup = BeautifulSoup(res, 'html.parser')
        rects = soup.find_all('rect')
        for rect in rects:
            if rect['fill'] == '#ebedf0':
                pass
            else:
                self.contributed_days.append(ContributedDay(rect['data-date'], rect['data-count']))

    def show_contributions(self):
        if len(self.contributed_days) == 0:
            print('It seems that you have not worked this year')
        else:
            print(f'You contributions {ContributedDay.total_contributions} times in the last year\n' +
                  '\n'.join(map(str, self.contributed_days)))

    def get_repositories(self):
        res = self.session.get(self.repositories_url).text
        soup = BeautifulSoup(res, 'html.parser')
        self.repositories_links_list = [self.BASEURL + tag['href']
                                        for tag in soup.find_all('a', itemprop='name codeRepository')]

    def show_repositories(self):
        if len(self.repositories_links_list) == 0:
            return 'It seems that you have no public repository'
        else:
            print(f'You have  {len(self.repositories_links_list)} repository\n' +
                  '\n'.join(self.repositories_links_list))

    def get_language(self):
        for link in self.repositories_links_list:
            res = self.session.get(link).text
            soup = BeautifulSoup(res, 'html.parser')
            for tag in soup.find_all('span', class_='language-color', itemprop='keywords'):
                language = tag['aria-label'].split()[0]
                use = float(tag['aria-label'].split()[1][:-1])/100
                self.language.update({language: use})

    def show_language(self):
        language_sum = sum(self.language.values())
        language_type = len(self.language.keys())
        if language_type == 1:
            print(f'You use {language_type} type of language')
        else:
            print(f'You use {language_type} types of language')
        for language, use in self.language.items():
            print(f'{language}: {use/language_sum}')
