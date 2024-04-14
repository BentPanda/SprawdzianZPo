import unittest
from app import app, users

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        users.clear()

    def test_user_creation(self):
        response = self.app.post('/users', json={"name": "Wojciech", "lastname": "Oczkowski"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Wojciech")
        self.assertEqual(response.json['lastname'], "Oczkowski")

if __name__ == '__main__':
    unittest.main()
