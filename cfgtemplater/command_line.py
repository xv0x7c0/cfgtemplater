#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Defiles entry point for CLI
"""

import ast
import argparse
import sys

from importlib.machinery import SourceFileLoader

import jinja2.exceptions
import yaml

from cfgtemplater.config_template import ConfigTemplate


def get_parser():
    """Return CLI parser
    """
    description = "A simple YAML/Jinja2 config generator."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        '-y',
        metavar="YAML",
        dest='yaml',
        help='YAML file',
        action="append"
    )

    parser.add_argument(
        '-p',
        metavar='KEY=VALUE',
        dest='cli',
        help='key/value pair',
        action="append"
    )

    parser.add_argument(
        '-e',
        metavar='FILE',
        dest='extensions',
        help='Jinja2 extensions modules',
        action='append'
    )

    parser.add_argument(
        'filepath',
        metavar='TEMPLATE',
        help='template'
    )
    return parser


def load_module(filepath):
    """Return extension module
    """
    loader = SourceFileLoader('extensions', filepath)
    return loader.load_module()


def main():
    parser = get_parser()
    args = parser.parse_args()

    template = ConfigTemplate(args.filepath)

    final_variables = template.defaults.copy()

    if args.extensions:
        for extension in args.extensions:
            module = load_module(extension)
            template.load_extension(module)

    if args.yaml:
        for yaml_file in args.yaml:
            with open(yaml_file, 'r') as f:
                yaml_variables = yaml.load(f.read())
                final_variables.update(yaml_variables)

    if args.cli:
        cli_variables = {}
        for k, v in [pair.split("=") for pair in args.cli]:
            value = ast.literal_eval(v)
            cli_variables[k] = value 

        final_variables.update(cli_variables)

    try:
        print(template.render(final_variables))
        sys.exit(0)
    except jinja2.exceptions.UndefinedError as ex:
        print("ERROR: Variable", ex)
        sys.exit(1)
    except jinja2.exceptions.TemplateNotFound as ex:
        print("ERROR: Subtemplate not found:", ex)
        sys.exit(2)
    except jinja2.exceptions.TemplateAssertionError as ex:
        print("ERROR: Missing filter:", ex)
        sys.exit(3)
