#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import re
import sys

import requests
from xmppbot import XmppBot, botcmd
from ...db import add_url
from ...utils import clean_url, re_url

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')

requests.packages.urllib3.disable_warnings()

class RssBot(XmppBot):

    @botcmd(rg_mode="findall", regex=re_url)
    def urls(self, *args, msg, **kwargs):
        for url in args:
            url = clean_url(url)
            add_url('xmpp', msg['from'].bare, url)
            
    def command_error(self, *args, **kwargs):
        return None

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(path)
    xmpp = RssBot("urlbot.yml")
    xmpp.run()
