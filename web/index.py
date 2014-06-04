import os
import subprocess

from flask import Flask, abort, render_template
from flask import url_for, redirect, send_from_directory, request, Response


app = Flask(__name__)


@app.route('/')
def index():
    base_url = request.url_root.rstrip("/")

    return render_template('index.html', base=base_url)


@app.route('/buildbot')
def buildbot():
    base_url = request.url_root.rstrip("/")
    iframe = "%s:8010/builders" % base_url
    return render_template('iframe.html', base=base_url, active="buildbot",
                            iframe_url=iframe)


@app.route('/docs')
def docs():
    base_url = request.url_root.rstrip("/")
    iframe = "https://quodlibet.readthedocs.org/en/latest/"
    return render_template('iframe.html', base=base_url, active="docs",
                            iframe_url=iframe)

@app.route('/ml')
def bug():
    base_url = request.url_root.rstrip("/")
    iframe = "https://groups.google.com/forum/#!forum/quod-libet-development"
    return render_template('iframe.html', base=base_url, active="ml",
                            iframe_url=iframe)


@app.route('/static/<path:filename>')
def static_(filename):
    static_path = os.path.join(this, "static")
    return send_from_directory(static_path, filename)


def irc_logs(irc_dir, name, filename=None, dir_mtime={}):

    if filename is None:
        return redirect("/%s/index.html" % name)

    if not filename.endswith(".html"):
        return send_from_directory(irc_dir, filename)

    update_needed = False
    # do our own mtime check here as well since calling logs2html is expensive
    # even if it does nothing
    for file_ in os.listdir(irc_dir):
        path = os.path.join(irc_dir, file_)
        mtime = os.path.getmtime(path)
        if mtime > dir_mtime.get(irc_dir, -1):
            dir_mtime[irc_dir] = mtime
            update_needed = True

    if update_needed:
        # update html logs first
        try:
            subprocess.call(["logs2html", irc_dir])
        except OSError:
            pass

    path = os.path.join(irc_dir, filename)
    data = open(path, "rb").read().decode("utf-8")
    data = data[data.find("<body>") + 6:data.find("</body")]
    base_url = request.url_root.rstrip("/")
    return render_template('irc.html', content=data, stylesheet="irclog.css",
                           base=base_url, active=name)


@app.route('/irc/')
@app.route('/irc/<path:filename>')
def irc(filename=None):
    this = os.path.abspath(os.path.dirname(__file__))
    irc_dir = os.path.abspath(
        os.path.join(this, "..", "googlebot", "irc-logs"))

    return irc_logs(irc_dir, "irc", filename)


@app.route('/pypy/')
@app.route('/pypy/<path:filename>')
def irc_pypy(filename=None):
    this = os.path.abspath(os.path.dirname(__file__))
    irc_dir = os.path.abspath(
        os.path.join(this, "..", "pypybot", "irc-logs"))

    return irc_logs(irc_dir, "pypy", filename)


@app.route('/robots.txt')
def robots():
    return Response("""\
User-agent: *
Disallow: /
""", mimetype="text/plain")


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80, use_reloader=False, debug=True)

    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(80)
    IOLoop.instance().start()
