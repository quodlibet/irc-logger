import sys

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from web import app


def main(argv):
    assert sys.version_info[0] == 3

    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = Site(wsgiResource)
    reactor.listenTCP(int(argv[1]), site)
    reactor.run()


if __name__ == "__main__":
    main(sys.argv)
