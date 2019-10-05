import multiprocessing

from bs4 import BeautifulSoup
import requests

from .ContributedDay import ContributedDay
from .Language import Language


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

        self.contributed_days = []
        self.repositories_links_list = []
        self.language = []

    @property
    def BASEURL(self):
        return 'https://github.com/'

    @property
    def login_url(self):
        return 'https://github.com/login'

    @property
    def contribution_url(self):
        return f'https://github.com/users/{self.username}/contributions'

    @property
    def repositories_url(self):
        return f'https://github.com/{self.username}?tab=repositories'

    def login(self):
        assert self.password, 'Password required'

    def get_contributions(self):
        res = requests.get(self.contribution_url).text
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
        res = requests.get(self.repositories_url).text
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
            res = requests.get(link).text
            soup = BeautifulSoup(res, 'html.parser')
            for tag in soup.find_all('span', class_='language-color', itemprop='keywords'):
                language = tag['aria-label'].split()[0]
                use = float(tag['aria-label'].split()[1][:-1])/100
                self.language.append(Language(language, use))

    def show_language(self):
        if Language.total_use == 0:
            print('It seems that you have not worked this year')
        else:
            print(f'You use {len(Language.language_dict.keys())} types of language \n' +\
                  '\n'.join(map(str, self.language)))


