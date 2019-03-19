from jinja2.nativetypes import NativeEnvironment
from jinja2 import StrictUndefined
from jinja2.loaders import FileSystemLoader
from cfgtemplater.base_template import BaseTemplate

class ConfigTemplate(BaseTemplate):
    def __init__(self, filepath, mandatory_metadata=[]):
        super().__init__(filepath, mandatory_metadata)

    def init(self):
        self.init_yaml()
        self.init_metadata()
        self.init_environment()
        self.init_template()
        self.init_defaults()

    def init_environment(self):
        """ Initiliazes Jinja2 environment """
        self.environment = NativeEnvironment(
                loader=FileSystemLoader(self.directory),
                lstrip_blocks=True,
                trim_blocks=True,
                undefined=StrictUndefined
                )

    def init_template(self):
        """ Initializes Jinja2 template based on pre-defined environment """
        self.template = self.environment.from_string(self.content)

    def init_defaults(self):
        """ Initializes a dict of default values based on YAML variables """
        self.defaults = {}
        if 'variables' in self.yaml.keys():
            for variable, attributes in self.yaml['variables'].items():
                if 'default' in attributes:
                    self.defaults[variable] = attributes['default']

    def render(self, attributes={}):
        """ Renders the template, merging user values with default values """
        variables = self.defaults.copy()
        variables.update(attributes)
        return self.template.render(variables)

    def save(self, filename, attributes={}):
        """ Save rendered template in a file """
        with open (filename, 'w') as f:
            f.write(self.render(attributes))
