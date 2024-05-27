from django.test import TestCase
from django.utils import timezone

from clinic.visits.choices import TimeChoices, VisitStatus, VisitType
from clinic.visits.factories import VisitFactory
from clinic.visits.filters import VisitFilter


class VisitFilterTest(TestCase):
    def setUp(self):
        self.visit1 = VisitFactory.create(
            date=timezone.now().date() - timezone.timedelta(days=1),
            time=timezone.now().time(),
            status=VisitStatus.BOOKED,
            visit_type=VisitType.SCHEDULED,
        )
        self.visit2 = VisitFactory.create(
            date=timezone.now().date() + timezone.timedelta(days=1),
            time=timezone.now().time(),
            status=VisitStatus.BOOKED,
            visit_type=VisitType.SCHEDULED,
        )

    def test_filter_time_upcoming(self):
        filterset = VisitFilter(data={"time": TimeChoices.UPCOMING})

        self.assertTrue(filterset.is_valid())

        filtered_queryset = filterset.qs
        self.assertNotIn(self.visit1, filtered_queryset)
        self.assertIn(self.visit2, filtered_queryset)

    def test_filter_time_past(self):
        filterset = VisitFilter(data={"time": TimeChoices.PAST})

        self.assertTrue(filterset.is_valid())

        filtered_queryset = filterset.qs
        self.assertIn(self.visit1, filtered_queryset)
        self.assertNotIn(self.visit2, filtered_queryset)

    def test_filter_time_all_times(self):
        filterset = VisitFilter(data={"time": TimeChoices.ALL})

        self.assertTrue(filterset.is_valid())

        filtered_queryset = filterset.qs
        self.assertIn(self.visit1, filtered_queryset)
        self.assertIn(self.visit2, filtered_queryset)
