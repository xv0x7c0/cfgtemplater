import sys
import unittest
from unittest.mock import mock_open, patch
import cfgtemplater.command_line
import pytest


class CommandLineTests(unittest.TestCase):
    def data_ok(self):
        return """---
variables:
  variable1:
    default: value1
---
{{ variable1 }}"""

    def data_missing_variable(self):
        return """{{ variable1 }}"""

    def data_missing_subtemplate(self):
        return """{% include 'subtemplate.j2' %}"""

    def data_missing_filter(self):
        return """{{ 'test' | missing_filter }}"""

    def data_syntax_error(self):
        return """{% include 'subtemplate.j2 }}"""

    def data_yaml_ok(self):
        return """---
variable1: test
"""

    def data_yaml_nok(self):
        return """---
variable1: ][
"""

    def setup_template(self, template, args):
        filepath = "/dir/template.cfg"
        mock = mock_open(read_data=template)
        with patch("cfgtemplater.base_template.open", mock) as f:
            with patch.object(sys, "argv", args):
                with patch.object(sys, "exit") as exit:
                    cfgtemplater.command_line.main()
                    self.out, self.err = self.capsys.readouterr()
                    self.exit = exit

    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    def test_render_ok(self):
        args = ["cfgtemplater", "/dir/template.cfg"]
        self.setup_template(self.data_ok(), args)
        self.assertEqual(self.out, "value1\n")

    def test_return_code_ok(self):
        args = ["cfgtemplater", "/dir/template.cfg"]
        self.setup_template(self.data_ok(), args)
        self.assertEqual(self.exit.call_args[0][0], 0)

    def test_return_code_missing_variable(self):
        args = ["cfgtemplater", "/dir/template.cfg"]
        self.setup_template(self.data_missing_variable(), args)
        self.assertEqual(self.exit.call_args[0][0], 10)

    def test_return_code_missing_subtemplate(self):
        args = ["cfgtemplater", "/dir/template.cfg"]
        self.setup_template(self.data_missing_subtemplate(), args)
        self.assertEqual(self.exit.call_args[0][0], 11)

    def test_return_code_missing_filter(self):
        args = ["cfgtemplater", "/dir/template.cfg"]
        self.setup_template(self.data_missing_filter(), args)
        self.assertEqual(self.exit.call_args[0][0], 12)

    def test_return_code_syntax_error(self):
        args = ["cfgtemplater", "/dir/template.cfg"]
        self.setup_template(self.data_syntax_error(), args)
        self.assertEqual(self.exit.call_args[0][0], 13)

    def test_cli_variables(self):
        args = ["cfgtemplater", "-p", "variable1='test'", "/dir/template.cfg"]
        self.setup_template(self.data_missing_variable(), args)
        self.assertEqual(self.exit.call_args[0][0], 0)
        self.assertEqual(self.out, "test\n")

    def test_cli_variables_nok(self):
        args = ["cfgtemplater", "-p", "variable1=test", "/dir/template.cfg"]
        self.setup_template(self.data_missing_variable(), args)
        self.assertEqual(self.exit.call_args[0][0], 14)

    def test_yaml_ok(self):
        args = ["cfgtemplater", "-y", "variables.yaml", "/dir/template.cfg"]
        mock = mock_open(read_data=self.data_yaml_ok())
        with patch("cfgtemplater.command_line.open", mock) as f:
            self.setup_template(self.data_missing_variable(), args)
        self.assertEqual(self.exit.call_args[0][0], 0)
        self.assertEqual(self.out, "test\n")

    def test_yaml_nok(self):
        args = ["cfgtemplater", "-y", "variables.yaml", "/dir/template.cfg"]
        mock = mock_open(read_data=self.data_yaml_nok())
        with patch("cfgtemplater.command_line.open", mock) as f:
            self.setup_template(self.data_missing_variable(), args)
            self.assertEqual(self.exit.call_args[0][0], 15)

    def test_yaml_file_nok(self):
        args = ["cfgtemplater", "-y", "variables.yaml", "/dir/template.cfg"]
        self.setup_template(self.data_missing_variable(), args)
        self.assertEqual(self.exit.call_args[0][0], 16)
