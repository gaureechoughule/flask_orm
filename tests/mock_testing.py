from unittest import TestCase, mock
from app import app

class TestGetRoute(TestCase):
    def setUp(self):
        self.client = app.test_client()

    @mock.patch('user.models.model.User')
    def test_get_data(self, mock_user):
        mock_user_instance = mock.MagicMock()
        mock_user_instance.id = 1
        mock_user_instance.username = 'narendra modi'
        mock_user_instance.email = 'nmodi@gmail.com'

        mock_user.query.all.return_value = [mock_user_instance]

        response = self.client.get('/data/1')

        self.assertEqual(response.status_code, 200)
        expected_data = [1, "narendra modi", "nmodi@gmail.com"]
        self.assertEqual(response.json, expected_data)

    @mock.patch('user.models.model.User')
    def test_post_data(self, mock_user_create):
        mock_user_create.return_value = mock.MagicMock(id=1, username='testuser', email='test@example.com')

        data = {'username': 'testuser', 'email': 'test@example.com'}
        response = self.client.post('/data', json=data)

        self.assertEqual(response.status_code, 201)

    # @mock.patch('user.models.model.User')
    # def test_post_data(self, mock_user):
    #     # Simulating the return value of the model constructor for creating a user
    #     mock_user_instance = mock.MagicMock()
    #     mock_user_instance.id = 1  # Assuming the user ID
    #     mock_user_instance.username = 'testuser'
    #     mock_user_instance.email = 'test@example.com'
    #
    #     # Mock the creation of the User object
    #     mock_user.return_value = mock_user_instance
    #
    #     # Make a POST request to create a user
    #     response = self.client.post('/data', json={'username': 'testuser',
    #                                                'email': 'test@example.com'})
    #
    #     # Verify that the API call returns the expected status code
    #     self.assertEqual(response.status_code, 201)
