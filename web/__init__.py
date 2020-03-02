import os
import subprocess

from flask import Flask, render_template
from flask import redirect, send_from_directory, request, Response


app = Flask(__name__)


@app.route('/')
def index():
    base_url = request.url_root.rstrip("/")

    return render_template('index.html', base=base_url)


def irc_logs(irc_dir, name, filename=None, dir_mtime={}):

    if filename is None:
        return redirect("/irc/%s/index.html" % name)

    if not filename.endswith(".html"):
        return send_from_directory(irc_dir, filename)

    update_needed = False
    # do our own mtime check here as well since calling logs2html is expensive
    # even if it does nothing
    logs = []
    try:
        entries = os.listdir(irc_dir)
    except OSError:
        entries = []

    for file_ in entries:
        if file_.endswith(".log"):
            logs.append(file_)

    logs.sort()
    if logs:
        path = os.path.join(irc_dir, logs[-1])
        mtime = os.path.getmtime(path)
        if mtime > dir_mtime.get(irc_dir, -1):
            dir_mtime[irc_dir] = mtime
            update_needed = True
    else:
        update_needed = True

    if update_needed:
        # update html logs first
        try:
            subprocess.call(
                ["python3", "-c",
                 "from irclog2html.logs2html import main; main()",
                 irc_dir])
        except OSError:
            pass

    path = os.path.join(irc_dir, filename)
    try:
        with open(path, "rb") as h:
            data = h.read().decode("utf-8")
    except IOError:
        data = u""
    data = data[data.find("<body>") + 6:data.find("</body")]
    base_url = request.url_root.rstrip("/")
    return render_template('irc.html', content=data, stylesheet="irclog.css",
                           base=base_url, active=name)


IRC_CHANS = {
    "quodlibet": "#quodlibet@irc.oftc.net",
    "pypy": "#pypy@irc.freenode.org",
    "pygobject": "#python@irc.gnome.org",
    "qownnotes": "#qownnotes@irc.freenode.org",
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
