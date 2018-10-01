# -*- coding: utf-8 -*-
from .irc import IrcBot
import sys
import os
import random
import string
import yaml
from ...db import add_url
from ...utils import clean_url, re_url

class MyIrcBot(IrcBot):

    def process_msg(self, channel, nick, msg):
        for url in re_url.findall(msg):
            url = clean_url(url)
            add_url('irc', channel+'@'+self.config['server'], url)

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(path)
    irc = MyIrcBot(sys.argv[1])
    irc.run()

