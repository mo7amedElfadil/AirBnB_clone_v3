#!/usr/bin/python3
"""
Unittest for the api/v1/app.py
"""
import unittest
import os
import inspect
import pycodestyle as pep8
from api.v1.app import app
import api.v1.views.index as index_module
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class TestIndexDocPep8(unittest.TestCase):
    """unittest class for FileStorage class
    documentation and pep8 conformaty"""

    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['api/v1/views/index.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_file_storage conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_api/test_v1/test_views/' +
                                    'test_index.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """test module documentation"""
        mod_doc = index_module.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all functions"""
        base_funcs = inspect.getmembers(index_module, inspect.isfunction)
        base_funcs.extend(inspect.getmembers(index_module, inspect.ismethod))
        for func in base_funcs:
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class TestIndex(unittest.TestCase):
    """unittest class for index.py"""

    def setUp(self):
        """Setup for the test"""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_status(self):
        """Test for app.py status"""
        with app.app_context():
            response = self.app.get('/api/v1/status')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"status":"OK"}\n')

    def test_index_stats(self):
        """Test for app.py stats"""
        with app.app_context():
            response = self.app.get('/api/v1/stats')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data,
                             jsonify({"states": storage.count(State),
                                      "cities": storage.count(City),
                                      "users": storage.count(User),
                                      "places": storage.count(Place),
                                      "reviews": storage.count(Review),
                                      "amenities":
                                      storage.count(Amenity)}).data)

    def test_index_404(self):
        """Test for app.py 404"""
        with app.app_context():
            response = self.app.get('/api/v1/404')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b'{"error":"Not found"}\n')
