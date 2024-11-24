# tests/test_nlp_processor.py

import unittest
from nlp_processor import extract_player_names, determine_query_type

class TestNLPProcessor(unittest.TestCase):
    """
    Unit tests for nlp_processor.py.
    """

    def setUp(self):
        self.name_variations = {
            'haaland': 'Haaland',
            'son': 'Son',
            'rashford': 'Rashford',
            'kane': 'Kane'
        }

    def test_extract_player_names_simple(self):
        """
        Test extracting player names from a simple sentence.
        """
        input_text = "Should I pick Haaland or Son?"
        extracted = extract_player_names(input_text, self.name_variations)
        self.assertEqual(set(extracted), {'Haaland', 'Son'})

    def test_extract_player_names_with_typos(self):
        """
        Test extracting player names with typos or variations.
        """
        input_text = "Is Haland a better choice than Rashy?"
        # Adding typo variations to name_variations
        self.name_variations['haland'] = 'Haaland'
        self.name_variations['haland'] = 'Haaland'
        self.name_variations['rashy'] = 'Rashford'
        extracted = extract_player_names(input_text, self.name_variations)
        self.assertEqual(set(extracted), {'Haaland', 'Rashford'})

    def test_determine_query_type_rmt(self):
        """
        Test determining query type for RMT.
        """
        input_text = "RMT please!"
        query_type = determine_query_type(input_text)
        self.assertEqual(query_type, 'RMT')

    def test_determine_query_type_transfer(self):
        """
        Test determining query type for Transfer.
        """
        input_text = "Should I transfer in Kane?"
        query_type = determine_query_type(input_text)
        self.assertEqual(query_type, 'Transfer')

    def test_determine_query_type_comparison(self):
        """
        Test determining query type for Comparison.
        """
        input_text = "Who is better, Haaland or Kane?"
        query_type = determine_query_type(input_text)
        self.assertEqual(query_type, 'Comparison')

    def test_determine_query_type_unknown(self):
        """
        Test determining query type when unknown.
        """
        input_text = "Good morning!"
        query_type = determine_query_type(input_text)
        self.assertEqual(query_type, 'Unknown')

if __name__ == '__main__':
    unittest.main()
