
# s07e10-created

from models.user import UserModel
from models.item import ItemModel
from models.store import StoreModel
from tests.system.system_base_test import SystemBaseTest
import json

# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest tests\system\test_item_system.py    (run all test cases in this file)

# To run all test cases (unit, integration, ... under the 'test' folder and its sub-folders:
# > cd C:\KamProgramming\Python\testing_slava\1-tested\s08\s08e09\rest
# > python -m unittest discover -s tests -p test_*.py       OR
# > python -m unittest discover -s tests


class ItemTest(SystemBaseTest):
    def setUp(self):                    # **NOTE** VIP
        # **NOTE** VIP call the setUp() method of the super-class that is SystemBaseTest
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()

                # **NOTE** VIP
                auth_request = client.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})

                # **NOTE** VIP - format of the authorization header is:
                # {'Authorization': 'JWT ' + auth_token
                self.auth_header = "JWT {}".format(json.loads(auth_request.data)['access_token'])


    def test_item_no_auth(self):
        with self.app() as client:
            resp = client.get('/item/test')     # **NOTE** get()
            # **NOTE** VIP - cross check with POS1 'resources/item.py' where we've
            # defined @jwt_required(). Because we haven't included the authorization header,
            # the response is 401, as expected.
            self.assertEqual(resp.status_code, 401)

        print("==> System.ItemTest.test_item_no_auth() ... passed")  # fDBG

    def test_item_not_found(self):
        with self.app() as client:
            # **NOTE** VIP - format of the authorization header is:
            # {'Authorization': 'JWT ' + auth_token
            resp = client.get('/item/test', headers={'Authorization': self.auth_header})
            self.assertEqual(resp.status_code, 404)

        print("==> System.ItemTest.test_item_not_found() ... passed")  # fDBG

    def test_item_found(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                resp = client.get('/item/test', headers={'Authorization': self.auth_header})    # **NOTE** get()

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(d1={'name': 'test', 'price': 17.99},
                                     d2=json.loads(resp.data))
        print("==> System.ItemTest.test_item_found() ... passed")  # fDBG

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                resp = client.delete('/item/test')      # **NOTE** delete()

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(d1={'message': 'Item deleted'},
                                     d2=json.loads(resp.data))

        print("==> System.ItemTest.test_delete_item() ... passed")  # fDBG

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test', data={'price': 17.99, 'store_id': 1})  # **NOTE** post()

                self.assertEqual(resp.status_code, 201)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual(d1={'name': 'test', 'price': 17.99},
                                     d2=json.loads(resp.data))

        print("==> System.ItemTest.test_create_item() ... passed")  # fDBG

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.post('/item/test', data={'price': 17.99, 'store_id': 1})
                resp = client.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 400)

        print("==> System.ItemTest.test_create_duplicate_item() ... passed")  # fDBG

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', data={'price': 17.99, 'store_id': 1})   # **NOTE** put()

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual(d1={'name': 'test', 'price': 17.99},
                                     d2=json.loads(resp.data))

        print("==> System.ItemTest.test_put_item() ... passed")  # fDBG

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.put('/item/test', data={'price': 17.99, 'store_id': 1})
                resp = client.put('/item/test', data={'price': 18.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 18.99)

        print("==> System.ItemTest.test_put_update_item() ... passed")  # fDBG

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                resp = client.get('/items')

                self.assertDictEqual(d1={'items': [{'name': 'test', 'price': 17.99}]},
                                     d2=json.loads(resp.data))

        print("==> System.ItemTest.test_item_list() ... passed")  # fDBG
