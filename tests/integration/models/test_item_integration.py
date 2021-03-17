
from models.item import ItemModel
from models.store import StoreModel
from tests.integration.integration_base_test import IntegrationBaseTest

# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest tests\integration\models\test_item_integration.py    (run all test cases in this file)

# To run all test cases (unit, integration, ... under the 'test' folder and its sub-folders:
# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest discover -s tests -p test_*.py       OR
# > python -m unittest discover -s tests

class ItemTest(IntegrationBaseTest):           # **NOTE** IntegrationBaseTest
    def test_crud(self):
        with self.app_context():    # **NOTE** pretends to be running the app
            store = StoreModel('test')          # s06e04-added
            store.save_to_db()                  # s06e04-added

            # If you remove the previous two lines, program will work without
            # checking referential integrity. This is because we're using 'sqlite'
            # in 'integration_base_test.py'. As soon as converting 'sqlite' to PostgreSql,  MySql, ...,
            # the following line (in absence of the two preceding lines) will cause an error
            item = ItemModel('test', 19.99, 1)  # s06e04-added 1

            # **NOTE** Make sure the item doesn't exist before saving it in DB
            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()       # **NOTE** save to sqlite

            self.assertIsNotNone(ItemModel.find_by_name('test'),
                                 "Did not find an item with name 'test' after save_to_db")

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name 'test' after delete_from_db")

        print("==> Integration.ItemTest.test_crud() ... passed")

    # s06e05-added
    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, 'test_store')

        print("==> Integration.ItemTest.test_store_relationship() ... passed")
