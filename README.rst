=================
Quod Libet Server
=================

* Buildbot setup (http://buildbot.net/)

    * Automated builds/tests
    * IRC status messages

* Google IRC bot (https://github.com/jmhobbs/googlecode-irc-bot)
  for logging and reporting of commits/bug tracker changes

* Flask app as entry point & IRC logs formatting using irclog2html
  (https://pypi.python.org/pypi/irclog2html)

* Dynamic DNS update for https://www.duckdns.org


HOWTO
-----

* Fill out usernames and passwords in  ``main.cfg``
* Call all ``bootstrap-*.sh`` scripts
* Call ``start.sh``
* Call ``stop.sh`` to stop all services or ``start.sh`` to restart them
* Call ``reconfig.sh`` to rewrite config files, needs restart afterwards.
