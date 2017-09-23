import sys

from werkzeug.wsgi import DispatcherMiddleware
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from twisted.python import log

from web import app
from msys2_web.main import app as msys2_app
from ircbot import setup


def main(argv):
    assert sys.version_info[0] == 3

    final_app = DispatcherMiddleware(app, {
        "/msys2": msys2_app,
    })

    log.startLogging(sys.stdout)
    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), final_app)
    site = Site(wsgiResource)
    reactor.listenTCP(int(argv[1]), site)
    if "--irc" in argv[1:]:
        setup()
    reactor.run()


if __name__ == "__main__":
    main(sys.argv)
