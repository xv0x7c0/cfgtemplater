import argparse
import os
import sys

import jinja2.exceptions
import yaml
from cfgtemplater.config_template import ConfigTemplate

description = "A simple YAML/Jinja2 config generator."
parser = argparse.ArgumentParser(description=description)

parser.add_argument('-y',
                    metavar="YAML",
                    dest='yaml',
                    help='YAML file',
                    action="append")

parser.add_argument('-p',
                    metavar='KEY=VALUE',
                    dest='cli',
                    help='key/value pair',
                    action="append")

parser.add_argument('filepath',
                    metavar='TEMPLATE',
                    help='template')


def main():
    args = parser.parse_args()

    template = ConfigTemplate(args.filepath)

    final_variables = template.defaults.copy()

    if args.yaml:
        for yaml_file in args.yaml:
            with open(yaml_file, 'r') as f:
                yaml_variables = yaml.load(f.read())
                final_variables.update(yaml_variables)

    if args.cli:
        cli_variables = dict(pair.split("=") for pair in args.cli)
        final_variables.update(cli_variables)

    try:
        print(template.render(final_variables))
        exit(0)
    except jinja2.exceptions.UndefinedError as ex:
        print("ERROR: Variable", ex)
        exit(1)
    except jinja2.exceptions.TemplateNotFound as ex:
        print("ERROR: Subtemplate not found:", ex)
        exit(1)

if __name__ == "__main__":
	main()
