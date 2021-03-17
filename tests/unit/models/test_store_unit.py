
# s06e06-created

from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest

# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest tests\unit\models\test_store_unit.py       (run all test cases in this file)

# To run all test cases (unit, integration, ... under the 'test' folder and its sub-folders:
# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest discover -s tests -p test_*.py       OR
# > python -m unittest discover -s tests

class StoreTest(UnitBaseTest ):
    def test_create_store(self):
        store = StoreModel('test')

        self.assertEqual(store.name, 'test',
                         "The name of the store after creation does not equal the constructor argument.")

    print("==> Unit.StoreTest.test_create_store() ... passed")
