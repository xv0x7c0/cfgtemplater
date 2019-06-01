#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Defines Base Template class
"""

import os
import re
import traceback

import yaml


class BaseTemplate:
    """Base Template class
    """

    YAML_SPLIT_RE = re.compile(
        r"""
                               \A(?:^---[\n\r])
                               (?P<yaml>.*)
                               (?:^---[\n\r])
                               (?P<template>.*)
                               """,
        re.MULTILINE | re.DOTALL | re.VERBOSE,
    )

    def __init__(self, filepath):
        self.filepath = os.path.abspath(filepath)
        self.filename = os.path.basename(filepath)
        self.directory = os.path.dirname(self.filepath)

        self.header = None
        self.content = None

        self.yaml = None

        self.init()

    def init(self):
        """Can be overriden to manage default behavior in child classes
        """
        self.init_split()
        self.init_yaml()
        self.init_metadata()

    def init_split(self):
        """Split given template in two parts: YAML front matter and JINJA2 part
        """
        try:
            with open(self.filepath, "r") as f:
                text = f.read()
                m = re.match(BaseTemplate.YAML_SPLIT_RE, text)
                if m:
                    self.header, self.content = m.group(1, 2)
                else:
                    self.header = None
                    self.content = text
        except IOError as err:
            print(type(err), repr(err), traceback.format_exc())
            raise

    def init_yaml(self):
        """Load header as YAML markup
        """
        if self.header:
            try:
                self.yaml = yaml.load(self.header, Loader=yaml.FullLoader)
            except yaml.YAMLError as err:
                print(err)

    def init_metadata(self):
        """Initialize instance variables for each key found in YAML header
        """
        if self.yaml:
            for key, value in self.yaml.items():
                setattr(type(self), key, value)
