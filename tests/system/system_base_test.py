
# s07e06-created

"""
IntegrationBaseTest should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase       # **NOTE**
from app import app
from db import db

# **NOTE** We don't want to run this file directly, therefore we call
# it 'system_base_test.py' instead of 'test_system_base.py'.

class SystemBaseTest(TestCase):           # **NOTE**

    @classmethod
    def setUpClass(cls):    # **NOTE** VIP - runs once for each test case/test class
        # **NOTE** Make sure database exists
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tyler@localhost:5432/test'
        app.config['DEBUG'] = False

        with app.app_context():
            db.init_app(app)        # **NOTE**

        # print("* SystemBaseTest.setUpClass()")    # fDBG


    def setUp(self):    # **NOTE** VIP - runs before every test method
        # s07e06 - Moved to 'setUpClass'
        # **NOTE** Make sure database exists
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tyler@localhost:5432/test'

        # **NOTE** loads up all the app variables, config, ... and
        # pretends to be running the app.
        with app.app_context():
            # db.init_app(app)          # **NOTE** s07e06 - Moved to 'setUpClass'
            db.create_all()             # **NOTE**

        # **NOTE** Get a test client
        # self.app = app.test_client()
        self.app = app.test_client      # **NOTE** s07e06 - removed parenthesis
        self.app_context = app.app_context

        # print("* SystemBaseTest.setUp()")    # fDBG

    def tearDown(self):             # **NOTE** tearDown() runs after every test
        # Database is blank
        with app.app_context():
            db.session.remove()     # **NOTE**
            db.drop_all()           # **NOTE**

        # print("* SystemBaseTest.tearDown()")    # fDBG
