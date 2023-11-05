import unittest
from user.handlers import handlers
from flask import Flask, jsonify

app = Flask(__name__)
app.register_blueprint(handlers)


class TestGetRoute(unittest.TestCase):
    def test_get_data(self):
        with app.test_client() as client:
            response = client.get('/data')

            data = response.get_json()
            limited_data = data[:1]  # limited_data = [(user[1], user[2]) for user in data]
            # limited_data = [tuple(user) for user in data[:2]]           # for tuples
            expected_data = [[1, 'harrypotter', 'harrypotter@gmail.com']]  # Add other expected data as needed

            self.assertEqual(response.status_code, 200)
            self.assertEqual(limited_data, expected_data)


    def test_post_data(self):
        with app.test_client() as client:
            data = {'username': 'testuser',
                'email': 'test@example.com'}
            response = client.post('/data', json=data)
            self.assertEqual(response.status_code, 201)

    def test_put_data(self):
        initial_data = {'username': 'initialuser',
                        'email': 'initial@example.com'}
        with app.test_client() as client:
            response_post = client.post('/data', json=initial_data)
            self.assertEqual(response_post.status_code,
                             201)  # Check if the initial creation was successful

            user_id = None              # Extract the user_id from the response and update the data
            if response_post.json:
                user_id = response_post.json.get('id')

            if user_id is not None:
                updated_data = {'username': 'modifieduser',
                                'email': 'modified@example.com'}
                response_put = client.put(f'/data/{user_id}', json=updated_data)

                self.assertEqual(response_put.status_code, 200)

    def test_patch_data(self):
        # Create initial data
        initial_data = {'username': 'initialuser',
                        'email': 'initial@example.com'}
        with app.test_client() as client:
            response_post = client.post('/data', json=initial_data)
            self.assertEqual(response_post.status_code, 201)
            user_id = None
            if response_post.json:
                user_id = response_post.json.get('id')

            if user_id is not None:
                patched_data = {'email': 'patched@example.com'}
                response_patch = client.patch(f'/data/{user_id}', json=patched_data)

                self.assertEqual(response_patch.status_code, 200)

    def test_delete_data(self):
        # Create initial data
        initial_data = {'username': 'initialuser',
                        'email': 'initial@example.com'}
        with app.test_client() as client:
            response_post = client.post('/data', json=initial_data)
            self.assertEqual(response_post.status_code, 201)

            user_id = None
            if response_post.json:
                user_id = response_post.json.get('id')

            if user_id is not None:
                response_delete = client.delete(f'/data/{user_id}')
                self.assertEqual(response_delete.status_code, 200)

if __name__ == '__main__':
    unittest.main()
