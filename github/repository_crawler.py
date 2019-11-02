import requests
from bs4 import BeautifulSoup


class RepositoryCrawler:
    def __init__(self, username, repository_name, reverse=False):
        self.repository_name = repository_name
        self.username = username
        self.reverse = reverse

    @property
    def repository_url(self):
        return f'https://github.com/{self.username}/{self.repository_name}/'

    @property
    def commit(self):
        res = requests.get(self.repository_name).text
        soup = BeautifulSoup(res, 'html.parser')
        check_code = [tag.string for tag in soup.find_all('a', {'class':'sha'})]
        if self.reverse:
            check_code.reverse()
        return check_code