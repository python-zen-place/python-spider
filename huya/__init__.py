from bs4 import BeautifulSoup
import requests
import re


class Crawler:
    def __init__(self, url):
        assert 'https://www.huya.com/' in url, '地址有误'
        self._url = url

    @property
    def url(self):
        return self._url

    @property
    def pid(self):
        try:
            headers = {
                'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                'accept-encoding': "gzip, deflate, br",
                'accept-language': "zh,zh-CN;q=0.9,en;q=0.8",
                'cache-control': "max-age=0,no-cache",
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
                'Host': "www.huya.com",
            }
            html = requests.get(self.url).text
            soup = BeautifulSoup(html)
            res = soup.find(name='a', attrs={'class': 'host-video'})
            pid = res['href'].split('/')[-1]
        except (ConnectionError, TimeoutError, WindowsError) as e:
            print(e)
            raise e

    @property
    def union_name(self):
        info_url = 'https://chgate.huya.com/proxy/index?service=thrift_sign&amp;iface=getSignChannelInfo&amp;callback' \
                   '=getSignChannelInfo&amp;data={}'.format(self.pid)
        html = requests.get(info_url).text
        union_name = re.findall(r'\"name\":\"(.*?)\",', html)[0]
        print(union_name)
