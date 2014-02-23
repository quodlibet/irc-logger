import os
import subprocess

from flask import Flask
from flask import url_for, redirect, send_from_directory, request, Response


app = Flask(__name__)


@app.route('/')
def hello_world():
    base_url = request.url_root.rstrip("/")

    return """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title></title>

    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css">
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>

  </head>
  <body>

<br>
<div class="container">
<div class="jumbotron well well-lg">

    <img src="http://quodlibet.googlecode.com/hg/quodlibet/quodlibet/images/hicolor/scalable/apps/quodlibet.svg" style="height:4em;float:left;margin:0.4em 0.4em 0 0">

    <p>
    This is the public server of the Quod Libet project. For any 
    questions regarding this setup please contact
    <a href="mailto:reiter.christoph@gmail.com">reiter.christoph@gmail.com</a>
    </p>

    <p>The following list points to all available resources that are part 
    of the Quod Libet project, both on this server and on the web.</p>

    <div class="list-group">
        <a class="list-group-item" href="%(base)s:8010/one_line_per_build">Buildbot Status <span class="badge">%(base)s:8010/one_line_per_build</span></a>
        <a class="list-group-item" href="%(base)s/irc/index.html">IRC Logs <span class="badge">%(base)s/irc/index.html</span></a>
        <a class="list-group-item" href="https://quodlibet.readthedocs.org/en/latest/">Online Documentation <span class="badge">https://quodlibet.readthedocs.org/en/latest/</span></a>
        <a class="list-group-item" href="http://code.google.com/p/quodlibet/">Main Website <span class="badge">http://code.google.com/p/quodlibet/</span></a>
        <a class="list-group-item" href="http://code.google.com/p/quodlibet/source/checkout">Google Code Repo <span class="badge">http://code.google.com/p/quodlibet/source/checkout</span></a>
        <a class="list-group-item" href="https://bitbucket.org/lazka/quodlibet">Bitbucket Mirror <span class="badge">https://bitbucket.org/lazka/quodlibet</span></a>
        <a class="list-group-item" href="https://groups.google.com/forum/#!forum/quod-libet-development">Mailing List <span class="badge">https://groups.google.com/forum/#!forum/quod-libet-development</span></a>
        <a class="list-group-item" href="http://code.google.com/p/quodlibet/issues/list">Bug Tracker <span class="badge">http://code.google.com/p/quodlibet/issues/list</span></a>
    </div>
</div>
</div>

  </body>
</html>

""" % {"base": base_url}


@app.route('/irc/<path:filename>')
def irc(filename):
    this = os.path.abspath(os.path.dirname(__file__))
    irc_dir = os.path.abspath(
        os.path.join(this, "..", "googlebot", "irc-logs"))

    # update html logs first
    subprocess.call(["logs2html", irc_dir])

    return send_from_directory(irc_dir, filename)


@app.route('/robots.txt')
def robots():
    return Response("""\
User-agent: *
Disallow: /
""", mimetype="text/plain")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, use_reloader=False, debug=False)
