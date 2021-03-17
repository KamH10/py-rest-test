# s07e07-created

from models.user import UserModel
from tests.system.system_base_test import SystemBaseTest
import json

# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest tests\system\test_user_system.py    (run all test cases in this file)

# To run all test cases (unit, integration, ... under the 'test' folder and its sub-folders:
# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest discover -s tests -p test_*.py       OR
# > python -m unittest discover -s tests

class UserTest(SystemBaseTest):
    def test_register_user(self):
        with self.app() as client:      # **NOTE**
            with self.app_context():    # **NOTE** to save data to database
                # **NOTE** pretend to be a client of our API
                r = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(r.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual(d1={'message': 'User created successfully.'},
                                     d2=json.loads(r.data))
                # **NOTE** json.loads() converting json object to python dictionary

    print("==> System.UserTest.test_register_user() ... passed")    # fDBG


    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})

                # **NOTE** VIP - the '/auth' endpoint requires us to send the data in
                # json format (not in form format).
                auth_response = client.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})       # **NOTE**

                # **NOTE** VIP
                self.assertIn('access_token', json.loads(auth_response.data).keys())

        print("==> System.UserTest.test_register_and_login() ... passed")    # fDBG

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                # **NOTE** with the first request we're saving the user. When we do the second
                # request, we should get a 400 error.
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(d1={'message': 'A user with that username already exists'},
                                     d2=json.loads(response.data))

        print("==> System.UserTest.test_register_duplicate_user() ... passed")    # fDBG
