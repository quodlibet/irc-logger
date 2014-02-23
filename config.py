#!/usr/bin/python

"""
Returns a config value for a config key or if the first argument
is a valid file replaces all %KEY% with the right value and
prints the replaced file content to stdout.
"""

import ConfigParser
import sys
import os


def main(argv):
    config = ConfigParser.RawConfigParser()
    current = os.path.dirname(os.path.realpath(__file__))
    config.read(os.path.join(current, "main.cfg"))

    values = {}
    for option in config.options("config"):
        values[option.upper()] = config.get("config", option)

    arg = argv[1]
    if not os.path.exists(arg):
        sys.stdout.write(values.get(arg, ""))
        exit()

    with open(arg, "rb") as h:
        data = h.read()

        for key, value in values.items():
            data = data.replace("%%%s%%" % key, value)

    print data


if __name__ == "__main__":
    exit(main(sys.argv))
