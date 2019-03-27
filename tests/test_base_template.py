import unittest
from unittest.mock import mock_open, patch

from cfgtemplater.base_template import BaseTemplate


class BaseTemplateTests(unittest.TestCase):
    
    def data_with_yaml(self):
        return """---
title: Example template
description: Example description
variables:
  variable1:
    default: value1
---
{{ variable1 }}
"""
    def header(self):
        return """title: Example template
description: Example description
variables:
  variable1:
    default: value1
"""
  
    def content(self):
        return """{{ variable1 }}
"""
    
    def setUp(self):
        filepath = '/dir/template.cfg'
        mock = mock_open(read_data=self.data_with_yaml())
        with patch('cfgtemplater.base_template.open', mock) as f:
            self.template = BaseTemplate(filepath)
    
    def test_template_filepath(self):
      self.assertEqual(self.template.filepath, '/dir/template.cfg')

    def test_template_filename(self):
      self.assertEqual(self.template.filename, 'template.cfg')

    def test_template_directory(self):
      self.assertEqual(self.template.directory, '/dir')

    def test_template_header(self):
      self.assertEqual(self.template.header, self.header()) 
    
    def test_template_content(self):
      self.assertEqual(self.template.content, self.content())

    def test_template_yaml(self):
      self.assertEqual(self.template.yaml["title"], "Example template")
      self.assertEqual(self.template.yaml["description"], "Example description")

    def test_template_metadata(self):
      self.assertEqual(self.template.title, "Example template")
      self.assertEqual(self.template.description, "Example description")
