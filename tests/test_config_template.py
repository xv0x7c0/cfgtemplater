import unittest
from unittest.mock import mock_open, patch

import jinja2.exceptions

from cfgtemplater.config_template import ConfigTemplate


class ConfigTemplateTests(unittest.TestCase):
    def data_with_yaml(self):
        return """---
title: Example template
description: Example description
variables:
  variable1:
    default: value1
---
{{ variable1 }} {{ variable2 }}"""

    def header(self):
        return """title: Example template
description: Example description
variables:
  variable1:
    default: value1
"""

    def content(self):
        return """{{ variable1 }} {{ variable2 }}"""

    def setup_template_with_yaml(self):
        filepath = "/dir/template.cfg"
        mock = mock_open(read_data=self.data_with_yaml())
        with patch("cfgtemplater.base_template.open", mock) as f:
            self.template_w = ConfigTemplate(filepath)

    def setup_template_without_yaml(self):
        filepath = "/dir/template.cfg"
        mock = mock_open(read_data=self.content())
        with patch("cfgtemplater.base_template.open", mock) as f:
            self.template_wo = ConfigTemplate(filepath)

    def setUp(self):
        self.setup_template_with_yaml()
        self.setup_template_without_yaml()

    def test_template_filepath(self):
        self.assertEqual(self.template_w.filepath, "/dir/template.cfg")
        self.assertEqual(self.template_wo.filepath, "/dir/template.cfg")

    def test_template_filename(self):
        self.assertEqual(self.template_w.filename, "template.cfg")
        self.assertEqual(self.template_wo.filename, "template.cfg")

    def test_template_directory(self):
        self.assertEqual(self.template_w.directory, "/dir")
        self.assertEqual(self.template_wo.directory, "/dir")

    def test_template_header(self):
        self.assertEqual(self.template_w.header, self.header())
        self.assertEqual(self.template_wo.header, None)

    def test_template_content(self):
        self.assertEqual(self.template_w.content, self.content())
        self.assertEqual(self.template_wo.content, self.content())

    def test_template_yaml(self):
        self.assertEqual(self.template_w.yaml["title"], "Example template")
        self.assertEqual(self.template_w.yaml["description"], "Example description")
        self.assertEqual(self.template_wo.yaml, None)

    def test_template_metadata(self):
        self.assertEqual(self.template_w.title, "Example template")
        self.assertEqual(self.template_wo.description, "Example description")

    def test_defaults(self):
        self.assertEqual(self.template_w.defaults["variable1"], "value1")
        self.assertEqual(self.template_wo.defaults, {})

    def test_render_defaults(self):
        variables = {"variable2": "value2"}
        output = "value1 value2"
        self.assertEqual(self.template_w.render(variables), output)

        with self.assertRaises(jinja2.exceptions.UndefinedError) as context:
            self.template_wo.render()
        self.assertTrue("'variable1' is undefined" in str(context.exception))

    def test_dont_render_undefined(self):
        with self.assertRaises(jinja2.exceptions.UndefinedError) as context:
            self.template_w.render()
        self.assertTrue("'variable2' is undefined" in str(context.exception))

    def test_render(self):
        variables = {"variable1": "test1", "variable2": "test2"}
        output = "test1 test2"
        self.assertEqual(self.template_w.render(variables), output)
        self.assertEqual(self.template_wo.render(variables), output)

    def test_save(self):
        variables = {"variable2": "value2"}
        output = "value1 value2"
        filepath = "/dir/rendered.cfg"
        with patch("cfgtemplater.config_template.open", mock_open()) as f:
            self.template_w.save(filepath, variables)
            print(f.mock_calls)
            f.assert_called_once_with(filepath, "w")
            f().write.assert_called_once_with("value1 value2")
