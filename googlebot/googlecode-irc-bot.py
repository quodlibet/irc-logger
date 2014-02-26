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

# Gracious credit goes to Steven Robertson, whose Quodlibot provided
# inspiration and foundation
# http://strobe.cc/quodlibot/

import sys
import os

from twisted.internet import reactor, task
from twisted.python import log

from gib import ircbot, project, readers, logger


def run_bot(project):

    bot_cls = ircbot.GoogleCodeIRCBot
    bot_cls.nickname = project.settings['project']['bot']['name']

    if project.settings['project']['logging']:
        irc_logs = sys.path[0] + "/irc-logs/"
        try:
            os.makedirs(irc_logs)
        except OSError:
            pass
        bot_cls.logger = logger.IRCLogger(irc_logs, project.name)

    factory = ircbot.GoogleCodeIRCBotFactory(
        project.settings['project']['bot']['channel'])

    issues_feed = None
    if project.settings['project']['feeds']['issues'] != 0:
        issues_feed = readers.IssueUpdatesReader(project.name)

    downloads_feed = None
    if project.settings['project']['feeds']['downloads'] != 0:
        downloads_feed = readers.DownloadsReader(project.name)

    wiki_feed = None
    if project.settings['project']['feeds']['wiki'] != 0:
        wiki_feed = readers.WikiReader(project.name, project.vcs)

    code_feed = None
    if project.settings['project']['feeds']['code'] != 0:
        code_feed = readers.CodeUpdatesReader(project.name, project.vcs)

    reactor.connectTCP(project.settings['project']['bot']['server'],
                       project.settings['project']['bot']['port'],
                       factory)

    if issues_feed:
        issues_update_task = task.LoopingCall(ircbot.announce, issues_feed)
        issues_update_task.start(
            project.settings['project']['feeds']['issues'], now=False)
        reactor.callLater(20, ircbot.announce, issues_feed)

    if downloads_feed:
        downloads_update_task = task.LoopingCall(
            ircbot.announce, downloads_feed)
        downloads_update_task.start(
            project.settings['project']['feeds']['downloads'], now=False)
        reactor.callLater(20, ircbot.announce, downloads_feed)

    if wiki_feed:
        wiki_update_task = task.LoopingCall(ircbot.announce, wiki_feed)
        wiki_update_task.start(
            project.settings['project']['feeds']['wiki'], now=False)
        reactor.callLater(20, ircbot.announce, wiki_feed)

    if code_feed:
        code_update_task = task.LoopingCall(ircbot.announce, code_feed)
        code_update_task.start(
            project.settings['project']['feeds']['code'], now=False)
        reactor.callLater(20, ircbot.announce, code_feed)

    reactor.run()


def main():
    bot = project.Project(sys.path[0] + "/bot.yaml")
    assert bot

    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        log.startLogging(sys.stdout)

    run_bot(bot)


if __name__ == "__main__":
    exit(main())
