import json
import requests
from requests import session
from config import config
from .utils import get_tomorrow_week_number, get_tomorrow_weekday


class Crawler:
    session_ = None

    is_login = False

    token = ''
    session_id = ''

    account = ''
    password = ''

    info = None

    def __init__(self, account=config['login_account'],
                 password=config['login_password']):
        if self.session_ is None:
            self.session_ = session()
        self.account = account
        self.password = password

    def login(self):
        payload = f'{{"userCode":"{self.account}","password":"{self.password}","userCodeType":"account"}}'
        response = requests.request('POST', config['login_url'],
                                    data=payload,
                                    headers=config['login_headers'])
        j_response = json.loads(response.text)

        if j_response['errorCode'] != "success":
            return
        self.token = j_response['data']['token']
        self.session_id = response.cookies.get_dict()['SESSION']
        self.is_login = True

    def get_info(self):
        if not self.is_login:
            return
        headers = config['api_headers']
        headers['TOKEN'] = self.token
        headers['Cookie'] = f'SESSION={self.session_id}; token='
        payload = f'{{"jczy013id":"2019-2020-1","pkgl002id":"W13414710000WH","zt":"2","pkzc":"{get_tomorrow_week_number()}"}}'
        response= self.session_.request('POST', config['api_url'],
                                        data=payload,
                                        headers=headers)
        weekday = get_tomorrow_weekday()
        data = json.loads(response.text)['data']
        data.sort(key=lambda x: int(x['pksjmx'][:3]))
        self.info = [x for x in data if x['pksjmx'].startswith(f'{weekday}')]

    def __call__(self):
        self.login()
        self.get_info()

    def __repr__(self):
        return '\n'.join([x['pksjshow']+'\n' +
                        x['kc_name']+'\n' +
                        x['teachernames_1']+'\n' +
                        x['js_name'] + '\n' for x in self.info])


