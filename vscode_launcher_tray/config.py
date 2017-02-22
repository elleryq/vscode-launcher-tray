# -*- coding: utf-8 -*-
"""Config."""
import os
import json
import logging


# Compat between Python 3.4 and Python 3.5
if not hasattr(json, 'JSONDecodeError'):
    json.JSONDecodeError = ValueError

logger = logging.getLogger(__name__)


class Config(dict):
    """Config."""

    def __init__(self, json_config_file=None):
        """Constructor."""
        super(Config, self).__init__(self)
        if not json_config_file:
            json_config_file = os.path.join(
                os.path.expanduser("~/.config/"),
                "vscode-launcher-tray.json")
        self.json_config_file = json_config_file
        self.load()

    def save(self):
        """Save."""
        json.dump(self, open(self.json_config_file, "wt"))

    def load(self):
        try:
            self.update(json.load(open(self.json_config_file)))
        except (FileNotFoundError, json.JSONDecodeError) as ex:
            logger.warning("{} not found.".format(self.json_config_file))