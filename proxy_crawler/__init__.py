from bs4 import BeautifulSoup
import re
import requests
from config import config
from multiprocessing import Pool
import os
import time


def get_proxy(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/78.0.3904.70 Safari/537.36",
    }
    res = requests.get(url, headers=headers).text
    soup = BeautifulSoup(res, 'html.parser')
    servers = soup.find_all(string=re.compile(r'(\d{1,3}\.){3}\d{1,3}'))
    ports = [port.string for port in soup.find_all(name='td', string=re.compile(r'^\d{1,5}$'))]
    return ['{}:{}'.format(server, port) for server, port in zip(servers, ports)]


def test_proxy(proxy, test_url='http://www.baidu.com'):
    proxies = {
        'http': proxy,
        'https': proxy
    }
    try:
        res = requests.get(test_url, proxies=proxies, timeout=1)
        return proxy
    except (requests.exceptions.ProxyError, requests.exceptions.Timeout) as e:
        return None


if __name__ == '__main__':
    urls = config.get('urls')
    start = time.time()
    res, proxies = [], []
    pool = Pool(os.cpu_count())
    tasks = [pool.apply_async(get_proxy, args=(url,)) for url in urls]
    pool.close()
    pool.join()
    pool = Pool(os.cpu_count(logical=False))
    for each_list in [task.get() for task in tasks]:
        proxies.extend(each_list)

    tasks = [pool.apply_async(test_proxy, args=(proxy,)) for proxy in proxies]
    pool.close()
    pool.join()
    for each_list in [task.get() for task in tasks]:
        res.extend(each_list)

    print('time: {}'.format(time.time() - start))
    print(res)
