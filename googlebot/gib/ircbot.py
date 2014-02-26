# -*- coding: utf-8 -*-

# Copyright (c) 2010 John Hobbs
#               2014 Christoph Reiter
#
# http://github.com/jmhobbs/googlecode-irc-bot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log


def announce(feed):
    new = feed.update()

    for entry in new:
        msg = feed.get_message(entry)
        if GoogleCodeIRCBot.instance:
            msg = msg.replace('\n', '').encode('utf-8')
            GoogleCodeIRCBot.instance.trysay(msg)
        else:
            print "No Bot", msg


class GoogleCodeIRCBot(irc.IRCClient):

    versionName = "IRC Bot"
    versionNum = "0.1"
    username = "%s-%s" % (versionName, versionNum)
    sourceURL = "http://code.google.com/p/quodlibet/"

    instance = None
    channel = None
    lineRate = 2
    logger = None

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        log.msg(self.nickname + ": Connected")

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        log.msg(self.nickname + ": Connection Lost")

    def signedOn(self):
        self.join(self.factory.channel)
        log.msg(self.nickname + ": Signed On")
        GoogleCodeIRCBot.instance = self

    def joined(self, channel):
        self.channel = self.factory.channel

        log.msg(self.nickname + ": Joined " + self.channel)
        if self.logger:
            self.logger.joined(self.nickname, channel)

    def userJoined(self, user, channel):
        if self.logger:
            self.logger.joined(user, channel)

    def left(self, channel):
        log.msg(self.nickname + ": Left Channel " + channel)
        self.channel = None
        if self.logger:
            self.logger.left(self.nickname, channel)

    def userLeft(self, user, channel):
        if self.logger:
            self.logger.left(user, channel)

    def trysay(self, msg):
        """Attempts to send the given message to the channel."""

        if self.channel:
            try:
                self.say(self.channel, msg)
                log.msg(self.nickname + ": Say : " + msg)
                if self.logger:
                    self.logger.message(self.nickname, msg)
                return True
            except Exception as e:
                log.msg(self.nickname + ": Error saying : " + str(e))

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]

        log.msg(self.nickname + ": Private Message : " +
                user + " says: " + msg)

        if self.logger:
            self.logger.message(user, msg)

    def action(self, user, channel, msg):
        if self.logger:
            self.logger.action(user, msg)

    def irc_NICK(self, prefix, params):
        if self.logger:
            old_nick = prefix.split('!')[0]
            new_nick = params[0]
            self.logger.nick_change(old_nick, new_nick)


class GoogleCodeIRCBotFactory(protocol.ReconnectingClientFactory):

    protocol = GoogleCodeIRCBot

    def __init__(self, channel):
        self.channel = channel

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()
