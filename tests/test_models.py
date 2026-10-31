"""
Test cases for Account Model
"""
import os
import logging
from unittest import TestCase
from service.models import Account, DataValidationError, db
from service import app
from tests.factories import AccountFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "sqlite:///../test.db"
)


class TestAccountModel(TestCase):
    """Test Cases for Account Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Account.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def test_create_an_account(self):
        """It should Create an Account and assert that it exists"""
        fake_account = AccountFactory()
        account = Account(
            name=fake_account.name,
            email=fake_account.email,
            address=fake_account.address,
            phone_number=fake_account.phone_number,
            date_joined=fake_account.date_joined,
        )
        self.assertIsNotNone(account)
        self.assertEqual(account.id, None)
        account.create()
        self.assertIsNotNone(account.id)

    def test_read_an_account(self):
        """It should Read an Account"""
        account = AccountFactory()
        account.create()
        self.assertIsNotNone(account.id)
        found_account = Account.find(account.id)
        self.assertEqual(found_account.id, account.id)
        self.assertEqual(found_account.name, account.name)

    def test_update_an_account(self):
        """It should Update an Account"""
        account = AccountFactory()
        account.create()
        self.assertIsNotNone(account.id)
        account.email = "updated@example.com"
        account.update()
        found_account = Account.find(account.id)
        self.assertEqual(found_account.email, "updated@example.com")

    def test_delete_an_account(self):
        """It should Delete an Account"""
        account = AccountFactory()
        account.create()
        self.assertEqual(len(Account.all()), 1)
        account.delete()
        self.assertEqual(len(Account.all()), 0)

    def test_list_all_accounts(self):
        """It should List all Accounts in the database"""
        accounts = Account.all()
        self.assertEqual(len(accounts), 0)
        for _ in range(5):
            account = AccountFactory()
            account.create()
        self.assertEqual(len(Account.all()), 5)

    def test_serialize_an_account(self):
        """It should serialize an Account"""
        account = AccountFactory()
        data = account.serialize()
        self.assertIsNotNone(data)
        self.assertEqual(data["name"], account.name)
        self.assertEqual(data["email"], account.email)

    def test_deserialize_an_account(self):
        """It should deserialize an Account"""
        data = AccountFactory().serialize()
        account = Account()
        account.deserialize(data)
        self.assertIsNotNone(account)
        self.assertEqual(account.name, data["name"])
        self.assertEqual(account.email, data["email"])

    def test_deserialize_with_missing_data(self):
        """It should not deserialize an Account with missing data"""
        data = {"id": 1, "name": "Jane"}
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, data)

    def test_deserialize_with_bad_data(self):
        """It should not deserialize an Account with bad data"""
        data = "this is not a dictionary"
        account = Account()
        self.assertRaises(DataValidationError, account.deserialize, data)
