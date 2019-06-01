#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Defines Config Template class
"""

from jinja2 import Environment, StrictUndefined
from jinja2.loaders import FileSystemLoader

from cfgtemplater.base_template import BaseTemplate
from cfgtemplater.extensions import ip_filters, ip_tests


class ConfigTemplate(BaseTemplate):
    """Config Template class
    """

    def init(self):
        self.init_split()
        self.init_yaml()
        self.init_metadata()
        self.init_environment()
        self.init_default_extensions()
        self.init_defaults()

    def init_environment(self):
        """Initiliazes default Jinja2 environment
        """
        self.environment = Environment(
            loader=FileSystemLoader(self.directory),
            lstrip_blocks=True,
            trim_blocks=True,
            undefined=StrictUndefined,
        )

    def init_default_extensions(self):
        """Load default cfgtemplater extensions
        """
        for module in [ip_filters, ip_tests]:
            self.load_extension(module)

    def init_defaults(self):
        """Initializes a dict of default values based on YAML variables
        """
        self.defaults = {}
        if self.yaml:
            if "variables" in self.yaml.keys() and self.yaml["variables"] is not None:
                for variable, attributes in self.yaml["variables"].items():
                    if "default" in attributes:
                        self.defaults[variable] = attributes["default"]

    def load_extension(self, module):
        """Load jinja2 extensions from a python module
        """
        for attr in [getattr(module, f) for f in dir(module)]:
            if callable(attr):
                self.environment.filters[attr.__name__] = attr

    def render(self, attributes=None):
        """Renders the template, merging user values with default values
        """
        attributes = attributes or {}
        template = self.environment.from_string(self.content)
        variables = self.defaults.copy()
        variables.update(attributes)
        return template.render(variables)

    def save(self, filename, attributes=None):
        """ Save rendered template in a file
        """
        attributes = attributes or {}
        with open(filename, "w") as f:
            f.write(self.render(attributes))
