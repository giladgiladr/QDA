import os
import sys
import ConfigParser


class Configuration(object):
    def __init__(self, config_file_path):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file_path)

    def get(self, path):
        tokens = path.split("/")
        assert len(tokens) == 2
        self.config.get(tokens[0], tokens[1])

