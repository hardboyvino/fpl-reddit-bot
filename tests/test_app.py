import unittest
from unittest.mock import patch, MagicMock
import praw
from praw.exceptions import PRAWException

import app
import config

class TestTransferBot(unittest.TestCase):
    """
    Unit tests for app.py.
    """

    @patch('app.praw.Reddit')
    def test_reddit_instance_creation(self, mock_reddit):
        """
        Test that the Reddit instance is created with correct credentials.
        """
        app.main()
        mock_reddit.assert_called_with(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            username=config.REDDIT_USERNAME,
            password=config.REDDIT_PASSWORD,
            user_agent=config.REDDIT_USER_AGENT
        )

    @patch('app.praw.Reddit')
    def test_fetch_submission(self, mock_reddit):
        """
        Test fetching a submission with a valid URL.
        """
        # Mock the Reddit instance and submission
        mock_submission = MagicMock()
        mock_submission.title = 'Mock Thread Title'
        
        # Mock the CommentForest
        mock_comment_forest = MagicMock()
        mock_comment_forest.replace_more.return_value = None

        # Mock the comments
        mock_comment = MagicMock()
        mock_comment.author = 'TestAuthor'
        mock_comment.body = 'Test comment body'

        # Make the CommentForest iterable
        mock_comment_forest.__iter__.return_value = [mock_comment]

        # Assign the mocked CommentForest to submission.contents
        mock_submission.comments = mock_comment_forest

        # Mock the Reddit instance
        mock_reddit_instance = mock_reddit.return_value
        mock_reddit_instance.submission.return_value = mock_submission

        # Call the function under test
        title, comments = app.fetch_top_level_comments('test_url')

        # Ensure submission was called with the correct URL
        mock_reddit_instance.submission.assert_called_with(url='test_url')

        # Verify the title and comments
        self.assertEqual(title, 'Mock Thread Title')
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].author, 'TestAuthor')
        self.assertEqual(comments[0].body, 'Test comment body')

    @patch('app.praw.Reddit')
    def test_invalud_credentials(self, mock_reddit):
        """
        Test handling of invalud Reddit credentials.
        """
        # Simulate an authentication error
        mock_reddit.side_effect = PRAWException("Invalid credentials")

        with self.assertRaises(PRAWException):
            app.main()

if __name__ == "__main__":
    unittest.main()