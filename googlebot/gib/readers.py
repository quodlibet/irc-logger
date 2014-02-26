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

import re

import feedparser


def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value)


class GoogleFeedReader(object):

    _schema = ''
    _name = 'base'
    _use_updated = False

    def __init__(self, project, *args):
        self.schema_keys = [project]
        self.schema_keys.extend(args)

        # Prevent first run spamming
        self.last_id = None
        self.update()

    def update(self):
        """Returns list of new items."""

        # TODO: ETag & Last-Modified

        feed = feedparser.parse(self._schema % tuple(self.schema_keys))
        if feed.status != 200:
            return []

        return self.parse(feed)

    def parse(self, feed):
        """Parses the content returned from update()"""

        print "Parse %s" % self._name

        added = []
        if self._use_updated:
            for entry in feed['entries']:
                if self.last_id is not None and \
                        entry.updated_parsed <= self.last_id:
                    break
                added.insert(0, entry)

            if feed['entries']:
                self.last_id = feed['entries'][0].updated_parsed
        else:
            for entry in feed['entries']:
                if entry['id'] == self.last_id:
                    break
                added.insert(0, entry)

            if feed['entries']:
                self.last_id = feed['entries'][0]['id']

        # oldest first
        return added

    def get_message(self, entry):
        return '%s: %s' % (strip_tags(entry['title']), entry['link'])


class IssueUpdatesReader(GoogleFeedReader):

    _schema = 'http://code.google.com/feeds/p/%s/issueupdates/basic'
    _name = 'issues'

    def get_message(self, entry):
        return '[Issues] %s: %s' % (
            strip_tags(entry['title']), entry['link'])


class DownloadsReader(GoogleFeedReader):

    _schema = 'http://code.google.com/feeds/p/%s/downloads/basic'
    _name = 'downloads'

    def get_message(self, entry):
        return '[Downloads] %s: %s' % (
            strip_tags(entry['title']), entry['link'])


class WikiReader(GoogleFeedReader):

    _schema = 'http://code.google.com/feeds/p/%s/%schanges/basic?path=/wiki/'
    _name = 'wiki'

    def get_message(self, entry):
        return '[Wiki] %s: %s' % (
            strip_tags(entry['title']), entry['link'])


class CodeUpdatesReader(GoogleFeedReader):

    _schema = 'http://code.google.com/feeds/p/%s/%schanges/basic'
    _name = 'code'
    _use_updated = True

    def get_message(self, entry):
        return '[Code] %s: %s' % (
            strip_tags(entry['title']), entry['link'])
