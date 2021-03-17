
# from unittest import TestCase         # s06e05-commented out
from models.item import ItemModel
from tests.unit.unit_base_test import UnitBaseTest    # s06e05-added

# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest tests\unit\models\test_item_unit.py       (run all test cases in this file)

# To run all test cases (unit, integration, ... under the 'test' folder and its sub-folders:
# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest discover -s tests -p test_*.py       OR
# > python -m unittest discover -s tests

# class ItemTest(TestCase):             # **NOTE** TestCase       # s06e05-commented out
# **NOTE** We could use 'BaseTest' but running test cases would take longer.
class ItemTest(UnitBaseTest):               # s06e05-added
    def test_create_item(self):

        # **NOTE** because we're not going to save in a database,
        # we can make up an store-id of 1.
        item = ItemModel('test', 19.99, 1)     # s06e05-added 1

        # **NOTE** The third argument is the error message that will be shown when
        # the first two arguments are not equal.
        self.assertEqual(item.name, 'test',
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.price, 19.99,
                         "The price of the item after creation does not equal the constructor argument.")

        # s06e05-added
        self.assertEqual(item.store_id, 1,
                         "The store_id of the item after creation does not equal the constructor argument.")
        self.assertIsNone(item.store,
                          "The item's store was not None even though the store was not created.")

        print("==> Unit.ItemTest.test_create_item() ... passed")

    def test_item_json(self):
        item = ItemModel('test', 19.99, 1)      # s06e05-added 1
        expected = {
            'name': 'test',
            'price': 19.99
        }

        self.assertEqual(
            item.json(),
            expected,
            "The JSON export of the item is incorrect. Received {}, expected {}.".format(item.json(), expected))

        print("==> Unit.ItemTest.test_item_json() ... passed")
