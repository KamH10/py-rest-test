
# s06e06-created

from models.store import StoreModel
from models.item import ItemModel
from tests.integration.integration_base_test import IntegrationBaseTest

# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest tests\integration\models\test_store_integration.py    (run all test cases in this file)

# To run all test cases (unit, integration, ... under the 'test' folder and its sub-folders:
# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest discover -s tests -p test_*.py       OR
# > python -m unittest discover -s tests

class StoreTest(IntegrationBaseTest):

    def test_create_store(self):
        store = StoreModel('test')
        # **NOTE** VIP - cross check with POS1 in 'models/store.py'.
        # We want to make sure that the items property (and database) is empty at this stage.
        self.assertListEqual(store.items.all(), [],
                             "The store's items length was not 0 even though no items were added.")

    print("==> Integration.StoreTest.test_create_store() ... passed")

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'),
                              "Found an store with name 'test' before save_to_db")

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'),
                                 "Did not find an store with name 'test' after save_to_db")

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'),
                              "Found an store with name 'test' after delete_from_db")

        print("==> Integration.StoreTest.test_crud() ... passed")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)     # **NOTE**

            # **NOTE** store doesn't need the item, but item needs the store,
            # therefore we need to save the store first.
            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)    # **NOTE** count()
            self.assertEqual(store.items.first().name, 'test_item')

        print("==> Integration.StoreTest.test_store_relationship() ... passed")

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name': 'test',
                'items': [{'name':'test_item', 'price':19.99}]         # **NOTE**
            }

            self.assertEqual(
                store.json(),
                expected,
                "Storing JSON with items is incorrect")

        print("==> Integration.StoreTest.test_store_json_with_item() ... passed")


    def test_store_json(self):
        store = StoreModel('test')
        expected = {
            'name': 'test',
            'items': []         # **NOTE**
        }

        self.assertEqual(
            store.json(),
            expected,
            "The JSON export of the store is incorrect. Received {}, expected {}.".format(store.json(), expected))

        print("==> Integration.StoreTest.test_store_json() ... passed")
