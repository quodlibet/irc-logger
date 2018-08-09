import sys
import os

from werkzeug.wsgi import DispatcherMiddleware
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from twisted.python import log
from twisted.internet.endpoints import serverFromString

from web import app
from msys2_web.main import app as msys2_app
from ircbot import setup


def main(argv):
    assert sys.version_info[0] == 3

    final_app = DispatcherMiddleware(app, {
        "/msys2": msys2_app,
    })

    http_port, https_port = int(argv[1]), int(argv[2])

    log.startLogging(sys.stdout)
    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), final_app)
    site = Site(wsgiResource)
    endpoint = serverFromString(reactor, "tcp:%d" % http_port)
    endpoint.listen(site)

    try:
        os.mkdir("_certs")
    except OSError:
        pass
    pem_path = os.path.join("_certs", "quodlibet.duckdns.org.pem")
    if not os.path.exists(pem_path):
        open(pem_path, "wb").close()

    endpoint = serverFromString(reactor, "le:_certs:tcp:%d" % https_port)
    endpoint.listen(site)

    if "--irc" in argv[1:]:
        setup()
    reactor.run()


if __name__ == "__main__":
    main(sys.argv)
