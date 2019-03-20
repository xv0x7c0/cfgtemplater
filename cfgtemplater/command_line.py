import os
import sys
from optparse import OptionParser

import jinja2.exceptions
import yaml

from cfgtemplater.config_template import ConfigTemplate

usage = "usage: %prog [options] TEMPLATE"
parser = OptionParser(usage=usage)

parser.add_option('-y', 
                  metavar="FILE", 
                  dest='yaml', 
                  help='Key/value YAML file')

parser.add_option('-p',
                  metavar='KEY=VALUE', 
                  dest='cli', 
                  help='Key/value pair', 
                  action="append")

def main():
    (options, args) = parser.parse_args()

    template = ConfigTemplate(args[0])

    final_variables = template.defaults.copy()

    if options.yaml:
        with open(options.yaml, 'r') as f:
            yaml_variables = yaml.load(f.read())
            final_variables.update(yaml_variables)

    if options.cli:
        cli_variables = dict(pair.split("=") for pair in options.cli)
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
