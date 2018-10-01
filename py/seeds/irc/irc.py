import socket
import sys
import time
import re

re_sp = re.compile(r"\s+")

ban_end=(' QUIT :Read error: EOF from client', ' QUIT :Signed off')

def is_ban_end(s):
    for b in ban_end:
        if s.endswith(b):
            return True
    return False

class IRC:

    irc = socket.socket()

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channel = None
        self.botnick = None
        self.pong = False
        self.inChannel = False

    def _send(self, s):
        print (">> "+s)
        self.irc.send((s+"\r\n").encode())

    def send(self, chan, msg):
        self._send("PRIVMSG " + chan + " " + msg)

    def connect(self, server, channel, botnick, enconde='utf-8',port=6667):
        self.channel = channel
        self.botnick = botnick
        self.enconde = enconde
        print ("connecting "+botnick+" to:"+server+":"+str(port))
        self.irc.connect((server, port))
        self._send("NICK " + self.botnick)
        self._send('USER '+ ((self.botnick+' ')*3) +':rainbow pie')
        self._send("JOIN " + self.channel)

    def get_text(self):
        _text=self.irc.recv(4096).decode(self.enconde).strip()  #receive the text

        for text in _text.split("\n"):
            text = text.strip()
            if not text:
                continue

            if text.startswith('PING'):
                print('++ '+text)
                pong = text.split()[1]
                time.sleep(2)
                self._send('PONG ' + pong)
                self.pong = True
                continue
            if text.endswith('JOIN :'+self.channel) or is_ban_end(text):
                continue

            cmd = text.split(":")
            if len(cmd)>1:
                tag = cmd[1].strip()
                if tag.endswith(self.channel):
                    if "PRIVMSG" in tag:
                        self.inChannel = True
                        nick = tag.split("!")[0]
                        txt = ":".join(cmd[2:])
                        msg = ("%s >>> %s" %(nick, txt))
                        yield msg

            if self.inChannel and self.channel in text:
                continue
                
            yield text
            if text.find("End of /MOTD command") != -1:
                self._send("JOIN " + self.channel)

