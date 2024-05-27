from django.test import TestCase

from clinic.staff.factories import StaffFactory
from clinic.staff.filters import StaffFilter
from clinic.users.factories import UserFactory


class StaffFilterTest(TestCase):
    def setUp(self):
        self.staff1 = StaffFactory.create(
            user=UserFactory.create(first_name="John", last_name="Doe"),
        )
        self.staff2 = StaffFactory.create(
            user=UserFactory.create(first_name="Jane", last_name="Smith"),
        )

    def test_filter_fullname(self):
        filterset = StaffFilter(data={"fullname": "john"})

        self.assertTrue(filterset.is_valid())
        filtered_queryset = filterset.qs
        self.assertIn(self.staff1, filtered_queryset)
        self.assertNotIn(self.staff2, filtered_queryset)
