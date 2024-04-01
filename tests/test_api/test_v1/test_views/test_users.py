#!/usr/bin/python3
"""
Unittest for the api/v1/app.py
"""
import unittest
import os
import inspect
import pycodestyle as pep8
from api.v1.app import app
import api.v1.views.users as users_module
from datetime import datetime
from flask import jsonify
from models import storage, db
from models.user import User
from json import loads


class TestUsersDocPep8(unittest.TestCase):
    """unittest class for users module
    documentation and pep8 conformaty"""

    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['api/v1/views/users.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_users conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_api/test_v1/test_views/' +
                                    'test_users.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """test module documentation"""
        mod_doc = users_module.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all functions"""
        base_funcs = inspect.getmembers(users_module, inspect.isfunction)
        base_funcs.extend(inspect.getmembers(users_module, inspect.ismethod))
        for func in base_funcs:
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class TestUsers(unittest.TestCase):
    """unittest class for index.py"""

    @staticmethod
    def refine(response):
        """Refine the response"""
        return loads(response.data)

    def setUp(self):
        """Setup for the test"""
        self.app = app.test_client()
        self.app.testing = True
        kwargs = {'email': 'email', 'password': 'password'}
        self.users = []
        self.users.append(User(**kwargs))
        self.users[0].save()

    def tearDown(self):
        """Teardown for the test"""
        for user in self.users:
            user.delete()

    def test_get_users(self):
        """Test for GET /api/v1/users"""
        with app.app_context():
            response = self.app.get('/api/v1/users')
            self.assertEqual(response.status_code, 200)
            expected = jsonify([user.to_dict() for user
                                in storage.all(User).values()])
            self.assertEqual(self.refine(response), self.refine(expected))

    def test_get_user(self):
        """Test for GET /api/v1/users/<user_id>"""
        with app.app_context():
            response = self.app.get('/api/v1/users/{}'
                                    .format(self.users[0].id))
            self.assertEqual(response.status_code, 200)
            expected = jsonify(self.users[0].to_dict())
            self.assertEqual(self.refine(response), self.refine(expected))

    def test_get_user_404(self):
        """Test for GET /api/v1/users/<user_id> 404"""
        with app.app_context():
            response = self.app.get('/api/v1/users/{}'
                                    .format('49627dd4-3d39-4e0f' +
                                            '-b48-256850b248df'))
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json['error'], 'Not found')

    def test_delete_user(self):
        """Test for DELETE /api/v1/users/<user_id>"""
        with app.app_context():
            self.user_delete = User(email='email1', password='password1')
            self.user_delete.save()
            response = self.app.delete('/api/v1/users/{}'
                                       .format(self.user_delete.id))
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(self.user_delete, storage.all(User).values())

    def test_delete_user_404(self):
        """Test for DELETE /api/v1/users/<user_id> 404"""
        with app.app_context():
            response = self.app.delete('/api/v1/users/{}'
                                       .format('49627dd4-3d39-4e0f' +
                                               '-b48-256850b248df'))
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json['error'], 'Not found')

    def test_post_user(self):
        """Test for POST /api/v1/users"""
        with app.app_context():
            response = self.app.post('/api/v1/users',
                                     json={'email': 'email2',
                                           'password': 'password2'})
            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(storage.get(User, response.json['id']))
            self.assertEqual(response.json['email'], 'email2')
            self.app.delete('/api/v1/users/{}'.format(response.json['id']))

    def test_post_user_400(self):
        """Test for POST /api/v1/users 400"""
        with app.app_context():
            response = self.app.post('/api/v1/users', json=[])
            self.assertEqual(response.status_code, 400)
            response = self.app.post('/api/v1/users',
                                     json={'password': 'password3'})
            self.assertEqual(response.status_code, 400)
            response = self.app.post('/api/v1/users',
                                     json={'email': 'email3'})
            self.assertEqual(response.status_code, 400)

    @unittest.skipIf(not db, "not db")
    def test_put_user(self):
        """Test for PUT /api/v1/users/<user_id>"""
        iso = datetime.fromisoformat
        with app.app_context():
            # test ignore email
            response = self.app.put('/api/v1/users/{}'
                                    .format(self.users[0].id),
                                    json={'email': 'email4'})
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(response.json['email'], 'email4')
            self.assertEqual(response.json['email'], self.users[0].email)
            # test ignore id
            response = self.app.put('/api/v1/users/{}'
                                    .format(self.users[0].id),
                                    json={'id': 'id4'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['id'], self.users[0].id)
            # test ignore created_at
            response = self.app.put('/api/v1/users/{}'
                                    .format(self.users[0].id),
                                    json={'created_at': 'created_at4'})
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(response.json['created_at'], 'created_at4')
            self.assertEqual(iso(response.json['created_at']),
                             self.users[0].created_at)
            # test ignore updated_at
            response = self.app.put('/api/v1/users/{}'
                                    .format(self.users[0].id),
                                    json={'updated_at': 'updated_at4'})
            self.assertEqual(response.status_code, 200)
            self.assertNotEqual(response.json['updated_at'], 'updated_at4')
            self.assertEqual(iso(response.json['updated_at']),
                             self.users[0].updated_at)
            # test not ignore password
            response = self.app.put('/api/v1/users/{}'
                                    .format(self.users[0].id),
                                    json={'password': 'password4'})
            self.assertEqual(response.status_code, 200)

    def test_put_user_404(self):
        """Test for PUT /api/v1/users/<user_id> 404"""
        with app.app_context():
            response = self.app.put('/api/v1/users/{}'
                                    .format('49627dd4-3d39-4e0f' +
                                            '-b48-256850b248df'),
                                    json={'email': 'email4'})
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json['error'], 'Not found')
            response = self.app.put('/api/v1/users/{}'
                                    .format(self.users[0].id),
                                    json=[])
            self.assertEqual(response.status_code, 400)
