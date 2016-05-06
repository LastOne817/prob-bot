# -*- coding: utf-8 -*-

from connector.ircmessage import IRCMessage
from queue import Queue
import hashlib
from datetime import date, datetime


class Bot():
    irc = None
    msgQueue = Queue()

    def __init__(self):
        from connector.ircconnector import IRCConnector
        self.irc = IRCConnector(self.msgQueue)
        self.irc.setDaemon(True)
        self.irc.start()

    def run(self):
        while True:
            packet = self.msgQueue.get()
            if packet['type'] == 'msg':
                msg = packet['content']
                for channel in self.channel_list:
                    self.irc.sendmsg(channel, msg)

            elif packet['type'] == 'irc':
                message = packet['content']
                print(message)
                if message.msgType == 'INVITE':
                    self.irc.joinchan(message.channel)

                elif message.msgType == 'MODE':
                    if message.msg == '+o ' + self.irc.botnick:
                        self.irc.sendmsg(message.channel, '감사합니다 :)')

                elif message.msgType == 'KICK':
                    pass

                elif message.msgType == 'PRIVMSG':
                    if message.msg.find('!확률 ') == 0:
                        content = message.msg[len('!확률 '):]
                        print(content)
                        if content == '':
                            continue
                        m = hashlib.md5()
                        m.update(content.encode())
                        m.update(datetime.now().strftime("%Y%m%d").encode())
                        print(m.hexdigest())
                        prob = int(m.hexdigest(), 16) % 10000
                        print(prob)
                        self.irc.sendmsg(message.channel, content + ' = ' + str(prob / 100.0) + '%')

if __name__ == '__main__':
    bot = Bot()
    bot.run()
