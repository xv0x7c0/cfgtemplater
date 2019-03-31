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

Pass python literals from CLI

```
cfgtemplater -p "variable1=[{'name':'varx', 'value':'x'}, {'name':'vary', 'value':'y'}]" template.j2
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

## Integrated filters and tests

### IP filters

#### first_address

```jinja
{{ ipv4_net | first_address }}
{{ ipv6_net | first_address }}
```
```
192.0.2.1/24
2001:db8::1/120
```

#### last_address

```jinja
{{ ipv4_net | last_address }}
{{ ipv6_net | last_address }}
```
```
192.0.2.254/24
2001:db8::ff/120
```

#### address

```jinja
{{ ipv4_net | address }}
{{ ipv6_net | address }}
```
```
192.0.2.0
2001:db8::
```

#### network

```jinja
{{ ipv4_net | first_address | network }}
{{ ipv6_net | first_address | network }}
```
```
192.0.2.0/24
2001:db8::/120
```

#### broadcast

```jinja
{{ ipv4_net | broadcast }}
{{ ipv6_net | broadcast }}
```
```
192.0.2.255/24
2001:db8::ff/120
```

#### prefixlen

```jinja
{{ ipv4_net | prefixlen }}
{{ ipv6_net | prefixlen }}
```
```
24
120
```

#### netmask

```jinja
{{ ipv4_net | netmask }}
{{ ipv6_net | netmask }}
```
```
255.255.255.0
ffff:ffff:ffff:ffff:ffff:ffff:ffff:ff00
```

#### hostmask

```jinja
{{ ipv4_net | first_address | hostmask }}
{{ ipv6_net | first_address | hostmask }}
```
```
0.0.0.255
::ff
```

#### compress

```jinja
{{ '192.000.002.001' | compress }}
{{ '2001:0db8:0000:0000:0000:0000:0000:0001' | compress }}
```
```
192.0.2.1
2001:db8::1
```

#### uncompress

```jinja
{{ '192.0.2.1' | uncompress }}
{{ '2001:db8::1' | uncompress }}
```
```
192.000.002.001
2001:0db8:0000:0000:0000:0000:0000:0001
```

#### octets

```jinja
{% for octet in ipv4_net | octets %}
  {{ octet }}
{% endfor %}
```
```
  192
  0
  2
  0
```

#### hextets

```jinja
{% for hextet in ipv6_net | hextets %}
  {{ hextet }}
{% endfor %}
```
```
  2001
  0db8
  0000
  0000
  0000
  0000
  0000
  0000
```

### IP tests

#### is_ip

```jinja
{{ ipv4_net | is_ip }}
{{ ipv6_net | is_ip }}
{{ 'test' | is_ip
```
```
True
True
False
```

#### is_ipv4

```jinja
{{ ipv4_net | is_ipv4 }}
{{ ipv6_net | is_ipv4 }}
```
```
True
False
```

#### is_ipv6

```jinja
{{ ipv6_net | is_ipv6 }}
{{ ipv4_net | is_ipv6 }}
```
```
True
False
```

#### is_ip_net

```jinja
{{ ipv4_net | is_ip_net }}
{{ ipv6_net | is_ip_net }}
{{ ipv6_net | first_address | is_ip_net }}
{{ ipv6_net | first_address | is_ip_net }}
```
```
True
True
False
False
```

#### is_ipv4_net

```jinja
{{ ipv4_net | is_ipv4_net }}
{{ ipv6_net | is_ipv4_net }}
{{ ipv4_net | first_address | is_ipv4_net }}
{{ ipv6_net | first_address | is_ipv4_net }}
```
```
True
False
False
False
```

#### is_ipv6_net

```jinja
{{ ipv6_net | is_ipv6_net }}
{{ ipv4_net | is_ipv6_net }}
{{ ipv6_net | first_address | is_ipv4_net }}
{{ ipv4_net | first_address | is_ipv4_net }}
```
```
True
False
False
False
```

#### is_ipv4_host

```jinja
{{ ipv4_net | first_address | is_ipv4_host }}
{{ ipv4_net | is_ipv4_host }}
```
```
True
False
```
