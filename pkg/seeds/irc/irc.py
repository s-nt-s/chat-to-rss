import socket
import sys
import time
import re
import random
import string
import yaml
import logging

re_sp = re.compile(r"\s+")

ban_end=(' QUIT :Read error: EOF from client', ' QUIT :Signed off')

def is_ban_end(s):
    for b in ban_end:
        if s.endswith(b):
            return True
    return False

class IrcBot:

    irc = socket.socket()

    def __init__(self, config_path):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with open(config_path, 'r') as f:
            self.config = yaml.load(f)
        if "nick" not in self.config:
            self.config['nick']="ZZ"+(''.join([random.choice(string.ascii_letters) for i in range(6)])).lower()
        if "port" not in self.config:
            self.config['port']=6667
        if "enconde" not in self.config:
            self.config['enconde']='utf-8'
        logging.basicConfig(level=self.config.get(
            'LOG', logging.INFO), format='%(levelname)-8s %(message)s')
        self.log = logging.getLogger()
        self.connect()

    def _send(self, s):
        self.log.info(">> "+s)
        self.irc.send((s+"\r\n").encode())

    def send(self, chan, msg):
        self._send("PRIVMSG " + chan + " " + msg)

    def connect(self):
        self.log.info("connecting "+self.config['nick']+" to:"+self.config['server']+":"+str(self.config['port']))
        self.irc.connect((self.config['server'], self.config['port']))
        self._send("NICK " + self.config['nick'])
        self._send('USER '+ ((self.config['nick']+' ')*3) +':rainbow pie')
        self.join()

    def join(self):
        for c in self.config.get('channels', []):
            self._send("JOIN #" + c)

    def get_msg(self):
        _text=self.irc.recv(4096).decode(self.config['enconde']).strip()

        for text in _text.split("\n"):
            text = text.strip()
            if not text:
                continue

            if text.startswith('PING'):
                self.log.info('++ '+text)
                pong = text.split()[1]
                time.sleep(2)
                self._send('PONG ' + pong)
                self.pong = True
                continue
            if is_ban_end(text):
                continue

            cmd = text.split(":")
            if len(cmd)>1:
                tag = cmd[1].strip()
                channel = self.get_channel(tag)
                if channel:
                    if "PRIVMSG" in tag:
                        nick = tag.split("!")[0]
                        txt = ":".join(cmd[2:])
                        self.process_msg(channel, nick, txt)

            if text.find("End of /MOTD command") != -1:
                self.join()

    def get_channel(self, tag):
        for c in self.config.get('channels', []):
            if tag.endswith('#'+c):
                return c
        return None

    def process_msg(self, channel, nick, msg):
        pass

    def run(self):
        while 1:
            self.get_msg()

