#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys

import requests
from xmppbot import XmppBot, botcmd
from .db import add_url
from ...utils import clean_url

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')

requests.packages.urllib3.disable_warnings()

re_url = re.compile(r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)")

class RssBot(XmppBot):

    @botcmd(rg_mode="findall", regex=re_url)
    def urls(self, *args, msg, **kwargs):
        for url in args:
            url = clean_url(url)
            add_url(msg['from'].bare, url)

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(path)
    xmpp = RssBot("urlbot.yml")
    xmpp.run()
