import sys
import argparse

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from twisted.python import log

from web import app
from ircbot import setup


def main(argv):
    assert sys.version_info[0] == 3

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8160,
                        help="port number")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-i", "--irc", action="store_true")
    args = parser.parse_args()

    if args.debug:
        app.debug = True
        log.startLogging(sys.stdout)

    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(wsgiResource)
    reactor.listenTCP(args.port, site)

    if args.irc:
        setup()
    reactor.run()


if __name__ == "__main__":
    main(sys.argv)
