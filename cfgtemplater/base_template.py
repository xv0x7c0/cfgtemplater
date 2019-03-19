import errno
import os
import re
import yaml

class BaseTemplate:

    def __init__(self, filepath, mandatory_metadata=[]):
        self.filepath           = os.path.abspath(filepath)
        self.filename           = os.path.basename(filepath)
        self.directory          = os.path.dirname(self.filepath)
        self.mandatory_metadata = mandatory_metadata
        
        self.init_split()
        self.init()

    def init_split(self):
        """Split given template in two parts : YAML front matter and JINJA2 part"""
        r = re.compile("""
                        \A(?:^---[\n\r])
                        (?P<yaml>.*)
                        (?:^---[\n\r])
                        (?P<template>.*)
                        """,
                        re.MULTILINE|re.DOTALL|re.VERBOSE)
        try:
            with open(self.filepath, 'r') as f:
                m = re.match(r, f.read())
                self.header, self.content = m.group(1,2)
        except IOError:
            print(IOError(errno.ENOENT, os.strerror(errno.ENOENT), filepath))
            raise

    def init(self):
        """Can be overriden to manage default behavior in child classes"""
        self.init_yaml()
        self.init_metadata()

    def init_yaml(self):
        """Load header as YAML markup"""
        try:
            self.yaml = yaml.load(self.header)
        except yaml.YAMLError as ex:
            print(ex)

    def init_metadata(self):
        """Check if declared mandatory metadata are present and initialize
        instance variables for each key found in YAML header"""
        for metadata in self.mandatory_metadata:
            if metadata not in self.yaml.keys():
                raise yaml.YAMLError("Mandatory metadata not in file")
            
        for key, value in self.yaml.items():
            setattr(type(self), key, value)
