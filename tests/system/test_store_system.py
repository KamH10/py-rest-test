
# s07e09-created

from models.item import ItemModel
from models.store import StoreModel
from tests.system.system_base_test import SystemBaseTest
import json

# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest tests\system\test_store_system.py    (run all test cases in this file)

# To run all test cases (unit, integration, ... under the 'test' folder and its sub-folders:
# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest discover -s tests -p test_*.py       OR
# > python -m unittest discover -s tests

class StoreTest(SystemBaseTest):

    def test_create_store(self):
        with self.app() as client:                      # **NOTE**
            with self.app_context():                    # **NOTE**
                response = client.post('/store/test')   # **NOTE** client.post()

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(d1={'name': 'test', 'items': []},      # **NOTE**
                                     d2=json.loads(response.data))

        print("==> System.StoreTest.test_create_store() ... passed")    # fDBG

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')                  # **NOTE**
                resp = client.post('/store/test')       # **NOTE** client.post()

                self.assertEqual(resp.status_code, 400)

        print("==> System.StoreTest.test_create_duplicate_store() ... passed")    # fDBG

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()             # **NOTE**
                resp = client.delete('/store/test')     # **NOTE** client.delete()

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(d1={'message': 'Store deleted'},
                                     d2=json.loads(resp.data))

        print("==> System.StoreTest.test_delete_store() ... passed")    # fDBG

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/store/test')       # **NOTE** client.get()

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name':'test', 'items':[]},
                                     json.loads(resp.data))

        print("==> System.StoreTest.test_find_store() ... passed")    # fDBG

    def test_store_not_found(self):
        with self.app() as client:
            resp = client.get('/store/test')
            self.assertEqual(resp.status_code, 404)

        print("==> System.StoreTest.test_store_not_found() ... passed")    # fDBG

    def test_store_found(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/store/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(d1={'name': 'test', 'items': []},
                                     d2=json.loads(resp.data))

        print("==> System.StoreTest.test_store_found() ... passed")    # fDBG

    def test_store_with_items_found(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()             # **NOTE**
                ItemModel('test', 2.99, 1).save_to_db()     # **NOTE**
                resp = client.get('/store/test')            # **NOTE** client.get()

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(d1={'name': 'test', 'items': [{'name': 'test', 'price': 2.99}]},
                                     d2=json.loads(resp.data))

        print("==> System.StoreTest.test_store_with_items_found() ... passed")    # fDBG

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.get('/stores')

                self.assertDictEqual(d1={'stores': [{'name': 'test', 'items': []}]},
                                     d2=json.loads(resp.data))

        print("==> System.StoreTest.test_store_list() ... passed")    # fDBG

    def test_store_with_items_list(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()             # **NOTE**
                ItemModel('test', 17.99, 1).save_to_db()    # **NOTE**
                resp = c.get('/stores')

                self.assertDictEqual(d1={'stores': [{'name': 'test', 'items': [{'name': 'test', 'price': 17.99}]}]},
                                     d2=json.loads(resp.data))

        print("==> System.StoreTest.test_store_with_items_list() ... passed")    # fDBG
