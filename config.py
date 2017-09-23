#!/usr/bin/env python3

import configparser
import sys
import os


def main(argv):
    config = configparser.RawConfigParser()
    current = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(current, "main.cfg")
    assert os.path.exists(config_path)
    config.read(config_path)

    values = {}
    for option in config.options("config"):
        values[option.upper()] = config.get("config", option)

    print(config.get("config", argv[1]), end="", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
