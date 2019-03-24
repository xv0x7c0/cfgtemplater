# cfgtemplater

cfgtemplater is a Jinja2 template CLI rendering tool. It allows to integrate metadata and defaults variables values within a YAML header. It is also integrates basic IP filters and tests since it's main development purpose is to generate network devices configuration files. It is as well able to load external filters and tests from other python modules.

## Installation

```
pip install cfgtemplater
```

## Usage

```
usage: cfgtemplater [-h] [-y YAML] [-p KEY=VALUE] [-e FILE] TEMPLATE

A simple YAML/Jinja2 config generator.

positional arguments:
  TEMPLATE      template

optional arguments:
  -h, --help    show this help message and exit
  -y YAML       YAML file
  -p KEY=VALUE  key/value pair
  -e FILE       Jinja2 extensions modules
```

## Usage examples

Load variables from a YAML file
```
cfgtemplater -y variables.yml template.j2
```

Load variables from multiple YAML files (merged in order)
```
cfgtemplater -y default_variables.yml -y instance_variables.yml template.j2
```

Override variables from CLI
```
cfgtemplater -y default_variables -p 'variable1=value1' template.j2
```

## Template

(Main) template may look like this:

```jinja
---
name: Example template

variables:
  variable1:
    default:      "example"
    description:  "example variable"
  variable2:
    default:
      - value: 0
        name: zero
      - value: 1
        name: one
---
This is an {{ variable1 }} file.

{% for variable in variable2 %}
  This is a {{ variable.name }} : {{ variable.value }}
{% endfor %}

{{ variable3 }}
```

The YAML header may contain template metadata (like name, description, whatever). It may as well contain default variables or variables descriptions or any variable metadata. Defaults values are injected in the template when rendering, and can be redefined using CLI or YAML file.

## Extensions

Jinja2 filters and tests can be loaded from external files.

Load ansible ipaddr filter (ansible_ipaddr.py)
```python
import netaddr
from ansible.plugins.filter.ipaddr import *
```

Render template using ipaddr filters
```
cfgtemplater -e ansible_ipaddr.py template.j2
```

## Basic module usage

```python
>>> from cfgtemplater.config_template import ConfigTemplate
>>> t = ConfigTemplate('examples/example1.j2')
>>> t.name
'Example template'
>>> t.variables
{'variable1': {'default': 'example', 'description': 'example variable'}, 'variable2': {'default': [{'value': 0, 'name': 'zero'}, {'value': 1, 'name': 'one'}]}}
>>> t.content
'This is an {{ variable1 }} file.\n\n{% for variable in variable2 %}\n  This is a {{ variable.name }} : {{ variable.value }}\n{% endfor %}\n\n{{ variable3 }}\n'
>>> print(t.render({'variable3': 'TEST'}))
This is an example file.

  This is a zero : 0
  This is a one : 1

TEST
```
