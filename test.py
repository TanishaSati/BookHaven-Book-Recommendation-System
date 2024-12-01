import unittest
import pickle
import numpy as np

class TestBookRecommendationSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Using 'with' to open and automatically close files after loading
        with open('popular.pkl', 'rb') as f:
            cls.popular_df = pickle.load(f)
        with open('pt.pkl', 'rb') as f:
            cls.pt = pickle.load(f)
        with open('books.pkl', 'rb') as f:
            cls.books = pickle.load(f)
        with open('similarity_scores.pkl', 'rb') as f:
            cls.similarity_scores = pickle.load(f)

    def test_popular_books(self):
        # Check if the top 50 popular books have been loaded correctly
        self.assertEqual(len(self.popular_df), 50)  # Assert that there are 50 books in popular_df
        self.assertIn('Book-Title', self.popular_df.columns)  # Check if 'Book-Title' exists in the columns

    def test_similarity_scores(self):
        # Ensure similarity scores for a book are within the expected range
        book_title = "The Catcher in the Rye"  # Replace with an actual book title from your dataset
        index = np.where(self.pt.index == book_title)[0]

        # Ensure that we found a matching index for the book title
        self.assertGreater(len(index), 0, f"Book title '{book_title}' not found in pt index.")

        index = index[0]  # Get the first index (assuming we have found it)

        # Get similar items based on similarity scores
        similar_items = sorted(list(enumerate(self.similarity_scores[index])), key=lambda x: x[1], reverse=True)

        # Check if there are at least 8 similar items
        self.assertGreater(len(similar_items), 8)

        # Check if similarity scores are between 0 and 1
        for item in similar_items:
            self.assertGreaterEqual(item[1], 0)
            self.assertLessEqual(item[1], 1)

if __name__ == '__main__':
    unittest.main()
