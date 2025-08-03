# test_app.py
import unittest
import json
from app import app
import init_db
import sqlite3

class UserManagementTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Use a fresh in-memory database
        app.config['DATABASE'] = ':memory:'
        self.conn = sqlite3.connect(':memory:')
        self._init_db_for_test()

    def _init_db_for_test(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        users = [
            ("Alice", "alice@example.com", "hashed_password1"),
            ("Bob", "bob@example.com", "hashed_password2"),
        ]
        cursor.executemany("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", users)
        self.conn.commit()
        self.conn.close()

    def test_get_users(self):
        response = self.app.get("/users")
        self.assertEqual(response.status_code, 200)

    def test_get_user_not_found(self):
        response = self.app.get("/user/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.get_data(as_text=True))

    def test_create_user_success(self):
        data = {"name": "Charlie", "email": "charlie@example.com", "password": "secret"}
        response = self.app.post("/users", data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created", response.get_data(as_text=True))

    def test_create_user_duplicate_email(self):
        payload = {"name": "John Doe", "email": "alice@example.com", "password": "secret"}
        # First creation
        self.app.post("/users", json=payload)
        # Duplicate creation
        response = self.app.post("/users", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email already exists", response.get_data(as_text=True))
if __name__ == "__main__":
    unittest.main()
