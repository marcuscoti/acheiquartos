import os
import unittest
import app
#from app import app as app_root, db

TEST_DB = 'test.db'
#python -m unittest discover

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        app.app.config['DEBUG'] = False
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB
        self.app = app.app.test_client()
        app.db.drop_all()
        app.db.create_all()

    # executed after each test
    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()