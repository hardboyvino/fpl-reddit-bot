import unittest
from app import hello_world

class TestApp(unittest.TestCase):
    """
    Test case for app.py
    """

    def test_hello_world(self):
        """
        Test hello_world functnion
        """
        self.assertEqual(hello_world(), "Hello, World!")

if __name__ == '__main__':
    unittest.main()
