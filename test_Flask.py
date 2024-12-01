import unittest
from app import app

class TestFlaskApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()  # Use Flask's test client
        cls.app.testing = True

    def test_homepage(self):
        # Test if the homepage renders with the expected status code (200)
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Discover the Top 50 Must-Read Books of All Time', response.data)  # Check if title exists in response

    def test_recommendation_page(self):
        # Test if the recommendation page loads correctly
        response = self.app.get('/recommend')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recommend Books', response.data)  # Check if the page has the 'Recommend Books' heading

    def test_recommend_books(self):
        # Simulate a POST request to the recommend_books route
        response = self.app.post('/recommend_books', data={'user_input': 'Some Book Title'})  # Replace with a valid book title
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recommended Books', response.data)  # Check if recommendations are displayed
        self.assertIn(b'Book-Title', response.data)  # Check if book titles appear in response data

if __name__ == '__main__':
    unittest.main()
