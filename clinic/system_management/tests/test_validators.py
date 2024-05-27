from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from clinic.system_management.factories import PackageFactory
from clinic.system_management.validators import PackageActiveStatusValidator


class PackageActiveStatusValidatorTest(TestCase):
    def setUp(self):
        self.validator = PackageActiveStatusValidator()

    def test_package_not_active(self):
        package = PackageFactory.create(active=False)

        with self.assertRaises(ValidationError) as context:
            self.validator(package)

        self.assertEqual(context.exception.message, _("Package is not active"))

    def test_package_active(self):
        package = PackageFactory.create(active=True)

        try:
            self.validator(package)
        except ValidationError:
            self.fail("PackageActiveStatusValidator raised ValidationError unexpectedly!")

    def test_equality(self):
        validator1 = PackageActiveStatusValidator()
        validator2 = PackageActiveStatusValidator()
        validator3 = object()  # Different type to ensure inequality

        self.assertEqual(validator1, validator2)
        self.assertNotEqual(validator1, validator3)
