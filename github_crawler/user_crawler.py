from collections import Counter

import requests
from bs4 import BeautifulSoup

from .contributed_day import ContributedDay
from .repository_crawler import RepositoryCrawler

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


class UserCrawler:
    def __init__(self, username, password=None):
        self.username = username
        self.password = password
        self.is_login = False
        self.session = requests.session()

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

    @property
    def contributions(self):
        """

        :return: return user's contributions of last year
        :rtype: ContributedDay list
        """
        contributed_days = []
        res = self.session.get(self.contribution_url).text
        soup = BeautifulSoup(res, 'html.parser')
        rects = soup.find_all('rect')
        for rect in rects:
            if rect['fill'] == '#ebedf0':
                pass
            else:
                contributed_days.append(ContributedDay(rect['data-date'], rect['data-count']))
        return contributed_days

    @property
    def repositories(self):
        """

        :return: return all urls of user
        :rtype:  string list
        """
        res = self.session.get(self.repositories_url).text
        soup = BeautifulSoup(res, 'html.parser')
        return [self.BASEURL + tag['href'] for tag in soup.find_all('a', itemprop='name codeRepository')]

    @property
    def language(self):
        """
        PS: You should not use the variable 'use' straightly
            You need to divide the sum of 'use'
        :return: a counter of language usage
        :rtype: Counter
        """
        for link in self.repositories:
            language = Counter()
            res = self.session.get(link).text
            soup = BeautifulSoup(res, 'html.parser')
            for tag in soup.find_all('span', class_='language-color', itemprop='keywords'):
                language = tag['aria-label'].split()[0]
                use = float(tag['aria-label'].split()[1][:-1])
                language.update({language: use})
            return language

    @property
    def commit(self, repository_name=None):
        """

        :param repository_name: name of repository
        :return: check-out code of target repository
        :rtype: string list
        """
        if not repository_name:
            raise AttributeError('Repository name required')
        crawler = RepositoryCrawler(self.username, repository_name)
        return crawler.commit

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



