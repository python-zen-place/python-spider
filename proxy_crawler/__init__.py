import os
import re
import time

from bs4 import BeautifulSoup
import aiohttp
import asyncio
from multiprocessing import Pool

from config import config
from error import IPBannedException

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/78.0.3904.70 Safari/537.36",
}


async def get_proxy(url, session):
    res = await session.get(url, headers=headers)
    html = await res.text()
    return html


async def test_proxy(proxy, session, test_url='http://www.baidu.com'):
    try:
        await session.get(test_url, proxy='http://' + proxy, timeout=1)
        return proxy
    except (asyncio.TimeoutError, aiohttp.client_exceptions.ClientOSError) as why:
        return None


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    servers = soup.find_all(string=re.compile(r'(\d{1,3}\.){3}\d{1,3}'))
    ports = [port.string for port in soup.find_all(name='td', string=re.compile(r'^\d{1,5}$'))]
    return ['{}:{}'.format(server, port) for server, port in zip(servers, ports)]


async def main(loop):
    with Pool(os.cpu_count()) as pool:
        async with aiohttp.ClientSession() as session:
            get_proxy_tasks = [loop.create_task(get_proxy(url, session)) for url in config['urls']]
            finished, unfinished = await asyncio.wait(get_proxy_tasks)
            pages = [task.result() for task in finished]

            parse_tasks = [pool.apply_async(parse, args=(page,)) for page in pages]
            untested_proxies = [task.get() for task in parse_tasks]

            test_proxy_tasks = [loop.create_task(test_proxy(proxy, session)) for each in untested_proxies for proxy in
                                each]
            finished, unfinished = await asyncio.wait(test_proxy_tasks)
            available_proxies = [task.result() for task in finished if task.result()]
            if not available_proxies:
                raise IPBannedException
    return available_proxies


