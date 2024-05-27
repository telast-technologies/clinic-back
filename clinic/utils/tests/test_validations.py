from django.core.exceptions import ValidationError
from django.test import TestCase

from clinic.utils.validators import RangeValidator


class RangeValidatorTest(TestCase):
    def test_valid_range(self):
        # This should not raise any exception
        validator = RangeValidator(1, 10)
        validator()

    def test_invalid_range(self):
        # This should raise a ValidationError
        validator = RangeValidator(10, 1)
        with self.assertRaises(ValidationError) as context:
            validator()
        self.assertEqual(context.exception.message, "invalid range")
        self.assertEqual(context.exception.code, "invalid")
