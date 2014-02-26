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
    iframe = "%s:8010/one_line_per_build" % base_url
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


irclogs_mtime = -1

@app.route('/irc/')
@app.route('/irc/<path:filename>')
def irc(filename=None):
    global irclogs_mtime

    if filename is None:
        return redirect("/irc/index.html")

    this = os.path.abspath(os.path.dirname(__file__))
    irc_dir = os.path.abspath(
        os.path.join(this, "..", "googlebot", "irc-logs"))

    if not filename.endswith(".html"):
        return send_from_directory(irc_dir, filename)

    update_needed = False
    # do our own mtime check here as well since calling logs2html is expensive
    # even if it does nothing
    for file_ in os.listdir(irc_dir):
        path = os.path.join(irc_dir, file_)
        mtime = os.path.getmtime(path)
        if mtime > irclogs_mtime:
            irclogs_mtime = mtime
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
                           base=base_url, active="irc")


@app.route('/robots.txt')
def robots():
    return Response("""\
User-agent: *
Disallow: /
""", mimetype="text/plain")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, use_reloader=False, debug=False)
