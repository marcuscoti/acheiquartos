import unittest
from app import app as app_root, db
TEST_DB = 'test.db'
#python -m unittest discover

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app_root.config['TESTING'] = True
        app_root.config['WTF_CSRF_ENABLED'] = False
        app_root.config['DEBUG'] = False
        app_root.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB
        self.client = app_root.test_client()
        db.drop_all()
        db.create_all()

    # executed after each test
    def tearDown(self):
        pass

    def register(self, email, password):
        return self.client.post('/user/register', data=dict(email=email, password=password, retype_password=password), follow_redirects=True)

    def login(self, email, password):
        return self.client.post('/user/sign-in', data=dict(email=email, password=password), follow_redirects=True)

    def test_register_login(self):
        email = 'marcuscoti@gmail.com'
        password = 'Lenovo2018'
        response = self.register(email, password)
        self.assertEqual(200, response.status_code, 'REGISTER FAILURE')
        response = self.login(email, password)
        self.assertIn('You have signed in successfully.', response.data, 'LOGIN FAILURE')
        response = self.client.post('/dashboard', follow_redirects=True)
        self.assertIn('Gerenciar', response.data, 'DASHBOARD FAILURE')
        response = self.client.post('/user/sign-out', follow_redirects=True)
        self.assertIn('You have signed out successfully.', response.data, 'LOGOUT FAILURE')

if __name__ == "__main__":
    unittest.main()