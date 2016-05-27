=================
Quod Libet Server
=================

* IRC bot for logging

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
