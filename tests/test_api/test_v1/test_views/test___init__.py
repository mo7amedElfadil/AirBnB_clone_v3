#!/usr/bin/python3
"""
Unittest for the api/v1/app.py
"""
import unittest
import pycodestyle as pep8


class TestIndexDocPep8(unittest.TestCase):
    """unittest class for FileStorage class
    documentation and pep8 conformaty"""

    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['api/v1/views/__init__.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_file_storage conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_api/test_v1/test_views/' +
                                    'test___init__.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")
