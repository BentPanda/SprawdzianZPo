import unittest
from app import app, users, next_user_id

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        users.clear()
        global next_user_id
        next_user_id = 1

    def test_get_user(self):
        users[1] = {"id": 1, "name": "Wojciech", "lastname": "Oczkowski"}
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": 1, "name": "Wojciech", "lastname": "Oczkowski"})

    def test_get_user_not_found(self):
        response = self.app.get('/users/999')
        self.assertEqual(response.status_code, 404)

    def test_create_user(self):
        user = {"name": "Wojciech", "lastname": "Oczkowski"}
        response = self.app.post('/users', json=user)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"id": 1, "name": "Wojciech", "lastname": "Oczkowski"})

    def test_update_user(self):
        self.test_create_user()
        update = {"name": "Updated Wojciech"}
        response = self.app.patch('/users/1', json=update)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(users[1]["name"], "Updated Wojciech")

    def test_update_user_invalid_data(self):
        self.test_create_user()
        update = {"age": 30}
        response = self.app.patch('/users/1', json=update)
        self.assertEqual(response.status_code, 400)

    def test_replace_user(self):
        self.test_create_user()
        user = {"name": "Wojciech", "lastname": "Nowak"}
        response = self.app.put('/users/1', json=user)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(users[1], {"id": 1, "name": "Wojciech", "lastname": "Nowak"})

    def test_delete_user(self):
        self.test_create_user()
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 204)
        self.assertNotIn(1, users)

    def test_delete_user_not_found(self):
        response = self.app.delete('/users/999')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
