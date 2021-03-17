
# s07e05-created

from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest

# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest tests\unit\models\test_user_unit.py       (run all test cases in this file)

# To run all test cases (unit, integration, ... under the 'test' folder and its sub-folders:
# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest discover -s tests -p test_*.py       OR
# > python -m unittest discover -s tests

class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test', 'abcd')

        self.assertEqual(user.username, 'test',
                         "The name of the user after creation does not equal the constructor argument.")
        self.assertEqual(user.password, 'abcd',
                         "The password of the user after creation does not equal the constructor argument.")

        print("==> Unit.UserTest.test_create_user() ... passed")
