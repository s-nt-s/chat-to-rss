# -*- coding: utf-8 -*-
from irc import IRC
import os
import random
import string
 
channel = "#madrid"
server = "irc.irc-hispano.org"
nickname = "ZZ"+(''.join([random.choice(string.ascii_letters) for i in range(6)])).lower()
enconde = 'latin-1'

#channel = "##linux"
#server = "irc.freenode.net"
#enconde = 'utf-8'

irc = IRC()
irc.connect(server, channel, nickname, enconde)

while 1:
    for text in irc.get_text():
        print("")
        print (text)
     
