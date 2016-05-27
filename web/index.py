import os
import shutil

from flask import Flask, render_template
from flask import redirect, send_from_directory, request, Response


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


@app.route('/static/<path:filename>')
def static_(filename):
    this = os.path.abspath(os.path.dirname(__file__))
    static_path = os.path.join(this, "static")
    return send_from_directory(static_path, filename)


def get_year(filename):
    if "_" not in filename:
        return ""
    return filename.split("_", 1)[-1].split("-", 1)[0]


def logs2html(dir_):
    import irclog2html.logs2html

    try:
        irclog2html.logs2html.main(["logs2html", dir_])
    except SystemExit:
        pass


def irc_logs(irc_dir, name, filename=None):

    if filename is None:
        return redirect("/irc/%s/index.html" % name)

    if not filename.endswith(".html"):
        return send_from_directory(irc_dir, filename)

    old_dir = os.path.join(irc_dir, "old")

    try:
        os.mkdir(old_dir)
    except OSError:
        pass

    new_old = False
    for filename in os.listdir(irc_dir):
        year = get_year(filename)
        if not year:
            continue
        if int(year) <= 2015:
            shutil.move(os.path.join(irc_dir, filename), old_dir)
            new_old = True

    if new_old:
        logs2html(old_dir)

    logs2html(irc_dir)

    path = os.path.join(irc_dir, filename)
    data = open(path, "rb").read().decode("utf-8")
    data = data[data.find("<body>") + 6:data.find("</body")]
    base_url = request.url_root.rstrip("/")
    return render_template('irc.html', content=data, stylesheet="irclog.css",
                           base=base_url, active=name)


IRC_CHANS = {
    "quodlibet": "#quodlibet@irc.oftc.net",
    "pypy": "#pypy@irc.freenode.org",
    "foo": "#gtk+@irc.gnome.org",
    "pygobject": "#python@irc.gnome.org",
}

DEFAULT_CHAN = "quodlibet"

@app.route('/irc/<name>/')
@app.route('/irc/<name>/<path:filename>')
def irc(name, filename=None):
    this = os.path.abspath(os.path.dirname(__file__))
    irc_dir = os.path.abspath(
        os.path.join(this, "..", "_irc-logs",
        IRC_CHANS.get(name, IRC_CHANS[DEFAULT_CHAN])))
    return irc_logs(irc_dir, name, filename)


@app.route('/robots.txt')
def robots():
    return Response("""\
User-agent: *
Disallow: /
""", mimetype="text/plain")


if __name__ == '__main__':

    #app.run(host='0.0.0.0', port=80, use_reloader=False, debug=True)

    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(80)
    IOLoop.instance().start()
