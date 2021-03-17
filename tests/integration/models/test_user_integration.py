
# s07e05-created

from models.user import UserModel
from tests.integration.integration_base_test import IntegrationBaseTest

# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest tests\integration\models\test_user_integration.py    (run all test cases in this file)

# To run all test cases (unit, integration, ... under the 'test' folder and its sub-folders:
# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest discover -s tests -p test_*.py       OR
# > python -m unittest discover -s tests

class UserTest(IntegrationBaseTest):
    def test_crud(self):
        with self.app_context():                # **NOTE**
            user = UserModel('test', 'abcd')

            self.assertIsNone(UserModel.find_by_username('test'),
                              "Found an user with name 'test' before save_to_db")
            self.assertIsNone(UserModel.find_by_id(1),
                              "Found an user with id '1' before save_to_db")

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('test'),
                                 "Did not find an user with name 'test' after save_to_db")
            self.assertIsNotNone(UserModel.find_by_id(1),
                                 "Did not find an user with id '1' after save_to_db")

        print("==> Integration.UserTest.test_crud() ... passed")
