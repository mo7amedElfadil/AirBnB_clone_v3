#!/usr/bin/python3
"""
Unittest for the api/v1/app.py
"""
import unittest
import inspect
import pycodestyle as pep8
from api.v1.app import app
import api.v1.views.places as places_module
from datetime import datetime
from flask import jsonify
from models import storage, db
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from json import loads


class TestPlacesDocPep8(unittest.TestCase):
    """unittest class for places module
    documentation and pep8 conformaty"""

    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['api/v1/views/places.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_places conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_api/test_v1/test_views/' +
                                    'test_places.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """test module documentation"""
        mod_doc = places_module.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all functions"""
        base_funcs = inspect.getmembers(places_module, inspect.isfunction)
        base_funcs.extend(inspect.getmembers(places_module, inspect.ismethod))
        for func in base_funcs:
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class TestPlaces(unittest.TestCase):
    """unittest class for index.py"""

    @staticmethod
    def refine(response):
        """Refine the response"""
        return loads(response.data)

    def setUp(self):
        """Setup for the test"""
        self.app = app.test_client()
        self.app.testing = True
        self.instances = {}
        self.instances['state'] = State(name='state')
        self.instances['state'].save()
        self.instances['city'] = City(name='city',
                                      state_id=self.instances['state'].id)
        self.instances['city'].save()
        self.instances['user'] = User(email='email', password='password')
        self.instances['user'].save()
        self.kwargs = {'name': 'place', 'user_id': self.instances['user'].id,
                       'city_id': self.instances['city'].id}
        self.instances['place1'] = Place(**self.kwargs)
        self.instances['place1'].save()

    def tearDown(self):
        """Teardown for the test"""
        instances = [key for key in self.instances.keys() if
                     key.startswith('state') or key.startswith('user')]
        for instance in instances:
            self.instances[instance].delete()

    @unittest.skipIf(not db, "not db")
    def test_get_places(self):
        """Test for GET /api/v1/cities/<city_id>/places"""
        with app.app_context():
            response = self.app.get('/api/v1/cities/{}/places'
                                    .format(self.instances['city'].id))
            self.assertEqual(response.status_code, 200)
            expected = jsonify([place.to_dict() for place
                                in storage.all(Place).values()])
            self.assertEqual(self.refine(response), self.refine(expected))

    def test_get_place(self):
        """Test for GET /api/v1/places/<place_id>"""
        with app.app_context():
            response = self.app.get('/api/v1/places/{}'
                                    .format(self.instances['place1'].id))
            self.assertEqual(response.status_code, 200)
            expected = jsonify(self.instances['place1'].to_dict())
            self.assertEqual(self.refine(response), self.refine(expected))

    def test_get_place_404(self):
        """Test for GET /api/v1/places/<place_id> 404"""
        with app.app_context():
            response = self.app.get('/api/v1/places/{}'
                                    .format('49627dd4-3d39-4e0f' +
                                            '-b48-256850b248df'))
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json['error'], 'Not found')

    def test_delete_place(self):
        """Test for DELETE /api/v1/places/<place_id>"""
        with app.app_context():
            self.place_delete = Place(**self.kwargs)
            self.place_delete.save()
            response = self.app.delete('/api/v1/places/{}'
                                       .format(self.place_delete.id))
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(self.place_delete, storage.all(Place).values())

    def test_delete_place_404(self):
        """Test for DELETE /api/v1/places/<place_id> 404"""
        with app.app_context():
            response = self.app.delete('/api/v1/places/{}'
                                       .format('49627dd4-3d39-4e0f' +
                                               '-b48-256850b248df'))
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json['error'], 'Not found')

    def test_post_place(self):
        """Test for POST /api/v1/places"""
        with app.app_context():
            response = self.app.post('/api/v1/cities/{}/places'
                                     .format(self.instances['city'].id),
                                     json=self.kwargs)
            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(storage.get(Place, response.json['id']))
            self.assertEqual(response.json['name'], self.kwargs['name'])
            self.assertEqual(response.json['user_id'], self.kwargs['user_id'])
            self.assertEqual(response.json['city_id'], self.kwargs['city_id'])
            self.app.delete('/api/v1/places/{}'.format(response.json['id']))

    def test_post_place_400(self):
        """Test for POST /api/v1/places 400"""
        with app.app_context():
            response = self.app.post('/api/v1/cities/{}/places'
                                     .format('49627dd4-3d39-4e0f' +
                                             '-b48-256850b248df'),
                                     json=self.kwargs)
            self.assertEqual(response.status_code, 404)

            response = self.app.post('/api/v1/cities/{}/places'
                                     .format(self.instances['city'].id),
                                     json=[])
            self.assertEqual(response.status_code, 400)
            response = self.app.post('/api/v1/cities/{}/places'
                                     .format(self.instances['city'].id),
                                     json={'name': 'name3'})
            self.assertEqual(response.status_code, 400)
            response = self.app.post('/api/v1/cities/{}/places'
                                     .format(self.instances['city'].id),
                                     json={'user_id': 'user_id3'})
            self.assertEqual(response.status_code, 400)

    @unittest.skipIf(not db, "not db")
    def test_put_place(self):
        """Test for PUT /api/v1/places/<place_id>"""
        iso = datetime.fromisoformat
        with app.app_context():
            # test ignore user_id
            response = self.app.put('/api/v1/places/{}'
                                    .format(self.instances['place1'].id),
                                    json={'user_id': 'user_id4'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['user_id'],
                             self.instances['place1'].user_id)
            self.assertNotEqual(response.json['user_id'], 'user_id4')
            # test ignore id
            response = self.app.put('/api/v1/places/{}'
                                    .format(self.instances['place1'].id),
                                    json={'id': 'id4'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['id'], self.instances['place1'].id)
            self.assertNotEqual(response.json['id'], 'id4')
            # test ignore created_at
            response = self.app.put('/api/v1/places/{}'
                                    .format(self.instances['place1'].id),
                                    json={'created_at': 'created_at4'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(iso(response.json['created_at']),
                             self.instances['place1'].created_at)
            self.assertNotEqual(response.json['created_at'], 'created_at4')
            # test ignore updated_at
            response = self.app.put('/api/v1/places/{}'
                                    .format(self.instances['place1'].id),
                                    json={'updated_at': 'updated_at4'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(iso(response.json['updated_at']),
                             self.instances['place1'].updated_at)
            self.assertNotEqual(response.json['updated_at'], 'updated_at4')
            # test not ignore name
            response = self.app.put('/api/v1/places/{}'
                                    .format(self.instances['place1'].id),
                                    json={'name': 'name4'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['name'], 'name4')
            self.assertEqual(response.json['name'],
                             self.instances['place1'].name)

    def test_put_place_404(self):
        """Test for PUT /api/v1/places/<place_id> 404"""
        with app.app_context():
            response = self.app.put('/api/v1/places/{}'
                                    .format('49627dd4-3d39-4e0f' +
                                            '-b48-256850b248df'),
                                    json={'name': 'name4'})
            self.assertEqual(response.status_code, 404)
            response = self.app.put('/api/v1/places/{}'
                                    .format(self.instances['place1'].id),
                                    json=[])
            self.assertEqual(response.status_code, 400)
