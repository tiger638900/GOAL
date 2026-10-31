"""
Account API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from tests.factories import AccountFactory
from service.common import status
from service.models import db, Account
from service.routes import app
from service import talisman

DATABASE_URI = os.getenv(
    "DATABASE_URI", "sqlite:///../test.db"
)
HTTPS_ENV = "True"


class TestAccountService(TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Account.init_db(app)
        talisman.force_https = False

    @classmethod
    def tearDownClass(cls):
        """Runs once after all test cases"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Runs after each test"""
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################
    def _create_accounts(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []
        for _ in range(count):
            account = AccountFactory()
            response = self.client.post("/accounts", json=account.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            new_account = response.get_json()
            account.id = new_account["id"]
            accounts.append(account)
        return accounts

    ######################################################################
    #  A C C O U N T   T E S T   C A S E S
    ######################################################################
    def test_index(self):
        """It should return 200_OK and the home page info"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Account REST API Service")

    def test_create_account(self):
        """It should Create a new Account"""
        account = AccountFactory()
        response = self.client.post(
            "/accounts",
            json=account.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data returned
        new_account = response.get_json()
        self.assertEqual(new_account["name"], account.name)
        self.assertEqual(new_account["email"], account.email)
        self.assertEqual(new_account["address"], account.address)
        self.assertEqual(new_account["phone_number"], account.phone_number)
        self.assertEqual(new_account["date_joined"], str(account.date_joined))

    def test_read_account(self):
        """It should Read an Account"""
        account = self._create_accounts(1)[0]
        response = self.client.get(f"/accounts/{account.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], account.name)

    def test_get_account_not_found(self):
        """It should not Read an Account that is not found"""
        response = self.client.get("/accounts/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_accounts(self):
        """It should List all Accounts"""
        self._create_accounts(5)
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_update_account(self):
        """It should Update an existing Account"""
        test_account = AccountFactory()
        response = self.client.post(
            "/accounts", json=test_account.serialize(), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_account = response.get_json()
        new_account["name"] = "Updated Name"
        response = self.client.put(
            f"/accounts/{new_account['id']}",
            json=new_account,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_account = response.get_json()
        self.assertEqual(updated_account["name"], "Updated Name")

    def test_update_account_not_found(self):
        """It should not Update an Account that is not found"""
        response = self.client.put(
            "/accounts/0", json={}, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_account(self):
        """It should Delete an Account"""
        account = self._create_accounts(1)[0]
        response = self.client.delete(f"/accounts/{account.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_security_headers(self):
        """It should return security headers from Talisman"""
        response = self.client.get("/", environ_overrides={"wsgi.url_scheme": "https"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        headers = {
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'self'; object-src 'none'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        for key, value in headers.items():
            self.assertEqual(response.headers.get(key), value)

    def test_cors_security(self):
        """It should return a CORS header"""
        response = self.client.get("/", environ_overrides={"wsgi.url_scheme": "https"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check for the CORS header
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")
