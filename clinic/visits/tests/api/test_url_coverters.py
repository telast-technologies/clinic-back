from datetime import datetime

from django.test import SimpleTestCase

from clinic.visits.api.url_converters import DateConverter


class DateConverterTest(SimpleTestCase):
    def setUp(self):
        self.converter = DateConverter()

    def test_to_python_valid(self):
        # Test conversion from string to datetime.date object with valid input
        input_date_str = "2024-05-27"
        expected_date = datetime.strptime(input_date_str, "%Y-%m-%d").date()
        converted_date = self.converter.to_python(input_date_str)
        self.assertEqual(converted_date, expected_date)

    def test_to_python_invalid(self):
        # Test conversion from string to datetime.date object with invalid input
        invalid_date_str = "2024-05-270"  # Invalid day part
        with self.assertRaises(ValueError):
            self.converter.to_python(invalid_date_str)

    def test_to_python_missing(self):
        # Test conversion from string to datetime.date object with missing input
        missing_date_str = ""  # Missing date
        with self.assertRaises(ValueError):
            self.converter.to_python(missing_date_str)

    def test_to_url(self):
        # Test conversion from datetime.date object to string
        input_date = datetime.strptime("2024-05-27", "%Y-%m-%d").date()
        expected_date_str = "2024-05-27"
        converted_date_str = self.converter.to_url(input_date)
        self.assertEqual(converted_date_str, expected_date_str)
