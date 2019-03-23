from jinja2 import StrictUndefined
from jinja2.loaders import FileSystemLoader
from jinja2.nativetypes import NativeEnvironment

from cfgtemplater.base_template import BaseTemplate


class ConfigTemplate(BaseTemplate):
    def __init__(self, filepath):
        super().__init__(filepath)

    def init(self):
        self.init_split()
        self.init_yaml()
        self.init_metadata()
        self.init_environment()
        self.init_defaults()

    def init_environment(self):
        """ Initiliazes default Jinja2 environment """
        self.environment = NativeEnvironment(
                loader=FileSystemLoader(self.directory),
                lstrip_blocks=True,
                trim_blocks=True,
                undefined=StrictUndefined
                )

    def init_defaults(self):
        """ Initializes a dict of default values based on YAML variables """
        self.defaults = {}
        if self.yaml:
            if 'variables' in self.yaml.keys():
                for variable, attributes in self.yaml['variables'].items():
                    if 'default' in attributes:
                        self.defaults[variable] = attributes['default']

    def render(self, attributes={}):
        """ Renders the template, merging user values with default values """
        template = self.environment.from_string(self.content)
        variables = self.defaults.copy()
        variables.update(attributes)
        return template.render(variables)

    def save(self, filename, attributes={}):
        """ Save rendered template in a file """
        with open (filename, 'w') as f:
            f.write(self.render(attributes))
