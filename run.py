import sys

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from web import app
from msys2_web.main import app as msys2_app


def main(argv):
    assert sys.version_info[0] == 3

    from werkzeug.wsgi import DispatcherMiddleware

    final_app = DispatcherMiddleware(app, {
        "/msys2": msys2_app,
    })

    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), final_app)
    site = Site(wsgiResource)
    reactor.listenTCP(int(argv[1]), site)
    reactor.run()


if __name__ == "__main__":
    main(sys.argv)
