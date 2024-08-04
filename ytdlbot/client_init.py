#!/usr/local/bin/python3
# coding: utf-8

# ytdlbot - client_init.py
# 12/29/21 16:20
#

__author__ = "Benny <benny.think@gmail.com>"

from pyrogram import Client

from config import APP_HASH, APP_ID, PYRO_WORKERS, TOKEN, IPv6
import requests
import random

def get_random_proxy(protocol):
    url = f'https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}'
    response = requests.get(url)
    proxies = response.text.split('\n')
    return random.choice(proxies).strip()

randproxy = get_random_proxy("socks5")

def create_app(name: str, workers: int = PYRO_WORKERS) -> Client:
    proxy1 = dict(scheme="socks5", host=randproxy.split(':')[0], port=randproxy.split(':')[1])
    return Client(
        name,
        APP_ID,
        APP_HASH,
        bot_token=TOKEN,
        workers=workers,
        ipv6=IPv6,
        proxy=proxy1,
        # max_concurrent_transmissions=max(1, WORKERS // 2),
        # https://github.com/pyrogram/pyrogram/issues/1225#issuecomment-1446595489
    )
