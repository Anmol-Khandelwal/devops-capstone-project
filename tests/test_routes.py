import os
import logging
from unittest import TestCase
from service import app
from service.models import db, Account

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///test.db")


class TestAccountService(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)

    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()

    def _create_account(self):
        payload = {
            "name": "John Doe",
            "email": "john@example.com",
            "address": "123 Main St",
            "phone_number": "555-1234",
        }
        return self.client.post("/accounts", json=payload)

    def test_index(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_create_account(self):
        resp = self._create_account()
        self.assertEqual(resp.status_code, 201)

    def test_list_accounts(self):
        self._create_account()
        resp = self.client.get("/accounts")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 1)

    def test_read_account(self):
        resp = self._create_account()
        account_id = resp.get_json()["id"]
        resp = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, 200)

    def test_update_account(self):
        resp = self._create_account()
        account_id = resp.get_json()["id"]
        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "address": "456 Side St",
            "phone_number": "555-5678",
        }
        resp = self.client.put(f"/accounts/{account_id}", json=payload)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Jane Doe")

    def test_delete_account(self):
        resp = self._create_account()
        account_id = resp.get_json()["id"]
        resp = self.client.delete(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, 204)
