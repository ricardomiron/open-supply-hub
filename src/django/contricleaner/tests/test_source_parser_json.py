from contricleaner.lib.parsers.json_parser import JSONParser

from django.test import TestCase


class SourceParserJsonTest(TestCase):
    def setUp(self):
        self.json_data = {
            "country": "USA",
            "name": "Name of the company",
            "address": "1234 Main St",
        }

        self.parser = JSONParser(self.json_data)

    def test_get_parsed_rows(self):
        # Ensure get_parsed_rows returns a list containing
        # the original JSON data
        parsed_rows = self.parser.get_parsed_rows()
        self.assertIsInstance(parsed_rows, list)
        self.assertEqual(len(parsed_rows), 1)
        self.assertEqual(parsed_rows[0], self.json_data)

    def test_empty_json(self):
        # Test behavior when initialized with an empty JSON
        empty_json_parser = JSONParser({})
        parsed_rows = empty_json_parser.get_parsed_rows()
        self.assertIsInstance(parsed_rows, list)
        self.assertEqual(len(parsed_rows), 1)
        self.assertEqual(parsed_rows[0], {})

    def test_invalid_json(self):
        # Test behavior when initialized with invalid JSON data
        invalid_json_parser = JSONParser(None)
        parsed_rows = invalid_json_parser.get_parsed_rows()
        self.assertIsInstance(parsed_rows, list)
        self.assertEqual(len(parsed_rows), 1)
        self.assertEqual(parsed_rows[0], None)
