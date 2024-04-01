#!/usr/bin/python3
"""
Unittest for the api/v1/app.py
"""
import unittest
import os
import inspect
import pycodestyle as pep8
from api.v1.app import app
from datetime import datetime
from flask import jsonify
from models import storage, db
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from json import loads


class TestPlacesDocPep8(unittest.TestCase):
    """unittest class for states module
    documentation and pep8 conformaty"""

    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['api/v1/views/states.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_states conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_api/test_v1/test_views/' +
                                    'test_states.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")


class TestStates(unittest.TestCase):
    """unittest class for states.py"""

    @staticmethod
    def refine(response):
        """Refine the response"""
        return loads(response.data)

    def setUp(self):
        """Setup for the test"""
        self.app = app.test_client()
        self.app.testing = True
        self.instances = {}
        self.instances['state1'] = State(name='alabama')
        self.instances['state1'].save()
        self.instances['state2'] = State(name='lousiana')
        self.instances['state2'].save()
        self.instances['city'] = City(name='city',
                                      state_id=self.instances['state1'].id)
        self.instances['city'].save()
        self.instances['user'] = User(email='email', password='password')
        self.instances['user'].save()
        self.kwargs = {'name': 'new mexico'}

# ******ask about teardown
    def tearDown(self):
        """Teardown for the test"""
        instances = [key for key in self.instances.keys() if
                     key.startswith('state') or key.startswith('user')]
        for instance in instances:
            self.instances[instance].delete()

    @unittest.skipIf(not db, "not db")
    def test_get_states(self):
        """Test for GET /api/v1/states"""
        with app.app_context():
            response = self.app.get('/api/v1/states/')
            self.assertEqual(response.status_code, 200)
            expected = jsonify([state.to_dict() for state
                                in storage.all(State).values()])
            self.assertEqual(self.refine(response), self.refine(expected))

    def test_get_state(self):
        """Test for GET /api/v1/states/<state_id>"""
        with app.app_context():
            response = self.app.get('/api/v1/states/{}'
                                    .format(self.instances['state1'].id))
            self.assertEqual(response.status_code, 200)
            expected = jsonify(self.instances['state1'].to_dict())
            self.assertEqual(self.refine(response), self.refine(expected))

    def test_get_state_404(self):
        """Test for GET /api/v1/states/<state_id> 404"""
        with app.app_context():
            response = self.app.get('/api/v1/states/{}'
                                    .format('49627dd4-3d39-4e0f' +
                                            '-b48-256850b248df'))
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json['error'], 'Not found')

    def test_delete_state(self):
        """Test for DELETE /api/v1/states/<state_id>"""
        with app.app_context():
            self.state_delete = State(**self.kwargs)
            self.state_delete.save()
            response = self.app.delete('/api/v1/states/{}'
                                       .format(self.state_delete.id))
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(self.state_delete, storage.all(State).values())

    def test_delete_state_404(self):
        """Test for DELETE /api/v1/states/<state_id> 404"""
        with app.app_context():
            response = self.app.delete('/api/v1/states/{}'
                                       .format('49627dd4-3d39-4e0f' +
                                               '-b48-256850b248df'))
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json['error'], 'Not found')

    def test_post_state(self):
        """Test for POST /api/v1/states"""
        with app.app_context():
            response = self.app.post('/api/v1/states', json=self.kwargs)
            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(storage.get(State, response.json['id']))
            self.assertEqual(response.json['name'], self.kwargs['name'])
            self.app.delete('/api/v1/states/{}'.format(response.json['id']))

    def test_post_state_400(self):
        """Test for POST /api/v1/states 400"""
        with app.app_context():
            response = self.app.post('/api/v1/states', json=[])
            self.assertEqual(response.status_code, 400)
            response = self.app.post('/api/v1/states', json={'notname': 'abc'})
            self.assertEqual(response.status_code, 400)

    @unittest.skipIf(not db, "not db")
    def test_put_state(self):
        """Test for PUT /api/v1/states/<state_id>"""
        iso = datetime.fromisoformat
        with app.app_context():
            # test ignore id
            response = self.app.put('/api/v1/states/{}'
                                    .format(self.instances['state1'].id),
                                    json={'id': 'id4'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['id'], self.instances['state1'].id)
            self.assertNotEqual(response.json['id'], 'id4')
            # test ignore created_at
            response = self.app.put('/api/v1/states/{}'
                                    .format(self.instances['state1'].id),
                                    json={'created_at': 'created_at4'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(iso(response.json['created_at']),
                             self.instances['state1'].created_at)
            self.assertNotEqual(response.json['created_at'], 'created_at4')
            # test ignore updated_at
            response = self.app.put('/api/v1/states/{}'
                                    .format(self.instances['state1'].id),
                                    json={'updated_at': 'updated_at4'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(iso(response.json['updated_at']),
                             self.instances['state1'].updated_at)
            self.assertNotEqual(response.json['updated_at'], 'updated_at4')
            # test not ignore name
            response = self.app.put('/api/v1/states/{}'
                                    .format(self.instances['state1'].id),
                                    json={'name': 'name4'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['name'], 'name4')
            self.assertEqual(response.json['name'],
                             self.instances['state1'].name)

    def test_put_state_404(self):
        """Test for PUT /api/v1/states/<state_id> 404"""
        with app.app_context():
            response = self.app.put('/api/v1/states/{}'
                                    .format('49627dd4-3d39-4e0f' +
                                            '-b48-256850b248df'),
                                    json={'name': 'name4'})
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json['error'], 'Not found')
            response = self.app.put('/api/v1/states/{}'
                                    .format(self.instances['state1'].id),
                                    json=[])
            self.assertEqual(response.status_code, 400)
