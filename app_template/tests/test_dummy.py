import os
import tempfile
import unittest

from appstore import app
from appstore.models import db

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + tempfile.mkstemp()[1]
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_dummy_pass(self):
        assert 1+1 == 2

    def test_dummy_fail(self):
        assert 3*4 == 11
