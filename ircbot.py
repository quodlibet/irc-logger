#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import os
import time

from twisted.python import log
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol


class Bot(object):

    def __init__(self, nickname, channel, server, port):
        self.nickname = nickname
        self.channel = channel
        self.server = server
        self.port = port


BOTS = [
    Bot("marvin", "#pypy", "irc.freenode.org", 6667),
    Bot("marvin", "#gtk+", "irc.gnome.org", 6667),
    Bot("marvin", "#python", "irc.gnome.org", 6667),
    Bot("marvin", "#quodlibet", "irc.oftc.net", 6667),
]


class IRCLogger(object):

    def __init__(self, path, server, channel):
        self._path = path
        self._channel = channel
        self._server = server
        self._date = self._date_key()
        try:
            os.makedirs(os.path.dirname(self._get_log_file_path()))
        except OSError:
            pass
        self.file = open(self._get_log_file_path(), "a")

    def _date_key(self):
        return time.strftime("%Y-%m-%d", time.localtime(time.time()))

    def _get_log_file_path(self):
        return os.path.join(
            self._path, "%s@%s" % (self._channel, self._server),
            self._channel.lstrip("#") + "_" + self._date + ".log")

    def log(self, message):
        if self._date != self._date_key():
            self.file.close()
            self._date = self._date_key()
            self.file = open(self._get_log_file_path(), "a")
        self.file.write('%s %s\n' % (
            time.strftime("[%H:%M:%S]", time.localtime(time.time())), message)
        )
        self.file.flush()

    def close(self):
        self.file.close()

    def joined(self, user, channel):
        self.log("[%s joined %s]" % (user, channel))

    def left(self, user, channel):
        self.log("[%s left %s]" % (user, channel))

    def quit(self, user, message):
        self.log("[%s quit (%s)]" % (user, message))

    def action(self, user, message):
        user = user.split('!')
        self.log("[* %s %s]" % (user[0], message))

    def nick_change(self, old_nick, new_nick):
        self.log("[%s is now known as %s]" % (old_nick, new_nick))


class IRCBot(irc.IRCClient):

    def __init__(self, factory, nickname, channel, logger):
        self.lineRate = 2
        self.factory = factory
        self.nickname = nickname
        self._channel = channel
        self._logger = logger

    def irc_unknown(self, prefix, command, params):
        if command == "ERR_UNAVAILRESOURCE":
            self.irc_ERR_NICKNAMEINUSE(prefix, params)

    def connectionMade(self):
        self.factory.resetDelay()
        irc.IRCClient.connectionMade(self)

    def signedOn(self):
        self.join(self._channel)

    def joined(self, channel):
        self._logger.joined(self.nickname, channel)

    def userJoined(self, user, channel):
        self._logger.joined(user, channel)

    def left(self, channel):
        self._logger.left(self.nickname, channel)

    def userLeft(self, user, channel):
        self._logger.left(user, channel)

    def userQuit(self, user, quitMessage):
        self._logger.quit(user, quitMessage)

    def action(self, user, channel, msg):
        self._logger.action(user, msg)

    def userRenamed(self, oldname, newname):
        self._logger.nick_change(oldname, newname)


class IRCBotFactory(protocol.ReconnectingClientFactory):

    def __init__(self, bot, log_dir):
        self._bot = bot
        self._log_dir = log_dir

    def buildProtocol(self, addr):
        bot = self._bot
        logger = IRCLogger(self._log_dir, bot.server, bot.channel)
        return IRCBot(self, bot.nickname, bot.channel, logger)


def main(argv):

    log_dir = argv[1]
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except OSError:
            pass
    assert os.path.isdir(log_dir)
    log.startLogging(sys.stdout)

    for bot in BOTS:
        factory = IRCBotFactory(bot, log_dir)
        reactor.connectTCP(bot.server, bot.port, factory)

    reactor.run()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
