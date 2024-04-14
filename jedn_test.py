import unittest
from app import app, users, next_user_id

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        users.clear()
        global next_user_id
        next_user_id = 1

    def setup_user(self, name="Wojciech", lastname="Oczkowski"):
        user = {"name": name, "lastname": lastname}
        response = self.app.post('/users', json=user)
        return response.json['id']
    def test_get_user(self):
        user_id = self.setup_user()
        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": user_id, "name": "Wojciech", "lastname": "Oczkowski"})

    def test_get_user_not_found(self):
        response = self.app.get('/users/999')
        self.assertEqual(response.status_code, 404)

    def test_create_user(self):
        user_id = self.setup_user()
        self.assertTrue(user_id in users)
        self.assertEqual(users[user_id], {"id": user_id, "name": "Wojciech", "lastname": "Oczkowski"})

    def test_update_user(self):
        user_id = self.setup_user()
        update = {"name": "Updated Wojciech"}
        response = self.app.patch(f'/users/{user_id}', json=update)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(users[user_id]["name"], "Updated Wojciech")

    def test_update_user_invalid_data(self):
        user_id = self.setup_user()
        update = {"age": 30}
        response = self.app.patch(f'/users/{user_id}', json=update)
        self.assertEqual(response.status_code, 400)

    def test_replace_user(self):
        user_id = self.setup_user()
        user = {"name": "Wojciech", "lastname": "Nowak"}
        response = self.app.put(f'/users/{user_id}', json=user)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(users[user_id], {"id": user_id, "name": "Wojciech", "lastname": "Nowak"})

    def test_delete_user(self):
        user_id = self.setup_user()
        response = self.app.delete(f'/users/{user_id}')
        self.assertEqual(response.status_code, 204)
        self.assertNotIn(user_id, users)

    def test_delete_user_not_found(self):
        response = self.app.delete('/users/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
