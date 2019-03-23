import errno
import os
import re

import yaml


class BaseTemplate:
    
    YAML_SPLIT_RE = re.compile("""
                               \A(?:^---[\n\r])
                               (?P<yaml>.*)
                               (?:^---[\n\r])
                               (?P<template>.*)
                               """,
                               re.MULTILINE|re.DOTALL|re.VERBOSE)

    def __init__(self, filepath):
        self.filepath = os.path.abspath(filepath)
        self.filename = os.path.basename(filepath)
        self.directory = os.path.dirname(self.filepath)
        
        self.init()

    def init(self):
        """Can be overriden to manage default behavior in child classes"""
        self.init_split()
        self.init_yaml()
        self.init_metadata()

    def init_split(self):
        """Split given template in two parts : YAML front matter and JINJA2 part"""
        try:
            with open(self.filepath, 'r') as f:
                m = re.match(BaseTemplate.YAML_SPLIT_RE, f.read())
                if m:
                    self.header, self.content = m.group(1,2)
                else:
                    f.seek(0)
                    self.header = None
                    self.content = f.read()
        except IOError:
            print(IOError(errno.ENOENT, os.strerror(errno.ENOENT), filepath))
            raise

    def init_yaml(self):
        """Load header as YAML markup"""
        self.yaml = None
        if self.header:
            try:
                self.yaml = yaml.load(self.header)
            except yaml.YAMLError as ex:
                print(ex)

    def init_metadata(self):
        """Initialize instance variables for each key found in YAML header"""
        if self.yaml:
            for key, value in self.yaml.items():
                setattr(type(self), key, value)
